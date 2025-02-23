import discord
import aiohttp
import asyncio
from discord.ext import commands, tasks

TOKEN = "DISCORD BOT TOKEN GOES HERE"  
CHANNEL_ID = "THE ID OF THE CHANNEL YOU WANT THE BOT TO BE IN, ALSO REMOVE THE QUOTATION MARKS, AND ONLY LEAVE NUMBERS"

ROBLOX_API_HEADERS = {"Accept": "application/json"}


# THE LETTERS FOR THE LB/KOS LIST
leaderboard_map = {
    "A": "Asynd",
    "G": "Grand Navy",
    "B": "Bounty",
    "F": "Fame",
    "K": "KOS LIST"
}

# List of LB/KOS players. The way you format it is:
#    "username": ["LeaderboardCode"],  # For example, "B" for Bounty, "K" for KOS, etc.
#    "another_username": ["LeaderboardCode"],
# ALSO FOR THE LAST USERNAME IN THE LIST REMOVE THE COMMA

players = {
 
  "John": ["B", "A], # REMOVE THESE, THEY ARE JUST EXAMPLES
  "Jake": [F],
  "Joe": [K]


}

# List of required players; only one of these needs to be online (in-game) for the bot to proceed
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
                return data["userPresences"][0]["userPresenceType"] == 2  # 2 means 'In-game'
    return False

@tasks.loop(seconds=720)
async def check_players():
    """Main function to check if tracked players are in a game."""
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        return

  
    required_online = False
    for player in required_players:
        player_id = await get_user_id(player)
        if player_id and await is_player_in_game(player_id):
            required_online = True
            break  

    if not required_online:
        return

  
    user_ids = {}
    for username in players.keys():
        user_id = await get_user_id(username)
        if user_id:
            user_ids[username] = user_id

    
    for username, user_id in user_ids.items():
        if await is_player_in_game(user_id):
            full_leaderboards = [leaderboard_map[lb] for lb in players[username]]
            await channel.send(f"Player: {username}, LB: {', '.join(full_leaderboards)} is in a game")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    check_players.start()  
bot.run(TOKEN)
