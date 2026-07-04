import discord
from discord import app_commands
from discord.ext import commands
import random
import database as db
from utils.base import BaseCog
from utils.embeds import success_embed, error_embed, info_embed, stats_bar, format_money
from config import (
    STATS, STAT_KEYS, BASE_STAT_VALUE, MAX_STAT_VALUE,
    TRAINING_CONFIG, QUALIFICATIONS, STAT_BOOSTER_ITEMS,
)


class StatsCog(BaseCog):
    """RPG stats, training, schooling, and qualifications."""

    stats_group = app_commands.Group(name="stats", description="View and train your RPG stats")
    school_group = app_commands.Group(name="school", description="Browse and enroll in qualifications")

    @stats_group.command(name="view", description="View all your stats and qualifications")
    async def stats_view(self, interaction: discord.Interaction):
        stats = await db.get_all_stats(interaction.user.id)
        quals = await db.get_qualifications(interaction.user.id)
        total_training = await db.get_total_training_sessions(interaction.user.id)

        embed = info_embed("📊 Your Stats", f"Total training sessions: {total_training}")
        for stat_key in STAT_KEYS:
            stat_info = STATS[stat_key]
            val = stats.get(stat_key, BASE_STAT_VALUE)
            bar = stats_bar(val, MAX_STAT_VALUE, 15)
            embed.add_field(
                name=f"{stat_info['emoji']} {stat_info['short']} — {val}/100",
                value=f"{bar}\n{stat_info['description']}",
                inline=False,
            )

        if quals:
            qual_names = [QUALIFICATIONS[q]["name"] for q in quals if q in QUALIFICATIONS]
            embed.add_field(name="📜 Qualifications", value="\n".join(qual_names), inline=False)
        else:
            embed.add_field(name="📜 Qualifications", value="None yet. Use `/school list` to browse.", inline=False)

        await interaction.response.send_message(embed=embed)

    @stats_group.command(name="train", description="Train a specific stat (costs coins + energy)")
    @app_commands.choices(stat=[
        app_commands.Choice(name=f"{STATS[k]['emoji']} {STATS[k]['name']}", value=k)
        for k in STAT_KEYS
    ])
    async def stats_train(self, interaction: discord.Interaction, stat: app_commands.Choice[str]):
        data = await self.get_user(interaction)

        if self.bot and await self.check_cooldown(interaction, "train"):
            return

        stat_key = stat.value
        current_val = await db.get_stat(interaction.user.id, stat_key)

        if current_val >= MAX_STAT_VALUE:
            await interaction.response.send_message(
                embed=info_embed("Maxed Out", f"Your {STATS[stat_key]['name']} is already at maximum ({MAX_STAT_VALUE})!")
            )
            return

        cost = min(
            int(eval(TRAINING_CONFIG["cost_formula"], {"stat_level": current_val})),
            TRAINING_CONFIG["cost_cap"],
        )
        energy_cost = TRAINING_CONFIG["energy_cost"]

        if data["wallet"] < cost:
            await interaction.response.send_message(
                embed=error_embed("Not Enough Coins", f"Training costs {format_money(cost)}. You have {format_money(data['wallet'])}.")
            )
            return

        if data.get("energy", 100) < energy_cost:
            await interaction.response.send_message(
                embed=error_embed("Not Enough Energy", f"Training requires {energy_cost} energy. You have {data.get('energy', 100)}.")
            )
            return

        gain = random.randint(TRAINING_CONFIG["min_gain"], TRAINING_CONFIG["max_gain"])
        new_val = await db.add_stat(interaction.user.id, stat_key, gain)
        sessions = await db.increment_training(interaction.user.id, stat_key)

        await db.update_user(
            interaction.user.id,
            wallet=data["wallet"] - cost,
            energy=max(0, data.get("energy", 100) - energy_cost),
            total_spent=data["total_spent"] + cost,
        )
        await db.set_cooldown(interaction.user.id, "train", TRAINING_CONFIG["cooldown_seconds"])

        stat_info = STATS[stat_key]
        embed = success_embed(
            f"{stat_info['emoji']} Training Complete!",
            f"You trained **{stat_info['name']}** and gained **+{gain}** points!\n"
            f"{stat_info['short']}: {current_val} → **{new_val}**/100\n"
            f"Cost: {format_money(cost)} | Energy: -{energy_cost}\n"
            f"Training sessions for this stat: {sessions}",
        )
        await interaction.response.send_message(embed=embed)

    @school_group.command(name="list", description="Browse available qualifications and schooling")
    async def school_list(self, interaction: discord.Interaction):
        user_quals = await db.get_qualifications(interaction.user.id)
        user_stats = await db.get_all_stats(interaction.user.id)

        embed = info_embed("🎓 School & Qualifications", "Enroll to earn qualifications needed for advanced jobs. Each requires multiple sessions.")

        for qual_id, qual in QUALIFICATIONS.items():
            has = qual_id in user_quals
            status = "✅ Earned" if has else self._check_qual_status(qual, user_quals, user_stats)

            req_text = ""
            if qual["stat_reqs"]:
                req_parts = []
                for stat, req in qual["stat_reqs"].items():
                    have = user_stats.get(stat, BASE_STAT_VALUE)
                    icon = "✅" if have >= req else "❌"
                    req_parts.append(f"{icon} {STATS[stat]['short']}: {have}/{req}")
                req_text += "Stats: " + " | ".join(req_parts)
            if qual["qual_reqs"]:
                qual_parts = []
                for pq in qual["qual_reqs"]:
                    icon = "✅" if pq in user_quals else "❌"
                    qname = QUALIFICATIONS.get(pq, {}).get("name", pq)
                    qual_parts.append(f"{icon} {qname}")
                if req_text:
                    req_text += "\n"
                req_text += "Prereqs: " + " | ".join(qual_parts)

            embed.add_field(
                name=f"{qual['name']} — {format_money(qual['cost'])}",
                value=f"{qual['description']}\n{req_text}\nStatus: {status}",
                inline=False,
            )

        await interaction.response.send_message(embed=embed)

    @school_group.command(name="enroll", description="Enroll in a qualification program")
    @app_commands.choices(qualification=[
        app_commands.Choice(name=QUALIFICATIONS[q]["name"], value=q)
        for q in QUALIFICATIONS
    ])
    async def school_enroll(self, interaction: discord.Interaction, qualification: app_commands.Choice[str]):
        data = await self.get_user(interaction)
        qual_id = qualification.value
        qual = QUALIFICATIONS[qual_id]

        has = await db.has_qualification(interaction.user.id, qual_id)
        if has:
            await interaction.response.send_message(
                embed=error_embed("Already Earned", f"You already have {qual['name']}.")
            )
            return

        if await self.check_cooldown(interaction, "school"):
            return

        user_quals = await db.get_qualifications(interaction.user.id)
        user_stats = await db.get_all_stats(interaction.user.id)

        for pq in qual["qual_reqs"]:
            if pq not in user_quals:
                pq_name = QUALIFICATIONS.get(pq, {}).get("name", pq)
                await interaction.response.send_message(
                    embed=error_embed("Missing Prerequisite", f"You need {pq_name} first.")
                )
                return

        for stat, req in qual["stat_reqs"].items():
            if user_stats.get(stat, BASE_STAT_VALUE) < req:
                await interaction.response.send_message(
                    embed=error_embed(
                        "Stat Too Low",
                        f"You need {STATS[stat]['short']} {req} (you have {user_stats.get(stat, BASE_STAT_VALUE)}). Train with `/stats train`."
                    )
                )
                return

        if data["wallet"] < qual["cost"]:
            await interaction.response.send_message(
                embed=error_embed("Not Enough Coins", f"{qual['name']} costs {format_money(qual['cost'])}. You have {format_money(data['wallet'])}.")
            )
            return

        await db.update_user(
            interaction.user.id,
            wallet=data["wallet"] - qual["cost"],
            total_spent=data["total_spent"] + qual["cost"],
        )

        for stat, reward in qual.get("stat_rewards", {}).items():
            await db.add_stat(interaction.user.id, stat, reward)

        await db.add_qualification(interaction.user.id, qual_id)
        await db.set_cooldown(interaction.user.id, "school", qual["cooldown_seconds"])

        reward_text = ""
        if qual.get("stat_rewards"):
            reward_parts = [f"{STATS[s]['short']} +{v}" for s, v in qual["stat_rewards"].items()]
            reward_text = f"\nStat rewards: {', '.join(reward_parts)}"

        embed = success_embed(
            f"🎓 Enrolled & Completed!",
            f"You earned **{qual['name']}**!\n"
            f"Cost: {format_money(qual['cost'])}{reward_text}\n"
            f"This qualification unlocks new job opportunities.",
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="qualifications", description="View your earned qualifications")
    async def qualifications_view(self, interaction: discord.Interaction):
        quals = await db.get_qualifications(interaction.user.id)
        if not quals:
            await interaction.response.send_message(
                embed=info_embed("📜 Qualifications", "You have no qualifications yet. Use `/school list` to browse available programs.")
            )
            return

        embed = info_embed("📜 Your Qualifications", f"You have {len(quals)} qualification(s):")
        for qual_id in quals:
            qual = QUALIFICATIONS.get(qual_id)
            if qual:
                embed.add_field(name=qual["name"], value=qual["description"], inline=False)
        await interaction.response.send_message(embed=embed)

    @staticmethod
    def _check_qual_status(qual: dict, user_quals: list, user_stats: dict) -> str:
        for pq in qual["qual_reqs"]:
            if pq not in user_quals:
                return "🔒 Missing prerequisite"
        for stat, req in qual["stat_reqs"].items():
            if user_stats.get(stat, BASE_STAT_VALUE) < req:
                return "🔒 Stats too low"
        return "✅ Available"


async def setup(bot):
    await bot.add_cog(StatsCog(bot))
