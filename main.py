
import connection # Conexion a base de datos PostgreSQL
import conversations # Importacion de librerias propias

from telegram.ext import Updater # Importacion del Updater de telegram
TOKEN = "5798240265:AAGdgZ4EwjoDAZL2JmCkreoBgwtIbLhRO-0"
CHAT_ID = ""

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    
    conversations.start(dispatcher)
    #CONNECTION
    # connection.verify_user(CHAT_ID)
    # #CONVERSATIONS
    conversations.welcome_conversation(updater,dispatcher)
    print(CHAT_ID)
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()
    


