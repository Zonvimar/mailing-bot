from aiogram.types import ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
###  start_menu
start_menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
btn_list_group = KeyboardButton('Список групп')

start_menu_kb.add(btn_list_group)
###


###
list_action_kb = InlineKeyboardMarkup(row_width=2)
btn_act_1 = InlineKeyboardButton('id групп', callback_data='btn_act_1')
btn_act_2 = InlineKeyboardButton('Отправить сообщение в группу', callback_data='btn_act_2')
list_action_kb.add(btn_act_1)
list_action_kb.add(btn_act_2)

list_action_kb2 = InlineKeyboardMarkup(row_width=2)
btn_act_3 = InlineKeyboardButton('Отправить во все группы', callback_data='btn_act_3')
btn_act_4 = InlineKeyboardButton('Отправить в одну группу', callback_data='btn_act_4')
list_action_kb2.add(btn_act_3)
list_action_kb2.add(btn_act_4)

take_number_gr = InlineKeyboardMarkup(row_width=1)
btn_5 = InlineKeyboardButton('Выбрать группу', callback_data='btn_5')
take_number_gr.add(btn_5)


