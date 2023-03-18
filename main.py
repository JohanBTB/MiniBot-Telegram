
import connection # Conexion a base de datos PostgreSQL
import conversations # Importacion de librerias propias

import warnings
#WARNINGS
warnings.filterwarnings("ignore", category=UserWarning, module="telegram.ext.conversationhandler")
import asyncio
from telegram.ext import Updater # Importacion del Updater de telegram
import tracemalloc


TOKEN = ""
CHAT_ID = ""

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    conversations.start(dispatcher)
    conversations.welcome_conversation(updater,dispatcher)
    conversations.productos(updater,dispatcher)
    print(CHAT_ID)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

    


