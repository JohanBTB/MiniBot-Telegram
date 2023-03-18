from telegram import Update, ParseMode, Poll, InputMediaPhoto, InputMediaVideo, KeyboardButton, ReplyKeyboardMarkup, \
                     InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, \
                    InlineQueryResultGame
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler, ConversationHandler, \
                        CallbackQueryHandler, InlineQueryHandler
import time
import random
import requests
from bs4 import BeautifulSoup
from requests import HTTPError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

TOKEN = "5798240265:AAGdgZ4EwjoDAZL2JmCkreoBgwtIbLhRO-0"
ID_CHAT = '1596810917'
PATH = 'D:\\JOHAN\\recursos\\'
USER, CORREO = range(2)
OPINION, NO = range(2)

#Funcion que replica el texto que envía
def echo(update: Update, context:CallbackContext):
    mensaje = update.message.text
    imagen = "https://laverdadnoticias.com/__export/1666210054760/sites/laverdad/img/2022/10/19/el_anime_bocchi_the_rock_censura_pechos_de_sus_waifus_y_los_fans_se_enojan.jpg_457752357.jpg"
    imagen_path = "D:\\IMGSRAND\\bocchi3.jpg"
    audio = "https://www.elongsound.com/images/mp3/trueno04.mp3"
    thumb_path = "D:\\IMGSRAND\\lol1.jpg"
    video_path = "D:\\JOHAN\\recursos\\videos\\faraon.mp4"
    pdf_path = "D:\\JOHAN\\recursos\\pdf\\pdf1.pdf"
    gif_path = "D:\\JOHAN\\recursos\\gifts\\dangan.gif"
    latitude = "-12.1058974"
    longitude = "-76.9466793"

    inicio = mensaje.split()[0]

    numRandom = random.randint(0,1)
    res = 'Si' if numRandom == 1 else 'No'

    # El reply_to_message_id ayuda a responder a un mensaje determinado
    if inicio.lower()=='hablame':
        # Mandamos texto como respuesta, puede ser HTML
        update.message.reply_text(f"<strike>La respuesta es </strike><b><i>{res}.</i></b>Visitame en <a target='_blank'>www.google.com.pe</a>", parse_mode = ParseMode.HTML ,reply_to_message_id = update.message.message_id)
# Notificaciones
def notificaciones(update: Update, context:CallbackContext):
    if update.message == None:
        update.edited_message.reply_text('Has editado tu mensaje')
    else:
        update.message.reply_text('Recibi un mensaje sin editar', reply_to_message_id = update.message.message_id)

# Printea update
def printUpdate(update, context):
    print(update)

# Mensaje de bienvenida para nuevos usuarios
def AddUsers(update: Update, context:CallbackContext):
    update.message.reply_text(f'Bienvenido al grupo de los {update.message.chat.title}, {update.message.new_chat_members[0].username}')

# Nuevo comando saludar
def saludar(update:Update, context:CallbackContext):
    context.job_queue.run_repeating(tiempoSaludo, int(context.args[0]), context = update.message.chat_id)
    update.message.reply_text(f"Te saludo desde args {context.args}")

def tiempoSaludo(context:CallbackContext):
    context.bot.send_message(chat_id = context.job.context, text="Te saludo desde la funcion tiempoSaludo ")

def PlayMusic(update:Update, context:CallbackContext):
    palabras = update.message.text.split()
    palabras = palabras[1::]
    search = ""
    for palabra in palabras:
        search += palabra + "+"
    link= "https://www.youtube.com/results?search_query=" + search


    try:
        options = Options()
        
        options.add_argument("start_maximized")
        chrome_exe = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        chrome_driver = "C:\\Users\\jonat\\OneDrive\\Escritorio\\Cositas\\progms\\chromedriver.exe"
        options.binary_location = chrome_exe
        driver = webdriver.Chrome(chrome_options = options, executable_path=chrome_driver)


        driver.get(link)
    except Exception as err:
        print(f"Other error occurred: {err}")
    else:
        tags = driver.find_elements(By.ID, "video-title")
        # for tag in tags:
        #     print(tag.get_attribute('href'))
        search = tags[0].get_attribute('href')
        time.sleep(5)
        update.message.reply_text("Aqui te llega el link")
        
        update.message.reply_text(f"<a href='{search}'> Link </a>", parse_mode = ParseMode.HTML)
        driver.close()

# Iniciar conversacion
def startCallback(update: Update, context:CallbackContext):
    update.message.reply_text(f'¡Bienvenido! Soy un bot de asistencia, ¿Cómo es que quisieras que te llame?')
    print(update)
    return USER

def userCallback(update: Update, context: CallbackContext):
    update.message.reply_text(f'Hola, {update.message.text}, ¿cuál es tu correo? Esto me va a servir para poder comunicarme contigo.')
    return CORREO

def correoCallback(update:Update, context: CallbackContext):
    update.message.reply_text('Email recibido de forma exitosa')
    return ConversationHandler.END
            
def errorCallback(update:Update, context:CallbackContext):
    update.message.reply_text('Algo salio maaaaal :,(')


