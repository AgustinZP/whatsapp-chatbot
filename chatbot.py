# -*- coding: utf-8 -*-
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import unicodedata

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Para manejar sesiones en Flask

# Diccionario de estados para cada usuario
user_states = {}

def normalizar_texto(texto):
    texto = texto.lower()
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    return texto.strip()

def es_saludo(mensaje):
    saludos = ["hola", "buenos dias", "buenas tardes", "buenas noches", "hola que tal", "saludos"]
    return any(saludo in mensaje for saludo in saludos)

def preguntar_mas_ayuda():
    return "¿Puedo ayudarte en algo más? (Responde 'sí' para volver al menú principal o 'no' para salir)"

def generar_respuesta(user_id, mensaje):
    resp = MessagingResponse()
    mensaje = normalizar_texto(mensaje)
    respuesta = "❓ No entendí tu mensaje. Escribe 'menu' para volver al inicio."
    
    # Obtener el estado actual del usuario
    estado = user_states.get(user_id, "inicio")
    
    if estado == "ayuda_adicional":
        if mensaje.strip() == "si":
            user_states[user_id] = "inicio"
            return generar_respuesta(user_id, "menu")
        elif mensaje.strip() == "no":
            user_states.pop(user_id, None)
            return str(resp.message("Gracias por comunicarte con nosotros. ¡Que tengas un excelente día! 😊"))
        else:
            return str(resp.message("Por favor, responde con 'sí' para volver al menú principal o 'no' para salir."))

    
    if mensaje in ["menu", "volver", "inicio"] or es_saludo(mensaje):
        user_states[user_id] = "inicio"
        respuesta = ("👋 ¡Hola! Bienvenido al servicio de atención al cliente de Compañía X.\n"
                     "Escribe un número según la opción que necesites:\n"
                     "1️⃣ Información sobre planes y servicios\n"
                     "2️⃣ Soporte técnico\n"
                     "3️⃣ Facturación y pagos\n"
                     "4️⃣ Hablar con un agente\n"
                     "5️⃣ Salir")
        resp.message(respuesta)
        return str(resp)
    
    elif estado == "inicio":
        if mensaje == "1":
            respuesta = ("📶 Nuestros planes incluyen llamadas ilimitadas y datos de alta velocidad.\n"
                         "¿Te gustaría conocer más sobre nuestros planes prepago o pospago? (Responde con 'prepago' o 'pospago')")
            user_states[user_id] = "planes"
        elif mensaje == "2":
            respuesta = ("🔧 Para soporte técnico, dime qué problema estás experimentando:\n"
                         "1️⃣ Problemas con la señal\n"
                         "2️⃣ Configuración del equipo\n"
                         "3️⃣ Otro")
            user_states[user_id] = "soporte"
        elif mensaje == "3":
            respuesta = ("💰 Para facturación y pagos, selecciona una opción:\n"
                         "1️⃣ Consultar saldo y pagos\n"
                         "2️⃣ Reportar un cobro no reconocido\n"
                         "3️⃣ Otro")
            user_states[user_id] = "facturacion"
        elif mensaje == "4":
            respuesta = "📞 Un agente se pondrá en contacto contigo en breve. Por favor, espera unos momentos."
        elif mensaje == "5":
            respuesta = "Gracias por comunicarte con nosotros. ¡Que tengas un excelente día! 😊"
            user_states.pop(user_id, None)
    
    elif estado == "soporte":
        if mensaje == "1":
            respuesta = "📶 ¿Tu señal es débil o no tienes servicio en absoluto? (Responde 'débil' o 'sin servicio')"
            user_states[user_id] = "soporte_senal"
        elif mensaje == "2":
            respuesta = "📱 ¿Necesitas ayuda para configurar tu APN o red móvil? (Responde 'APN' o 'red')"
            user_states[user_id] = "soporte_config"
        elif mensaje == "3":
            respuesta = "😵‍💫 Por favor, describe tu problema y haremos lo posible por ayudarte."
            user_states[user_id] = "soporte_otro"
    
    elif estado == "soporte_senal":
        if mensaje in ["debil", "sin servicio"]:
            respuesta = "🔍 Te recomendamos reiniciar tu dispositivo y verificar tu cobertura en nuestra página. Si el problema persiste, comunícate con soporte técnico."
            respuesta += "\n\n" + preguntar_mas_ayuda()
            user_states[user_id] = "ayuda_adicional"
        else:
            respuesta = "Por favor, indica si el problema es señal 'débil' o 'sin servicio'."
        
    
    elif estado == "soporte_config":
        if mensaje in ["apn", "red"]:
            respuesta = "🛠️ Para configurar tu APN o red móvil, sigue los pasos en nuestra guía en línea o contáctanos para asistencia personalizada."
            respuesta += "\n\n" + preguntar_mas_ayuda()
            user_states[user_id] = "ayuda_adicional"
        else:
            respuesta = "Indica si necesitas ayuda con 'APN' o 'red'."
    
    elif estado == "soporte_otro":
        respuesta = "Gracias por compartir tu problema. Lo revisaremos y te daremos una respuesta pronto."
        respuesta += "\n\n" + preguntar_mas_ayuda()
        user_states[user_id] = "ayuda_adicional"
    
    elif estado == "facturacion":
        if mensaje == "1":
            respuesta = "📊 Puedes consultar tu saldo y pagos en nuestra app o página web."
        elif mensaje == "2":
            respuesta = "💳 Si has identificado un cobro no reconocido, por favor, contáctanos con el detalle del pago."
        elif mensaje == "3":
            respuesta = "Por favor, describe tu problema y haremos lo posible por ayudarte."
            user_states[user_id] = "facturacion_otro"
            
    elif estado =="facturacion_otro":
        respuesta = "Gracias por compartir tu problema. Lo revisaremos y te daremos una respuesta pronto."
        respuesta += "\n\n" + preguntar_mas_ayuda()
        user_states[user_id] = "ayuda_adicional"
    
    resp.message(respuesta)
    return str(resp)

@app.route('/bot', methods=['POST'])
def bot():
    user_id = request.values.get('From', '')
    incoming_msg = request.values.get('Body', '').strip()
    response_text = generar_respuesta(user_id, incoming_msg)
    return response_text

@app.route('/test', methods=['GET'])
def test():
    mensaje = request.args.get('msg', '')
    if not mensaje:
        return "Debes enviar un mensaje con ?msg="
    respuesta = generar_respuesta('test_user', mensaje)
    return f"📩 Mensaje: {mensaje}\n🖋️ Respuesta: {respuesta}"

if __name__ == '__main__':
    app.run(port=5000, debug=True)