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
 STATEMENT_CATEGORY, FIND_SPEC_LATER_CONFIRMATION, USER_DATA_OK, CHOOSING_ABOUT) = map(chr, range(17))

ABOUT_US, PRICING, FEEDBACK, FAQ, PRESS, FEEDBACK_BACK, FEEDBACK_NEXT, ADD_FEEDBACK, ADD_FAQ, ADD_FAQ_MSG, FAQ_BACK, FAQ_NEXT, DELETE, PRESS_BACK, PRESS_NEXT = map(chr, range(17,32))

# Some constant vars for user data
MALE, FEMALE = "Male", "Female"

FAMILY, FRIENDS, LOVE, WORK, STUDY, OTHER_PROBLEM = 'family', 'friends', 'love', 'work', 'study', 'other_problem'

ST_CAT_1, ST_CAT_2, ST_CAT_3, ST_CAT_4, ST_CAT_5, ST_CAT_6, ST_CAT_OTHER = 'st_1','st_2','st_3','st_4','st_5','st_6','st_other'

FEEDBACK_1, FEEDBACK_2, FEEDBACK_3, FEEDBACK_4, FEEDBACK_5 = 1,2,3,4,5

def start(update, context):
    # Get user that sent /start and log his name
    user = update.effective_user.first_name
    logger.info("User %s goes to find_spec section.", user)
    keyboard = [
        [InlineKeyboardButton('Найти специалиста', callback_data=str(FIND_SPEC)),
         InlineKeyboardButton('О сервисе', callback_data=str(ABOUT))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # чтобы не отправлять лишние сообщения
    try:
        if update.message.text == '/start':
            update.effective_chat.send_message(
                text = """Привет!\n\nЭтот бот поможет тебе справиться с депрессией или другими психологическими проблемами, которые тебя беспокоят!\n\nДавай начнем: выбери "Найти специалиста" или узнай о нас больше выбрав "О сервисе", так же ты можешь выбрать быструю помощь и мы найдем тебе ближайшего освободившегося специалиста""",
                reply_markup=reply_markup
            )
    except:
        query = update.callback_query
        bot = context.bot
#         if query.data == START:
        bot.edit_message_text(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            text="""Привет!\n\nЭтот бот поможет тебе справиться с депрессией или другими психологическими проблемами, которые тебя беспокоят!\n\nДавай начнем: выбери "Найти специалиста" или узнай о нас больше выбрав "О сервисе", так же ты можешь выбрать быструю помощь и мы найдем тебе ближайшего освободившегося специалиста""",
            reply_markup=reply_markup
        )

    return START


def stop(update, context):
    """Закончить общение с ботом по команде /stop"""
    update.message.reply_text("""Пока!""")

    return ConversationHandler.END


def find_spec(update, context):
    # Секция "Найти специалиста"
    user = update.effective_user.first_name
    logger.info("User %s goes to find_spec section.", user)
    #Update message and keyboard
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton('Быстрая помощь', callback_data=str(FIND_SPEC_NOW))],
        [InlineKeyboardButton('Подобрать специалиста', callback_data=str(FIND_SPEC_LATER))],
        [InlineKeyboardButton('Список специалистов', callback_data=str(SPEC_LIST))],
        [InlineKeyboardButton('Назад', callback_data=str(START))]
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

    return GET_INFO

def spec_list(update, context):
    pass


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

    # Нужно допилить алгоритм поиска специалиста
    # Job queue будет здесь в самый раз (см ниже)
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
    logger.info("User %s goes to stop_search section.", update.effective_user.first_name)

    context.user_data['msg'] = update.effective_chat.send_message(
        text = "Поиск специалиста отменен."
    )

    context.job_queue.run_once(delete_msg, 5, context=context.user_data)

    find_spec(update, context)

    return FIND_SPEC

def delete_msg(context):
    context.bot.delete_message(
        chat_id=context.job.context['msg']['chat']['id'],
        message_id = context.job.context['msg']['message_id']
        )

def about(update, context):
    r"""О нас"""
    logger.info("User %s goes to  about section.", update.effective_user.first_name)
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton('О сервисе', callback_data=str(ABOUT_US))],
        [InlineKeyboardButton('Стоимость услуг', callback_data=str(PRICING))],
        [InlineKeyboardButton('Отзывы', callback_data=str(FEEDBACK))],
        [InlineKeyboardButton("FAQ", callback_data=str(FAQ))],
        [InlineKeyboardButton("О нас пишут", callback_data=str(PRESS))],
        [InlineKeyboardButton("Назад", callback_data=str(START))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="PsyHelp - это сервис психологической поддержки в формате Telegram-бота.",
        reply_markup=reply_markup
    )

    return ABOUT