# Permitir que el bot haga admins a otros miembros
def admin(update:Update, context:CallbackContext):
    context.bot.promote_chat_member( update.message.chat.id, update.message.from_user.id, can_change_info=True, can_delete_messages=True, can_invite_users=True, \
                                    can_restrict_members=True, can_pin_messages=True, can_promote_members=True)

# Actualiza el titulo del grupo
def updateGroup(update : Update, context:CallbackContext):
    palabras = update.message.text.split()
    chat_id = update.message.chat.id
    bot = context.bot
    if(palabras[0].lower() == 'title' ): 
        bot.set_chat_title(chat_id, ' '.join(palabras[1::]))
    elif(palabras[0].lower() == 'description'):
        bot.set_chat_description(chat_id, ' '.join(palabras[1::]))
    elif(palabras[0].lower() == 'photo'):
        bot.set_chat_photo(chat_id, open(' '.join(palabras[1::]), 'rb'))

# Fija mensajes
def fijarMensaje(update:Update, context:CallbackContext):
    palabras = update.message.text.split()
    if(palabras[0].lower() == 'fijar'):
        print(f"{update.message.chat.id}  --- {update.message.message_id}")
        context.bot.pin_chat_message(update.message.chat.id, update.message.reply_to_message.message_id)

# pregunta
def pregunta(update:Update, context:CallbackContext):
    buttons = [[
        KeyboardButton('Me gustó mucho'),
        KeyboardButton("No me gustó")
    ],
    [
        
    ]]

    keyboardMarkup = ReplyKeyboardMarkup(buttons, one_time_keyboard = True)

    update.message.reply_text('¿Te gustó nuestro producto?', reply_markup = keyboardMarkup)

def pregunta2(update:Update, context:CallbackContext):
    buttons=[
        [
            InlineKeyboardButton("si",url="https://www.facebook.com"),
            InlineKeyboardButton("no", url = "google.com.pe")
        ],
        [
            InlineKeyboardButton("cancelar", url = "google.com.pe")
        ]
    ]
    keyboardMarkup = InlineKeyboardMarkup(buttons)
    update.message.reply_text("Quieres agregar productos?", reply_markup = keyboardMarkup ) 

def pregunta3(update:Update, context:CallbackContext):
    buttons=[
        [
            InlineKeyboardButton('Si', callback_data = "Excelente")
        ],
        [
            InlineKeyboardButton("No", callback_data = "Para la próxima será")
        ]
        
    ]
    keyboarMarkup = InlineKeyboardMarkup(buttons)
    update.message.reply_text("Le gustó nuestros productos?", reply_markup = keyboarMarkup)

def pregunta4(update: Update, context:CallbackContext):
    buttons=[
        [
            InlineKeyboardButton('Bien', callback_data="si")
        ],
        [
            InlineKeyboardButton('Mal', callback_data ="no")
        ]
    ]

    markupKeyboard = InlineKeyboardMarkup(buttons)
    update.message.reply_text('¿Le gustaron nuestros productos?', reply_markup=markupKeyboard)
    return OPINION

def respuesta(update:Update, context:CallbackContext):
    consulta = update.callback_query
    consulta.answer("Perfecto recibi la orden")
    consulta.edit_message_text(f"Hemos recibido tu respuesta como: {consulta.data}")

def si(update:Update,context:CallbackContext):
    consulta = update.callback_query
    consulta.answer()
    consulta.edit_message_text("Muchas gracias por tu opinion")

    return ConversationHandler.END

def no(update:Update, context:CallbackContext):
    consulta = update.callback_query
    consulta.answer()
    buttons = [
        [
            InlineKeyboardButton("Falta de contenido",callback_data = "mal"),
            InlineKeyboardButton("Muchca falta de respeto",callback_data = "falta de respeto"),
        ],
        [
            InlineKeyboardButton("Otro motivo",callback_data = "otro motivo")
        ]
    ]

    keyboardMarkup = InlineKeyboardMarkup(buttons)
    consulta.edit_message_text('Lo sentimos mucho, cual fue la razon  de tu mala puntuacion?', reply_markup = keyboardMarkup)
    return NO

def motivo(update:Update, context:CallbackContext):
    consulta = update.callback_query
    consulta.answer()

    consulta.edit_message_text('Gracias por colaborar')
    return ConversationHandler.END

def miBotEnLinea(update:Update,context:CallbackContext):
    query = update.inline_query.query
    if query=="":
        query = "Vacio"
    resultados = [
        InlineQueryResultArticle("1", "Mayuscula",InputTextMessageContent(query.upper()), description="Convierto todo " + \
                                "en mayuscula"),
        InlineQueryResultArticle("2", "Minuscula",InputTextMessageContent(query.lower()), description = "Conviernte todo" + \
                                "en minuscula"),
        InlineQueryResultArticle("3", "Cursiva",InputTextMessageContent(f"_{query}_", parse_mode = ParseMode.MARKDOWN_V2 )),
        InlineQueryResultArticle("4", "Negrita",InputTextMessageContent(f"*{query}*", parse_mode = ParseMode.MARKDOWN_V2 )),
        InlineQueryResultArticle("5", "Subrayado",InputTextMessageContent(f"<u>{query}</u>", parse_mode = ParseMode.HTML )),
        
        ]
    update.inline_query.answer(resultados, is_personal = False)

