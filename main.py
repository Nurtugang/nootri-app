import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from utils import calculate_bmr, calculate_calories, calculate_macros

# Состояния для диалога
GENDER, GOAL, AGE, HEIGHT, WEIGHT = range(5)

# Начало диалога и предложение команд с кнопками
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_keyboard = [['/set_data', '/view_data', '/calculate_macros']]
    greeting_message = (
        f'Привет, {update.effective_user.first_name}! Добро пожаловать в нутриционный бот.\n\n'
        'Вы можете ввести или обновить свои данные, используя кнопку "/set_data".\n'
        'Или вы можете посмотреть свои данные, используя кнопку "/view_data".\n'
        'Для получения рекомендации используйте "/calculate_macros".'
    )
    await update.message.reply_text(
        greeting_message,
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    )


# Функция начала ввода данных
async def set_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [['Мужской', 'Женский']]
    await update.message.reply_text(
        'Пожалуйста, выберите ваш пол:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return GENDER

# Функция для обработки пола
async def set_gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['gender'] = update.message.text
    reply_keyboard = [['Сброс', 'Поддержание', 'Набор']]
    await update.message.reply_text(
        'Теперь выберите вашу цель:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return GOAL

# Функция для обработки цели
async def set_goal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['goal'] = update.message.text
    await update.message.reply_text('Теперь укажите ваш возраст.', reply_markup=ReplyKeyboardRemove())
    return AGE

# Функция для обработки возраста
async def set_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['age'] = update.message.text
    await update.message.reply_text('Теперь укажите ваш рост в сантиметрах.')
    return HEIGHT

# Функция для обработки роста
async def set_height(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['height'] = update.message.text
    await update.message.reply_text('Теперь укажите ваш вес в килограммах.')
    return WEIGHT

# Функция для обработки веса и завершения диалога
async def set_weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['weight'] = update.message.text
    await update.message.reply_text(
        'Ваши данные сохранены. Вы можете просмотреть их, используя команду /view_data или обновить, используя команду /set_data.\n'
        'Для получения рекомендуемых данных используйте - "/calculate_macros".',
        reply_markup=ReplyKeyboardMarkup([['/set_data', '/view_data', '/calculate_macros']], resize_keyboard=True, one_time_keyboard=True)
    )
    return ConversationHandler.END

# # Функция для расчета BMR
# async def calculate_bmr_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     try:
#         gender = context.user_data['gender']
#         age = int(context.user_data['age'])
#         height = float(context.user_data['height'])
#         weight = float(context.user_data['weight'])
#         bmr = calculate_bmr(gender, weight, height, age)
#         await update.message.reply_text(f'Ваш BMR (базальный уровень метаболизма): {bmr:.2f} ккал.')
#     except KeyError:
#         await update.message.reply_text('Пожалуйста, сначала введите свои данные с помощью команды /set_data.')

# # Функция для расчета рекомендуемого количества калорий
# async def calculate_calories_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     try:
#         gender = context.user_data['gender']
#         goal = context.user_data['goal']
#         age = int(context.user_data['age'])
#         height = float(context.user_data['height'])
#         weight = float(context.user_data['weight'])
#         bmr = calculate_bmr(gender, weight, height, age)
#         recommended_calories = calculate_calories(goal, bmr)
#         await update.message.reply_text(
#             f'Рекомендуемое потребление калорий для вашей цели "{goal}": {recommended_calories:.2f} ккал.'
#         )
#     except KeyError:
#         await update.message.reply_text('Пожалуйста, сначала введите свои данные с помощью команды /set_data.')

# Функция для отмены диалога
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Ввод данных отменен.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# Функция для просмотра данных пользователя
async def view_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    gender = context.user_data.get('gender', 'не указано')
    goal = context.user_data.get('goal', 'не указано')
    age = context.user_data.get('age', 'не указано')
    height = context.user_data.get('height', 'не указано')
    weight = context.user_data.get('weight', 'не указано')

    summary_message = (
        f'Ваши данные:\n'
        f'Пол: {gender}\n'
        f'Цель: {goal}\n'
        f'Возраст: {age}\n'
        f'Рост: {height} см\n'
        f'Вес: {weight} кг'
    )
    await update.message.reply_text(
        summary_message,
        reply_markup=ReplyKeyboardMarkup([['/set_data', '/view_data', '/calculate_bmr', '/calculate_macros']], resize_keyboard=True, one_time_keyboard=True)
    )

# Функция для расчета макронутриентов
async def calculate_macros_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        # Получение данных пользователя
        gender = context.user_data['gender']
        goal = context.user_data['goal']
        age = int(context.user_data['age'])
        height = float(context.user_data['height'])
        weight = float(context.user_data['weight'])

        # Расчет BMR и калорийности
        bmr = calculate_bmr(gender, weight, height, age)
        calories = calculate_calories(goal, bmr)

        # Расчет макронутриентов
        macros = calculate_macros(calories, goal)
        
        # Формирование сообщения с результатами
        result_message = (
            f"Ваш BMR (базальный уровень метаболизма): {bmr:.2f} ккал\n"
            f"Рекомендуемое потребление калорий для цели '{goal}': {calories:.2f} ккал\n\n"
            "Суточная норма макронутриентов:\n"
            f"Белки: {macros['Белки (г)']} г\n"
            f"Жиры: {macros['Жиры (г)']} г\n"
            f"Углеводы: {macros['Углеводы (г)']} г"
        )
        await update.message.reply_text(result_message)
    except KeyError:
        await update.message.reply_text('Пожалуйста, сначала введите свои данные с помощью команды /set_data.')

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv('TELEGRAM_API_TOKEN')

# Создание приложения
app = ApplicationBuilder().token(TOKEN).build()

# Создание обработчика диалога
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("set_data", set_data)],
    states={
        GENDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_gender)],
        GOAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_goal)],
        AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_age)],
        HEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_height)],
        WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_weight)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

# Добавление обработчиков
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("view_data", view_data))
# app.add_handler(CommandHandler("calculate_bmr", calculate_bmr_command))
# app.add_handler(CommandHandler("calculate_calories", calculate_calories_command))
app.add_handler(CommandHandler("calculate_macros", calculate_macros_command))
app.add_handler(conv_handler)

# Запуск бота
app.run_polling()
