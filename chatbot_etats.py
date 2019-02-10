#!/usr/bin/env python
# -- coding: utf-8 --
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

# on call la librairie sys
import sys, logging, requests



from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
# depuis la lib "telegram.ext" on IMPORT juste les CLASS: "Updater, CommandHandler"
# Updater        = recoit les cmd
# CommandHandler = répond à une commande précise
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

#???
logger = logging.getLogger(__name__)

# Le premier paramètre (0 étant le nom du script)
# 0 = chatboy_etats.py
# 1 = Launch option (en l'occurence notre token)
bot_token = sys.argv[1]

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# ICI ON DECLARE LA LISTE DES ETATS A VENIR
START, SORTIR_CHOIX, RESTAURANTS_CHOIX, RESTAU_RESULTATS, CARTES, RETOUR, TRANSPORT = range(7)


def start(bot, update):
    reply_keyboard = [['RESTAURANTS', 'SORTIES']]

    update.message.reply_text(
        'Hello ! My name is Alka_Bot. \n Je suis la pour vous aiguiller sur les choix que vous pourriez avoir pour ce soir.\n\n'
        'Que voulez vous faire ce soir ?\n'
        'Un restaurant ou une petite sortie ?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return START

def sortir_choix(bot, update):
    reply_keyboard = [['Musées', 'Bars', 'Clubs', 'Restau', 'Retour']]

    user = update.message.from_user
    logger.info("Volontée de %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Je vois. ce soir vous voulez vous faire une petite sortie, '
        'Voici donc les choix que nous vous proposons pour ce soir. ',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return SORTIR_CHOIX

def musees(bot, update):
    reply_keyboard = [['Retour']]

    update.message.reply_text(
        'Oh vous voulez aller au musée ?.\n'
        'Voici le top 3 des musées :\n\nMuseum d\'ethnographie de Genève\nFondation Baur Musée des arts d\'Extrême-Orient\nMuséum d\'histoire naturelle de Genève',
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return RETOUR

def bars(bot, update):
    reply_keyboard = [['Retour']]

    update.message.reply_text(
        'Alors comme ça on veut sortir boire un verre ?.\n\n'
        'Je te conseil ces 3 bars :\n\nBoulevard du vin\n\t\tBoulevard Georges-Favon 3\n\n'
        'PAV Bar\n\t\t1227 Allée H, Route des Jeunes 27\n\n'
        'Meltdown Genève\n\t\tRoute des Acacias',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return RETOUR

def clubs(bot, update):
    reply_keyboard = [['Retour']]

    update.message.reply_text(
        'Je crois connaitres quelques clubs sympas.\n'
        'Voici ceux que je te conseil :\n\n'
        'L\'usine\n'
        'La Gravière\n'
        'L\'audio',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return RETOUR

def restaurant_choix(bot, update):
    reply_keyboard = [['Asiate', 'Kebab', 'Pizza', 'Burger', 'Pates', 'Retour']]

    user = update.message.from_user
    logger.info("%s a choisis %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Vous voulez vous faire une bonne bouffe,\n '
        'Voilà donc les choix que nous vous proposons pour ce soir. ',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return RESTAURANTS_CHOIX

def asiate(bot, update):
    reply_keyboard = [['Resto1','Resto2','Resto3','Resto4','Resto5', 'Retour']]

    update.message.reply_text(
        'Voici les restau dispo.\n\n'
        'Lequel vous interesse ?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return RESTAU_RESULTATS

def restau1(bot, update):
    reply_keyboard = [['RESTAURANTS', 'SORTIES']]
    update.message.reply_location(46.19118164680693,6.1307090520858765)
    update.message.reply_text(
        'C\'est encore moi l\'empereur Alka_bot.\n\n'
        'Tu veux faire quoi ce soir ? \n'
        '\t\t Un restaurant ou une petite sortie ?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return CARTES

def appeler_opendata(path):
    url = "http://transport.opendata.ch/v1/"+path
    print(url)
    reponse = requests.get(url)
    return reponse.json()

def afficher_arrets(update,arrets):
    texte_de_reponse= "Voici les arrets:\n"

    for station in arrets["stations"]:
        if station["id"]is not None:
            texte_de_reponse += "\n Arret: "+station["name"]

    update.message.reply_text(texte_de_reponse)

def bienvenue(bot, update):
    update.message.reply_text("Ou êtes vous ?",
    reply_markup = ReplyKeyboardRemove())
    return TRANSPORT

def lieu_a_chercher(bot, update):
    resultats_opendata = appeler_opendata("locations?query="+update.message.text)
    afficher_arrets(update, resultats_opendata)
    return TRANSPORT

def coordonnees_a_traiter(bot, update):
    location=update.message.location
    resultats_opendata = appeler_opendata("locations?x={}&y={}".format(location.latitude, location.longitude))
    afficher_arrets(update, resultats_opendata)
    return TRANSPORT

def details_arret(bot, update):
    update.message.reply_text("Details d'un arret")
    return TRANSPORT

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(bot_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO

    conv_handler_discussion = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            START:
                [
                    RegexHandler('^(SORTIES)$', sortir_choix),
                    RegexHandler('^(RESTAURANTS)$', restaurant_choix)
                ],

            SORTIR_CHOIX:
                [
                    RegexHandler('^(Musées)$', musees),
                    RegexHandler('^(Bars)$', bars),
                    RegexHandler('^(Clubs)$', clubs),
                    RegexHandler('^(Restau)$', restaurant_choix),
                    RegexHandler('^(Retour)$', start)
                ],
            RETOUR:
                [
                    RegexHandler('^(Retour)$', sortir_choix)
                ],

            RESTAURANTS_CHOIX:
                [
                    RegexHandler('^(Asiate)$', asiate),
                    RegexHandler('^(Kebab)$',  asiate),
                    RegexHandler('^(Pizza)$',  asiate),
                    RegexHandler('^(Burger)$', asiate),
                    RegexHandler('^(Pates)$',  asiate),
                    RegexHandler('^(Retour)$', start)
                ],

            RESTAU_RESULTATS:
                [
                    RegexHandler('^(Resto1)$', restau1),
                    RegexHandler('^(Resto2)$', restau1),
                    RegexHandler('^(Resto3)$', restau1),
                    RegexHandler('^(Resto4)$', restau1),
                    RegexHandler('^(Resto5)$', restau1),
                    RegexHandler('^(Retour)$', restaurant_choix)
                ],

            CARTES:
                [
                    RegexHandler('^(SORTIES)$', sortir_choix),
                    RegexHandler('^(RESTAURANTS)$', restaurant_choix)
                ],


        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    conv_handler_transport = ConversationHandler(
        entry_points=[CommandHandler('transport', bienvenue)],

        states={
            TRANSPORT:
                [
                    (MessageHandler(Filters.text, lieu_a_chercher)),
                    (MessageHandler(Filters.location, coordonnees_a_traiter)),
                    (CommandHandler('detail', details_arret))
                ],

        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler_discussion)
    dp.add_handler(conv_handler_transport)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()