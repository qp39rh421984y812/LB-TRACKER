import discord
import aiohttp
import asyncio
from discord.ext import commands, tasks

TOKEN = ""
CHANNEL_ID = ""

ROBLOX_API_HEADERS = {"Accept": "application/json"}

leaderboard_map = {
    "A": "Asynd",
    "G": "Grand Navy",
    "B": "Bounty",
    "F": "Fame",
    "K": "KOS LIST"
}

#Player List:
players = {




}

#White list
required_players = [
    
]

intents = discord.Intents.default()
intents.presences = True  
intents.members = True    
bot = commands.Bot(command_prefix="!", intents=intents)

async def get_user_id(username):
    """Fetch Roblox user ID from username."""
    url = "https://users.roblox.com/v1/usernames/users"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"usernames": [username]}, headers=ROBLOX_API_HEADERS) as resp:
            data = await resp.json()
            if "data" in data and data["data"]:
                return data["data"][0]["id"]
    return None

async def is_player_in_game(user_id):
    """Check if a user ID is currently in a game."""
    url = "https://presence.roblox.com/v1/presence/users"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"userIds": [user_id]}, headers=ROBLOX_API_HEADERS) as resp:
            data = await resp.json()
            if "userPresences" in data and data["userPresences"]:
                return data["userPresences"][0]["userPresenceType"] == 2 
    return False

@tasks.loop(seconds=720)
async def check_players():
    """Main function to check if tracked players are in a game."""
    print(f"Attempting to fetch channel with ID {CHANNEL_ID}")

    try:
        channel = await bot.fetch_channel(CHANNEL_ID)
        print(f"Found channel: {channel.name} (ID: {channel.id}) in server: {channel.guild.name} (ID: {channel.guild.id})")
    except discord.NotFound:
        print(f"Could not find channel with ID {CHANNEL_ID}")
        return
    except discord.Forbidden:
        print(f"Bot does not have permission to view the channel with ID {CHANNEL_ID}")
        return
    except discord.HTTPException as e:
        print(f"An error occurred while trying to fetch the channel: {e}")
        return


    if not channel.permissions_for(channel.guild.me).send_messages:
        print(f"Bot doesn't have permission to send messages in {channel.name}.")
        return

    try:
        await channel.send("Test message: I'm checking if players are in-game.")
        print("Test message sent successfully.")
    except Exception as e:
        print(f"Error sending test message: {e}")

  
    for username, leaderboards in players.items():
        user_id = await get_user_id(username)
        if user_id and await is_player_in_game(user_id):
            full_leaderboards = [leaderboard_map.get(lb, lb) for lb in leaderboards]
            await channel.send(f"Player {username} is in-game and belongs to: {', '.join(full_leaderboards)}")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    check_players.start() 

bot.run(TOKEN)