def about_us(update, context):
    ### КАК СДЕЛАТЬ АБЗАЦ?
    r"""О сервисе"""
    logger.info("User %s goes to  about_us section.", update.effective_user.first_name)
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton('Круто!', callback_data=str(ABOUT))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="PsyHelp - это сервис психологической поддержки. Мы отбираем лучших психотерапевтов на рынке, чтобы они смогли оказать Вам профессиональную психологическую поддержку. Вы всегда можете выбрать специалиста самостоятельно, или довериться системе подбора, если неуверены в своем выборе.\n\n   Мы считаем, что психотерапия должна быть доступна каждому, в независимости от бюджета и местонахождения клиента. Ключевая особенность нашего сервиса заключается в постоянном доступе специалистов для наших клиентов. Общение с психотерапевтами может проходить в форме чата, голосовых и видео сообщений прямо внутри Telegram бота. Такой подход дает специалистам и клиентам гибкость и удобство в выборе способа терапии.",
        reply_markup=reply_markup
    )

    return ABOUT

def pricing(update, context):
    r"""О ценах"""
    logger.info("User %s goes to  pricing section.", update.effective_user.first_name)
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton('Понятно!', callback_data=str(ABOUT))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="   Мы искренне считаем, что психотерапия должна быть не только качественной, но и доступной каждому. Поэтому каждый новый клиент может оценить качество услуг, воспользовавшись первым бесплатным сеансом у психотерапевта.\n\n   Мы используем две схемы оплаты наших специалистов - фиксированная оплата за сеанс и гибкая оплата за проведенное время общения со специалистом. Вы можете сами опробовать каждый из подходов и остановиться на более удобном. В среднем, стоимость одного сеанса со специалистом средней категории будет стоить 1500 руб. за сеанс (примерно 60 минут). В случае гибкой оплаты Вы платите только за количество минут, проведенных со специалистом. Для специслистов средней категории стоимость составит в среднем 30 руб. за минуту диалога.",
        reply_markup=reply_markup
    )

    return ABOUT

def feedback(update, context):
    r"""Отзывы"""
    logger.info("User %s goes to  feedback section.", update.effective_user.first_name)
    query = update.callback_query
    bot = context.bot
    fb_kb_1 = [
            [InlineKeyboardButton('<', callback_data=str(FEEDBACK_BACK)), InlineKeyboardButton('>', callback_data=str(FEEDBACK_NEXT))],
            [InlineKeyboardButton('Оставить отзыв', callback_data=str(ADD_FEEDBACK))],
            [InlineKeyboardButton('Назад', callback_data=str(ABOUT))]
        ]
    fb_kb_2 = [
            [InlineKeyboardButton('>', callback_data=str(FEEDBACK_NEXT))],
            [InlineKeyboardButton('Оставить отзыв', callback_data=str(ADD_FEEDBACK))],
            [InlineKeyboardButton('Назад', callback_data=str(ABOUT))]
        ]
    if update.callback_query.data == str(FEEDBACK_NEXT):
        context.user_data['feedback_page'] += 1
        keyboard = fb_kb_1
        fb_text = 'page {}'.format(context.user_data['feedback_page'])
    elif update.callback_query.data == str(FEEDBACK_BACK) and context.user_data['feedback_page'] > 2:
        context.user_data['feedback_page'] -= 1
        keyboard = fb_kb_1
        fb_text = 'page {}'.format(context.user_data['feedback_page'])
    else:
        context.user_data['feedback_page'] = 1
        keyboard = fb_kb_2
        fb_text = 'page {}'.format(context.user_data['feedback_page'])
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=fb_text,
        reply_markup=reply_markup
    )

    return FEEDBACK

def add_feedback(update, context):
    r"""Оставить отзыв"""
    logger.info("User %s goes to  add_feedback section.", update.effective_user.first_name)
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton('Отлично!', callback_data=str(FEEDBACK_5))],
        [InlineKeyboardButton('Хорошо', callback_data=str(FEEDBACK_4))],
        [InlineKeyboardButton('Сносно', callback_data=str(FEEDBACK_3))],
        [InlineKeyboardButton('Плохо', callback_data=str(FEEDBACK_2))],
        [InlineKeyboardButton('Ужасно!', callback_data=str(FEEDBACK_1))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Пожалуйста, оцените наш сервис по пятибальной шкале. Далее, вы сможете оставить подробный отзыв.",
        reply_markup=reply_markup
    )
    return ADD_FEEDBACK

