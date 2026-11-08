import telebot

# توكن البوت الخاص بك من BotFather
TOKEN = '8998430604:AAG_ZjLiko94ETL3S2LvtPCc8f1nlVk-ajA'
bot = telebot.TeleBot(TOKEN)

# رقم معرفك الشخصي (Chat ID) لتصلك عليه طلبات العملاء كخدمة عملاء
ADMIN_CHAT_ID = 8287570358

user_data = {}

# 1. بداية المحادثة مع العميل
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "أهلاً بك في متجر بن زهرة البرازيل! ☕\nمن فضلك، أرسل اسمك الثلاثي:")
    user_data[chat_id] = {'step': 'waiting_for_name'}

# 2. جمع البيانات خطوة بخطوة
@bot.message_handler(func=lambda message: message.chat.id in user_data)
def handle_user_steps(message):
    chat_id = message.chat.id
    current_step = user_data[chat_id].get('step')

    if current_step == 'waiting_for_name':
        user_data[chat_id]['name'] = message.text
        user_data[chat_id]['step'] = 'waiting_for_phone'
        bot.send_message(chat_id, f"أهلاً بك يا {message.text}.\nالآن أرسل رقم هاتفك المحمول:")

    elif current_step == 'waiting_for_phone':
        user_data[chat_id]['phone'] = message.text
        user_data[chat_id]['step'] = 'waiting_for_order'
        bot.send_message(chat_id, "ممتاز! ما هو طلبك بالتفصيل؟ (مثال: نصف كيلو بن محوج):")

    elif current_step == 'waiting_for_order':
        user_data[chat_id]['order'] = message.text
        name = user_data[chat_id]['name']
        phone = user_data[chat_id]['phone']
        order = user_data[chat_id]['order']

        # تأكيد الطلب للعميل
        confirmation_text = (
            "✅ تم تسجيل طلبك بنجاح وتحويله إلى خدمة العملاء!\n\n"
            f"👤 الاسم: {name}\n"
            f"📱 الهاتف: {phone}\n"
            f"📦 الطلب: {order}\n\n"
            "سنتواصل معك قريباً لتأكيد الشحن والتوصيل. ☕"
        )
        bot.send_message(chat_id, confirmation_text)

        # إرسال تفاصيل الطلب فوراً إلى حسابك الشخصي (خدمة العملاء) لضمان عدم ضياعه
        admin_message = (
            "🚨 **طلب جديد لمتجر البن!**\n\n"
            f"👤 الاسم: {name}\n"
            f"📱 الهاتف: {phone}\n"
            f"📦 الطلب: {order}\n"
            f"💬 معرف محادثة العميل: `{chat_id}`"
        )
        try:
            bot.send_message(ADMIN_CHAT_ID, admin_message, parse_mode="Markdown")
        except Exception as e:
            print(f"Error sending to admin: {e}")

        # مسح الذاكرة المؤقتة للعميل
        del user_data[chat_id]

# 3. الرد على أي رسالة أخرى
@bot.message_handler(func=lambda message: True)
def reply_anything(message):
    bot.reply_to(message, "أهلاً بك! لطلب البن والتواصل مع خدمة العملاء، يرجى إرسال الأمر:\n/start")

bot.infinity_polling()
import telebot

# توكن البوت الخاص بك من BotFather
TOKEN = '8998430604:AAG_ZjLiko94ETL3S2LvtPCc8f1nlVk-ajA'
bot = telebot.TeleBot(TOKEN)

# رقم معرفك الشخصي (Chat ID) لتصلك عليه طلبات العملاء كخدمة عملاء
ADMIN_CHAT_ID = 8287570358

user_data = {}

# 1. بداية المحادثة مع العميل
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "أهلاً بك في متجر بن زهرة البرازيل! ☕\nمن فضلك، أرسل اسمك الثلاثي:")
    user_data[chat_id] = {'step': 'waiting_for_name'}

