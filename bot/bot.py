import logging
import pandas as pd
import re
import time

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler, Handler)


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

(START, FIND_SPEC, ABOUT, FIND_SPEC_NOW, STOP_SEARCH, SEARCH_SPEC, FIND_SPEC_LATER, SPEC_LIST, GET_INFO, BACK, GENDER, AGE, PROBLEM_CATEGORY, 
 STATEMENT_CATEGORY, FIND_SPEC_LATER_CONFIRMATION, USER_DATA_OK, CHOOSING_ABOUT) = range(17)

# Some constant vars for user data
MALE, FEMALE = "Male", "Female" 

FAMILY, FRIENDS, LOVE, WORK, STUDY, OTHER_PROBLEM = 'family', 'friends', 'love', 'work', 'study', 'other_problem'

ST_CAT_1, ST_CAT_2, ST_CAT_3, ST_CAT_4, ST_CAT_5, ST_CAT_6, ST_CAT_OTHER = 'st_1','st_2','st_3','st_4','st_5','st_6','st_other'


def start(update, context):
#     reply_keyboard = [['Найти специалиста', 'О сервисе']]

#     markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
#     update.message.reply_text(
#         """Привет! Этот бот поможет тебе справиться с депрессией или другими психологическими проблемами, которые тебя беспокоят! 
#         Давай начнем: выбери "Найти специалиста" или узнай о нас больше выбрав "О сервисе", 
#         так же ты можешь выбрать быструю помощь и мы найдем тебе ближайшего освободившегося специалиста""",
#         reply_markup=markup)
    # Get user that sent /start and log his name
    user = update.effective_user.first_name
    logger.info("User %s goes to find_spec section.", user)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [InlineKeyboardButton('Найти специалиста', callback_data=str(FIND_SPEC)),
         InlineKeyboardButton('О сервисе', callback_data=str(ABOUT))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.effective_chat.send_message(
        text = """Привет!\n\nЭтот бот поможет тебе справиться с депрессией или другими психологическими проблемами, которые тебя беспокоят!\n\nДавай начнем: выбери "Найти специалиста" или узнай о нас больше выбрав "О сервисе", так же ты можешь выбрать быструю помощь и мы найдем тебе ближайшего освободившегося специалиста""",
        reply_markup=reply_markup
    )
    return START


def stop(update, context):
    """Закончить общение с ботом по команде /stop"""
    update.message.reply_text("""Пока!""")
    
    return ConversationHandler.END

def done(update, context):
    update.message.reply_text("""Пока!""")
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    print(user_data)

    user_data.clear()
    return ConversationHandler.END

def find_spec(update, context):
#     r"""найи специалиста выбор из двух альтернатив и переход к след шагу"""
#     reply_keyboard_loc = [['Быстрая помощь','Подобрать', 'Список Специалистов']]

#     markup_loc = ReplyKeyboardMarkup(reply_keyboard_loc, one_time_keyboard=True)
    
#     update.message.reply_text(
#         """Мы можем помочь подобрать Вам специалиста сразу или в зависимости от характера вашей проблемы, 
#         либо вы можете выбрать его самостоятельно из списка специалистов.""",
#         reply_markup=markup_loc)
    user = update.effective_user.first_name
    logger.info("User %s goes to find_spec section.", user)
    #Update message and keyboard
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton('Быстрая помощь', callback_data=str(FIND_SPEC_NOW))],
        [InlineKeyboardButton('Подобрать специалиста', callback_data=str(FIND_SPEC_LATER))],
        [InlineKeyboardButton('Список специалистов', callback_data=str(SPEC_LIST))],
#         [InlineKeyboardButton('Назад', callback_data=str(START))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Мы можем помочь подобрать тебе специалиста сразу или в зависимости от характера твоей проблемы, либо ты можешь выбрать его самостоятельно из списка специалистов.",
        reply_markup=reply_markup
        )
    
    return FIND_SPEC

