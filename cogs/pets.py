import discord
from discord import app_commands
from discord.ext import commands
import random
import database as db
from utils.embeds import success_embed, error_embed, info_embed, format_money
from utils.helpers import check_level_up, xp_for_next_level, clamp, stat_modifier
from utils.narrative import get_action_text
from config import PETS, HEALTH_MAX, HUNGER_MAX, THIRST_MAX, ACHIEVEMENTS


class Pets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="pet", description="Manage your pet: shop, adopt, info, feed, play, battle, abandon")
    @app_commands.choices(action=[
        app_commands.Choice(name="\U0001F6D2 Shop", value="shop"),
        app_commands.Choice(name="\U0001F43E Adopt", value="adopt"),
        app_commands.Choice(name="\U0001F4CA Info", value="info"),
        app_commands.Choice(name="\U0001F356 Feed", value="feed"),
        app_commands.Choice(name="\U0001F3BE Play", value="play"),
        app_commands.Choice(name="\u2694\uFE0F Battle", value="battle"),
        app_commands.Choice(name="\U0001F44B Abandon", value="abandon"),
    ])
    @app_commands.choices(pet=[
        app_commands.Choice(name=f"{p['emoji']} {p['name']} — {format_money(p['price'])}", value=pid)
        for pid, p in PETS.items()
    ])
    async def pet(self, interaction: discord.Interaction, action: str, pet: str = None, user: discord.Member = None):
        if action == "shop":
            await self._pet_shop(interaction)
        elif action == "adopt":
            if not pet:
                await interaction.response.send_message(embed=error_embed("Error", "Select a pet to adopt."), ephemeral=True)
                return
            await self._adopt(interaction, pet)
        elif action == "info":
            await self._pet_info(interaction)
        elif action == "feed":
            await self._pet_feed(interaction)
        elif action == "play":
            await self._pet_play(interaction)
        elif action == "battle":
            if not user:
                await interaction.response.send_message(embed=error_embed("Error", "Select a user to battle."), ephemeral=True)
                return
            await self._pet_battle(interaction, user)
        elif action == "abandon":
            await self._pet_abandon(interaction)
        else:
            await interaction.response.send_message(embed=error_embed("Error", "Invalid action."), ephemeral=True)

    async def _pet_shop(self, interaction: discord.Interaction):
        embed = info_embed("🐾 Pet Shop", "Adopt a companion! Pets give passive bonuses and can battle.")
        for pet_id, pet in PETS.items():
            embed.add_field(
                name=f"{pet['emoji']} {pet['name']} — {format_money(pet['price'])}",
                value=f"Type: {pet['type']}\nBonus: {pet['bonus']}\nBase Power: {pet['base_power']}",
                inline=True,
            )
        await interaction.response.send_message(embed=embed)

    async def _adopt(self, interaction: discord.Interaction, pet_id: str):
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        pet_data = PETS[pet_id]

        if data.get("pet_id"):
            await interaction.response.send_message(embed=error_embed("Already Have Pet", f"You already have a pet. Use `/pet` with action Abandon first."), ephemeral=True)
            return

        if data["wallet"] < pet_data["price"]:
            await interaction.response.send_message(embed=error_embed("Insufficient Funds", f"You need {format_money(pet_data['price'])} but only have {format_money(data['wallet'])}."), ephemeral=True)
            return

        await db.update_user(interaction.user.id,
            wallet=data["wallet"] - pet_data["price"],
            pet_id=pet_id,
            pet_name=pet_data["name"],
            pet_level=1,
            pet_xp=0,
            pet_happiness=100,
            pet_hunger=100,
            pet_health=100,
        )
        await db.add_transaction(interaction.user.id, "pet_adopt", pet_data["price"], f"Adopted {pet_data['name']}")

        embed = success_embed(f"🐾 Adopted {pet_data['name']}!", get_action_text("pets", "adopt", emoji=pet_data['emoji'], pet_name=pet_data['name']))
        new_achievements = await db.check_achievements(interaction.user.id)
        for ach_id in new_achievements:
            ach = ACHIEVEMENTS[ach_id]
            embed.add_field(name="🏆 Achievement Unlocked!", value=f"{ach['emoji']} **{ach['name']}** — +{format_money(ach['reward'])}!", inline=False)
        if new_achievements:
            ach_reward = sum(ACHIEVEMENTS[a]["reward"] for a in new_achievements)
            await db.update_user(interaction.user.id, wallet=data["wallet"] - pet_data["price"] + ach_reward, total_earned=data["total_earned"] + ach_reward)
        await interaction.response.send_message(embed=embed)

    async def _pet_info(self, interaction: discord.Interaction):
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        if not data.get("pet_id"):
            await interaction.response.send_message(embed=error_embed("No Pet", "You don't have a pet. Use `/pet` with action Adopt to get one!"), ephemeral=True)
            return

        pet_data = PETS.get(data["pet_id"], {})
        embed = info_embed(f"🐾 {data.get('pet_name', 'Pet')}", pet_data.get("emoji", "🐱"))
        embed.add_field(name="Type", value=pet_data.get("type", "Unknown"), inline=True)
        embed.add_field(name="Level", value=str(data.get("pet_level", 1)), inline=True)
        embed.add_field(name="XP", value=f"{data.get('pet_xp', 0)} / {xp_for_next_level(data.get('pet_level', 1))}", inline=True)
        embed.add_field(name="❤️ Health", value=f"{data.get('pet_health', 100)}/100", inline=True)
        embed.add_field(name="😊 Happiness", value=f"{data.get('pet_happiness', 100)}/100", inline=True)
        embed.add_field(name="🍖 Hunger", value=f"{data.get('pet_hunger', 100)}/100", inline=True)
        power = pet_data.get("base_power", 10) + data.get("pet_level", 1) * 5
        embed.add_field(name="⚔️ Power", value=str(power), inline=True)
        embed.add_field(name="✨ Bonus", value=pet_data.get("bonus", "None"), inline=False)
        await interaction.response.send_message(embed=embed)

    async def _pet_feed(self, interaction: discord.Interaction):
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        if not data.get("pet_id"):
            await interaction.response.send_message(embed=error_embed("No Pet", "You don't have a pet."), ephemeral=True)
            return

        cd = await db.check_cooldown(interaction.user.id, "pet_feed")
        if cd > 0:
            mins = int(cd // 60)
            secs = int(cd % 60)
            await interaction.response.send_message(embed=error_embed("On Cooldown", f"Your pet is still digesting. Try again in {mins}m {secs}s."), ephemeral=True)
            return

        cost = 50
        if data["wallet"] < cost:
            await interaction.response.send_message(embed=error_embed("Insufficient Funds", f"Feeding costs {format_money(cost)}."), ephemeral=True)
            return

        await db.update_user(interaction.user.id,
            wallet=data["wallet"] - cost,
            pet_hunger=clamp(data.get("pet_hunger", 100) + 30, 0, 100),
            pet_happiness=clamp(data.get("pet_happiness", 100) + 5, 0, 100),
        )
        await db.set_cooldown(interaction.user.id, "pet_feed", 300)
        await interaction.response.send_message(embed=success_embed("🍖 Pet Fed!", get_action_text("pets", "feed", pet_name=data.get('pet_name', 'Your pet'), cost=format_money(cost))))

    async def _pet_play(self, interaction: discord.Interaction):
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        if not data.get("pet_id"):
            await interaction.response.send_message(embed=error_embed("No Pet", "You don't have a pet."), ephemeral=True)
            return

        cd = await db.check_cooldown(interaction.user.id, "pet_play")
        if cd > 0:
            mins = int(cd // 60)
            await interaction.response.send_message(embed=error_embed("On Cooldown", f"Your pet is tired. Try again in {mins}m."), ephemeral=True)
            return

        xp_gain = random.randint(5, 15)
        new_pet_xp = data.get("pet_xp", 0) + xp_gain
        pet_level = data.get("pet_level", 1)
        leveled = False
        while new_pet_xp >= xp_for_next_level(pet_level):
            new_pet_xp -= xp_for_next_level(pet_level)
            pet_level += 1
            leveled = True

        await db.update_user(interaction.user.id,
            pet_happiness=clamp(data.get("pet_happiness", 100) + 20, 0, 100),
            pet_xp=new_pet_xp,
            pet_level=pet_level,
        )
        await db.set_cooldown(interaction.user.id, "pet_play", 1800)

        embed = success_embed("🎾 Played with Pet!", get_action_text("pets", "play", pet_name=data.get('pet_name', 'Your pet'), xp=xp_gain))
        if leveled:
            embed.add_field(name="🎉 Pet Leveled Up!", value=get_action_text("pets", "pet_levelup", pet_name=data.get('pet_name', 'Your pet'), level=pet_level), inline=False)
        await interaction.response.send_message(embed=embed)

    async def _pet_battle(self, interaction: discord.Interaction, user: discord.Member):
        if user.id == interaction.user.id:
            await interaction.response.send_message(embed=error_embed("Error", "You can't battle yourself."), ephemeral=True)
            return

        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        target_data = await db.get_or_create_user(user.id, interaction.guild.id if interaction.guild else 0)

        cd = await db.check_cooldown(interaction.user.id, "pet_battle")
        if cd > 0:
            mins = int(cd // 60)
            await interaction.response.send_message(embed=error_embed("On Cooldown", f"Your pet is recovering from its last battle. Try again in {mins}m."), ephemeral=True)
            return

        if not data.get("pet_id"):
            await interaction.response.send_message(embed=error_embed("No Pet", "You don't have a pet."), ephemeral=True)
            return
        if not target_data.get("pet_id"):
            await interaction.response.send_message(embed=error_embed("No Pet", f"{user.display_name} doesn't have a pet."), ephemeral=True)
            return

        my_pet = PETS.get(data["pet_id"], {})
        their_pet = PETS.get(target_data["pet_id"], {})

        my_power = my_pet.get("base_power", 10) + data.get("pet_level", 1) * 5 + data.get("pet_happiness", 100) // 10
        their_power = their_pet.get("base_power", 10) + target_data.get("pet_level", 1) * 5 + target_data.get("pet_happiness", 100) // 10

        mods = stat_modifier(data, "pet_battle")
        my_power = int(my_power * mods["pay_mult"])

        my_roll = random.randint(1, my_power)
        their_roll = random.randint(1, their_power)

        if my_roll >= their_roll:
            reward = random.randint(50, 150)
            xp_gain = int(random.randint(15, 30) * mods["xp_mult"])
            new_xp = data["xp"] + xp_gain
            new_level, leveled_up = check_level_up(new_xp, data["level"])
            if leveled_up:
                new_xp -= sum(xp_for_next_level(l) for l in range(data["level"], new_level))

            await db.update_user(interaction.user.id,
                wallet=data["wallet"] + reward,
                xp=new_xp,
                level=new_level,
                pet_xp=data.get("pet_xp", 0) + 20,
                total_earned=data["total_earned"] + reward,
                battles_won=data.get("battles_won", 0) + 1,
            )
            await db.update_user(user.id,
                pet_happiness=clamp(target_data.get("pet_happiness", 100) - 10, 0, 100),
            )
            embed = success_embed("⚔️ Pet Battle — Victory!", get_action_text("pets", "battle_win", pet_name=data.get('pet_name', 'pet'), opponent=user.display_name, opponent_pet=target_data.get('pet_name', 'pet'), reward=format_money(reward), xp=xp_gain))
            if leveled_up:
                embed.add_field(name="🎉 Level Up!", value=f"Level {new_level}!", inline=False)
        else:
            health_loss = random.randint(5, 15)
            await db.update_user(interaction.user.id,
                pet_health=clamp(data.get("pet_health", 100) - health_loss, 0, 100),
                pet_happiness=clamp(data.get("pet_happiness", 100) - 5, 0, 100),
            )
            embed = error_embed("⚔️ Pet Battle — Defeat!", get_action_text("pets", "battle_loss", pet_name=data.get('pet_name', 'pet'), opponent=user.display_name, opponent_pet=target_data.get('pet_name', 'pet'), hp_loss=health_loss))

        await db.set_cooldown(interaction.user.id, "pet_battle", 3600)
        await interaction.response.send_message(embed=embed)

    async def _pet_abandon(self, interaction: discord.Interaction):
        data = await db.get_or_create_user(interaction.user.id, interaction.guild.id if interaction.guild else 0)
        if not data.get("pet_id"):
            await interaction.response.send_message(embed=error_embed("No Pet", "You don't have a pet."), ephemeral=True)
            return

        await db.update_user(interaction.user.id,
            pet_id=None, pet_name=None, pet_level=1, pet_xp=0,
            pet_happiness=100, pet_hunger=100, pet_health=100,
        )
        await interaction.response.send_message(embed=success_embed("🐾 Pet Abandoned", get_action_text("pets", "abandon")))


async def setup(bot):
    await bot.add_cog(Pets(bot))
