import telnetlib
import openai

HOST = 'localhost'  # Cambia esto por la dirección del servidor MUD
PORT = 1234  # Cambia esto por el puerto del servidor MUD

tn = telnetlib.Telnet(HOST, PORT)

# Lee un fragmento del texto del juego
output = tn.read_until(b'>').decode('utf-8')

# Formatea prompt y consulta a OpenAI
prompt = f"""Estás jugando un MUD. Esta es la descripción actual del entorno:

{output}

¿Qué deberías hacer ahora? Responde solo con el comando que escribirías:"""

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7
)

# Extrae comando sugerido y lo envía
command = response['choices'][0]['message']['content'].strip()
tn.write(command.encode('utf-8') + b'\n')
