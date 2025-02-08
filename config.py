import re, os

id_pattern = re.compile(r'^.\d+$') 

API_ID = os.environ.get("API_ID", "22299340")

API_HASH = os.environ.get("API_HASH", "09b09f3e2ff1306da4a19888f614d937")

BOT_TOKEN = os.environ.get("BOT_TOKEN", "7906213903:AAHCrLWgHppbCIdRm7kjnmovnBLIfCtPRVM") 

FORCE_SUB = os.environ.get("FORCE_SUB", "animelibraryn4") 

DB_NAME = os.environ.get("DB_NAME","Nt1")     

DB_URL = os.environ.get("DB_URL","mongodb+srv://Nt1:<db_password>@nt1.thwrt.mongodb.net/?retryWrites=true&w=majority&appName=NT1")
 
FLOOD = int(os.environ.get("FLOOD", "10"))

START_PIC = os.environ.get("START_PIC", "https://www.freepik.com/free-photo/bright-pop-landscape-design_21141824.htm#fromView=keyword&page=1&position=0&uuid=e54373c7-1b2e-427f-b931-ce2f10adc902&query=Anime+Wallpaper")

ADMIN = [int(admin) if id_pattern.search(admin) else admin for admin in os.environ.get('ADMIN', '5380609667').split()]

PORT = os.environ.get("PORT", "8080")
