"""Police chase cog — interactive chase minigame with Discord Views and buttons.

Features:
    - Background loop for heat decay
    - /wanted command to check heat/warrant status
    - Arrest attempt View (comply or run)
    - Multi-stage chase View with button choices
    - Help system — other players can assist runners
    - Integration with crime and activity cogs via police module
"""

import discord
from discord import app_commands
from discord.ext import commands, tasks
import random
import database as db
import police as _police
from utils.embeds import success_embed, error_embed, info_embed, warning_embed, format_money
from utils.helpers import clamp, check_level_up, xp_for_next_level
from config import HEALTH_MAX, ENERGY_MAX, ACHIEVEMENTS
from config.police import (
    HEAT_TAILING_THRESHOLD,
    HEAT_WARRANT_THRESHOLD,
    HEAT_MAX,
    HEAT_DECAY_INTERVAL,
    CHASE_STAGES,
    HELP_ACTIONS,
    CHASE_ENERGY_COST_PER_STAGE,
    CHASE_HEALTH_RISK_BASE,
    CHASE_HEALTH_RISK_MAX,
    FINE_PER_HEAT,
    JAIL_COOLDOWN_BASE,
    JAIL_COOLDOWN_PER_HEAT,
    JAIL_COOLDOWN_MAX,
)


# ============================================================
# ARREST ATTEMPT VIEW — Comply or Run
# ============================================================

