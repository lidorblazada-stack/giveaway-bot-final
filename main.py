import discord
from discord.ext import commands
import asyncio

# הגדרת הבוט והרשאות בסיסיות
intents = discord.Intents.default()
intents.message_content = True  # חייב להיות מופעל גם ב-Discord Developer Portal
bot = commands.Bot(command_prefix="!", intents=intents)

# אירוע שקורה כשהבוט נדלק ומסנכרן את הפקודות
@bot.event
async def on_ready():
    print(f'הבוט נדלק בהצלחה בתור: {bot.user.name}')
    try:
        # השורה הזו דואגת שהפקודה תופיע בדיסקורד שלך מיד!
        synced = await bot.tree.sync()
        print(f"סונכרנו {len(synced)} פקודות סלאש בהצלחה!")
    except Exception as e:
        print(f"שגיאה בסנכרון הפקודות: {e}")

# הפקודה שתשגע את המשתמשים חחח
@bot.tree.command(name="ping-user", description="לתייג חבר שלא עונה כדי להציק לו חחח")
async def ping_user(interaction: discord.Interaction, target: discord.User, amount: int):
    # הגבלת כמות ל-10 כדי שדיסקורד לא יחסמו את הבוט על ספאם
    if amount > 10:
        amount = 10
    if amount < 1:
        amount = 1
        
    # הודעה זמנית שרק אתה רואה
    await interaction.response.send_message(f"מתחיל לתייג את {target.mention} כ-{amount} פעמים... חחח", ephemeral=True)
    
    # הלולאה שמציקה בערוץ
    for i in range(amount):
        await interaction.channel.send(f"נוווו ענה כברררר {target.mention} !!!")
        await asyncio.sleep(1) # הפסקה של שנייה בין תיוג לתיוג

# שים לב אחי: את הטוקן (Token) של הבוט שלך אתה צריך לשים ב-Render בתוך ה-Environment Variables תחת השם BOT_TOKEN
import os
bot.run(os.getenv('BOT_TOKEN'))
