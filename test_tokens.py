import discord
import asyncio
import os

async def test_discord_token():
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("No Discord token found")
        return
        
    try:
        bot = discord.Client(intents=discord.Intents.default())
        await bot.login(token)
        print("✅ Discord token is valid")
        await bot.close()
    except Exception as e:
        print(f"❌ Discord token error: {e}")

if __name__ == "__main__":
    asyncio.run(test_discord_token())