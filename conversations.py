from telegram import Update, ParseMode, Poll, InputMediaPhoto, InputMediaVideo, KeyboardButton, ReplyKeyboardMarkup, \
                     InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, \
                    InlineQueryResultGame
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler, ConversationHandler, \
                        CallbackQueryHandler, InlineQueryHandler
from telegram.ext.dispatcher import run_async

import connection
import time, datetime
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

def sendMessage():
    sender_email = connection.get_user_info(CHAT_ID, 'email')
    receiver = "jonny.tu.pai.69@gmail.com"

def cancel_callback(update:Update, context:CallbackContext):
    global start_handler
    mensaje = "Nom puedem serm 😞."
    update.message.reply_text(mensaje)
    return ConversationHandler.END

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
        if (start_handler!=''):
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

    # Callback of error
    def error_callback(update: Update, context:CallbackContext):
        print("Salio error")
        update.message.reply_text("Algo salió mal pipipi\n Eescribemelo nuevamente.")
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
                MessageHandler(filters = Filters.regex("^[a-zA-Z0-9]+[\._]?[ a-zA-Z0-9]+[@]\w+[. ]\w{2,3}$"), callback = update_email_callback)
            },
            NEW_EMAIL:{
                MessageHandler(filters = Filters.regex("^[a-zA-Z0-9]+[\._]?[ a-zA-Z0-9]+[@]\w+[. ]\w{2,3}$"), callback = new_email_callback)
            },
            KC_EMAIL:{
                CallbackQueryHandler(callback = kc_email_callback)
            },
            KC_EMAIL2:{
                CallbackQueryHandler(callback = kc_email2_callback)
            }
        }
    errorUser = {
            CommandHandler(command = ['cancelar', 'cancel', 'cancela'], callback = cancel_callback),
            MessageHandler(filters = Filters.text & ~Filters.command, callback = error_callback),
        }
    dispatcher.add_handler(ConversationHandler(entry_points = entry_point, states = states, fallbacks = errorUser))

# FIN Start Conversation --------------------------------------------------------------------------------------------------------------------------------------

