from flask import Flask, render_template, request
import wikipediaapi

app = Flask(__name__)

# Funciones para el chatbot de Wikipedia
palabras_comunes = ["oye", "hablame", "sobre", "los", "las", "el", "la", "que", "sabes", "de", "un", "una", "bien", "mal"]

def normalizar_texto(texto):
    reemplazos = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ü': 'u', 'ñ': 'n'}
    texto = texto.lower()
    for acento, reemplazo in reemplazos.items():
        texto = texto.replace(acento, reemplazo)
    return texto

def extraer_palabras_clave(texto):
    palabras = texto.split()
    palabras_clave = [palabra for palabra in palabras if palabra not in palabras_comunes]
    return " ".join(palabras_clave)

def buscar_en_wikipedia(pregunta):
    wiki_wiki = wikipediaapi.Wikipedia(language='es', user_agent='MyPythonChatbot/1.0 (https://tusitioweb.com)')
    pregunta_limpia = pregunta.strip()
    pagina = wiki_wiki.page(pregunta_limpia)

    if pagina.exists():
        return pagina.summary[:500]  # Devuelve un resumen de 500 caracteres
    else:
        return f"No encontré información sobre '{pregunta_limpia}' en Wikipedia."

@app.route('/')
def index():
    return render_template('index.html')

# Chatbot de Wikipedia
@app.route('/chatbot_wikipedia', methods=['POST'])
def chatbot_wikipedia():
    user_input = request.form['user_input']
    palabras_clave = extraer_palabras_clave(normalizar_texto(user_input))
    if not palabras_clave:
        respuesta = "No encontré términos relevantes para buscar en Wikipedia. ¿Podrías darme más detalles?"
    else:
        respuesta = buscar_en_wikipedia(palabras_clave)
    
    return {'respuesta': respuesta}

# Chatbot de Seguros con menú mostrado desde el principio
@app.route('/chatbot_seguros', methods=['POST'])
def chatbot_seguros():
    user_input = request.form['user_input'].lower()

    # Menú principal siempre visible
    menu = ("Elige una opción:<br>"
        "1. Reportar un siniestro<br>"
        "2. Solicitar una grúa<br>"
        "3. Ver planes de seguros<br>"
        "4. Notificar un problema con la póliza<br>"
        "5. Hablar con un agente")

    # Mostrar el menú desde el principio si es la primera interacción
    if user_input == "" or user_input == "menu":
        return {'respuesta': menu}

    # Opción 1: Reportar siniestro
    if "1" in user_input or "siniestro" in user_input:
        return {'respuesta': f"¿Cuál es la gravedad del siniestro? (1. Leve, 2. Moderado, 3. Grave)\n{menu}"}
    
    elif "leve" in user_input:
        return {'respuesta': f"Has reportado un siniestro leve. Gracias por la información.\n{menu}"}
    
    elif "moderado" in user_input:
        return {'respuesta': f"Has reportado un siniestro moderado. Gracias por la información.\n{menu}"}
    
    elif "grave" in user_input:
        return {'respuesta': f"Has reportado un siniestro grave. ¿Necesitas una ambulancia?\n{menu}"}
    
    elif "ambulancia" in user_input:
        return {'respuesta': f"Ambulancia solicitada. Estamos en camino.\n{menu}"}

    # Opción 2: Solicitar grúa
    elif "2" in user_input or "grúa" in user_input:
        return {'respuesta': f"¿Necesitas asistencia para: 1. Batería agotada, 2. Falta de combustible, 3. Pinchazo?\n{menu}"}
    
    elif "batería" in user_input or "1" in user_input:
        return {'respuesta': f"Grúa solicitada para batería agotada. Llegará en breve.\n{menu}"}
    
    elif "combustible" in user_input or "2" in user_input:
        return {'respuesta': f"Grúa solicitada para falta de combustible. Llegará en breve.\n{menu}"}
    
    elif "pinchazo" in user_input or "3" in user_input:
        return {'respuesta': f"Grúa solicitada para pinchazo. Llegará en breve.\n{menu}"}

    # Opción 3: Ver planes de seguros
    elif "3" in user_input or "planes" in user_input:
        return {'respuesta': (f"Aquí tienes tres opciones de seguro:\n"
                              "1. Seguro básico: Cobertura esencial por 200€/año.\n"
                              "2. Seguro intermedio: Cobertura amplia y asistencia por 350€/año.\n"
                              "3. Seguro completo: Cobertura total, asistencia y sin deducible por 500€/año.\n"
                              f"{menu}")}

    # Opción 4: Notificar un problema con la póliza
    elif "4" in user_input or "póliza" in user_input:
        return {'respuesta': f"¿Cuál es el problema con tu póliza? (Describa brevemente el problema).\n{menu}"}

    # Opción 5: Hablar con un agente
    elif "5" in user_input or "hablar con un agente" in user_input:
        return {'respuesta': f"Un agente te contactará pronto. Gracias por tu paciencia.\n{menu}"}

    # Si el usuario no ingresa una opción válida
    else:
        return {'respuesta': f"Lo siento, no entendí eso. Por favor, elige una opción válida del menú: \n{menu}"}


if __name__ == "__main__":
    app.run(debug=True)
