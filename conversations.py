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

REPORT_CHOSE, REPORT_DATE, REPORT_DATE2, REPORT_NAME, REPORT_UNIT, REPORT_UNIT2, REPORT_DONE= range(7)
UPDATE_GETTING_PRODUCT, UPDATE_CHOOSE, UPDATE_SELECTION, UNIT_UPDATED, DATE_UPDATED = range(5)
UPDATE_UNIT, NEW_PRODUCT, DATE,KC_DATE, UPDATE_DATE, VERIFY_PRODUCT, UPDATE_CONTINUE= range(7)
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
            mensaje = f"Tal parece que ya existe el producto {product['name']} ¿Quiere actualizarlo o dejarlo asi?"
            buttons = [[
                InlineKeyboardButton(f'Ir a actualizar', callback_data = 1),
                InlineKeyboardButton(f'Dejarlo como está', callback_data = 0)
            ]]
            keyboardMarkup = InlineKeyboardMarkup(buttons)
            update.message.reply_text(mensaje, reply_markup = keyboardMarkup )
            return UPDATE_CONTINUE   
        else:
            update.message.reply_text('Aahh, Parece que es un nuevo producto ¿Cuantas unidades desea colocar?')
            return NEW_PRODUCT
    
    def update_continue_callback(update:Update, context:CallbackContext):
        if(update.callback_query.data == '1'):
            mensaje = f"Vamos a actualizar entonces.\nTal parece que ya existe y tiene {product['unit']} unidad(es), ¿A cuantas unidades quiere cambiarlo?"
            context.bot.send_message(chat_id  = CHAT_ID, text = mensaje)
            return UPDATE_UNIT
        else:
            context.bot.send_message(chat_id  = CHAT_ID, text = "Está bien.")
            end(context)
            return ConversationHandler.END


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
        connection.update_product(CHAT_ID,product)
        update.message.reply_text("Su fecha a sido guardada.")
        end(context)
        return ConversationHandler.END

    # Callback of error
    def error_product_callback(update: Update, context:CallbackContext):
        print("Salio error")
        update.message.reply_text("Todo salio mal.")
        update.message.reply_animation(open(HOME_PATH + r"\recursos\dangan.gif", "rb"))


    update_entry_points = {
        CommandHandler(command = ['guardar','guarda','guardo'], callback = start_product_callback)
    }
    update_states = {
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
        },
        UPDATE_CONTINUE:{
            CallbackQueryHandler(callback =  update_continue_callback)
        }
    }
    update_fallbacks = {
            CommandHandler(command = ['cancelar', 'cancel', 'cancela'], callback = cancel_callback),
            MessageHandler(filters = Filters.text & ~Filters.command, callback = error_product_callback),
    }
    dispatcher.add_handler(ConversationHandler(entry_points = update_entry_points, states = update_states,  fallbacks = update_fallbacks))


    # END PRODUCT SAVE --------------------------------------------------------------------------------------------------------------------

    # START PRODUCT DELETE ----------------------------------------------------------------------------------------------------------------
    
    # Function that returns a message for the end of the conoversation
    def end2(context:CallbackContext):
        context.bot.send_message(chat_id = CHAT_ID, text = 'Hasta la proxima.')
        context.bot.send_animation(chat_id = CHAT_ID, animation = open(HOME_PATH + r"\recursos\hasta_la_proxima.gif", "rb"))

    # Callback that manage the start of the command delete
    def start_delete_product_callback(update:Update, context:CallbackContext):
        global start_handler
        if(start_handler != ''):
            updater.dispatcher.remove_handler(start_handler) 
        update.message.reply_text(f"Hola { connection.get_user_info(CHAT_ID, 'nickname') }, ¿qué es lo que deseas borrar?")
        return GUESSING_PRODUCT

    # Callback that checks if the product exist and how many alike exist
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
            end2(context)
            return ConversationHandler.END

    # Callbacks that checks if the selection is correct
    def yn_delete_product_callback(update:Update, context:CallbackContext):
        if(update.callback_query.data == 'yes'):
            connection.delete_product(CHAT_ID,product[0])
            context.bot.send_message(chat_id = CHAT_ID, text = 'Su producto ha sido eliminado con un 99.9%/ de exito.')
            end2(context)
            return ConversationHandler.END
        else:
            context.bot.send_message(chat_id = CHAT_ID, text = "Entonces el producto que busca ya habrá sido eliminado antes.")
            end2(context)
            return ConversationHandler.END
           
    # Callback that receives the product that deserves a deleting. 0 if none of them deserve that
    def delete_product_callback(update:Update, context:CallbackContext):
        print(update.callback_query.data)
        print(type(update.callback_query.data))
        if(update.callback_query.data == '0'):
            context.bot.send_message(chat_id = CHAT_ID, text = 'Mmm, entonces su producto ya debió haber sido eliminado antes.🙁')
            end2(context)
            return ConversationHandler.END
        else:
            connection.delete_product(CHAT_ID, update.callback_query.data)
            context.bot.send_message(chat_id = CHAT_ID, text = "Su producto ha sido eliminado con un 99.9%/ de exito.")
            end2(context)
            return ConversationHandler.END
    
    # Callback that manage the error fallback
    def error_delete_product_callback(update: Update, context:CallbackContext):
        print("Salio error")
        update.message.reply_text("Todo salio mal.")
        update.message.reply_animation(open(HOME_PATH + r"\recursos\anya.gif", "rb"))

    GUESSING_PRODUCT, YN_DELETE_PRODUCT, DELETE_PRODUCT= range(3)
    delete_entry_points = {
        CommandHandler(command = ['borrar','borra','eliminar','elimino'], callback = start_delete_product_callback)
    }
    delete_states = {
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
    delete_fallbacks = {
            CommandHandler(command = ['cancelar', 'cancel', 'cancela'], callback = cancel_callback),
            MessageHandler(filters = Filters.text & ~Filters.command, callback = error_delete_product_callback),
    }
    dispatcher.add_handler(ConversationHandler(entry_points = delete_entry_points, states = delete_states,  fallbacks = delete_fallbacks))


    # END PRODUCT DELETE--------------------------------------------------------------------------------------------------------------------------
    # START PRODUCT UPDATE -----------------------------------------------------------------------------------------------------------------------

    def start_update_callback(update:Update, context:CallbackContext):
        global start_handler
        if(start_handler != ''):
            updater.dispatcher.remove_handler(start_handler) 
        update.message.reply_text(f"Hola { connection.get_user_info(CHAT_ID, 'nickname') }, ¿que producto quiere actualizar?")
        return UPDATE_GETTING_PRODUCT

    # Callback that check if the product exist and how many alike do
    def update_getting_product_callback(update:Update, context:CallbackContext):
        rows = connection.get_products(CHAT_ID ,update.message.text)
        if len(rows) == 1:
            row = rows[0]
            buttons = [[
                    InlineKeyboardButton(f'Si lo es', callback_data = row[0]),
                    InlineKeyboardButton(f'No, imposible', callback_data = 0)
                ]]
            keyboardMarkup = InlineKeyboardMarkup(buttons)
            
            update.message.reply_text(f"¿Es {row[1]} lo que desea actualizar, verdad?", reply_markup = keyboardMarkup)
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
        else:
            update.message.reply_text("El nombre que me indicas no lo encuentro en mi base de datos. Ya debió haber sido eliminado antes.🙁")
            end2(context)
            return ConversationHandler.END
        return UPDATE_CHOOSE

    # Callback that ask you for which data update
    def update_choose_callback(update:Update, context:CallbackContext):
        if (update.callback_query.data == '0'):
            context.bot.send_message(chat_id = CHAT_ID, text ="Parece que no existe lo que buscas")
            end2(context)
            return ConversationHandler.END
        global product
        product = connection.get_product(CHAT_ID, int(update.callback_query.data))
        buttons = [[
                    InlineKeyboardButton(f"Fecha de Vencimiento\n{product['dued_at']}", callback_data = 'date'),
                    InlineKeyboardButton(f"Unidades\n{product['unit']}", callback_data = 'unit')
                ]]
        keyboardMarkup = InlineKeyboardMarkup(buttons)
        context.bot.send_message(chat_id = CHAT_ID, text = "¿Qué quiere actualizar?", reply_markup = keyboardMarkup)        
        return UPDATE_SELECTION

    # Callback that update the selection
    def update_selection_callback(update:Update, context:CallbackContext):
        # Choose inline buttons date or unit
        if(update.callback_query.data == 'date'):
            context.bot.send_message(chat_id = CHAT_ID, text = "Indique la fecha por la que quiere cambiarla.")
            return DATE_UPDATED
        else:
            context.bot.send_message(chat_id = CHAT_ID, text = "Indique las uniades por las que quiere cambiarla.")
            return UNIT_UPDATED

    # Callback that corraborate the update of the units
    def unit_updated_callback(update:Update, context:CallbackContext):
        global product
        product['unit'] = int(update.message.text)
        print("Esta en update_date")
        connection.update_product(CHAT_ID,product)
        update.message.reply_text("Sus unidades han sido actualizada.")
        end2(context)
        return ConversationHandler.END

    # Callback that corraborate the update of the date
    def date_updated_callback(update:Update, context:CallbackContext):
        print("Esta en update_date")
        global product
        try:
            product['dued_at'] = datetime.datetime.strptime(update.message.text, '%d-%m-%Y').date()
            update.message.reply_text("Su fecha a sido guardada.")
            connection.update_product(CHAT_ID, product)
            end2(context)
            return ConversationHandler.END
        except Exception as e:
            print(e)
            return ConversationHandler.continue_conversation(update, context, error_product_callback)        

    update_entry_points = {
        CommandHandler(command = ['actualizar','actualiza','actualizo'], callback = start_update_callback)
    }
    update_states = {
        UPDATE_GETTING_PRODUCT:{
            MessageHandler(filters = Filters.regex('[a-zA-Z0-9]{2,30}'), callback = update_getting_product_callback)
        },
        UPDATE_CHOOSE:{
           CallbackQueryHandler(callback = update_choose_callback)
        },
        UPDATE_SELECTION:{
            CallbackQueryHandler(callback = update_selection_callback)
        },
        UNIT_UPDATED:{
            MessageHandler(filters = Filters.regex('^[0-9]{1,3}$'), callback = unit_updated_callback)
        },
        DATE_UPDATED:{
            MessageHandler(filters = Filters.regex('^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[012])-(19|20)\d\d$'), callback = date_updated_callback)

        },
    }
    update_fallbacks = {
            CommandHandler(command = ['cancelar', 'cancel', 'cancela'], callback = cancel_callback),
            MessageHandler(filters = Filters.text & ~Filters.command, callback = error_delete_product_callback),
    }
    dispatcher.add_handler(ConversationHandler(entry_points = update_entry_points, states = update_states,  fallbacks = update_fallbacks))

    global rangos
    global full_search
    def end3(context:CallbackContext):
        global rangos
        rangos = []
        context.bot.send_message(chat_id = CHAT_ID, text = 'Hasta la proxima.')
        context.bot.send_animation(chat_id = CHAT_ID, animation = open(HOME_PATH + r"\recursos\hasta_la_proxima.gif", "rb"))

    # Callback that manage the start of the command report
    def start_report_callback(update:Update, context:CallbackContext):
        global rangos
        global full_search
        rangos = []
        full_search = False
        if(start_handler != ''):
            updater.dispatcher.remove_handler(start_handler) 
        mensaje = f"Hola { connection.get_user_info(CHAT_ID, 'nickname') }, ¿Sobre que datos quieres tener el reporte?"
        buttons = [[
                InlineKeyboardButton(f'Fecha', callback_data = 'date')],[
                InlineKeyboardButton(f'Unidades', callback_data = 'unit')],[
                InlineKeyboardButton(f'Nombre', callback_data = 'name')],[
                InlineKeyboardButton(f'Todas', callback_data = 'all')],
            ]
        keyboardMarkup = InlineKeyboardMarkup(buttons)
        update.message.reply_text(mensaje, reply_markup = keyboardMarkup)
        return REPORT_CHOSE
    
    # Cllback that check what was chose
    def report_chose_callback(update: Update, context:CallbackContext):
        global full_search
        data = update.callback_query.data
        if(data == 'date'):
            context.bot.send_message(chat_id = CHAT_ID ,text = "Ingrese el primer rango de la fecha")
            return REPORT_DATE
        elif(data == 'unit'):
            context.bot.send_message(chat_id = CHAT_ID ,text = "Ingrese el primer rango de la cantidad de unidades")
            return REPORT_UNIT
        elif(data == 'name'):
            context.bot.send_message(chat_id = CHAT_ID ,text = "Ingrese el nombre del producto")
            return REPORT_NAME
        else:
            full_search = True
            context.bot.send_message(chat_id = CHAT_ID ,text = "Bueno, comencemos por la fecha.\nIngrese el primer rango de fecha")
            return REPORT_DATE
    # Callback that receives a date and ask you for the second one
    def report_date_callback(update: Update, context:CallbackContext):
        global rangos
        rangos.append(update.message.text)
        update.message.reply_text("Ahora ingrese el segundo rango de fecha")
        return REPORT_DATE2

    # Callback that that asks you for the name or just finish the conversation    
    def report_date2_callback(update: Update, context:CallbackContext):
        global rangos
        rangos.append(update.message.text)
        if full_search:
            update.message.reply_text("Continuemos con el nombre, por favor ingrese el nombre del producto.")
            return REPORT_NAME
        else:
            update.message.reply_text("Aqui esta el reporte generado:")
            end3(context)
            return ConversationHandler.END
    
    def report_name_callback(update: Update, context:CallbackContext):
        global rangos
        rangos.append(update.message.text)
        if full_search:
            update.message.reply_text("Ahora terminemos con las unidades, ingresa el primer rango de la unidades.")
            return REPORT_UNIT
        else:
            update.message.reply_text("Aqui esta el reporte generado:")
            end3(context)
            return ConversationHandler.END
    
    def report_unit_callback(update: Update, context:CallbackContext):
        global rangos
        rangos.append(update.message.text)
        update.message.reply_text("Ingrese el segundo rango de unidades")
        return REPORT_UNIT2
    
    def report_unit2_callback(update: Update, context:CallbackContext):
        global rangos
        update.message.reply_text("Aqui esta el reporte generado")
        end3(context)
        return ConversationHandler.END
    
    report_entry_points = {
        CommandHandler(command = ['reporte','reporta','reportar'], callback = start_report_callback)
    }

    def report_done_callback(update:Update, context:CallbackContext):
        update.message.reply_Text("Aqui esta el reporte")
        end3(context)
        return ConversationHandler.END
        
    report_states = {
        REPORT_CHOSE:{
            CallbackQueryHandler(callback = report_chose_callback)
        },
        REPORT_DATE:{
            MessageHandler(filters = Filters.regex('^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[012])-(19|20)\d\d$'), callback = report_date_callback)
        },
        REPORT_DATE2:{
            MessageHandler(filters = Filters.regex('^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[012])-(19|20)\d\d$'), callback = report_date2_callback)
        },
        REPORT_NAME:{
            MessageHandler(filters = Filters.regex('[a-zA-Z0-9]{2,30}'), callback = report_name_callback)
        },
        REPORT_UNIT:{
            MessageHandler(filters = Filters.regex('^[0-9]{1,3}$'), callback = report_unit_callback)
        },
        REPORT_UNIT2:{
            MessageHandler(filters = Filters.regex('^[0-9]{1,3}$'), callback = report_unit2_callback)
        },
        REPORT_DONE:{
            MessageHandler(filters = Filters.text & ~Filters.command, callback = report_done_callback)
        }
    }
    report_fallbacks = {
            CommandHandler(command = ['cancelar', 'cancel', 'cancela'], callback = cancel_callback),
            MessageHandler(filters = Filters.text & ~Filters.command, callback = error_delete_product_callback),
    }
    dispatcher.add_handler(ConversationHandler(entry_points = report_entry_points, states = report_states,  fallbacks = report_fallbacks))

    
