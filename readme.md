# Chatbot que responde preguntas sobre la constitución política de Nicaragua

## Instalación

1. Crear entorno virtual utilizando el siguiente comando: ```python3 -m venv .venv```
2. Activar el entorno virtual utilizando: ```source .venv/bin/activate``` (Linux) o ```bat .venv/bin/activate``` (Windows)   
3. Instalar los paquetes necesarios utilizando el siguiente comando: ```pip3 install -r requirements.txt```
4. Generar un API Key con tu cuenta de OpenAI: https://platform.openai.com/account/api-keys
5. Agregar la API Key generada al código

## Ejecución
- Los archivos para entrenar al bot deben estar en la el directorio /docs. Pueden ser formato PDF, TXT o CSV
- Para iniciar el programa ejecutar el siguiente comando: ```python3 train_chatbot.py```