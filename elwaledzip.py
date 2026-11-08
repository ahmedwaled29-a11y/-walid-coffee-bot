# -*- coding: utf-8 -*-
# بوت شركة الوليد للبن - أزرار تفاعلية جذابة
import os
import threading
import telebot
from telebot import types
from flask import Flask
from threading import Thread

# إعداد السيرفر الوهمي Keep-Alive لإبقاء البوت شغال 24/7
app_web = Flask("")

@app_web.route("/")
def home():
    return "Waleed Coffee Bot is running 24/7!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

TOKENS = [
    "8998430604:AAG_ZjLiko94ETL3S2LvtPCc8f1nlVk-ajA",
    "",  
    "",  
]
ADMIN_ID = 8287570358  # رقم الآدمن الخاص بك
COMPANY = "شركة الوليد للبن"

PRODUCTS = {
    "بن زهرة البرازيل": {"kg": 420, "photos": ["product_photo_1.jpg", "product_photo_2.jpg", "product_photo_3.jpg"]},
    "بن الفخامة": {"kg": 700, "photos": []},
    "بن كلومبي": {"kg": 600, "photos": []},
    "بن المصري": {"kg": 1000, "photos": []},
    "البن البرازيلي الذهبي": {"kg": 630, "photos": []},
}
SIZES = {"كيلو": 1000, "250 جرام": 250, "125 جرام": 125, "50 جرام": 50}
ROASTS = ["سادة", "فاتحة", "وسط", "غامقة", "محوجة"]
STATES = {}