class ArrestView(discord.ui.View):
    """View shown when police attempt an arrest. Player can comply or run."""

    def __init__(self, user_id: int, location_id: str, heat: int):
        super().__init__(timeout=120)
        self.user_id = user_id
        self.location_id = location_id
        self.heat = heat
        self.helpers = []
        self.responded = False

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # Help button is available to everyone; comply/run only to the target
        return True

    @discord.ui.button(label="Comply", style=discord.ButtonStyle.secondary, emoji="🙅")
    async def comply(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your arrest!", ephemeral=True)
            return
        if self.responded:
            return
        self.responded = True
        self.stop()

        # Apply comply outcome
        fine = self.heat * FINE_PER_HEAT
        user_data = await db.get_user(self.user_id)
        if user_data:
            if fine > user_data["wallet"]:
                fine = user_data["wallet"]
            jail_time = min(JAIL_COOLDOWN_BASE + self.heat * JAIL_COOLDOWN_PER_HEAT, JAIL_COOLDOWN_MAX)
            await db.update_user(
                self.user_id,
                wallet=user_data["wallet"] - fine,
                total_lost=user_data["total_lost"] + fine,
            )
            await db.add_transaction(self.user_id, "police_fine", fine, "Complied with arrest")
            await db.set_cooldown(self.user_id, "jail", jail_time)
            await db.reset_heat(self.user_id)

            embed = error_embed(
                "🚔 Arrested",
                f"You comply with the officers. It's the smart move.\n\n"
                f"**Fine:** {format_money(fine)}\n"
                f"**Jail time:** {jail_time // 60}m {jail_time % 60}s cooldown on activities\n"
                f"**Heat:** Reset to 0",
            )
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            await interaction.response.edit_message(embed=error_embed("Error", "Something went wrong."), view=None)

    @discord.ui.button(label="Run!", style=discord.ButtonStyle.danger, emoji="🏃")
    async def run(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your arrest!", ephemeral=True)
            return
        if self.responded:
            return
        self.responded = True
        self.stop()

        # Start the chase!
        chase_view = ChaseView(self.user_id, self.location_id, self.heat, self.helpers)
        embed = await chase_view.build_embed(interaction)
        await interaction.response.edit_message(embed=embed, view=chase_view)
        chase_view.message = await interaction.original_response()

    @discord.ui.button(label="Help!", style=discord.ButtonStyle.success, emoji="🆘")
    async def help(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.user_id:
            await interaction.response.send_message("You can't help yourself! Choose to comply or run.", ephemeral=True)
            return
        if interaction.user.id in self.helpers:
            await interaction.response.send_message("You're already helping!", ephemeral=True)
            return
        if len(self.helpers) >= 2:
            await interaction.response.send_message("Too many people are already helping!", ephemeral=True)
            return

        self.helpers.append(interaction.user.id)
        # Show help action selection
        help_view = HelpActionView(self.user_id, interaction.user.id, self)
        embed = info_embed(
            "🆘 Helping the Runner",
            f"Choose how you want to help <@{self.user_id}> escape the police!",
        )
        for action in HELP_ACTIONS:
            embed.add_field(
                name=action["label"],
                value=f"{action['description']}\nEscape bonus: +{int(action['escape_bonus'] * 100)}%",
                inline=False,
            )
        await interaction.response.send_message(embed=embed, view=help_view, ephemeral=True)


# ============================================================
# HELP ACTION VIEW — Choose how to help
# ============================================================

class HelpActionView(discord.ui.View):
    """View for helpers to choose their action."""

    def __init__(self, runner_id: int, helper_id: int, arrest_view: ArrestView):
        super().__init__(timeout=60)
        self.runner_id = runner_id
        self.helper_id = helper_id
        self.arrest_view = arrest_view

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.helper_id

    @discord.ui.button(label="Distraction", style=discord.ButtonStyle.primary, emoji="🎆")
    async def distraction(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._apply_help(interaction, "distraction")

    @discord.ui.button(label="Escape Route", style=discord.ButtonStyle.primary, emoji="🚗")
    async def escape_route(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._apply_help(interaction, "escape_route")

    @discord.ui.button(label="Block Path", style=discord.ButtonStyle.primary, emoji="🚧")
    async def block_path(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._apply_help(interaction, "block")

    async def _apply_help(self, interaction: discord.Interaction, action_id: str):
        self.stop()
        action = _police.get_help_action(action_id)
        if not action:
            await interaction.response.edit_message(embed=error_embed("Error", "Invalid action."), view=None)
            return

        # Apply helper reward
        helper_data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        xp_gain = action["helper_reward_xp"]
        new_xp = helper_data["xp"] + xp_gain
        new_level, leveled_up = check_level_up(new_xp, helper_data["level"])
        if leveled_up:
            new_xp -= sum(xp_for_next_level(l) for l in range(helper_data["level"], new_level))

        health_loss = 0
        if action["helper_risk"] > 0:
            health_loss = random.randint(0, action["helper_risk"])
            new_health = clamp(helper_data["health"] - health_loss, 0, HEALTH_MAX)
            await db.update_user(interaction.user.id, xp=new_xp, level=new_level, health=new_health)
        else:
            await db.update_user(interaction.user.id, xp=new_xp, level=new_level)

        await db.add_reputation(interaction.user.id, "underworld", action["helper_reward_rep"])

        narrative = action["narrative"].format(helper=interaction.user.mention)
        embed = success_embed("🤝 Help Applied!", f"{narrative}\n\n**Your reward:** +{xp_gain} XP, +{action['helper_reward_rep']} Underworld rep")
        if health_loss > 0:
            embed.add_field(name="💔 Injury", value=f"You took {health_loss} damage while helping!", inline=False)
        if leveled_up:
            embed.add_field(name="🎉 Level Up!", value=f"You are now level {new_level}!", inline=False)
        await interaction.response.edit_message(embed=embed, view=None)


# ============================================================
# CHASE VIEW — Multi-stage chase minigame
# ============================================================

class ChaseView(discord.ui.View):
    """Interactive multi-stage chase minigame."""

    def __init__(self, user_id: int, location_id: str, heat: int, helpers: list = None):
        super().__init__(timeout=180)
        self.user_id = user_id
        self.location_id = location_id
        self.heat = heat
        self.helpers = helpers or []
        self.stage = 1
        self.choice_mod = 0.0
        self.prev_choice_key = None
        self.total_energy_cost = 0
        self.total_health_risk = 0
        self.accumulated_mod = 0.0
        self.finished = False
        self.message = None
        self._add_stage_buttons()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.user_id

    def _build_choice_buttons(self) -> list[discord.ui.Button]:
        """Build buttons for the current chase stage."""
        stage_data = _police.get_chase_stage(self.stage)
        choices = stage_data.get("choices", [])
        buttons = []
        for i, choice in enumerate(choices):
            btn = discord.ui.Button(
                label=choice["label"],
                style=discord.ButtonStyle.danger if i == 0 else discord.ButtonStyle.secondary,
                custom_id=f"chase_choice_{i}",
            )
            buttons.append(btn)
        return buttons

    async def build_embed(self, interaction: discord.Interaction = None) -> discord.Embed:
        """Build the embed for the current chase stage."""
        user_data = await db.get_user(self.user_id)
        if not user_data:
            return error_embed("Error", "Player data not found.")

        stage_data = _police.get_chase_stage(self.stage)
        title = stage_data.get("title", "Chase")

        if self.stage == 2 and self.prev_choice_key:
            narrative = _police.get_stage_narrative(self.stage, self.prev_choice_key)
        else:
            narrative = _police.get_stage_narrative(self.stage)

        embed = discord.Embed(
            title=f"🚨 POLICE CHASE — {title}",
            description=narrative,
            color=0xE74C3C,
        )

        # Show current stats
        embed.add_field(
            name="📊 Your Status",
            value=f"❤️ Health: {user_data['health']}/{HEALTH_MAX}\n⚡ Energy: {user_data.get('energy', 100)}/{ENERGY_MAX}",
            inline=True,
        )

        # Show heat
        embed.add_field(
            name="🔥 Heat Level",
            value=f"{self.heat}/{HEAT_MAX}",
            inline=True,
        )

        # Show helpers
        if self.helpers:
            helper_text = f"{len(self.helpers)} ally/allies helping (+{len(self.helpers) * 15}% escape)"
            embed.add_field(name="🆘 Helpers", value=helper_text, inline=True)

        # Show choices
        choices = stage_data.get("choices", [])
        choice_text = ""
        for i, choice in enumerate(choices):
            mod_sign = "+" if choice["escape_mod"] >= 0 else ""
            choice_text += f"**{i+1}.** {choice['label']} — {choice['description']}\n   Escape mod: {mod_sign}{int(choice['escape_mod'] * 100)}% | Energy: -{choice['energy_cost']} | Risk: {choice['health_risk']} HP\n"
        embed.add_field(name="🎯 Choices", value=choice_text, inline=False)

        embed.set_footer(text=f"Stage {self.stage}/3 • Choose wisely — your freedom depends on it!")
        return embed

    async def _handle_choice(self, interaction: discord.Interaction, choice_index: int):
        """Handle a chase stage choice."""
        if self.finished:
            return

        stage_data = _police.get_chase_stage(self.stage)
        choices = stage_data.get("choices", [])
        if choice_index < 0 or choice_index >= len(choices):
            return

        choice = choices[choice_index]
        self.accumulated_mod += choice["escape_mod"]
        self.total_energy_cost += choice["energy_cost"]
        self.total_health_risk += choice["health_risk"]

        # Map choice index to key for stage 2 narrative
        choice_keys = ["alleys", "rooftops", "crowd", "subway"]
        if self.stage == 1:
            self.prev_choice_key = choice_keys[choice_index] if choice_index < len(choice_keys) else "alleys"

        # Apply energy cost immediately
        user_data = await db.get_user(self.user_id)
        if user_data:
            new_energy = clamp(user_data.get("energy", 100) - choice["energy_cost"], 0, ENERGY_MAX)
            await db.update_user(self.user_id, energy=new_energy)

        # Advance stage
        self.stage += 1

        if self.stage > 3:
            # Final resolution
            self.finished = True
            self.stop()
            await self._resolve_chase(interaction)
        else:
            # Next stage — rebuild buttons
            self.clear_items()
            self._add_stage_buttons()
            embed = await self.build_embed(interaction)
            await interaction.response.edit_message(embed=embed, view=self)

    async def _resolve_chase(self, interaction: discord.Interaction):
        """Resolve the chase — determine outcome and apply results."""
        user_data = await db.get_user(self.user_id)
        if not user_data:
            await interaction.response.edit_message(embed=error_embed("Error", "Player data not found."), view=None)
            return

        # Calculate escape chance
        escape_chance = await _police.calculate_escape_chance(
            self.user_id, user_data, self.accumulated_mod, len(self.helpers)
        )

        roll = random.random()
        escaped = roll < escape_chance

        # Determine health loss
        health_loss = random.randint(CHASE_HEALTH_RISK_BASE, CHASE_HEALTH_RISK_MAX)
        if not escaped:
            health_loss = int(health_loss * 1.5)

        # Check if injured (high health loss regardless of escape)
        injured = health_loss >= 20

        if escaped:
            if injured:
                outcome = "injured_escape"
            else:
                outcome = "escape"
        else:
            if injured:
                outcome = "injured_caught"
            else:
                outcome = "caught"

        # Apply outcome
        energy_loss = self.total_energy_cost
        result = await _police.apply_chase_outcome(self.user_id, outcome, health_loss, energy_loss)

        outcome_text = _police.get_outcome_text(outcome)

        if outcome in ("caught", "injured_caught"):
            fine = result.get("fine", 0)
            jail_time = result.get("jail_time", 0)
            embed = error_embed(
                "🚔 CAUGHT!",
                f"{outcome_text}\n\n"
                f"**Fine:** {format_money(fine)}\n"
                f"**Health loss:** -{health_loss}\n"
                f"**Energy loss:** -{energy_loss}\n"
                f"**Jail cooldown:** {jail_time // 60}m {jail_time % 60}s\n"
                f"**Heat:** Reset to 0",
            )
        elif outcome == "escape":
            dropped = result.get("dropped", 0)
            xp = result.get("xp", 0)
            embed = success_embed(
                "🏃 ESCAPED!",
                f"{outcome_text}\n\n"
                f"**Health loss:** -{health_loss}\n"
                f"**Energy loss:** -{energy_loss}\n"
                f"**Dropped:** {format_money(dropped)} (lost while running)\n"
                f"**XP gained:** +{xp}\n"
                f"**Underworld rep:** +5\n"
                f"**Heat:** Reset to 0",
            )
            if result.get("leveled_up"):
                embed.add_field(name="🎉 Level Up!", value=f"You are now level {result['new_level']}!", inline=False)
        else:  # injured_escape
            embed = warning_embed(
                "🩸 Escaped — But Hurt",
                f"{outcome_text}\n\n"
                f"**Health loss:** -{health_loss}\n"
                f"**Energy loss:** -{energy_loss}\n"
                f"**Heat:** Reduced by 30\n"
                f"**Underworld rep:** +3",
            )

        # Check achievements
        new_achievements = await db.check_achievements(self.user_id)
        for ach_id in new_achievements:
            ach = ACHIEVEMENTS.get(ach_id, {})
            embed.add_field(
                name="🏆 Achievement Unlocked!",
                value=f"{ach.get('emoji', '🏆')} **{ach.get('name', ach_id)}** — +{format_money(ach.get('reward', 0))}!",
                inline=False,
            )
        if new_achievements:
            ach_reward = sum(ACHIEVEMENTS.get(a, {}).get("reward", 0) for a in new_achievements)
            if ach_reward > 0:
                current = await db.get_user(self.user_id)
                if current:
                    await db.update_user(self.user_id, wallet=current["wallet"] + ach_reward, total_earned=current["total_earned"] + ach_reward)

        await interaction.response.edit_message(embed=embed, view=None)

    def _add_stage_buttons(self):
        """Add buttons for the current stage."""
        stage_data = _police.get_chase_stage(self.stage)
        choices = stage_data.get("choices", [])
        for i, choice in enumerate(choices):
            btn = discord.ui.Button(
                label=choice["label"],
                style=discord.ButtonStyle.danger if i == 0 else discord.ButtonStyle.secondary,
                custom_id=f"chase_{self.stage}_{i}",
            )
            btn.callback = self._make_callback(i)
            self.add_item(btn)

    def _make_callback(self, index: int):
        async def callback(interaction: discord.Interaction):
            await self._handle_choice(interaction, index)
        return callback

    async def on_timeout(self):
        """Handle timeout — player hesitated too long, auto-caught."""
        if self.finished:
            return
        self.finished = True
        user_data = await db.get_user(self.user_id)
        if not user_data:
            return
        health_loss = random.randint(15, 30)
        result = await _police.apply_chase_outcome(self.user_id, "caught", health_loss, self.total_energy_cost)
        fine = result.get("fine", 0)
        jail_time = result.get("jail_time", 0)
        # Try to edit the original message
        try:
            msg = self.message
            if msg:
                embed = error_embed(
                    "⏰ Hesitated Too Long!",
                    f"You froze! The officers tackle you to the ground.\n\n"
                    f"**Fine:** {format_money(fine)}\n"
                    f"**Health loss:** -{health_loss}\n"
                    f"**Jail cooldown:** {jail_time // 60}m {jail_time % 60}s\n"
                    f"**Heat:** Reset to 0",
                )
                await msg.edit(embed=embed, view=None)
        except Exception:
            pass


# ============================================================
# CHASE COG
# ============================================================

class Chase(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.heat_decay_loop.start()

    def cog_unload(self):
        self.heat_decay_loop.cancel()

    @tasks.loop(seconds=HEAT_DECAY_INTERVAL)
    async def heat_decay_loop(self):
        """Background loop that decays all players' heat over time."""
        await _police.decay_heat()

    @heat_decay_loop.before_loop
    async def before_heat_decay_loop(self):
        await self.bot.wait_until_ready()

    @app_commands.command(name="wanted", description="Check your police heat level and warrant status")
    async def wanted(self, interaction: discord.Interaction):
        state = await db.get_police_state(interaction.user.id)
        if state is None or state["heat"] == 0:
            await interaction.response.send_message(
                embed=info_embed("🚔 Criminal Record", "You have a clean record. No heat, no warrants. Stay that way!"),
                ephemeral=True,
            )
            return

        heat = state["heat"]
        warrant = bool(state.get("warrant_active", 0))
        tailing = state.get("tailing_stage", 0)

        embed = warning_embed("🚔 Criminal Record", f"Your heat level: **{heat}/{HEAT_MAX}**")

        # Heat bar
        bar_length = 10
        filled = int((heat / HEAT_MAX) * bar_length)
        bar = "█" * filled + "░" * (bar_length - filled)
        embed.add_field(name="🔥 Heat", value=f"`{bar}` {heat}/{HEAT_MAX}", inline=False)

        if warrant:
            embed.add_field(
                name="📋 Warrant Active!",
                value="There is an active warrant for your arrest. Be careful during activities!",
                inline=False,
            )

        if tailing > 0:
            stage_text = {1: "Subtle surveillance — you may have noticed something", 2: "Active tail — police are clearly watching you", 3: "Arrest imminent!"}
            embed.add_field(
                name="👁️ Police Tailing",
                value=stage_text.get(tailing, "Unknown"),
                inline=False,
            )

        if heat >= HEAT_WARRANT_THRESHOLD:
            embed.add_field(
                name="⚠️ Danger",
                value="Your heat is critically high! A warrant may be issued at any time.",
                inline=False,
            )
        elif heat >= HEAT_TAILING_THRESHOLD:
            embed.add_field(
                name="⚠️ Warning",
                value="Police are interested in you. They may start watching your activities.",
                inline=False,
            )
        else:
            embed.add_field(
                name="✅ Status",
                value="Heat is low. You're under the radar for now.",
                inline=False,
            )

        embed.set_footer(text="Heat decays over time. Travel to new areas to shake tails.")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="police_status", description="Check if you're currently being tailed or have a warrant (alias for /wanted)")
    async def police_status(self, interaction: discord.Interaction):
        # Alias for /wanted
        await self.wanted.callback(self, interaction)


async def setup(bot):
    await bot.add_cog(Chase(bot))
