import os
import threading
import json
import random
from turtle import update
from dotenv import load_dotenv
from unidecode import unidecode
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from deep_translator import GoogleTranslator

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
        
       # Extraemos la frase y el autor en inglés
        frase = datos[0]['q']
        autor = datos[0]['a']
        
        # ¡Magia! Traducimos la frase al español
        traductor = GoogleTranslator(source='en', target='es')
        frase_es = traductor.translate(frase)
        
        # Armamos el mensaje final con la frase traducida
        mensaje_final = f"«{frase_es}»\n— {autor}"
        await update.message.reply_text(mensaje_final)
        
    except Exception as e:
        # Si el internet falla o la API se cae, el bot no explota
        await update.message.reply_text("Mi conexión con los filósofos está fallando un poco. ¡Pero recuerda que tú puedes con esto! 💪")

#RESPONDER
def cargar_conocimiento():
    with open('conocimiento.json', 'r', encoding='utf-8') as f:
        return json.load(f)

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 1. ¡Extraemos el nombre del usuario de Telegram!
    nombre_usuario = update.message.from_user.first_name

    # 2. Limpiamos el texto del usuario
    texto_usuario = update.message.text.lower()
    texto_usuario = unidecode(texto_usuario) 

    # Respuesta por defecto (¡ahora con nombre!)
    respuesta_final = f"Aún sigo aprendiendo, {nombre_usuario}. 🌱 Prueba hablándome sobre estrés, organización, exámenes o motivación."

    import json
    with open('conocimiento.json', 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)

    # 3. Buscamos en el JSON
    for intencion in datos['intenciones']:
        if any(tag in texto_usuario for tag in intencion['tags']):
            
            # --- NUEVA LÓGICA DE RESPUESTAS ALEATORIAS ---
            respuesta_bruta = intencion['respuesta']
            
            # Si en tu JSON la respuesta es una lista [...], elige una al azar
            if isinstance(respuesta_bruta, list):
                respuesta_elegida = random.choice(respuesta_bruta)
            else:
                # Si sigue siendo un texto normal, la usa tal cual
                respuesta_elegida = respuesta_bruta
                
            # Inyectamos el nombre del usuario donde hayas puesto "{nombre}"
            respuesta_final = respuesta_elegida.replace("{nombre}", nombre_usuario)
            # ---------------------------------------------
            
            # 4. Lógica de la API para temas emocionales
            tags_emocionales = [
                "estres", "ansied", "agobi", "presion", "panico", "colaps",
                "motivacion", "rendirse", "no puedo", "triste", "desmotivad", "llorar",
                "reprobe", "fracas", "mala calificacion", "reprobado", "falle"
            ]
            
            if any(tag in texto_usuario for tag in tags_emocionales):
                try:
                    api_resp = requests.get('https://zenquotes.io/api/random')
                    datos_api = api_resp.json()
                    frase = datos_api[0]['q']
                    autor = datos_api[0]['a']
                    
                    traductor = GoogleTranslator(source='en', target='es')
                    frase_es = traductor.translate(frase)
                    
                    respuesta_final += f"\n\nAdemás, te comparto esta reflexión:\n«{frase_es}»\n— {autor}"
                except Exception as e:
                    pass 
            
            break 

    # 5. Enviamos el mensaje al usuario
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
        update.message.from_user.first_name