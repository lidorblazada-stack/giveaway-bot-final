import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import random
import time
import os
from flask import Flask
from threading import Thread

# שרת פנימי כדי ש-Render לא יכבה את הבוט
app = Flask('')
@app.route('/')
def home():
    return "I'm alive!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

class GiveawayView(discord.ui.View):
    def __init__(self, timeout):
        super().__init__(timeout=timeout)
        self.participants = []

    @discord.ui.button(label="join!", style=discord.ButtonStyle.danger, emoji="🎉")
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user in self.participants:
            return await interaction.response.send_message("אתה כבר רשום להגרלה!", ephemeral=True)
        
        self.participants.append(interaction.user)
        embed = interaction.message.embeds[0]
        embed.set_field_at(1, name="👥 Participants:", value=f"**{len(self.participants)}**", inline=True)
        await interaction.message.edit(embed=embed)
        await interaction.response.send_message("נרשמת בהצלחה! בהצלחה 🍀", ephemeral=True)

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"✅ הפקודות סונכרנו!")

bot = MyBot()

@bot.event
async def on_ready():
    print(f'✅ מחובר כ: {bot.user}')

@bot.tree.command(name="giveaway", description="התחלת הגרלה עם כפתור")
async def giveaway(interaction: discord.Interaction, days: int, prize: str):
    duration_seconds = days * 86400
    end_time_unix = int(time.time() + duration_seconds)
    
    embed = discord.Embed(
        title=f"🎉 {prize} 🎉",
        description="לחצו על הכפתור למטה כדי להשתתף!",
        color=discord.Color.from_rgb(255, 215, 0)
    )
    embed.add_field(name="🏆 Winners:", value="1", inline=True)
    embed.add_field(name="👥 Participants:", value="**0**", inline=True)
    embed.add_field(name="⏳ Ends in:", value=f"<t:{end_time_unix}:R>", inline=False)
    
    view = GiveawayView(timeout=duration_seconds)
    await interaction.response.send_message("ההגרלה פורסמה!", ephemeral=True)
    message = await interaction.channel.send(embed=embed, view=view)

    await asyncio.sleep(duration_seconds)

    if not view.participants:
        await interaction.channel.send(f"ההגרלה על **{prize}** הסתיימה ללא משתתפים.")
    else:
        winner = random.choice(view.participants)
        await interaction.channel.send(f"🎊 מזל טוב {winner.mention}! זכית ב-**{prize}**! 🎊")

keep_alive()
# כאן הבוט מושך את הטוקן מה-Environment Variables של Render
bot.run(os.getenv('DISCORD_TOKEN'))