UPDATE_UNIT, NEW_PRODUCT, DATE,KC_DATE, UPDATE_DATE, VERIFY_PRODUCT= range(6)
GUESSING, NO_PRODUCT, NO_PRODUCT2, DELETE_PRODUCT= range(4)
def productos(updater,dispatcher):

    global product
    # USEFUL FUNCTIONS
    def keep_or_change(column):

        print(f"Iniciando keep_or_chamge de {column}")
        buttons = [[
                InlineKeyboardButton(f'Mantener {column}', callback_data = f'keep_{column}'),
                InlineKeyboardButton(f'Cambiar {column}', callback_data = f'change_{column}')
            ]]
        keyboardMarkup = InlineKeyboardMarkup(buttons)
        return keyboardMarkup

    def end(context):
        global product
        product = ""
        context.bot.send_message(chat_id = CHAT_ID, text = 'Eso seria todo amig@.')

    # Callback that starts the conversation of the command "guardar"
    def start_product_callback(update:Update, context:CallbackContext):
        global start_handler
        if(start_handler != ''):
            updater.dispatcher.remove_handler(start_handler) 
        update.message.reply_text(f"Hola { connection.get_user_info(CHAT_ID, 'nickname') }, ¿cómo se va a llamar lo que va a guardar? ")
        return VERIFY_PRODUCT
    
    # Callback that verifies the existance of the product 
    def verify_product_callback(update:Update, context:CallbackContext):
        print("Se esta verificando")
        global product
        product = {}
        exist, product = connection.verify_product(update.message.text)
        if (exist):
            mensaje = f"Tal parece que ya existe y tiene {product['unit']} unidad(es), ¿A cuantas unidades quiere cambiarlo?"
            update.message.reply_text(mensaje)
            return UPDATE_UNIT     
        else:
            update.message.reply_text('Aahh, Parece que es un nuevo producto ¿Cuantas unidades desea colocar?')
            return NEW_PRODUCT
    
    # Callback the receives the units of the product and asks for the due date
    def new_product_callback(update:Update, context:CallbackContext):
        global product
        print("Esta en new_product")
        product['unit'] = int(update.message.text)
        update.message.reply_text('¿Cuál es la fecha de vencimiento?\n Un ejemplo de fecha que debe ingresar es: 12-10-2021')
        return DATE

    # It updates the units and asks if you wanna change the due date
    def update_unit_callback(update:Update, context:CallbackContext):
        global product
        print("Esta en update_unit")
        product['unit'] = int(update.message.text)
        mensaje = f"Las unidades han sido cambiadas.\nLa fecha está en {product['dued_at']} ¿desea cambiarla?" 
        keyboardMarkup = keep_or_change('dued_at')
        update.message.reply_text(mensaje, reply_markup = keyboardMarkup)
        return KC_DATE
    
    # It saves the date and finish the conversation
    def date_callback(update:Update, context:CallbackContext):
        print("Esta en date")
        try:
            product['dued_at'] = datetime.datetime.strptime(update.message.text, '%d-%m-%Y').date()
            update.message.reply_text("Su fecha a sido guardada.")
            connection.creating_product(CHAT_ID, product)
            end(context)
            
            return ConversationHandler.END
        except Exception as e:
            print(e)
            return ConversationHandler.continue_conversation(update, context, error_product_callback)

        
        
    # Callback that could receive a change for the date or just finish the conversation
    def kc_date_callback(update:Update, context:CallbackContext):
        global product
        print("Esta en kc_date")
        if(update.callback_query.data == 'change_dued_at'):
            context.bot.send_message(chat_id = CHAT_ID, text = 'Ingrese la fecha de vencimiento de producto.\nUn ejemplo de fecha que debe ingresar es: 12-10-2021')
            return UPDATE_DATE
        else:
            connection.update_product(CHAT_ID,product)
            end(context)
            return ConversationHandler.END
    
    # Callback that updates the date and ends the conversation
    def update_date_callback(update:Update, context:CallbackContext):
        print("Esta en update_date")
        global product
        keys = list(product.keys())
        connection.update_product(CHAT_ID,product)
        update.message.reply_text("Su fecha a sido guardada.")
        end(context)
        return ConversationHandler.END

    # Callback of error
    def error_product_callback(update: Update, context:CallbackContext):
        print("Salio error")
        update.message.reply_text("Todo salio mal.")
        update.message.reply_animation(open(HOME_PATH + r"\recursos\dangan.gif", "rb"))


    entry_points = {
        CommandHandler(command = ['guardar','guarda','guardo'], callback = start_product_callback)
    }
    states = {
        UPDATE_UNIT:{
            MessageHandler(filters = Filters.regex('^[0-9]{1,3}$'), callback = update_unit_callback)
        },
        NEW_PRODUCT:{
            MessageHandler(filters = Filters.regex('^[0-9]{1,3}$'), callback = new_product_callback)
        },
        DATE:{
            MessageHandler(filters = Filters.regex('^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[012])-(19|20)\d\d$'), callback = date_callback)
        },
        KC_DATE:{
            CallbackQueryHandler(callback = kc_date_callback)
        },
        UPDATE_DATE:{
            MessageHandler(filters = Filters.regex('^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[012])-(19|20)\d\d$'), callback = update_date_callback)
        },
        VERIFY_PRODUCT:{
            MessageHandler(filters = Filters.regex("[a-zA-Z]{4,30}"), callback = verify_product_callback)
        }
    }
    errorUser = {
            CommandHandler(command = ['cancelar', 'cancel', 'cancela'], callback = cancel_callback),
            MessageHandler(filters = Filters.text & ~Filters.command, callback = error_product_callback),
    }
    dispatcher.add_handler(ConversationHandler(entry_points = entry_points, states = states,  fallbacks = errorUser))


    # END PRODUCT SAVE --------------------------------------------------------------------------------------------------------------------

    # START PRODUCT DELETE ----------------------------------------------------------------------------------------------------------------
    
    def end(context:CallbackContext):
        context.bot.send_message(chat_id = CHAT_ID, text = 'Hasta la proxima.')
        context.bot.send_animation(chat_id = CHAT_ID, animation = open(HOME_PATH + r"\recursos\hasta_la_proxima.gif", "rb"))

    def start_delete_product_callback(update:Update, context:CallbackContext):
        global start_handler
        if(start_handler != ''):
            updater.dispatcher.remove_handler(start_handler) 
        update.message.reply_text(f"Hola { connection.get_user_info(CHAT_ID, 'nickname') }, ¿qué es lo que deseas borrar?")
        return GUESSING_PRODUCT

    def guessing_product_callback(update:Update, context:CallbackContext):
        rows = connection.get_products(CHAT_ID ,update.message.text)
        if len(rows) == 1:
            global product
            buttons = [[
                    InlineKeyboardButton(f'Si lo es', callback_data = 'yes'),
                    InlineKeyboardButton(f'No, imposible', callback_data = 'no')
                ]]
            keyboardMarkup = InlineKeyboardMarkup(buttons)
            product = rows[0]
            update.message.reply_text(f"¿Es {product[1]} lo que desea borrar, verdad?", reply_markup = keyboardMarkup)
            return YN_DELETE_PRODUCT
        elif len(rows) > 1:
            buttons = []
            for row in rows:
                button = []
                button.append(InlineKeyboardButton(f'{row[1]}', callback_data = row[0]))
                buttons.append(button)
            button = []
            button.append(InlineKeyboardButton("No es ninguno", callback_data = 0))
            buttons.append(button)
            print(buttons)
            keyboardMarkup = InlineKeyboardMarkup(buttons)
            update.message.reply_text('¿Es alguno de estos?', reply_markup = keyboardMarkup)
            return DELETE_PRODUCT
        else:
            update.message.reply_text("El nombre que me indicas no lo encuentro en mi base de datos. Ya debió haber sido eliminado antes.🙁")
            end(context)
            return ConversationHandler.END

    def yn_delete_product_callback(update:Update, context:CallbackContext):
        if(update.callback_query.data == 'yes'):
            connection.delete_product(CHAT_ID,product[0])
            context.bot.send_message(chat_id = CHAT_ID, text = 'Su producto ha sido eliminado con un 99.9%/ de exito.')
            end(context)
            return ConversationHandler.END
        else:
            context.bot.send_message(chat_id = CHAT_ID, text = "Entonces el producto que busca ya habrá sido eliminado antes.")
            end(context)
            return ConversationHandler.END
           

    def delete_product_callback(update:Update, context:CallbackContext):
        print(update.callback_query.data)
        print(type(update.callback_query.data))
        if(update.callback_query.data == '0'):
            context.bot.send_message(chat_id = CHAT_ID, text = 'Mmm, entonces su producto ya debió haber sido eliminado antes.🙁')
            end(context)
            return ConversationHandler.END
        else:
            connection.delete_product(CHAT_ID, update.callback_query.data)
            context.bot.send_message(chat_id = CHAT_ID, text = "Su producto ha sido eliminado con un 99.9%/ de exito.")
            end(context)
            return ConversationHandler.END

    def error_delete_product_callback(update: Update, context:CallbackContext):
        print("Salio error")
        update.message.reply_text("Todo salio mal.")
        update.message.reply_animation(open(HOME_PATH + r"\recursos\anya.gif", "rb"))

    GUESSING_PRODUCT, YN_DELETE_PRODUCT, DELETE_PRODUCT= range(3)
    entry_points = {
        CommandHandler(command = ['borrar','borra','eliminar','elimino'], callback = start_delete_product_callback)
    }
    states = {
        GUESSING_PRODUCT:{
            MessageHandler(filters = Filters.regex('[a-zA-Z0-9]{2,30}'), callback = guessing_product_callback)
        },
        YN_DELETE_PRODUCT:{
           CallbackQueryHandler(callback = yn_delete_product_callback)
        },
        DELETE_PRODUCT:{
            CallbackQueryHandler(callback = delete_product_callback)
        },
    }
    errorUser = {
            CommandHandler(command = ['cancelar', 'cancel', 'cancela'], callback = cancel_callback),
            MessageHandler(filters = Filters.text & ~Filters.command, callback = error_delete_product_callback),
    }
    dispatcher.add_handler(ConversationHandler(entry_points = entry_points, states = states,  fallbacks = errorUser))
