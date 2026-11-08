# -*- coding: utf-8 -*-
# بوت شركة الوليد للبن - Pydroid 3
# ثبّت المكتبة: pip install pyTelegramBotAPI
# ضع التوكنات في TOKENS. اترك الخانات غير المستخدمة فارغة.
# ضع الصور الثلاثة بجوار هذا الملف دون تعديل أسمائها.

import os
import threading
import telebot
from telebot import types

TOKENS = [
    "8998430604:AAG_ZjLiko94ETL3S2LvtPCc8f1nlVk-ajA",
    "",  # توكن البوت الثاني (اختياري)
    "",  # توكن البوت الثالث (اختياري)
]
ADMIN_ID = 8287570358  # غيّره إذا لم يكن هذا رقم حساب الإدارة الصحيح
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

def main_kb():
    k = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    k.add("☕ منتجاتنا", "💰 قائمة الأسعار")
    k.add("🛒 اطلب الآن", "🎧 خدمة العملاء")
    k.add("ℹ️ عن الشركة")
    return k

def product_kb():
    k = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    names = list(PRODUCTS)
    for i in range(0, len(names), 2):
        k.add(*names[i:i+2])
    k.add("⬅️ القائمة الرئيسية")
    return k

def size_kb():
    k = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    k.add("كيلو", "250 جرام", "125 جرام", "50 جرام")
    k.add("⬅️ القائمة الرئيسية")
    return k

def roast_kb():
    k = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    k.add(*ROASTS)
    k.add("بدون تحديد", "⬅️ القائمة الرئيسية")
    return k

def price_text(name):
    lines = [f"☕ {name}", "أسعار شركة الوليد:", ""]
    for size, grams in SIZES.items():
        lines.append(f"• {size}: {money(PRODUCTS[name]['kg'] * grams / 1000)} جنيه")
    return "\n".join(lines)

def send_photos(bot, chat_id, name):
    for filename in PRODUCTS[name]["photos"]:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        if os.path.isfile(path):
            with open(path, "rb") as photo:
                bot.send_photo(chat_id, photo)

