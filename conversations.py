from telegram import Update, ParseMode, Poll, InputMediaPhoto, InputMediaVideo, KeyboardButton, ReplyKeyboardMarkup, \
                     InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, \
                    InlineQueryResultGame
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler, ConversationHandler, \
                        CallbackQueryHandler, InlineQueryHandler
USER, EMAIL = range(2)
# StartConversation   

def welcomeConversation(dispatcher):
    def startCallback(update:Update, context:CallbackContext):
        update.message.reply_text('¡Bienvenido! Soy un bot de asistencia, ¿Cómo es que quisieras que te llame?')
        print(update)
        return USER
    
    def userCallback(update: Update, context:CallbackContext):
        update.message.reply_text(f"Hola {update.message.text}, mucho gusto en conocerte. Me podrias dar tu correo para poderme comunicar mejor")
        return EMAIL
    
    def emailCallback(update: Update, context:CallbackContext):
        update.message.reply_text("Tu correo ha sido memorizado con mi mente prodigiosa. Mucha gracias")
        return ConversationHandler.END
    
    def errorCallback(update: Update, context:CallbackContext):
        update.message.reply_text("Algo salio mal pipipi\nEscribemelo nuevamente")

    entry_point = {
            CommandHandler('biendenida', callback = startCallback)
        }

    states = {
            USER:{
                MessageHandler(filters = Filters.regex("[a-zA-Z]{4,30}"), callback = userCallback)
            },
            EMAIL:{
                MessageHandler(filters = Filters.regex("^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,3}$"), callback = emailCallback)
            }
        }

    errorUser = {
            MessageHandler(filters = Filters.text, callback = errorCallback)
        }

    dispatcher.add_handler(ConversationHandler(entry_points = entry_point, states = states, fallbacks = errorUser))

