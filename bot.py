import telebot
from telebot import types
from telebot.types import ReplyKeyboardRemove

bot = telebot.TeleBot("")#Enter your telegram bot token
admin_id = #Enter your telegram ID

ariza=types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
ariza.add(types.KeyboardButton("Ariza qoldirish📄"))

contact=types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
contact.add(types.KeyboardButton("Raqam qoldirish🔢",request_contact=True),types.KeyboardButton("🔙Orqaga"))

orqaga=types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True)
orqaga.add(types.KeyboardButton("🔙Orqaga"))


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Assalomu Alaykum Botga hush kelibsiz\nAriza qoldirish uchun "Ariza qoldirish📄" tugmasini bosing.',reply_markup=ariza)
    
@bot.message_handler(func=lambda message:True)
def text(message):
    if message.text == "Ariza qoldirish📄":
        bot.send_message(message.chat.id,"Hurmatli arizachi ismingizni kiriting:",reply_markup=orqaga)
        bot.register_next_step_handler(message,get_name)
    else:
        bot.send_message(message.chat.id,"Noto'g'ri buyruq kiritdingiz\nBotda faqat ariza qoldira olasiz!!!",reply_markup=ariza)

def get_name(message):
    if message.text=="🔙Orqaga":
        bot.send_message(message.chat.id,"Asosiy menyudasiz",reply_markup=ariza)
    elif message.text.isalpha():
        name = message.text.capitalize()
        bot.send_message(message.chat.id,f"Hurmatli {name} familiyangizni kiriting.",reply_markup=orqaga)
        bot.register_next_step_handler(message,get_surname,name=name) 
    else:
        bot.send_message(message.chat.id,"Ismingizni faqat harf bilan kiriting.",reply_markup=orqaga)
        bot.register_next_step_handler(message,get_name)

def get_surname(message,name):
    if message.text == "🔙Orqaga":
        bot.send_message(message.chat.id,"Hurmatli arizachi ismingizni kiriting:",reply_markup=orqaga)
        bot.register_next_step_handler(message,get_name)
    elif message.text.isalpha():
        surname = message.text.capitalize()
        bot.send_message(message.chat.id,f"Hurmatli {name} yoshigizni kiriting kiriting.")
        bot.register_next_step_handler(message,get_age,name=name,surname=surname) 
    else:
        bot.send_message(message.chat.id,f"Hurmatli {name} familiyangizni faqat harf bilan kiriting.")
        bot.register_next_step_handler(message,get_surname,name=name)

def get_age(message,name,surname):
    if message.text == "🔙Orqaga":
        bot.send_message(message.chat.id,f"Hurmatli {name} familiyangizni kiriting:",reply_markup=orqaga)
        bot.register_next_step_handler(message,get_surname,name)
    elif message.text.isdigit():
        age = int(message.text)
        bot.send_message(message.chat.id,f"Hurmatli {name} telefon raqamingizni pastdagi tugma orqali yoki yozib qoldiring, +998901234567 formatida",reply_markup=contact)
        bot.register_next_step_handler(message,get_phone,name=name,surname=surname,age=age)
    else:
        bot.send_message(message.chat.id,f"Yoshingizni faqat raqam bilan kiriting.")
        bot.register_next_step_handler(message,get_age,name=name, surname=surname)

def get_phone(message,name,surname,age):
    phone=message.text
    
    if message.text=="🔙Orqaga":
        bot.send_message(message.chat.id,f"Hurmatli {name} yoshigizni kiriting kiriting.",reply_markup=orqaga)
        bot.register_next_step_handler(message,get_age,name=name,surname=surname)
    elif 'contact' in message.content_type:
        phone= message.contact.phone_number
       
        bot.send_message(message.chat.id,"Manzilingizni kiriting.",reply_markup=orqaga)
        bot.register_next_step_handler(message,get_location,name=name,surname=surname,age=age,phone_number=phone)
    elif message.text[1:].isdigit() and len(phone)==13 and phone[:4]=="+998":
        bot.send_message(message.chat.id,"Manzilingizni kiriting.",reply_markup=orqaga)
        bot.register_next_step_handler(message,get_location,name=name,surname=surname,age=age,phone_number=phone)
    else:
        bot.send_message(message.chat.id,"Telefon raqamingizni +998901234567 ko'rinishida kiriting.") 
        bot.register_next_step_handler(message,get_phone,name=name,surname=surname,age=age)

def get_location(message,name,surname,age,phone_number):
    location=message.text
    if message.text=="🔙Orqaga":
        bot.send_message(message.chat.id,f"Hurmatli {name} telefon raqamingizni pastdagi tugma orqali yoki yozib qoldiring, +998901234567 formatida.",reply_markup=contact)
        bot.register_next_step_handler(message,get_phone,name=name,surname=surname,age=age)
    else:
        phone_number=int(phone_number)
        botfunc=bot.send_message(message.chat.id,"Arizangiz qabul qilindi\nAsosiy menyudasiz",reply_markup=ariza)
        bot.send_message(admin_id,f"🆕Yangi arizachi:\nIsmi: {name}\nFamiliyasi: {surname}\nYoshi: {age}\nTelefon raqami: +{str(phone_number)}\nManzili: {location}")
        bot.register_next_step_handler(botfunc,text)


bot.infinity_polling()