def find_spec_later(update, context):
    
    #IN PROGRESS
    
    # Section for complex search of specs
    user = update.effective_user.first_name
    logger.info("User %s goes to find_spec_later section.", user) 
    
    query = update.callback_query
    bot = context.bot
    
    keyboard = [
        [InlineKeyboardButton('Хорошо!', callback_data=str(GET_INFO))],
        [InlineKeyboardButton('Назад', callback_data=str(FIND_SPEC))]
#         [InlineKeyboardButton('Назад', callback_data=str(START))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Расскажи о себе, чтобы мы смогли подобрать подходящего специалиста.",
        reply_markup=reply_markup
        )
    if 'user_id' not in context.user_data.keys():
        context.user_data['user_id'] = update.effective_user.id
        
#     if context.user_data['user_id'] == None:
#         context.user_data['user_id'] = update.effective_user.id
#     print(update.message)
#     for data in context.user_data['find_spec_later_data'].columns:
#         if data == 'gender':            
#             print('2')
#             result = gender(update, context)
#             print('3')
#             print(update.callback_query)
#             while update.inline_query == None:
#                 user_data.loc[update.effective_user.id, 'gender'] = update.inline_query.query
#                 print(user_data.loc[update.effective_user.id, 'gender'])
    return GET_INFO