def setup_bot(token, number):
    bot = telebot.TeleBot(token)
    STATES[number] = {}

    def state(chat_id):
        return STATES[number].setdefault(chat_id, {})

    @bot.message_handler(commands=["start"])
    def start(m):
        STATES[number].pop(m.chat.id, None)
        bot.send_message(m.chat.id,
            "☕ شركة الوليد للبن\n━━━━━━━━━━━━━━\nأهلاً وسهلاً بحضرتك ❤️\n"
            "اختار الخدمة من الأزرار أو اكتب سؤالك واسم البن مباشرة.",
            reply_markup=main_kb())

    @bot.message_handler(commands=["admin"])
    def admin(m):
        if m.from_user.id != ADMIN_ID:
            return bot.reply_to(m, "هذا الأمر للإدارة فقط.")
        bot.reply_to(m,
            "👑 لوحة إدارة شركة الوليد\n"
            "للرد على عميل:\n/reply رقم_العميل نص_الرسالة\n"
            "لتعديل سعر الكيلو:\n/setprice اسم_المنتج السعر\n"
            "مثال: /setprice بن زهرة البرازيل 450")

    @bot.message_handler(commands=["reply"])
    def reply_customer(m):
        if m.from_user.id != ADMIN_ID:
            return
        p = m.text.split(maxsplit=2)
        if len(p) < 3 or not p[1].isdigit():
            return bot.reply_to(m, "استخدم: /reply رقم_العميل نص_الرسالة")
        try:
            bot.send_message(int(p[1]), "🎧 رسالة من خدمة عملاء شركة الوليد:\n\n" + p[2])
            bot.reply_to(m, "✅ تم إرسال الرد.")
        except Exception as e:
            bot.reply_to(m, "تعذر الإرسال: " + str(e))

    @bot.message_handler(commands=["setprice"])
    def setprice(m):
        if m.from_user.id != ADMIN_ID:
            return
        p = m.text.split()
        if len(p) < 4:
            return bot.reply_to(m, "مثال: /setprice بن زهرة البرازيل 450")
        name, raw = " ".join(p[1:-1]), p[-1]
        if name not in PRODUCTS:
            return bot.reply_to(m, "اسم المنتج غير موجود.")
        try:
            PRODUCTS[name]["kg"] = float(raw)
            bot.reply_to(m, f"✅ تم تحديث سعر كيلو {name} إلى {money(float(raw))} جنيه.")
        except ValueError:
            bot.reply_to(m, "السعر يجب أن يكون رقمًا.")

    @bot.message_handler(content_types=["text"])
    def handle(m):
        cid, msg = m.chat.id, (m.text or "").strip()
        s = state(cid)
        step = s.get("step")

        if msg == "⬅️ القائمة الرئيسية":
            STATES[number].pop(cid, None)
            return bot.send_message(cid, "☕ أهلاً بحضرتك في شركة الوليد ❤️", reply_markup=main_kb())

        if step == "support":
            try:
                bot.send_message(ADMIN_ID,
                    f"🎧 رسالة خدمة عملاء جديدة | البوت {number}\n"
                    f"العميل: {m.from_user.first_name}\nCustomer ID: {cid}\n\n{msg}\n"
                    f"للرد: /reply {cid} اكتب الرد")
                bot.send_message(cid, "✅ وصلت رسالتك لخدمة العملاء، سنرد عليك قريبًا ❤️", reply_markup=main_kb())
            except Exception:
                bot.send_message(cid, "تعذر إرسال الرسالة للإدارة. حاول لاحقًا.")
            s.clear()
            return

        if step == "product":
            if msg not in PRODUCTS:
                return bot.send_message(cid, "اختار منتجًا من الأزرار.", reply_markup=product_kb())
            s["product"] = msg
            s["step"] = "size"
            return bot.send_message(cid, "اختار الوزن:", reply_markup=size_kb())
        if step == "size":
            if msg not in SIZES:
                return bot.send_message(cid, "اختار وزنًا من الأزرار.", reply_markup=size_kb())
            s["size"] = msg
            s["step"] = "roast"
            return bot.send_message(cid, "اختار درجة التحميص:", reply_markup=roast_kb())
        if step == "roast":
            if msg not in ROASTS and msg != "بدون تحديد":
                return bot.send_message(cid, "اختار درجة التحميص من الأزرار.", reply_markup=roast_kb())
            s["roast"] = msg
            s["step"] = "name"
            return bot.send_message(cid, "اكتب اسم حضرتك:", reply_markup=types.ReplyKeyboardRemove())
        if step == "name":
            s["name"], s["step"] = msg, "phone"
            return bot.send_message(cid, "اكتب رقم الهاتف للتواصل:")
        if step == "phone":
            s["phone"], s["step"] = msg, "address"
            return bot.send_message(cid, "اكتب عنوان التوصيل:")
        if step == "address":
            s["address"] = msg
            grams = SIZES[s["size"]]
            s["cost"] = PRODUCTS[s["product"]]["kg"] * grams / 1000
            s["step"] = "confirm"
            summary = (
                "🧾 تفاصيل الطلب - شركة الوليد\n━━━━━━━━━━━━━━\n"
                f"المنتج: {s['product']}\nالوزن: {s['size']}\n"
                f"التحميص: {s['roast']}\nالسعر: {money(s['cost'])} جنيه\n\n"
                f"اسم العميل: {s['name']}\nالهاتف: {s['phone']}\n"
                f"العنوان: {s['address']}\nCustomer ID: {cid}\n\nهل تؤكد الطلب؟")
            k = types.ReplyKeyboardMarkup(resize_keyboard=True)
            k.add("✅ تأكيد الطلب", "❌ إلغاء")
            return bot.send_message(cid, summary, reply_markup=k)
        if step == "confirm":
            if msg == "❌ إلغاء":
                STATES[number].pop(cid, None)
                return bot.send_message(cid, "تم إلغاء الطلب.", reply_markup=main_kb())
            if msg != "✅ تأكيد الطلب":
                return bot.send_message(cid, "اختار تأكيد الطلب أو إلغاء.")
            order = (
                f"🛒 طلب جديد | شركة الوليد | البوت {number}\n"
                f"المنتج: {s['product']}\nالوزن: {s['size']}\nالتحميص: {s['roast']}\n"
                f"السعر: {money(s['cost'])} جنيه\nالاسم: {s['name']}\n"
                f"الهاتف: {s['phone']}\nالعنوان: {s['address']}\nCustomer ID: {cid}")
            try:
                bot.send_message(ADMIN_ID, order)
                bot.send_message(cid, "✅ تم تسجيل طلب حضرتك وإرساله للإدارة.\nسنتواصل معك لتأكيد الطلب. شكرًا لثقتك في شركة الوليد ❤️", reply_markup=main_kb())
            except Exception:
                bot.send_message(cid, "لم نتمكن من إرسال الطلب للإدارة الآن. حاول لاحقًا.", reply_markup=main_kb())
            STATES[number].pop(cid, None)
            return

        if msg in ("☕ منتجاتنا", "الأنواع", "المنتجات"):
            return bot.send_message(cid, "☕ منتجات شركة الوليد - اختار المنتج:", reply_markup=product_kb())
        if msg in ("💰 قائمة الأسعار", "الأسعار", "الأسعار كلها"):
            text = "💰 قائمة الأسعار (سعر الكيلو):\n\n" + "\n".join(
                f"☕ {n}: {money(d['kg'])} جنيه" for n, d in PRODUCTS.items())
            return bot.send_message(cid, text, reply_markup=main_kb())
        if msg in ("🛒 اطلب الآن", "اطلب", "طلب", "عايز أطلب", "اريد طلب"):
            s.clear()
            s["step"] = "product"
            return bot.send_message(cid, "اختار المنتج المطلوب:", reply_markup=product_kb())
        if msg in ("🎧 خدمة العملاء", "خدمة العملاء"):
            s["step"] = "support"
            return bot.send_message(cid, "اكتب رسالتك الآن وسيتم إرسالها لخدمة العملاء ❤️", reply_markup=main_kb())
        if msg in ("ℹ️ عن الشركة", "عن الشركة"):
            return bot.send_message(cid, "☕ شركة الوليد للبن\nجودة نختارها بعناية وطعم يسعد يومك ❤️", reply_markup=main_kb())

        # التقاط اسم المنتج من الرسائل المكتوبة بشكل عادي
        normalized = msg.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
        found = None
        for name in PRODUCTS:
            if name in msg or name.replace("أ", "ا") in normalized:
                found = name
                break
        if found:
            send_photos(bot, cid, found)
            return bot.send_message(cid, price_text(found), reply_markup=main_kb())
        if any(x in msg for x in ["سعر", "بكام", "بكم", "كيلو", "جرام"]):
            return bot.send_message(cid, "أهلاً بحضرتك ❤️ اختار نوع البن لمعرفة السعر:", reply_markup=product_kb())
        if any(x in msg for x in ["سلام", "مرحبا", "اهلا", "أهلا"]):
            return bot.send_message(cid, "أهلاً وسهلاً بحضرتك في شركة الوليد ❤️☕", reply_markup=main_kb())
        return bot.send_message(cid, "اكتب اسم نوع البن أو كلمة الأسعار، أو اختار خدمة من الأزرار.", reply_markup=main_kb())

    return bot

def main():
    active = []
    for number, token in enumerate(TOKENS, 1):
        token = token.strip()
        if not token or token.startswith("PUT_"):
            continue
        try:
            active.append((setup_bot(token, number), number))
        except Exception as e:
            print(f"خطأ في إعداد البوت {number}: {e}")
    if not active:
        print("ضع توكن البوت الأول في TOKENS ثم شغّل الملف.")
        return
    print(f"✅ تم تشغيل {len(active)} بوت/بوتات شركة الوليد.")
    for bot, number in active:
        threading.Thread(
            target=lambda b=bot: b.infinity_polling(skip_pending=True, timeout=30),
            daemon=True
        ).start()
    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("تم إيقاف التشغيل.")

if __name__ == "__main__":
    main()
