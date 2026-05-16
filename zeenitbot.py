import os
import json
import random
import requests
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
from unidecode import unidecode

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Cargamos el Token oculto
load_dotenv()

# Función para cuando le dan a /start
async def iniciar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.message.from_user.first_name
    
    # Menú de botones para el inicio
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

    # Le decimos al bot qué funciones usar
    app.add_handler(CommandHandler("start", iniciar))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    print("¡ZeenitBot está encendido y listo con botones!")
    app.run_polling()

if __name__ == '__main__':
    main()