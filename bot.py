import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import datetime
import json
import random
import requests
from flask import Flask
from threading import Thread

# -------------------
# Chargement des variables d'environnement
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# -------------------
# Keep alive pour Replit / VPS
app = Flask('')

@app.route('/')
def home():
    return "Bot actif ✅"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# -------------------
# Signes FR -> EN pour l'API
SIGNS_FR_EN = {
    "bélier": "aries",
    "taureau": "taurus",
    "gémeaux": "gemini",
    "cancer": "cancer",
    "lion": "leo",
    "vierge": "virgo",
    "balance": "libra",
    "scorpion": "scorpio",
    "sagittaire": "sagittarius",
    "capricorne": "capricorn",
    "verseau": "aquarius",
    "poissons": "pisces"
}

# -------------------
# Abonnés
ABONNES_FILE = "abonnes.json"

def charger_abonnes():
    if os.path.exists(ABONNES_FILE):
        with open(ABONNES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def sauvegarder_abonnes(data):
    with open(ABONNES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

abonnes = charger_abonnes()

# -------------------
# Générer horoscope stylé
def generer_horoscope_stylé(signe_fr):
    try:
        signe_en = SIGNS_FR_EN.get(signe_fr.lower())
        res = requests.get(f"https://ohmanda.com/api/horoscope/{signe_en}")
        texte_api = res.json().get("horoscope", "") if res.status_code == 200 else ""

        energies = ["Haute", "Stable", "Faible", "Changeante", "Équilibrée", "Intense", "Douce", "Positive", "Nerveuse", "Apaisée"]

        amours = [
            "Une belle surprise t’attend aujourd’hui 💕",
            "Un regard pourrait tout changer 💫",
            "Ton cœur vibre plus fort que d’habitude ❤️",
            "Ne cherche pas à tout contrôler, laisse la magie opérer ✨",
            "Une discussion sincère renforcera ton lien 💬",
            "L’amour est plus proche que tu ne le crois 🌹",
            "Tu attires naturellement les bonnes personnes 🌟",
            "Une ancienne flamme pourrait réapparaître 🔥",
            "Évite les malentendus : parle avec ton cœur 💖",
            "Aujourd’hui, fais confiance à ton intuition amoureuse 💞",
            "La tendresse te fera du bien, donne-en autant que tu en veux 🤗",
            "Un message inattendu pourrait te faire sourire 📩",
            "Si tu es en couple, un beau moment de complicité t’attend 💍",
            "Célibataire ? Ouvre les yeux, une belle rencontre est possible 💘",
            "Ne cours pas après l’amour, il te rattrapera 💌",
            "Un geste sincère va te toucher profondément 💓",
            "Apprends à aimer sans attentes, juste pour le plaisir d’aimer 🌈",
            "Ne te ferme pas à la nouveauté sentimentale 💭",
            "Laisse tomber les rancunes, fais place à la paix intérieure 🕊️",
            "L’amour te guide vers un chemin plus doux aujourd’hui 🌷"
        ]

        travails = [
            "Ta persévérance sera récompensée 💼",
            "Une opportunité se profile, reste attentif 👀",
            "Ton sérieux inspire confiance à tes collègues 🤝",
            "Un projet avance plus vite que prévu 🚀",
            "Prends les devants, ton audace paiera 🔥",
            "Reste calme face à la pression, tu gères 💪",
            "Ton travail parle pour toi, même en silence 🎯",
            "Une petite victoire va booster ta motivation 🏆",
            "Sois créatif, une idée peut tout changer 💡",
            "Ne néglige pas les détails, ils feront la différence 📋",
            "Ton esprit d’équipe sera apprécié aujourd’hui 🤗",
            "Un échange pourrait t’ouvrir une nouvelle porte 🔑",
            "Fais confiance à ton instinct professionnel 🌟",
            "Garde la tête froide, tout rentrera dans l’ordre 🧊",
            "Ta rigueur va impressionner quelqu’un d’important 👔",
            "Ne laisse pas la fatigue prendre le dessus 😴",
            "Apprends à déléguer, tu n’as pas à tout porter seul 🧠",
            "Ton courage face aux défis sera remarqué 🌄",
            "Un collègue pourrait devenir un véritable allié 🤝",
            "La réussite n’est pas loin, continue sur ta lancée 🏁"
        ]

        conseils = [
            "Ne doute pas de toi, avance avec confiance 🌟",
            "Laisse le passé derrière toi et avance 🚀",
            "Suis ton instinct, il est juste aujourd’hui 💫",
            "Prends du temps pour toi, tu le mérites ☕",
            "Une pause t’aidera à mieux repartir 🌿",
            "Écoute ton cœur avant ton mental 💭",
            "Accepte ce que tu ne peux pas changer 🍃",
            "Fais une action aujourd’hui qui te rend fier 🔥",
            "Apprends à dire non quand c’est nécessaire 🚫",
            "Ton sourire est ta meilleure arme 😄",
            "Sois indulgent envers toi-même 💖",
            "Ne te compare à personne, ton chemin est unique 🌈",
            "Écris ce que tu ressens, cela t’apaisera ✍️",
            "Garde ton calme, la clarté reviendra ☀️",
            "Une bonne nouvelle arrive, reste patient 🎁",
            "Laisse parler ton intuition, elle ne te trompe pas 🔮",
            "La gratitude attire encore plus de positif 🙏",
            "Fais confiance à la vie, elle sait où te conduire 🌊",
            "Ton énergie influence ton entourage, rayonne ✨",
            "N’oublie pas : le bonheur est souvent dans les petites choses 🌸"
        ]

        message = (
            f"**Horoscope du jour – {signe_fr.capitalize()} ♈**\n"
            f"> 💫 *Énergie :* {random.choice(energies)}\n"
            f"> ❤️ *Amour :* {random.choice(amours)}\n"
            f"> 💼 *Travail :* {random.choice(travails)}\n"
            f"> 🌟 *Conseil du jour :* {random.choice(conseils)}"
        )
        return message
    except Exception as e:
        return f"Erreur : {e}"

# -------------------
# Events et slash commands
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Connecté en tant que {bot.user}")
    if not daily_horoscope.is_running():
        daily_horoscope.start()

# -------------------
# Slash commands
@bot.tree.command(name="horoscope", description="Afficher l'horoscope du jour pour un signe")
@app_commands.describe(signe="Choisir votre signe astrologique")
async def horoscope(interaction: discord.Interaction, signe: str):
    signe = signe.lower()
    if signe not in SIGNS_FR_EN:
        await interaction.response.send_message("❌ Signe inconnu.")
    else:
        msg = generer_horoscope_stylé(signe)
        await interaction.response.send_message(msg)

@bot.tree.command(name="abonner", description="Recevoir ton horoscope en DM chaque matin")
@app_commands.describe(signe="Choisir votre signe astrologique")
async def abonner(interaction: discord.Interaction, signe: str):
    signe = signe.lower()
    if signe not in SIGNS_FR_EN:
        await interaction.response.send_message("❌ Signe inconnu.")
    else:
        abonnes[str(interaction.user.id)] = signe
        sauvegarder_abonnes(abonnes)
        await interaction.response.send_message(f"✨ Tu es abonné à **{signe.capitalize()}** !")

@bot.tree.command(name="désabonner", description="Arrêter de recevoir l'horoscope")
async def desabonner(interaction: discord.Interaction):
    uid = str(interaction.user.id)
    if uid in abonnes:
        del abonnes[uid]
        sauvegarder_abonnes(abonnes)
        await interaction.response.send_message("🚫 Tu es désabonné.")
    else:
        await interaction.response.send_message("Tu n’étais pas abonné 😉")

# -------------------
# Envoi automatique 8h
@tasks.loop(minutes=1)
async def daily_horoscope():
    now = datetime.datetime.now()
    if now.hour == 8 and now.minute == 0:
        for uid, signe in abonnes.items():
            user = await bot.fetch_user(int(uid))
            msg = generer_horoscope_stylé(signe)
            await user.send(msg)

# -------------------
# Lancement du bot
bot.run(TOKEN)
