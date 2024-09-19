import re
import wikipediaapi

# Lista de palabras comunes que queremos ignorar en las búsquedas
palabras_comunes = [
    "oye", "hablame", "sobre", "los", "las", "el", "la", "que", "sabes", "de", "un", "una", "bien", "mal"
]

def normalizar_texto(texto):
    reemplazos = {
        'á': 'a',
        'é': 'e',
        'í': 'i',
        'ó': 'o',
        'ú': 'u',
        'ü': 'u',
        'ñ': 'n'
    }
    texto = texto.lower()
    for acento, reemplazo in reemplazos.items():
        texto = texto.replace(acento, reemplazo)
    return texto

def extraer_palabras_clave(texto):
    palabras = texto.split()
    palabras_clave = [palabra for palabra in palabras if palabra not in palabras_comunes]
    return " ".join(palabras_clave)

def buscar_en_wikipedia(pregunta):
    wiki_wiki = wikipediaapi.Wikipedia(
        language='es',
        user_agent='MyPythonChatbot/1.0 (https://tusitioweb.com)'
    )
    
    pregunta_limpia = pregunta.strip()
    pagina = wiki_wiki.page(pregunta_limpia)

    if pagina.exists():
        # Intentar acceder a los miembros de la categoría si existen
        try:
            if len(pagina.categorymembers) > 0:
                return f"La palabra '{pregunta_limpia}' tiene varios significados. ¿Podrías ser más específico?"
        except KeyError:
            pass
        return pagina.summary[:500]  # Devuelve un resumen de 500 caracteres
    else:
        return f"No encontré información sobre '{pregunta_limpia}' en Wikipedia."

def responder(input_usuario):
    respuestas = [
        (r"(hola|buenas|buenos dias|buenas tardes)", "¡Hola! ¿Cómo estás?"),
        (r"(adios|hasta luego|nos vemos)", "Adiós, ¡que tengas un buen día!"),
        (r"(como te llamas|quien eres)", "Soy un chatbot creado en Python."),
        (r"(que puedes hacer|que sabes hacer|que puede hacer)", "Puedo responder preguntas simples y buscar información en Wikipedia."),
        (r"(como estas|como te sientes)", "Estoy bien, gracias por preguntar. ¿Y tú?"),
        (r"(bien y tu|como estas)", "Me alegro de escuchar eso. ¡Estoy aquí para ayudarte!"),
    ]

    input_usuario = normalizar_texto(input_usuario)

    for patron, respuesta in respuestas:
        if re.search(patron, input_usuario):
            return respuesta

    # Extraer palabras clave para la búsqueda en Wikipedia
    palabras_clave = extraer_palabras_clave(input_usuario)
    
    # Si no quedan palabras clave después de filtrarlas, devuelve un mensaje estándar
    if not palabras_clave:
        return "No encontré términos relevantes para buscar en Wikipedia. ¿Podrías darme más detalles?"

    respuesta_wiki = buscar_en_wikipedia(palabras_clave)
    return respuesta_wiki

# Presentación inicial del chatbot
print("Hola, soy el chatbot. Dime una palabra y te daré información sobre ella.")

# Bucle principal del chatbot
while True:
    input_usuario = input("Tú: ")
    if input_usuario.lower() == "salir":
        print("Chatbot: ¡Adiós!")
        break
    respuesta = responder(input_usuario)
    print(f"Chatbot: {respuesta}")
    print("¿Qué más te gustaría saber , dime la palabra y te dare su informacion?")