# Para banear pendejos
def baneo(update:Update, context:CallbackContext):
    insultos = ['pendejo','puto']
    message_text = update.message.text
    if (message_text.lower() in insultos):
        if context.chat_data.get(update.message.from_user.id):
            update.message.reply_text("TE AVISE QUE NO DIGAS ESAS PALABRAS")
            try:
                context.bot.ban_chat_member(update.message.chat.id, update.message.from_user.id)
            except:
                update.message.reply_text("Eres el admin jueputa")
        else:
            context.chat_data[update.message.from_user.id] = True
            update.message.reply_text("Se intento", reply_to_message_id = update.message.message_id)
    else:
        update.message.reply_text("No hay nada")

# Minijuego
def iniciar_juego(update: Update, context:CallbackContext):
    update.message.reply_game("Destructor")

def inlineQuery(update:Update,context:CallbackContext):
    results = [
        InlineQueryResultGame(1,'Destructor',)
    ]

    update.inline_query.answer("results")


# WebScrapping
def busquedaDePrecio(update:Update,context:CallbackContext):
    spliteado = update.message.text.split()
    busqueda2 = '%20'.join(spliteado)
    busqueda1 = '-'.join(spliteado)
    # elRequest = requests.get(f'https://nhentai.net/tag/{tipo}/popular-today')
    elRequest = requests.get(f'https://listado.mercadolibre.com.pe/{busqueda1}#D[A:{busqueda2}]')
    soup = BeautifulSoup(elRequest.text, 'html.parser')
    resultado_precio = soup.find('span', {'class':'price-tag-fraction'})
    resultado_link = soup.find('a', {'class': 'ui-search-item__group__element shops__items-group-details ui-search-link'})
    # link = 'nhentai.net' + resultado.text
    precio = resultado_precio.text
    link = resultado_link.get('href')
    update.message.reply_text(f'El precio es {precio}\n - Visitalo aquí: {link}', parse_mode = ParseMode.HTML )

    enviar_text = F"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id?chat_id={ID_CHAT}&parse_mode=Markdown&text={update.message.text}" 
    response = requests.get(enviar_text)
    print(update.message.chat.id)
    
    print(response.json())
    return response.json()

# Bot Srapping


# Inicializar
def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    
    # dispatcher.add_handler(MessageHandler(filters = Filters.text & ~Filters.update.edited_message, callback = notificaciones))
    dispatcher.add_handler(MessageHandler(filters = Filters.status_update.new_chat_members, callback = AddUsers))
    dispatcher.add_handler(CommandHandler('saludo', saludar))
    dispatcher.add_handler(CommandHandler('play',PlayMusic))
    entry_point = {
        CommandHandler('Iniciar', callback = inicioCallback)
    }
    states = {
        USER:{
            MessageHandler(filters = Filters.regex("[a-zA-Z]{4,30}"), callback = userCallback)
        },
        CORREO:{
            MessageHandler(filters = Filters.regex("^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,3}$"), callback = correoCallback)
        }
    }

    errorUsuario = {
        MessageHandler(filters = Filters.text, callback = errorCallback)
    }

    # entry = {
    #     CommandHandler('opinion', pregunta4)
    # }
    # states = {
    #     OPINION:{
    #         CallbackQueryHandler(si, pattern = r"^si$"),
    #         CallbackQueryHandler(no, pattern = r"^no$")
    #     },
    #     NO:{
    #         CallbackQueryHandler(motivo)
    #     }
    # }
    fallback = []
    # dispatcher.add_handler(ConversationHandler(entry,states,fallback))
    # dispatcher.add_handler(ConversationHandler(entry_point, states,errorUsuario))
    dispatcher.add_handler(CommandHandler('admin', admin))
    # dispatcher.add_handler(MessageHandler(filters = Filters.text & ~Filters.command,callback= printUpdate))
    # dispatcher.add_handler(MessageHandler(filters = Filters.text & ~Filters.command, callback=updateGroup))
    # dispatcher.add_handler(MessageHandler(filters = Filters.text & ~Filters.command, callback=fijarMensaje))
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    #texto = 'Bienvenido por primera vez' if ID_CHAT == '' else f"Bienvenido a mi chat: {ID_CHAT}" 
    # dispatcher.add_handler(CommandHandler('pregunta', pregunta4))
    # dispatcher.add_handler(CallbackQueryHandler(respuesta))
    # dispatcher.add_handler(InlineQueryHandler(miBotEnLinea))
    dispatcher.add_handler(MessageHandler(filters = Filters.text & ~ Filters.command, callback = baneo))
    dispatcher.add_handler(CommandHandler('iniciar',iniciar_juego))
    dispatcher.add_handler(CommandHandler('precio', busquedaDePrecio))
    dispatcher.add_handler(InlineQueryHandler(inlineQuery))
    updater.bot.send_message(ID_CHAT, 'Bienvenido chiquitin uwu')
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()