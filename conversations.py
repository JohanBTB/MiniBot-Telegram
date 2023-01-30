from telegram import Update, ParseMode, Poll, InputMediaPhoto, InputMediaVideo, KeyboardButton, ReplyKeyboardMarkup, \
                     InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, \
                    InlineQueryResultGame
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler, ConversationHandler, \
                        CallbackQueryHandler, InlineQueryHandler
import connection
import time
import asyncio
import smtplib
HOME_PATH = r"D:\JOHAN\python\MyBot"

NEW_USER, KC_USER,KC_EMAIL2, KC_EMAIL, NEW_EMAIL, UPDATE_EMAIL, UPDATE_USER = range(7)
CHAT_ID = ""
start_handler =""
# Start
def verifying(update:Update, context:CallbackContext):
    global CHAT_ID
    CHAT_ID = update.message.chat_id
    update.message.reply_text('Ey, hola 🐭.\nEscribe el comando /bienvenid@ para verificar su usuario.')


def start(dispatcher):
    global start_handler
    start_handler = MessageHandler(filters = Filters.text & ~Filters.command,callback= verifying)
    dispatcher.add_handler(start_handler)

def sendMessag():

    pass

# StartConversation   

def welcome_conversation(updater,dispatcher):
    
    # Functions that are USEFUL
    def keep_or_change(column):
        print(f"Iniciando keep_or_chamge de {column}")
        buttons = [[
                InlineKeyboardButton(f'Mantener {column}', callback_data = f'keep_{column}'),
                InlineKeyboardButton(f'Cambiar {column}', callback_data = f'change_{column}')
            ]]
        keyboardMarkup = InlineKeyboardMarkup(buttons)
        mensaje = f"¿Quieres cambiar tu {column} o quieres seguir utilizando {connection.get_user_info(CHAT_ID,column)}?"
        return mensaje, keyboardMarkup
    def end(context):
        context.bot.send_message(chat_id = CHAT_ID, text = 'Eso seria todo amig@.')

    # -------------------------------------------------------------------------------------------        
    # Callback that return a keep_or_change question o asks to the new_user for nickname
    def start_callback(update:Update, context:CallbackContext):
        global start_handler
        updater.dispatcher.remove_handler(start_handler) # Remueve el handler de Bienvenida
        exist, chat = connection.verify_user(CHAT_ID) # Verificando si existe el usuario
        print('iniciando bienvenida')
        if (exist):
            mensaje, keyboardMarkup = keep_or_change('nickname')
        
            update.message.reply_text(mensaje, reply_markup = keyboardMarkup)
            return KC_USER      
        else:
            update.message.reply_text('Aahh, Parece que eres nuevo. Soy un bot de asistencia, mucho gusto en conocerte.\n¿Como es que quisieras que te llame?')
            return NEW_USER
    
    # Callback that asks for nickname of the new_user
    def new_user_callback(update:Update,context:CallbackContext):
        message = update.message
        connection.creating_user(CHAT_ID, f"{message.from_user.first_name} {message.from_user.last_name}", message.text) # Creando nuevo usuario
        update.message.reply_text(f"Hola {update.message.text}, espero estes bien. Me podrias dar tu correo para poderme comunicar contigo mejor")
   
        return NEW_EMAIL

    # Callback that saves the email and put an end to the conversation
    def new_email_callback(update:Update, context:CallbackContext):
        connection.update_info(CHAT_ID, 'email', update.message.text)
        update.message.reply_text("Tu correo ha sido memorizado con mi mente prodigiosa y guardado en mi corazon.")
        return ConversationHandler.END
        
    # Callback that receives an QueryCallback and asks you to change or keep your nickname
    def kc_user_callback(update:Update, context:CallbackContext):
        if(update.callback_query.data == 'change_nickname'):
            context.bot.send_message(chat_id = CHAT_ID, text = '¿Cómo te gustaria que te empecemos a llamar?')
            return UPDATE_USER
        else:
            mensaje, keyboardMarkup = keep_or_change('email')
            context.bot.send_message(chat_id = CHAT_ID, text = mensaje, reply_markup = keyboardMarkup)
            return KC_EMAIL
    
    # Callback that receives an querycallback and asks your email or puts an end to the conversation
    def kc_email_callback(update:Update, context:CallbackContext):
        if(update.callback_query.data == 'change_email'):
            context.bot.send_message(chat_id = CHAT_ID, text = '¿Qué correo piensas usar?')
            return UPDATE_EMAIL
        else:
            end(context)
            return ConversationHandler.END
    
    # Callback that receives an QueryCallback and asks you to change or keep email
    def update_user_callback(update:Update, contet:CallbackContext):
        connection.update_info(CHAT_ID, 'nickname', update.message.text)
        mensaje, keyboardMarkup = keep_or_change('email')
        update.message.reply_text(mensaje, reply_markup = keyboardMarkup)
        return KC_EMAIL2

    # Callback that updates your email and put an end to the conversation    
    def update_email_callback(update:Update,context:CallbackContext):
        connection.update_info(CHAT_ID, 'email', update.message.text)
        update.message.reply_text("Tu correo ha sido memorizado con mi mente prodigiosa y guardado en mi corazon.")
        end(context)
        return ConversationHandler.END

    # Callback that receives an QueryCallback and asks your email or just put an end to the conversation
    def kc_email2_callback(update:Update, context:CallbackContext):
        if(update.callback_query.data == 'change_email'):
            context.bot.send_message(chat_id = CHAT_ID, text = '¿Qué correo deseas usar?')
            return UPDATE_EMAIL
        else:
            end(context)
            return ConversationHandler.END

    # Callback de error
    def error_callback(update: Update, context:CallbackContext):
        time.sleep(2)
        update.message.reply_text("Algo salio mal pipipi\nEscribemelo nuevamente")
        update.message.reply_animation(open(HOME_PATH + r"\recursos\bug_bocchi.gif", "rb"))

    entry_point = {
            CommandHandler(command = ["bienvenido","bienvenida", "bienvenid"], callback = start_callback)
        }
    states = {
            NEW_USER:{
                MessageHandler(filters = Filters.regex("[a-zA-Z]{4,30}"), callback = new_user_callback)
            },
            UPDATE_USER:{
                MessageHandler(filters = Filters.regex("[a-zA-Z]{4,30}"), callback = update_user_callback)
            },
            KC_USER:{
                CallbackQueryHandler(callback = kc_user_callback)
            },
            UPDATE_EMAIL:{
                MessageHandler(filters = Filters.regex("^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,3}$"), callback = update_email_callback)
            },
            NEW_EMAIL:{
                MessageHandler(filters = Filters.regex("^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,3}$"), callback = new_email_callback)
            },
            KC_EMAIL:{
                CallbackQueryHandler(callback = kc_email_callback)
            },
            KC_EMAIL2:{
                CallbackQueryHandler(callback = kc_email2_callback)
            }
        }
    errorUser = {
            MessageHandler(filters = Filters.text, callback = error_callback)
        }
    dispatcher.add_handler(ConversationHandler(entry_points = entry_point, states = states, fallbacks = errorUser))