def gender(update, context):
    logger.info("User %s goes to gender section.", update.effective_user.first_name)

    keyboard = [
        [InlineKeyboardButton('Мужской', callback_data = str(MALE)),
         InlineKeyboardButton('Женский', callback_data = str(FEMALE))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.effective_chat.send_message(
        text = "Твой пол?",
        reply_markup=reply_markup
    )
    
#     while (update.callback_query.data != 'Мужской' and update.callback_query.data != 'Женский'):
#         time.sleep(5)
#         print(update.callback_query.data)
#         continue
#     context.user_data['find_spec_later_data'].loc[update.effective_user.id, 'gender'] = update.callback_query.data
#     print(context.user_data['find_spec_later_data'].loc[update.effective_user.id, 'gender'])
    
    return GET_INFO

def spec_list(update, context):
    pass

# def gender(update, context):
#     r"""Пол"""
#     reply_keyboard_loc = [['М', 'Ж']]
#     markup_loc = ReplyKeyboardMarkup(reply_keyboard_loc, one_time_keyboard=True)
    
#     update.message.reply_text("""Выберите ваш пол.""", reply_markup=markup_loc)
#     return CHOOSE_AGE


def age(update, context):
    r"""Возраст"""
    logger.info("User %s goes to age section.", update.effective_user.first_name)
    context.user_data['gender'] = update.callback_query.data
    
    print(context.user_data)
 
    update.effective_chat.send_message(
        text = "Сколько тебе лет?"
    )
    
    return GET_INFO

def city(update, context):
    r"""Город проживания"""
    logger.info("User %s goes to  city section.", update.effective_user.first_name)
    context.user_data['age'] = update.message.text
    
    print(context.user_data)
 
    update.effective_chat.send_message(
        text = "В каком городе ты живешь?"
    )
    
    return GET_INFO

def problem_category(update, context):
    r"""Выбрать проблему из предложенных типов"""
    logger.info("User %s goes to problem_category section.", update.effective_user.first_name)
    
    context.user_data['city'] = update.message.text
    print(context.user_data)
    
    keyboard = [
        [InlineKeyboardButton('Семья', callback_data = str(FAMILY))],
        [InlineKeyboardButton('Друзья', callback_data = str(FRIENDS))],
        [InlineKeyboardButton('Отношения', callback_data = str(LOVE))],
        [InlineKeyboardButton('Работа', callback_data = str(WORK))],
        [InlineKeyboardButton('Учеба', callback_data = str(STUDY))],
        [InlineKeyboardButton('Другое', callback_data = str(OTHER_PROBLEM))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.effective_chat.send_message(
        text = "К какой категории Вы могли бы отнести свою психологическую проблему?",
        reply_markup=reply_markup
    )
    
    return GET_INFO

def statement_category(update, context):
    r"""Выбрать утверждение из предложенных типов"""
    logger.info("User %s goes to statement_category section.", update.effective_user.first_name)
    
    context.user_data['problem_category'] = update.callback_query.data
    keyboard = [
        [InlineKeyboardButton('Я запутался(лась)', callback_data = str(ST_CAT_1))],
        [InlineKeyboardButton('Мне не интересно или скучно', callback_data = str(ST_CAT_2))],
        [InlineKeyboardButton('Я устал(а)', callback_data = str(ST_CAT_3))],
        [InlineKeyboardButton('Меня никто не слушает', callback_data = str(ST_CAT_4))],
        [InlineKeyboardButton('Не знаю что делать дальше', callback_data = str(ST_CAT_5))],
        [InlineKeyboardButton('Не знаю как сделать правильный выбор', callback_data = str(ST_CAT_6))],
        [InlineKeyboardButton('Другое', callback_data = str(ST_CAT_OTHER))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.effective_chat.send_message(
        text = "Какое утверждение лучше всего характеризует твою проблему?",
        reply_markup=reply_markup
    )    
    
    return GET_INFO

def find_spec_later_confirmation(update, context):
    # Подтверждения правильности данных у пользователя
    logger.info("User %s goes to find_spec_later_confirmation section.", update.effective_user.first_name)
    
    context.user_data['statement_category'] = update.callback_query.data
    keyboard = [
        [InlineKeyboardButton('Все верно', callback_data = str(FIND_SPEC_NOW))],
        [InlineKeyboardButton('Нет, я хочу что-то исправить', callback_data = str(FIND_SPEC_LATER))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    update.effective_chat.send_message(
        text = "{0}. Все ли верно?".format(context.user_data), # Необходимо сделать красиво для юзера
        reply_markup=reply_markup
    )    
    
    return FIND_SPEC_LATER_CONFIRMATION
    
def find_spec_now(update, context):
    r"""Подбор специалиста сразу"""
    logger.info("User %s goes to  find_spec_now section.", update.effective_user.first_name)
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton('Отменить поиск', callback_data=str(STOP_SEARCH))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Мы уже ищем специалиста. Ожидайте...",
        reply_markup=reply_markup
    )
    
    ''' Нужно допилить алгоритм поиска специалиста'''
    def spec_search(update, context):
        if context.user_data == {}:
            print('Fast search')
        else:
            print('Regular search, data = {0}'.format(context.user_data))
        pass
    
    spec_search(update, context)
    
    return FIND_SPEC_NOW

def stop_search(update, context):
    # stop search of spec
    logger.info("User %s goes tostop_search section.", update.effective_user.first_name)
 
    update.effective_chat.send_message(
        text = "Поиск специалиста отменен."
    )
    find_spec(update, context)
    
    return FIND_SPEC
    
def about(update, context):
    r"""О нас"""
    reply_keyboard_loc = [['О сервисе', 'Стоимость услуг', 'Отзывы', "О нас пишут", "FAQ" ]]
    markup_loc = ReplyKeyboardMarkup(reply_keyboard_loc, one_time_keyboard=True)
    update.message.reply_text("""PsyHelp - бот психологической поддержки""", reply_markup=markup_loc)
    
    return CHOOSING_ABOUT
    
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("834607569:AAFOC-hNLiwAKQ_7I7_pOED9DoTgz1g61Q8", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
#     conv_handler2 = ConversationHandler(
#         entry_points=[CommandHandler('start', start)],

#         states={
#             CHOOSING: [MessageHandler(Filters.regex('^Найти специалиста$'),
#                                       Find_Spec),
#                        MessageHandler(Filters.regex('^О сервисе$'),
#                                       about),
#                        ],
#             STEP_2_FIND_SPEC: [ MessageHandler(Filters.regex('^Быстрая помощь$'),
#                                       find_spec_now),
#                                MessageHandler(Filters.regex('^Подобрать$'),
#                                       Pol),
#                        MessageHandler(Filters.regex('^Список Специалистов$'),
#                                       Pol)
#             ],

#             CHOOSE_AGE: [MessageHandler(Filters.regex('^.*$'), Age) 
#                             ],
            
#             PROBLEM_CATEGORY: [MessageHandler(Filters.regex('^.*$'), Problem_Category)
#                             ],
            
#             QUESTION_CATEGORY: [MessageHandler(Filters.regex('^.*$'), Question_Category)
#                             ],
#         },

#         fallbacks=[MessageHandler(Filters.regex('^Done$'), done),
#                   CommandHandler('stop', stop)]
#     )
    
    find_spec_later_data = ConversationHandler(
        entry_points=
                    [CallbackQueryHandler(find_spec_later, pattern='^' + str(FIND_SPEC_LATER) + '$')],
        states=
        {
            GET_INFO: 
                    [
                    CallbackQueryHandler(gender, pattern='^' + str(GET_INFO) + '$'),
                    CallbackQueryHandler(age, pattern='^' + str(MALE) + '$|^' + str(FEMALE) + '$'),
                    MessageHandler(Filters.regex(r'\d'), city),
                    MessageHandler(Filters.regex(r'[А-я]|[A-z]'), problem_category),
                    CallbackQueryHandler(statement_category, pattern='^' + '|'.join([FAMILY, FRIENDS, LOVE, WORK, STUDY, OTHER_PROBLEM]) + '$'),
                    CallbackQueryHandler(find_spec_later_confirmation, pattern='^' + '|'.join([ST_CAT_1, ST_CAT_2, ST_CAT_3, ST_CAT_4, ST_CAT_5, ST_CAT_6, ST_CAT_OTHER]) + '$')
                    ],
            FIND_SPEC_LATER_CONFIRMATION:
                    [
                    CallbackQueryHandler(find_spec_later, pattern='^' + str(FIND_SPEC_LATER) + '$')
                    ]
        },
        fallbacks=
                    [CommandHandler('start', start),
                    CallbackQueryHandler(start, pattern='^' + str(START) + '$'),
                    CallbackQueryHandler(find_spec, pattern='^' + str(FIND_SPEC) + '$'),
                    CallbackQueryHandler(find_spec_now, pattern='^' + str(FIND_SPEC_NOW) + '$')
                    ],
        map_to_parent=
        {
            # Return to second level menu
            FIND_SPEC: FIND_SPEC,
            FIND_SPEC_NOW: FIND_SPEC_NOW
        }
    )
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START: 
                    [
                    CallbackQueryHandler(find_spec, pattern='^' + str(FIND_SPEC) + '$'),
                    CallbackQueryHandler(about, pattern='^' + str(ABOUT) + '$')
                    ],
            
            FIND_SPEC: 
                    [
                    find_spec_later_data, 
                    CallbackQueryHandler(find_spec_now, pattern='^' + str(FIND_SPEC_NOW) + '$'),
                    CallbackQueryHandler(spec_list, pattern='^' + str(SPEC_LIST) + '$')
                    ],
            
            FIND_SPEC_NOW:   
                    [
                    CallbackQueryHandler(stop_search, pattern='^' + str(STOP_SEARCH) + '$') 
                    ]
#             FIND_SPEC_NOW: [CallbackQueryHandler(start, pattern='^' + str(START) + '$')],
            
#             ABOUT: [CallbackQueryHandler(start_over, pattern='^' + str(ONE) + '$'),
#                      CallbackQueryHandler(end, pattern='^' + str(TWO) + '$')]
        },
        fallbacks=
                    [
                    CommandHandler('start', start),
                    CallbackQueryHandler(start, pattern='^' + str(START) + '$')
                    ]
    )    

    dp.add_handler(conv_handler)

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