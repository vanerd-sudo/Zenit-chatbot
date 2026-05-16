import os
import json
import random
import requests
import threading
from flask import Flask
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
from unidecode import unidecode
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


# Cargamos el Token oculto
load_dotenv()

# SERVIDOR FANTASMA
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "ZeenitBot está vivo y respirando en la nube."

def run_web():
    port = int(os.environ.get("PORT", 5000))
    app_web.run(host="0.0.0.0", port=port)

# Función para cuando le dan a /start
async def iniciar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.message.from_user.first_name
    
    teclado_botones = [
        ["🧘‍♀️ Tengo Estrés", "⏱️ Pomodoro"],
        ["📝 Tips de Exámenes", "💡 Motivación"]
    ]
    menu_interactivo = ReplyKeyboardMarkup(teclado_botones, resize_keyboard=True, one_time_keyboard=False)
    
    await update.message.reply_text(
        f"¡Hola {nombre}! 👋 Soy ZeenitBot, tu asistente de bienestar. Usa los botones de abajo o háblame sobre cómo te sientes hoy.", 
        reply_markup=menu_interactivo
    )

# Función principal que lee y responde
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre_usuario = update.message.from_user.first_name
    texto_usuario = update.message.text.lower()
    texto_usuario = unidecode(texto_usuario) 

    respuesta_final = f"Aún sigo aprendiendo, {nombre_usuario}. 🌱 Prueba usar los botones de abajo o háblame sobre cómo te sientes."

    with open('conocimiento.json', 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)

    for intencion in datos['intenciones']:
        if any(tag in texto_usuario for tag in intencion['tags']):
            respuesta_bruta = intencion['respuesta']
            
            if isinstance(respuesta_bruta, list):
                respuesta_elegida = random.choice(respuesta_bruta)
            else:
                respuesta_elegida = respuesta_bruta
                
            respuesta_final = respuesta_elegida.replace("{nombre}", nombre_usuario)
            
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

    # --- MENÚ INTERACTIVO QUE ACOMPAÑA CADA RESPUESTA ---
    teclado_botones = [
        ["🧘‍♀️ Tengo Estrés", "⏱️ Pomodoro"],
        ["📝 Tips de Exámenes", "💡 Motivación"]
    ]
    menu_interactivo = ReplyKeyboardMarkup(teclado_botones, resize_keyboard=True, one_time_keyboard=False)

    await update.message.reply_text(respuesta_final, reply_markup=menu_interactivo)

# Configuración final para encender el bot
def main():
    TOKEN = os.getenv("TOKEN")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", iniciar))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    # Encendemos el servidor fantasma en segundo plano
    hilo_web = threading.Thread(target=run_web)
    hilo_web.start()

    print("¡ZeenitBot está encendido y listo con servidor web!")
    app.run_polling()

if __name__ == '__main__':
    main()