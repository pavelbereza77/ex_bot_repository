import random
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN = '7169718142:AAHjbuXoVAJUgv6H1Loh3sw0qW_lh47BrmI'


# Определяем первый вид форматирования
format_1 = '#%(levelname)-8s [%(asctime)s] - %(filename)s:'\
           '%(lineno)d - %(name)s - %(message)s'
# Определяем второй вид форматирования
format_2 = '[{asctime}] #{levelname:8} {filename}:'\
           '{lineno} - {name} - {message}'

logging.basicConfig(level=logging.DEBUG, format=format_1)

# Создаем логгер
logger = logging.getLogger(__name__)


# Инициализируем первый форматтер
# formatter_1 = logging.Formatter(fmt=format_1)
# Инициализируем второй формат/тер
formatter_2 = logging.Formatter(
    fmt=format_2,
    style='{'
)

# Инициализируем хэндлер, который будет перенаправлять логи в stderr
# stderr_handler = logging.StreamHandler()
# Инициализируем хэндлер, который будет перенаправлять логи в stdout
# stdout_handler = logging.StreamHandler(sys.stdout)

# stderr_handler.setFormatter(formatter_2)
# Добавляем хэндлеры логгеру
# logger.addHandler(stdout_handler)
# logger.addHandler(stderr_handler)


# Создаем объекты бота и диспетчера
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# Количество попыток, доступных пользователю в игре
ATTEMPTS = 5

# Словарь, в котором будут храниться данные пользователя
users = {}


# Функция возвращающая случайное целое число от 1 до 100
def get_random_number() -> int:
    num=random.randint(1, 100)
    logger.info('загадано число')
    return num

# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(CommandStart())
async def process_start_command(message: Message):
    logger.info('команда старт')
    await message.answer(
        'Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
        'Чтобы получить правила игры и список доступных ' 
        'команд - отправьте команду /help'
    )
    # Если пользователь только запустил бота и его нет в словаре '
    # 'users - добавляем его в словарь
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'in_game': False,
            'secret_number': None,
            'attempts': None,
            'total_games': 0,
            'wins': 0
        }
        logger.debug(f'Пользователь {message.from_user.id} в словаре для статистики игр')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    logger.warning('хэндлер на команду "/help"')

    await message.answer(
        f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
        f'попыток\n\nДоступные команды:\n/help - правила '
        f'игры и список команд\n/cancel - выйти из игры\n'
        f'/stat - посмотреть статистику\n\nДавай сыграем?'
    )


# Этот хэндлер будет срабатывать на команду "/stat"
@dp.message(Command(commands='stat'))
async def process_stat_command(message: Message):

    if users:
        logger.debug('хэндлер на команду "/stat"', message.from_user.id)
        await message.answer(
            f'Всего игр сыграно: '
            f'{users[message.from_user.id]["total_games"]}\n'
            f'Игр выиграно: {users[message.from_user.id]["wins"]}'
        )
    else:
        logger.debug('хэндлер на команду "/stat" если игр еще не было')

        await  message.answer('Мы с тобой еще не играли!\n Давай попробуем набери /start')


# Этот хэндлер будет срабатывать на команду "/cancel"
@dp.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):

    if users[message.from_user.id]['in_game']:
        logger.debug('хэндлер на команду "/cancel"', message.from_user.id)

        users[message.from_user.id]['in_game'] = False
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть '
            'снова - напишите об этом'
        )
    else:
        logger.debug('хэндлер на команду "/cancel" ', )

        await message.answer(
            'А мы и так с вами не играем. '
            'Может, сыграем разок?'
        )


# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра',
                                'играть', 'хочу играть']))
async def process_positive_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        print(users[message.from_user.id]['secret_number'])
        users[message.from_user.id]['attempts'] = ATTEMPTS
        await message.answer(
            'Ура!\n\nЯ загадал число от 1 до 100, '
            'попробуй угадать!'
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat'
        )


# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, числа от 1 до 100'
        )


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            await message.answer(
                'Ура!!! Вы угадали число!\n\n'
                'Может, сыграем еще?'
            )
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer('Мое число меньше')
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer('Мое число больше')

        if users[message.from_user.id]['attempts'] == 0:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            await message.answer(
                f'К сожалению, у вас больше не осталось '
                f'попыток. Вы проиграли :(\n\nМое число '
                f'было {users[message.from_user.id]["secret_number"]}'
                f'\n\nДавайте сыграем еще?'
            )
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


# Этот хэндлер будет срабатывать на остальные любые сообщения
@dp.message()
async def process_other_answers(message: Message):
    try:
        if users[message.from_user.id]['in_game']:
            await message.answer(
                'Мы же сейчас с вами играем. '
                'Присылайте, пожалуйста, числа от 1 до 100'
            )
        else:
            await message.answer(
                'Я довольно ограниченный бот, давайте '
                'просто сыграем в игру?'
            )
    except KeyError:
        await message.answer(
            'Я довольно ограниченный бот, давайте '
            'просто сыграем в игру?')


if __name__ == '__main__':
    dp.run_polling(bot)
