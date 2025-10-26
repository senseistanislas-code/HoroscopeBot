# cogs/daily_horoscope.py
import os
import io
import json
import datetime
from zoneinfo import ZoneInfo

import nextcord
from nextcord.ext import commands, tasks

from PIL import Image, ImageDraw, ImageFont

# --- CONFIGURE ICI si besoin ---
TEMPLATE_PATH = "assets/template.png"           # ton image déjà prête (fond + éléments statiques)
OUTPUT_PATH = "output/daily_horoscope.png"
HOROSCOPE_JSON = "assets/horoscopes.json"       # fichier contenant les 12 phrases
FONT_TITLE = "assets/fonts/PlayfairDisplay-Bold.ttf"   # pour les titres (ex. Bélier)
FONT_TEXT = "assets/fonts/Inter-Regular.ttf"           # pour les textes/descriptions
POST_HOUR = 8    # heure locale (Europe/Paris) où poster
CHANNEL_ID = 123456789012345678  # <-- remplace par l'ID du salon où poster
TIMEZONE = "Europe/Paris"
# -------------------------------

SIGNS_ORDER = [
    "Bélier", "Taureau", "Gémeaux", "Cancer",
    "Lion", "Vierge", "Balance", "Scorpion",
    "Sagittaire", "Capricorne", "Verseau", "Poissons"
]

class DailyHoroscope(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.tz = ZoneInfo(TIMEZONE)
        # démarre la tâche planifiée
        self.post_daily_horoscope.start()

    def cog_unload(self):
        self.post_daily_horoscope.cancel()

    def load_horoscopes(self):
        if not os.path.exists(HOROSCOPE_JSON):
            raise FileNotFoundError(f"{HOROSCOPE_JSON} introuvable.")
        with open(HOROSCOPE_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        # assure que toutes les clés existent
        for s in SIGNS_ORDER:
            if s not in data:
                data[s] = ""  # champ vide si absent
        return data

    def render_image(self, horoscopes: dict):
        # ouvre le template
        img = Image.open(TEMPLATE_PATH).convert("RGBA")
        W, H = img.size

        draw = ImageDraw.Draw(img)

        # charger polices (guider l'utilisateur à ajouter des fichiers de police)
        try:
            font_title = ImageFont.truetype(FONT_TITLE, size=int(W * 0.035))
        except Exception:
            font_title = ImageFont.load_default()
        try:
            font_text = ImageFont.truetype(FONT_TEXT, size=int(W * 0.023))
        except Exception:
            font_text = ImageFont.load_default()

        # date en haut (format français : 25 oct. 2025)
        now = datetime.datetime.now(self.tz)
        date_str = now.strftime("%-d %b. %Y")  # ex: 25 oct. 2025
        # position date (ajuster selon template)
        date_font = ImageFont.truetype(FONT_TEXT, size=int(W * 0.028)) if os.path.exists(FONT_TEXT) else font_text
        date_w, date_h = draw.textsize(date_str, font=date_font)
        # center top text
        draw.text(((W - date_w) / 2, H * 0.12), date_str, font=date_font, fill=(210, 198, 230, 255))

        # définir colonnes (2 colonnes comme ton exemple)
        left_x = int(W * 0.06)
        right_x = int(W * 0.53)
        col_width = int(W * 0.4)
        gap_y = int(H * 0.06)
        start_y = int(H * 0.20)

        for idx, sign in enumerate(SIGNS_ORDER):
            # colonne et ligne
            col_x = left_x if idx < 6 else right_x
            row = idx % 6
            y = start_y + row * gap_y

            # titre
            draw.text((col_x, y), sign, font=font_title, fill=(240, 230, 250, 255))
            # description — multi-line wrapping
            desc = horoscopes.get(sign, "")
            # wrap text to fit column width
            lines = []
            words = desc.split()
            if words:
                line = ""
                for w in words:
                    test = (line + " " + w).strip()
                    w_w, _ = draw.textsize(test, font=font_text)
                    if w_w <= col_width:
                        line = test
                    else:
                        lines.append(line)
                        line = w
                if line:
                    lines.append(line)
            else:
                lines = [""]

            text_y = y + int(H * 0.03)
            for l in lines:
                draw.text((col_x, text_y), l, font=font_text, fill=(220, 210, 230, 255))
                text_y += int(H * 0.028)

            # option : trait horizontal séparateur — si ton template n'en a pas, on peut dessiner un simple trait
            # draw.line([(col_x, text_y + 8), (col_x + col_width, text_y + 8)], fill=(120,100,140,120), width=1)

        # sauver dans bytes
        with io.BytesIO() as bio:
            img.save(bio, "PNG")
            bio.seek(0)
            return bio.read()

    @tasks.loop(time=datetime.time(hour=POST_HOUR, minute=0, tzinfo=ZoneInfo(TIMEZONE)))
    async def post_daily_horoscope(self):
        await self.bot.wait_until_ready()
        try:
            horoscopes = self.load_horoscopes()
        except Exception as e:
            print("Erreur chargement horoscopes:", e)
            return

        try:
            image_bytes = self.render_image(horoscopes)
        except Exception as e:
            print("Erreur génération image:", e)
            return

        channel = self.bot.get_channel(CHANNEL_ID)
        if channel is None:
            # essayer fetch (si bot n'a pas le channel en cache)
            try:
                channel = await self.bot.fetch_channel(CHANNEL_ID)
            except Exception as e:
                print("Impossible d'obtenir le salon :", e)
                return

        file = nextcord.File(io.BytesIO(image_bytes), filename="horoscope_du_jour.png")
        try:
            await channel.send(file=file)
            print(f"Horoscope posté le {datetime.datetime.now(self.tz).date()}")
        except Exception as e:
            print("Erreur envoi Discord :", e)

    @post_daily_horoscope.before_loop
    async def before_post(self):
        await self.bot.wait_until_ready()
        print("Tâche quotidienne horoscope démarrée.")

# setup
def setup(bot):
    bot.add_cog(DailyHoroscope(bot))
