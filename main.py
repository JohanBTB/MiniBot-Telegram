
import connection # Conexion a base de datos PostgreSQL
import conversations # Importacion de librerias propias

from telegram.ext import Updater # Importacion del Updater de telegram
TOKEN = "5798240265:AAGdgZ4EwjoDAZL2JmCkreoBgwtIbLhRO-0"
ID_CHAT = '1596810917'


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    updater.bot.send_message(ID_CHAT, 'Bienvenido 🐭.')

    #CONNECTION
    conn = connection.startConnection()
    connection.testConnection(conn)

    #CONVERSATIONS
    conversations.welcomeConversation(dispatcher)

    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()