# 2. جمع البيانات خطوة بخطوة
@bot.message_handler(func=lambda message: message.chat.id in user_data)
def handle_user_steps(message):
    chat_id = message.chat.id
    current_step = user_data[chat_id].get('step')

    if current_step == 'waiting_for_name':
        user_data[chat_id]['name'] = message.text
        user_data[chat_id]['step'] = 'waiting_for_phone'
        bot.send_message(chat_id, f"أهلاً بك يا {message.text}.\nالآن أرسل رقم هاتفك المحمول:")

    elif current_step == 'waiting_for_phone':
        user_data[chat_id]['phone'] = message.text
        user_data[chat_id]['step'] = 'waiting_for_order'
        bot.send_message(chat_id, "ممتاز! ما هو طلبك بالتفصيل؟ (مثال: نصف كيلو بن محوج):")

    elif current_step == 'waiting_for_order':
        user_data[chat_id]['order'] = message.text
        name = user_data[chat_id]['name']
        phone = user_data[chat_id]['phone']
        order = user_data[chat_id]['order']

        # تأكيد الطلب للعميل
        confirmation_text = (
            "✅ تم تسجيل طلبك بنجاح وتحويله إلى خدمة العملاء!\n\n"
            f"👤 الاسم: {name}\n"
            f"📱 الهاتف: {phone}\n"
            f"📦 الطلب: {order}\n\n"
            "سنتواصل معك قريباً لتأكيد الشحن والتوصيل. ☕"
        )
        bot.send_message(chat_id, confirmation_text)

        # إرسال تفاصيل الطلب فوراً إلى حسابك الشخصي (خدمة العملاء) لضمان عدم ضياعه
        admin_message = (
            "🚨 **طلب جديد لمتجر البن!**\n\n"
            f"👤 الاسم: {name}\n"
            f"📱 الهاتف: {phone}\n"
            f"📦 الطلب: {order}\n"
            f"💬 معرف محادثة العميل: `{chat_id}`"
        )
        try:
            bot.send_message(ADMIN_CHAT_ID, admin_message, parse_mode="Markdown")
        except Exception as e:
            print(f"Error sending to admin: {e}")

        # مسح الذاكرة المؤقتة للعميل
        del user_data[chat_id]

# 3. الرد على أي رسالة أخرى
@bot.message_handler(func=lambda message: True)
def reply_anything(message):
    bot.reply_to(message, "أهلاً بك! لطلب البن والتواصل مع خدمة العملاء، يرجى إرسال الأمر:\n/start")

bot.infinity_polling()
import telebot

# توكن البوت الخاص بك من BotFather
TOKEN = '8998430604:AAG_ZjLiko94ETL3S2LvtPCc8f1nlVk-ajA'
bot = telebot.TeleBot(TOKEN)

# رقم معرفك الشخصي (Chat ID) لتصلك عليه طلبات العملاء كخدمة عملاء
ADMIN_CHAT_ID = 8287570358

user_data = {}

# 1. بداية المحادثة مع العميل
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "أهلاً بك في متجر بن زهرة البرازيل! ☕\nمن فضلك، أرسل اسمك الثلاثي:")
    user_data[chat_id] = {'step': 'waiting_for_name'}

# 2. جمع البيانات خطوة بخطوة
@bot.message_handler(func=lambda message: message.chat.id in user_data)
def handle_user_steps(message):
    chat_id = message.chat.id
    current_step = user_data[chat_id].get('step')

    if current_step == 'waiting_for_name':
        user_data[chat_id]['name'] = message.text
        user_data[chat_id]['step'] = 'waiting_for_phone'
        bot.send_message(chat_id, f"أهلاً بك يا {message.text}.\nالآن أرسل رقم هاتفك المحمول:")

    elif current_step == 'waiting_for_phone':
        user_data[chat_id]['phone'] = message.text
        user_data[chat_id]['step'] = 'waiting_for_order'
        bot.send_message(chat_id, "ممتاز! ما هو طلبك بالتفصيل؟ (مثال: نصف كيلو بن محوج):")

    elif current_step == 'waiting_for_order':
        user_data[chat_id]['order'] = message.text
        name = user_data[chat_id]['name']
        phone = user_data[chat_id]['phone']
        order = user_data[chat_id]['order']

        # تأكيد الطلب للعميل
        confirmation_text = (
            "✅ تم تسجيل طلبك بنجاح وتحويله إلى خدمة العملاء!\n\n"
            f"👤 الاسم: {name}\n"
            f"📱 الهاتف: {phone}\n"
            f"📦 الطلب: {order}\n\n"
            "سنتواصل معك قريباً لتأكيد الشحن والتوصيل. ☕"
        )
        bot.send_message(chat_id, confirmation_text)

        # إرسال تفاصيل الطلب فوراً إلى حسابك الشخصي (خدمة العملاء) لضمان عدم ضياعه
        admin_message = (
            "🚨 **طلب جديد لمتجر البن!**\n\n"
            f"👤 الاسم: {name}\n"
            f"📱 الهاتف: {phone}\n"
            f"📦 الطلب: {order}\n"
            f"💬 معرف محادثة العميل: `{chat_id}`"
        )
        try:
            bot.send_message(ADMIN_CHAT_ID, admin_message, parse_mode="Markdown")
        except Exception as e:
            print(f"Error sending to admin: {e}")

        # مسح الذاكرة المؤقتة للعميل
        del user_data[chat_id]

# 3. الرد على أي رسالة أخرى
@bot.message_handler(func=lambda message: True)
def reply_anything(message):
    bot.reply_to(message, "أهلاً بك! لطلب البن والتواصل مع خدمة العملاء، يرجى إرسال الأمر:\n/start")

bot.infinity_polling()