def money(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")

# دالة الأزرار التفاعلية الرئيسية (تظهر تحت الرسالة بشكل جذاب)
def main_inline_kb():
    k = types.InlineKeyboardMarkup(row_width=2)
    k.add(
        types.InlineKeyboardButton("☕ منتجاتنا", callback_data="products"),
        types.InlineKeyboardButton("💰 الأسعار", callback_data="prices")
    )
    k.add(
        types.InlineKeyboardButton("🛒 اطلب الآن", callback_data="order"),
        types.InlineKeyboardButton("🎧 خدمة العملاء", callback_data="support")
    )
    k.add(types.InlineKeyboardButton("ℹ️ عن الشركة", callback_data="about"))
    return k

def product_inline_kb():
    k = types.InlineKeyboardMarkup(row_width=2)
    for name in PRODUCTS:
        k.add(types.InlineKeyboardButton(f"☕ {name}", callback_data=f"prod_{name}"))
    k.add(types.InlineKeyboardButton("⬅️ القائمة الرئيسية", callback_data="main_menu"))
    return k

def size_inline_kb():
    k = types.InlineKeyboardMarkup(row_width=2)
    for size in SIZES:
        k.add(types.InlineKeyboardButton(f"⚖️ {size}", callback_data=f"size_{size}"))
    k.add(types.InlineKeyboardButton("⬅️ القائمة الرئيسية", callback_data="main_menu"))
    return k

def roast_inline_kb():
    k = types.InlineKeyboardMarkup(row_width=2)
    for roast in ROASTS:
        k.add(types.InlineKeyboardButton(f"🔥 {roast}", callback_data=f"roast_{roast}"))
    k.add(types.InlineKeyboardButton("✨ بدون تحديد", callback_data="roast_بدون تحديد"))
    k.add(types.InlineKeyboardButton("⬅️ القائمة الرئيسية", callback_data="main_menu"))
    return k

def price_text(name):
    lines = [f"☕ *{name}*", "أسعار شركة الوليد:", ""]
    for size, grams in SIZES.items():
        lines.append(f"• {size}: *{money(PRODUCTS[name]['kg'] * grams / 1000)} جنيه*")
    return "\n".join(lines)

def setup_bot(token, number):
    bot = telebot.TeleBot(token)
    STATES[number] = {}

    def state(chat_id):
        return STATES[number].setdefault(chat_id, {})

    @bot.message_handler(commands=["start"])
    def start(m):
        STATES[number].pop(m.chat.id, None)
        bot.send_message(
            m.chat.id,
            "☕ *شركة الوليد للبن*\n━━━━━━━━━━━━━━\nأهلاً وسهلاً بحضرتك ❤️\n"
            "اختر الخدمة المطلوبة بالضغط على الأزرار أدناه:",
            reply_markup=main_inline_kb(),
            parse_mode="Markdown"
        )

    # التعامل مع الضغط على الأزرار التفاعلية (Inline Buttons)
    @bot.callback_query_handler(func=lambda call: True)
    def callback_handler(call):
        cid = call.message.chat.id
        data = call.data
        s = state(cid)

        if data == "main_menu":
            STATES[number].pop(cid, None)
            bot.edit_message_text(
                "☕ *شركة الوليد للبن*\nاختر الخدمة المطلوبة:",
                chat_id=cid,
                message_id=call.message.message_id,
                reply_markup=main_inline_kb(),
                parse_mode="Markdown"
            )

        elif data == "products":
            bot.edit_message_text(
                "☕ *منتجات شركة الوليد* - اختر المنتج المناسب:",
                chat_id=cid,
                message_id=call.message.message_id,
                reply_markup=product_inline_kb(),
                parse_mode="Markdown"
            )

        elif data == "prices":
            text = "💰 *قائمة الأسعار (سعر الكيلو)*:\n\n" + "\n".join(
                f"☕ {n}: *{money(d['kg'])} جنيه*" for n, d in PRODUCTS.items()
            )
            bot.edit_message_text(
                text,
                chat_id=cid,
                message_id=call.message.message_id,
                reply_markup=main_inline_kb(),
                parse_mode="Markdown"
            )

        elif data == "order":
            s.clear()
            s["step"] = "product_choice"
            bot.edit_message_text(
                "🛒 *خطوات طلب البن*\nاختر نوع البن المطلوب:",
                chat_id=cid,
                message_id=call.message.message_id,
                reply_markup=product_inline_kb(),
                parse_mode="Markdown"
            )

        elif data.startswith("prod_"):
            product_name = data.replace("prod_", "")
            s["product"] = product_name
            s["step"] = "size_choice"
            bot.edit_message_text(
                f"✅ اخترت: *{product_name}*\nاختر الوزن المطلوب:",
                chat_id=cid,
                message_id=call.message.message_id,
                reply_markup=size_inline_kb(),
                parse_mode="Markdown"
            )

        elif data.startswith("size_"):
            size_name = data.replace("size_", "")
            s["size"] = size_name
            s["step"] = "roast_choice"
            bot.edit_message_text(
                f"⚖️ اخترت وزن: *{size_name}*\nاختر درجة التحميص:",
                chat_id=cid,
                message_id=call.message.message_id,
                reply_markup=roast_inline_kb(),
                parse_mode="Markdown"
            )

        elif data.startswith("roast_"):
            roast_name = data.replace("roast_", "")
            s["roast"] = roast_name
            s["step"] = "waiting_name"
            bot.edit_message_text(
                "✍️ من فضلك، اكتب **اسمك الثلاثي** في رسالة جديدة:",
                chat_id=cid,
                message_id=call.message.message_id,
                parse_mode="Markdown"
            )

        elif data == "support":
            s["step"] = "waiting_support"
            bot.edit_message_text(
                "🎧 اترك رسالتك الآن في المحادثة وسنقوم بالرد عليك قريباً ❤️",
                chat_id=cid,
                message_id=call.message.message_id,
                reply_markup=main_inline_kb(),
                parse_mode="Markdown"
            )

        elif data == "about":
            bot.edit_message_text(
                "☕ *شركة الوليد للبن*\nجودة نختارها بعناية وطعم يسعد يومك ❤️",
                chat_id=cid,
                message_id=call.message.message_id,
                reply_markup=main_inline_kb(),
                parse_mode="Markdown"
            )

        elif data == "confirm_order":
            order = (
                f"🛒 *طلب جديد عبر الأزرار التفاعلية*\n"
                f"المنتج: {s.get('product')}\n"
                f"الوزن: {s.get('size')}\n"
                f"التحميص: {s.get('roast')}\n"
                f"السعر: {money(s.get('cost'))} جنيه\n"
                f"الاسم: {s.get('name')}\n"
                f"الهاتف: {s.get('phone')}\n"
                f"العنوان: {s.get('address')}\n"
                f"Customer ID: `{cid}`"
            )
            try:
                bot.send_message(ADMIN_ID, order, parse_mode="Markdown")
                bot.send_message(cid, "✅ تم تسجيل طلبك وإرساله للإدارة بنجاح وسنتواصل معك قريباً ❤️", reply_markup=main_inline_kb())
            except Exception:
                bot.send_message(cid, "حدث خطأ أثناء إرسال الطلب، حاول مرة أخرى.")
            STATES[number].pop(cid, None)

        elif data == "cancel_order":
            STATES[number].pop(cid, None)
            bot.edit_message_text("❌ تم إلغاء الطلب.", chat_id=cid, message_id=call.message.message_id, reply_markup=main_inline_kb())

    # التعامل مع النصوص الإدخالية (الاسم، الهاتف، العنوان)
    @bot.message_handler(func=lambda message: True)
    def handle_text(m):
        cid, msg = m.chat.id, (m.text or "").strip()
        s = state(cid)
        step = s.get("step")

        if step == "waiting_support":
            try:
                bot.send_message(ADMIN_ID, f"🎧 رسالة خدمة عملاء:\nالعميل: {m.from_user.first_name} (`{cid}`)\n\n{msg}", parse_mode="Markdown")
                bot.send_message(cid, "✅ وصلت رسالتك لخدمة العملاء وسنرد عليك قريباً ❤️", reply_markup=main_inline_kb())
            except Exception:
                bot.send_message(cid, "تعذر الإرسال، حاول لاحقاً.")
            s.clear()
            return

        if step == "waiting_name":
            s["name"] = msg
            s["step"] = "waiting_phone"
            return bot.send_message(cid, "📱 أرسل رقم هاتفك المحمول للتواصل:")

        if step == "waiting_phone":
            s["phone"] = msg
            s["step"] = "waiting_address"
            return bot.send_message(cid, "📍 أرسل عنوان التوصيل بالتفصيل:")

        if step == "waiting_address":
            s["address"] = msg
            grams = SIZES[s["size"]]
            s["cost"] = PRODUCTS[s["product"]]["kg"] * grams / 1000
            s["step"] = "confirm"
            
            summary = (
                "🧾 *مراجعة تفاصيل الطلب*\n"
                "━━━━━━━━━━━━━━\n"
                f"☕ المنتج: {s['product']}\n"
                f"⚖️ الوزن: {s['size']}\n"
                f"🔥 التحميص: {s['roast']}\n"
                f"💰 الإجمالي: *{money(s['cost'])} جنيه*\n\n"
                f"👤 الاسم: {s['name']}\n"
                f"📱 الهاتف: {s['phone']}\n"
                f"📍 العنوان: {s['address']}\n\n"
                "هل تؤكد الطلب؟"
            )
            k = types.InlineKeyboardMarkup(row_width=2)
            k.add(
                types.InlineKeyboardButton("✅ تأكيد الطلب", callback_data="confirm_order"),
                types.InlineKeyboardButton("❌ إلغاء", callback_data="cancel_order")
            )
            return bot.send_message(cid, summary, reply_markup=k, parse_mode="Markdown")

        bot.send_message(cid, "اختر من الأزرار التفاعلية أو اكتب /start للبداية:", reply_markup=main_inline_kb())

    return bot

def main():
    keep_alive()
    active = []
    for number, token in enumerate(TOKENS, 1):
        token = token.strip()
        if not token:
            continue
        try:
            active.append((setup_bot(token, number), number))
        except Exception as e:
            print(f"خطأ في تشغيل البوت {number}: {e}")
    if not active:
        print("ضع التوكن الصحيح.")
        return
    print(f"✅ تم تشغيل البوت بنجاح بالأزرار التفاعلية!")
    for bot, number in active:
        threading.Thread(target=lambda b=bot: b.infinity_polling(skip_pending=True, timeout=30), daemon=True).start()
    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("إيقاف.")

if __name__ == "__main__":
    main()
