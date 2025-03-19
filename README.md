# 🤖 WhatsApp Chatbot con Twilio y Flask

## 📌 Descripción

Este es un Chatbot de WhatsApp desarrollado con Flask y Twilio, diseñado para proporcionar asistencia automática a clientes. 
Permite responder preguntas frecuentes y guiar a los usuarios a través de diferentes opciones de servicio al cliente, como soporte técnico, facturación y contacto con un agente.

## 🚀 Tecnologías Utilizadas

Python 3.12.7

Flask (para el servidor web)

Twilio API (para la integración con WhatsApp)

unicodedata (para normalización de texto)

Ngrok para crear un túnel seguro y exponer la aplicación local a internet.

## 📂 Instalación y Configuración

### 1️⃣ Clonar el repositorio

git clone https://github.com/AgustinZP/whatsapp_chatbot.git

cd whatsapp_chatbot

### 2️⃣ Configurar Ngrok

Crea una cuenta en Ngrok.

Luego ejecuta en la consola el comando `ngrok http 5000`

### 3️⃣ Configurar Twilio

Crea una cuenta en Twilio en Twilio Console.

Configura un número de WhatsApp en Twilio Sandbox.

Guarda las credenciales (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) en un archivo .env.

### 4️⃣ Ejecutar la aplicación

python chatbot.py

## 💬 Endpoints

| Método | Ruta  | Descripción |
|--------|------|-------------|
| **POST** | `/bot`  | Recibe mensajes de WhatsApp y responde automáticamente. |
| **GET**  | `/test` | Permite probar respuestas del bot sin WhatsApp. |
