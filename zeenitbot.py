import os
import threading
import json
from dotenv import load_dotenv
from unidecode import unidecode
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# 1. CARGAR CONFIGURACIÓN
load_dotenv()
TOKEN = os.getenv("TOKEN")

# 2. CONFIGURACIÓN DE FLASK
web_app = Flask(__name__)

@web_app.route('/')
def health_check():
    return "Zeenit está vivo 🧠✨", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)

# 3. LÓGICA DEL BOT
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola 👋 Soy ZeenitBot 🧠✨. ¿En qué puedo ayudarte hoy?")


async def motivacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1. Avisamos que estamos buscando (para que el alumno no desespere)
    await update.message.reply_text("Buscando sabiduría en la red para ti... 🧠✨")
    
    try:
        # 2. Hacemos la llamada a la API de ZenQuotes
        respuesta = requests.get('https://zenquotes.io/api/random')
        
        # 3. Convertimos la respuesta a formato JSON (como el tuyo)
        datos = respuesta.json()
        
        # 4. Extraemos la frase (q = quote) y el autor (a = author)
        frase = datos[0]['q']
        autor = datos[0]['a']
        
        # 5. Armamos el mensaje final y lo enviamos
        mensaje_final = f"«{frase}»\n— {autor}"
        await update.message.reply_text(mensaje_final)
        
    except Exception as e:
        # Si el internet falla o la API se cae, el bot no explota
        await update.message.reply_text("Mi conexión con los filósofos está fallando un poco. ¡Pero recuerda que tú puedes con esto! 💪")

#RESPONDER
def cargar_conocimiento():
    with open('conocimiento.json', 'r', encoding='utf-8') as f:
        return json.load(f)

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto_usuario = unidecode(update.message.text.lower())
    palabras = texto_usuario.split()
    
    # Cargamos el "cerebro" del JSON
    datos = cargar_conocimiento()
    respuesta_final = None

    # Buscamos en el JSON si alguna palabra coincide con los tags
    for intencion in datos['intenciones']:
        if any(tag in texto_usuario for tag in intencion['tags']):
            respuesta_final = intencion['respuesta']
            break

    if not respuesta_final:
        respuesta_final = "Aún estoy aprendiendo sobre eso. Intenta preguntarme sobre estrés, exámenes o fatiga."

    await update.message.reply_text(respuesta_final)

# 4. EJECUCIÓN
if __name__ == "__main__":
    # Verificación de seguridad para el Token
    if not TOKEN:
        print("❌ ERROR: No se encontró el TOKEN. Revisa tu archivo .env")
    else:
        # Hilo para Flask
        threading.Thread(target=run_flask, daemon=True).start()
        
        print("Zeenit arrancando en modo Web Service Gratis...")
        
        # Construcción del Bot
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
        app.add_handler(CommandHandler("motivacion", motivacion))
        app.run_polling()