def add_feedback_score(update, context):
    r"""Записать отзыв пользователя по 5-бальной шкале"""
    logger.info("User %s goes to  add_feedback_score section.", update.effective_user.first_name)

    context.user_data['feedback_score'] = update.callback_query.data
    query = update.callback_query
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton('Завершить', callback_data=str(ABOUT))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg = bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text="Мы учли Вашу оценку! Будем рады, если оставите более подробный комментарий в сообщении боту.",
        reply_markup=reply_markup
    )
    context.chat_data['msg_id'] = msg.message_id
    return ADD_FEEDBACK

def add_feedback_msg(update, context):
    r"""Записать сообщение-отзыв пользователя"""
    logger.info("User %s goes to  add_feedback_msg section.", update.effective_user.first_name)

    context.user_data['feedback_msg'] = update.message.text
    bot = context.bot
    bot.delete_message(
        chat_id=update._effective_chat.id,
        message_id = context.chat_data['msg_id']
    )
    keyboard = [
        [InlineKeyboardButton('Завершить', callback_data=str(ABOUT))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(
        chat_id=update._effective_chat.id,
        text="Спасибо за подробный отзыв!",
        reply_markup=reply_markup
    )
    return ABOUT

def faq(update, context):
    r"""FAQ"""
    logger.info("User %s goes to  faq section.", update.effective_user.first_name)
    query = update.callback_query
    bot = context.bot
    faq_kb_1 = [
            [InlineKeyboardButton('<', callback_data=str(FAQ_BACK)), InlineKeyboardButton('>', callback_data=str(FAQ_NEXT))],
            [InlineKeyboardButton('Здесь нет ответа на мой вопрос', callback_data=str(ADD_FAQ))],
            [InlineKeyboardButton('Назад', callback_data=str(ABOUT))]
        ]
    faq_kb_2 = [
            [InlineKeyboardButton('>', callback_data=str(FAQ_NEXT))],
            [InlineKeyboardButton('Здесь нет ответа на мой вопрос', callback_data=str(ADD_FAQ))],
            [InlineKeyboardButton('Назад', callback_data=str(ABOUT))]
        ]
    if update.callback_query.data == str(FAQ_NEXT):
        context.user_data['faq_page'] += 1
        keyboard = faq_kb_1
        faq_text = 'faq question {0} - answer {0}'.format(context.user_data['faq_page'])
    elif update.callback_query.data == str(FAQ_BACK) and context.user_data['faq_page'] > 2:
        context.user_data['faq_page'] -= 1
        keyboard = faq_kb_1
        faq_text = 'faq question {0} - answer {0}'.format(context.user_data['faq_page'])
    else:
        context.user_data['faq_page'] = 1
        keyboard = faq_kb_2
        faq_text = 'faq question {0} - answer {0}'.format(context.user_data['faq_page'])
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=faq_text,
        reply_markup=reply_markup
    )
    return FAQ

def add_faq(update, context):
    r"""Записать сообщение-вопрос пользователя"""
    logger.info("User %s goes to  add_faq section.", update.effective_user.first_name)

    query = update.callback_query
    bot = context.bot
    keyboard = [
        [InlineKeyboardButton('Вернуться', callback_data=str(FAQ))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg = bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='Задайте нам вопрос и мы постараемся ответить на него в ближайшее время!',
        reply_markup=reply_markup
    )
    context.chat_data['msg_id'] = msg.message_id

    return ADD_FAQ

def add_faq_msg(update, context):
    r"""Записать сообщение-вопрос пользователя"""
    logger.info("User %s goes to  add_faq_msg section.", update.effective_user.first_name)

    context.user_data['faq_msg'] = update.message.text

    print(context.user_data['faq_msg'])

    query = update.inline_query
    bot = context.bot
    bot.delete_message(
        chat_id=update._effective_chat.id,
        message_id = context.chat_data['msg_id']
    )
    keyboard = [
        [InlineKeyboardButton('Назад', callback_data=str(ABOUT))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(
        chat_id=update._effective_chat.id,
#         message_id=query.message.message_id,
        text='Спасибо за вопрос!',
        reply_markup=reply_markup
    )

    return ABOUT

def press(update, context):
    r"""Пресса о нас"""
    logger.info("User %s goes to  press section.", update.effective_user.first_name)
    query = update.callback_query
    bot = context.bot
    press_kb_1 = [
            [InlineKeyboardButton('<', callback_data=str(PRESS_BACK)), InlineKeyboardButton('>', callback_data=str(PRESS_NEXT))],
            [InlineKeyboardButton('Назад', callback_data=str(ABOUT))]
        ]
    press_kb_2 = [
            [InlineKeyboardButton('>', callback_data=str(PRESS_NEXT))],
            [InlineKeyboardButton('Назад', callback_data=str(ABOUT))]
        ]
    if update.callback_query.data == str(PRESS_NEXT):
        context.user_data['press_page'] += 1
        keyboard = press_kb_1
        press_text = 'press article site {0}'.format(context.user_data['press_page'])
    elif update.callback_query.data == str(PRESS_BACK) and context.user_data['press_page'] > 2:
        context.user_data['press_page'] -= 1
        keyboard = press_kb_1
        press_text = 'press article site {0}'.format(context.user_data['press_page'])
    else:
        context.user_data['press_page'] = 1
        keyboard = press_kb_2
        press_text = 'press article site {0}'.format(context.user_data['press_page'])
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=press_text,
        reply_markup=reply_markup
    )
    return PRESS


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("834607569:AAFOC-hNLiwAKQ_7I7_pOED9DoTgz1g61Q8", use_context=True)

    jq = updater.job_queue

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

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

    feedback_conv = ConversationHandler(
        entry_points=
                    [CallbackQueryHandler(feedback, pattern='^' + str(FEEDBACK) + '$')],
        states=
        {
            FEEDBACK:
                    [
                    CallbackQueryHandler(feedback, pattern='^' + '|'.join([str(FEEDBACK_BACK),str(FEEDBACK_NEXT)]) + '$'),
                    CallbackQueryHandler(add_feedback, pattern='^' + str(ADD_FEEDBACK) + '$')
                    ],
            ADD_FEEDBACK:
                    [
                    MessageHandler(Filters.update.messages, add_feedback_msg),
                    CallbackQueryHandler(add_feedback_score, pattern='^' + '|'.join([str(FEEDBACK_1), str(FEEDBACK_2), str(FEEDBACK_3), str(FEEDBACK_4), str(FEEDBACK_5)]) + '$')
                    ]

        },
        fallbacks=
                    [CommandHandler('start', start),
                    CallbackQueryHandler(about, pattern='^' + str(ABOUT) + '$')
                    ],
        map_to_parent=
        {
            # Return to second level menu
            ABOUT: ABOUT
        }

    )

    faq_conv = ConversationHandler(
        entry_points=
                    [CallbackQueryHandler(faq, pattern='^' + str(FAQ) + '$')],
        states=
        {
            FAQ:
                    [
                    CallbackQueryHandler(faq, pattern='^' + '|'.join([str(FAQ_BACK),str(FAQ_NEXT)]) + '$'),
                    CallbackQueryHandler(add_faq, pattern='^' + str(ADD_FAQ) + '$')
                    ],
            ADD_FAQ:
                    [
                    CallbackQueryHandler(faq, pattern='^' + str(FAQ) + '$'),
                    MessageHandler(Filters.update.messages, add_faq_msg)
                    ]
        },
        fallbacks=
                    [CommandHandler('start', start),
                    CallbackQueryHandler(about, pattern='^' + str(ABOUT) + '$')
                    ],
        map_to_parent=
        {
            # Return to second level menu
            ABOUT: ABOUT
        }

    )

    press_conv = ConversationHandler(
        entry_points=
                    [CallbackQueryHandler(press, pattern='^' + str(PRESS) + '$')],
        states=
        {
            PRESS:
                    [
                    CallbackQueryHandler(press, pattern='^' + '|'.join([str(PRESS_BACK),str(PRESS_NEXT)]) + '$'),
                    ]

        },
        fallbacks=
                    [CommandHandler('start', start),
                    CallbackQueryHandler(about, pattern='^' + str(ABOUT) + '$')
                    ],
        map_to_parent=
        {
            # Return to second level menu
            ABOUT: ABOUT
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
                    CallbackQueryHandler(spec_list, pattern='^' + str(SPEC_LIST) + '$'),
                    CallbackQueryHandler(start, pattern='^' + str(START) + '$')
                    ],

            FIND_SPEC_NOW:
                    [
                    CallbackQueryHandler(stop_search, pattern='^' + str(STOP_SEARCH) + '$')
                    ],

            ABOUT: [
                    CallbackQueryHandler(about_us, pattern='^' + str(ABOUT_US) + '$'),
                    CallbackQueryHandler(pricing, pattern='^' + str(PRICING) + '$'),
                    feedback_conv,
                    faq_conv,
                    press_conv,
                    CallbackQueryHandler(about, pattern='^' + str(ABOUT) + '$'),
                    CallbackQueryHandler(start, pattern='^' + str(START) + '$')
                    ]
        },
        fallbacks=
                    [
                    CommandHandler('start', start),
#                     CallbackQueryHandler(start, pattern='^' + str(START) + '$')
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
