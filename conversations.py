from telegram import Update, ParseMode, Poll, InputMediaPhoto, InputMediaVideo, KeyboardButton, ReplyKeyboardMarkup, \
                     InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, \
                    InlineQueryResultGame
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler, ConversationHandler, \
                        CallbackQueryHandler, InlineQueryHandler
import connection
HOME_PATH = r"D:\JOHAN\python\MyBot"
NEW_USER, USER, EMAIL, EARLY_END = range(4)
CHAT_ID = ""
start_handler =""
# Start
def verifying(update:Update, context:CallbackContext):
    global CHAT_ID
    CHAT_ID = update.message.chat_id
    update.message.reply_text('Ey, hola 🐭.\nEscribe el comando /bienvenido para verificar su usuario')


def start(dispatcher):
    global start_handler
    start_handler = MessageHandler(filters = Filters.text & ~Filters.command,callback= verifying)
    dispatcher.add_handler(start_handler)

# StartConversation   

def welcome_conversation(updater,dispatcher):
    
    def start_callback(update:Update, context:CallbackContext):
        global start_handler
        updater.dispatcher.remove_handler(start_handler) # Remueve el handler de Bienvenida
        exist, chat = connection.verify_user(CHAT_ID) # Verificando si existe el usuario
        print('iniciando bienvenida')
        if (exist):
            buttons = [[
                InlineKeyboardButton('Cambiar nickname', callback_data = "¿Cómo quiere que lo llame? "),
                InlineKeyboardButton('Seguir utilizando el mismo', callback_data = "Está bien")
            ]]
            keyboardMarkup = ReplyKeyboardMarkup(buttons,  one_time_keyboard = True)

            update.message.reply_text(f"Hola {update.message.text}, ¿quieres cambiar tu nickname o quieres seguir utilizando {connection.get_user_info(CHAT_ID,'nickname')}?", reply_markup = keyboardMarkup)

            if(update.callback_query.data == '¿Cómo quiere que lo llame?'):

                return EMAIL
            else:
                return EMAIL
       
        else:
            update.message.reply_text('Aahh, Parece que eres nuevo. Soy un bot de asistencia, mucho gusto en conocerte.\n¿Como es que quisieras que te llame?')
            return NEW_USER
    
    def user_callback(update: Update, context:CallbackContext):
        buttons = [[
            InlineKeyboardButton('Cambiar correo', callback_data = "Me podría decir su nuevo correo."),
            InlineKeyboardButton('Seguir utilizando la misma', callback_data = "Eso seria todo amig@")
        ]]
        keyboardMarkup = ReplyKeyboardMarkup(buttons,  one_time_keyboard = True)

        update.message.reply_text(f"Hola {update.message.text}, ¿quieres cambiar tu correo o seguir utilizando {connection.get_user_info(CHAT_ID, 'email')}?", reply_markup = keyboardMarkup)

        if(update.callback_query.data == 'No hay problema'):
            return EARLY_END
        else:
            return EMAIL
        
    
    def new_user_callback(update: Update, context:CallbackContext):
        message = update.message
        connection.creating_user(CHAT_ID, f"{message.from_user.first_name} {message.from_user.last_name}", message.text) # Creando nuevo usuario
        update.message.reply_text(f"Hola {update.message.text}, espero estes bien. Me podrias dar tu correo para poderme comunicar contigo mejor")
        return EMAIL

    def email_callback(update: Update, context:CallbackContext):
        connection.update_info(CHAT_ID, 'email',update.message.text)
        update.message.reply_text("Tu correo ha sido memorizado con mi mente prodigiosa y guardado en mi corazon.")
        return ConversationHandler.END
    
    def early_end_callback(update: Update, context:CallbackContext):
        return ConversationHandler.END

    def error_callback(update: Update, context:CallbackContext):
        update.message.reply_text("Algo salio mal pipipi\nEscribemelo nuevamente")
        update.message.reply_animation(open(HOME_PATH + r"\recursos\bug_bocchi.gif", "rb"))

    entry_point = {
            CommandHandler(command = ["bienvenido","bienvenida", "bienvenid"], callback = start_callback)
        }
    states = {
            NEW_USER:{
                MessageHandler(filters = Filters.regex("[a-zA-Z]{4,30}"), callback = new_user_callback)
            },
            USER:{
                MessageHandler(filters = Filters.regex("[a-zA-Z]{4,30}"), callback = user_callback)
            },
            EMAIL:{
                MessageHandler(filters = Filters.regex("^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,3}$"), callback = email_callback)
            },
            EARLY_END:{
                MessageHandler(filters = Filters.text & ~Filters.command, callback = early_end_callback)
            }
        }
    errorUser = {
            MessageHandler(filters = Filters.text, callback = error_callback)
        }
    dispatcher.add_handler(ConversationHandler(entry_points = entry_point, states = states, fallbacks = errorUser))

