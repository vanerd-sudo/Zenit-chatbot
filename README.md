# 🧠 ZeenitBot - Tu Compañero de Bienestar Estudiantil

ZeenitBot es un chatbot de Telegram diseñado para acompañar a estudiantes universitarios en la gestión del estrés, la fatiga académica y la organización del tiempo. 

Este proyecto utiliza un **Sistema Experto** basado en reglas para identificar las emociones del usuario y proporcionar consejos prácticos basados en una base de conocimientos estructurada.

## 🚀 Características principales
* **Detección de intenciones:** Identifica palabras clave sobre estrés, cansancio, organización y exámenes.
* **Base de conocimientos desacoplada:** Utiliza un archivo `JSON` para gestionar las respuestas, 
permitiendo actualizaciones rápidas sin tocar el código principal.
* **Procesamiento de texto:** Implementa `unidecode` para entender mensajes sin importar los acentos.
* **Disponibilidad 24/7:** Desplegado en la nube a través de **Render**.

## 🛠️ Tecnologías utilizadas
* **Python 3.x**: Lenguaje principal.
* **python-telegram-bot**: Librería para la integración con la API de Telegram.
* **JSON**: Para el almacenamiento del conocimiento del bot.
* **Flask**: Para el mantenimiento del servidor (Health Checks) en la nube.
* **Git/GitHub**: Control de versiones y despliegue continuo.
* **requests**: Para consumo de la API REST de ZenQuotes.
* **deep-translator**: Para traducción de respuestas de la API en tiempo real.
## 📂 Estructura del Proyecto
* `zeenitbot.py`: El "motor" lógico del bot.
* `conocimiento.json`: La "sabiduría" del bot (tags y respuestas).
* `requirements.txt`: Librerías necesarias para que el bot funcione en cualquier servidor.
* `.gitignore`: Protección de archivos sensibles (como el `.env`).

## ⚙️ Instalación y Uso Local

1. Clona este repositorio.
2. Crea un archivo `.env` con tu `TOKEN` de Telegram.
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt