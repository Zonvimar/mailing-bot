import logging
from asyncio import sleep
from aiogram.utils import executor
from aiogram import Bot, Dispatcher, types
from config import TOKEN, ADMIN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import keyboard as kb
from db import cur
from fsm import Mailing
from db import chats, yea_chats, db_start
from aiogram.dispatcher import FSMContext


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

async def on_startup(_):
    await db_start()

#####

@dp.callback_query_handler(lambda c: c.data == 'btn_act_1')
async def sql_read(callback_query: types.CallbackQuery):
    rows = cur.execute('SELECT * FROM profile').fetchall()
    text = ""
    print(rows)
    lens = len(rows)
    for ret in rows:
        text = text + "" + f"{ret[1]}" ":  " f"{ret[0]} "'\n' "Число участников: " f"{ret[2]}"'\n\n'
    await bot.answer_callback_query(callback_query.id)

    await bot.send_message(callback_query.from_user.id, text)
    await sleep(0.3)
    await bot.send_message(callback_query.from_user.id, text=f'Всего групп: {lens}')


@dp.callback_query_handler(lambda c: c.data == 'btn_act_2')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Выберите как отправить сообщение',
                           reply_markup=kb.list_action_kb2)



@dp.callback_query_handler(lambda c: c.data == 'btn_act_3')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Напишите сообщение, которое хотели бы отправить во все группы,'
                                                        ' в которых есть бот')
    await Mailing.text.set()

@dp.callback_query_handler(lambda c: c.data == 'btn_act_4')
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Напишите сообщение, которое хотели бы отправить в определенную'
                                                        ' группу')
    await Mailing.text2.set()

@dp.callback_query_handler(lambda c: c.data == 'btn_5')
async def process_callback_btn_5(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Напиши номер группы из списка ниже\n(они идут по порядку, начиная'
                                                        ' с 1)')
    rows = cur.execute('SELECT * FROM profile').fetchall()
    text = ""
    i = 0
    for ret in rows:
        text = text + "" + f"{ret[1]}" ":  " f"{ret[0]} "'\n' "Число участников: " f"{ret[2]}"'\n\n'
    await bot.send_message(callback_query.from_user.id, text=text)

    await Mailing.number_gr.set()
###
@dp.message_handler(content_types=['new_chat_members'])
async def send_welcome(message: types.Message):
    chat_id = message.chat.id
    bot_obj = await bot.get_me()
    bot_id = bot_obj.id
    count = await bot.get_chat_members_count(chat_id)
    print(message.chat.type)
    if message.chat.type == 'group' or 'supergroup':
        await chats(chat_id=message.chat.id, title=message.chat.title, count=count)
    for chat_member in message.new_chat_members:
        if chat_member.id == bot_id:
            await message.reply("Привет! Я бот рассылки!")

@dp.message_handler(commands='start')
async def check(message: types.Message):
    await message.reply('Привет! Я бот рассылки!'
                        ' Отправь мне команду'
                        '\n/admin, чтобы создать рассылку по группам')


@dp.message_handler(commands='admin')
async def admin_panel(message: types.message):
    if message.chat.id == ADMIN:
        await message.answer('Админ панель бота', reply_markup=kb.start_menu_kb)
    else:
        await message.answer('Вы не являетесь админом бота')

@dp.message_handler(lambda message: message.text == 'Список групп')
async def list_yea(message: types.Message):
    if message.chat.id == ADMIN:
            list = yea_chats()
            await message.answer(f'Список групп, в которые добавлен бот: \n{list}', reply_markup=kb.ReplyKeyboardRemove())
            await message.answer("Список возможных действий", reply_markup=kb.list_action_kb)

    else:
        await message.answer('Вы не являетесь админом бота')


@dp.message_handler(state=Mailing.text)
async def enter_text(message: types.Message, state: FSMContext):
    if message.chat.id == ADMIN:
        text = message.text
        await state.update_data(text=text)
        cur.execute('SELECT chat_id FROM profile')
        spam_base = cur.fetchall()
        for i in range(len(spam_base)):
            try:
                await bot.send_message(spam_base[i][0], message.text)
            except Exception:
                pass

        await message.answer('Рассылка завершена')
        await state.finish()
    else:
        await message.answer('Вы не являетесь админом бота')


@dp.message_handler(state=Mailing.text2)
async def enter_text(message: types.Message, state: FSMContext):
    if message.chat.id == ADMIN:
        global text
        text = message.text
        await state.update_data(text=text)
        await message.answer('Отлично, теперь выбери группу', reply_markup=kb.take_number_gr)
        await state.finish()
    else:
        await message.answer('Вы не являетесь админом бота')

@dp.message_handler(state=Mailing.number_gr)
async def enter_text(message: types.Message, state: FSMContext):
    if message.chat.id == ADMIN:
        number = message.text
        if int(number) <= len(cur.execute('SELECT * FROM profile').fetchall()):
            await state.update_data(text=number)
            spam_base = cur.execute("SELECT chat_id FROM profile WHERE ROWID == '{key}'".format(key=number)).fetchone()
            await bot.send_message(spam_base[0], text=text)
            await message.answer('Рассылка выполнена')
            await state.finish()
        else:
            await message.answer('Ваше число больше количества групп, в которых есть бот'
                                 '\nПопробуйте еще раз')

    else:
        await message.answer('Вы не являетесь админом бота')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)