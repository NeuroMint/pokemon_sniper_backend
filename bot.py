import os
import discord
import requests
from dotenv import load_dotenv
load_dotenv()

# ---- CONFIG ----
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

API_BASE_URL = "http://127.0.0.1:8000"  # change to your deployed URL later

intents = discord.Intents.default()
intents.message_content = True  # ✅ critical line
client = discord.Client(intents=intents)



def get_listings():
    url = f"{API_BASE_URL}/listings"
    try:
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Error fetching listings: {e}")
        return None



def get_cards():
    url = f"{API_BASE_URL}/cards"
    try:
        res = requests.get(url, timeout=5)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"Error fetching cards: {e}")
        return None


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    # Prevent bot loops
    if message.author.bot:
        return

    content = message.content.strip()

    if content.startswith("!deals"):
        data = get_listings()
        if not data:
            await message.channel.send("No listings found.")
            return

        deals = [l for l in data if l["price"] < 20]  # example threshold

        if not deals:
            await message.channel.send("No deals right now.")
            return

        embed = discord.Embed(title="🔥 Deals Found", color=0xff4500)
        for d in deals[:5]:
            embed.add_field(
                name=d["title"],
                value=f"${d['price']} • {d['condition']}",
                inline=False
            )

        await message.channel.send(embed=embed)


    content = message.content.strip()

    # ---- COMMAND: !ping ----
    if content == "!ping":
        await message.channel.send("Pong 🏓")

    # ---- COMMAND: !listings ----
    if content == "!listings":
        data = get_listings()
        if data is None:
            await message.channel.send("❌ Error talking to backend.")
            return

        if len(data) == 0:
            await message.channel.send("No listings found.")
            return

        embed = discord.Embed(
            title="Latest Listings",
            color=0x00ff99
        )

        for listing in data[:5]:  # show first 5
            title = listing.get("title", "Untitled")
            price = listing.get("price", "N/A")
            condition = listing.get("condition", "Unknown")
            embed.add_field(
                name=f"{title}",
                value=f"💰 ${price} • {condition}",
                inline=False
            )

        await message.channel.send(embed=embed)

    # ---- COMMAND: !cards ----
    if content == "!cards":
        data = get_cards()
        if data is None:
            await message.channel.send("❌ Error talking to backend.")
            return

        if len(data) == 0:
            await message.channel.send("No cards found.")
            return

        embed = discord.Embed(
            title="Stored Cards",
            color=0x3498db
        )

        for card in data[:5]:
            name = card.get("name", "Unknown")
            set_name = card.get("set_name", "Unknown")
            card_number = card.get("card_number", "N/A")
            rarity = card.get("rarity", "N/A")
            embed.add_field(
                name=f"{name} ({set_name})",
                value=f"#{card_number} • {rarity}",
                inline=False
            )

        await message.channel.send(embed=embed)


client.run(DISCORD_TOKEN)
