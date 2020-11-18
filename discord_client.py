import discord
import logging

from os import getenv
from dotenv import load_dotenv
from discord.ext import commands
from logic import LogicManager
from spotify_client import SpotifyClient

LOG_FORMAT = "%(asctime)s - %(message)s"
logging.basicConfig(filename='data/logger.log', level=logging.CRITICAL, format=LOG_FORMAT)
logger = logging.getLogger()

load_dotenv()

intents = discord.Intents.default()
intents.messages = True

PREFIX = '!'
manager = LogicManager()
spotify = SpotifyClient()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.command(name="update")
async def update_database(ctx):
    if ctx.author.bot:
        return

    result = manager.update_database()
    decoded_changes = []

    for playlist in result:
        playlist_info = spotify.get_playlist(playlist['id'])

        decoded_new = []
        for i in playlist['new']:
            track = spotify.get_track(i)
            artists = ', '.join([x['name'] for x in track['artists']])
            logger.critical(f"Added track to \"{playlist_info['name']}\" - {track['name']} by {artists}")
            decoded_new.append({"name": track['name'], "artists": artists})

        decoded_del = []
        for i in playlist['del']:
            track = spotify.get_track(i)
            artists = ', '.join([x['name'] for x in track['artists']])
            logger.critical(f"Deleted track from \"{playlist_info['name']}\" - {track['name']} by {artists}")
            decoded_del.append({"name": track['name'], "artists": artists})

        decoded_changes.append({"name": playlist_info['name'], "new": decoded_new, "del": decoded_del})

    for playlist in decoded_changes:
        embed = discord.Embed(
            title=f'Changes detected in \"{playlist["name"]}\"',
        )
        if len(playlist['new']) > 0:
            embed.add_field(
                name=f"Added {len(playlist['new'])} songs:",
                value='\n\n'.join(f"{x['name']} by {x['artists']}" for x in playlist['new']),
                inline=False
            )

        if len(playlist['del']) > 0:
            embed.add_field(
                name=f"Deleted {len(playlist['del'])} songs:",
                value='\n\n'.join(f"{x['name']} by {x['artists']}" for x in playlist['del']),
                inline=False
            )

        await ctx.send(embed=embed)
    
    if not decoded_changes:
        await ctx.send("No changes detected in any of the playlists. How booooring!")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


bot.run(getenv('DISCORD_TOKEN'))
