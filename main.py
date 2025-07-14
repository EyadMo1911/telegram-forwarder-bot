from telethon import TelegramClient, events
from PIL import Image
import os
import asyncio
import re
from datetime import datetime
from pytz import timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ✅ بيانات API
api_id = 25671729
api_hash = '7a99f52526cd483c1d5abf27069d5e10'

# ✅ القنوات
source_channel = 'https://t.me/OPTION_Xn'
destination_channel = 'https://t.me/BOT_TOPSPX1'

# ✅ إنشاء العميل
client = TelegramClient('forwarder_session', api_id, api_hash)

# ✅ تبسيط تنبيه فني
def simplify_alert_message(text):
    try:
        match = re.search(r"تحت\s+(\d+)[^\d]+.*?(\d{5})", text)
        if match:
            level1 = match.group(1)
            level2 = match.group(2)
            return f"""🚨 تنبيه فني
📉 مستوى خطير تحت {level1}
⛔ تم رفض الاختراق أعلى {level2}
👀 المتابعة مطلوبة بدقة"""
        return text
    except Exception as e:
        print(f"❌ خطأ في تنسيق التنبيه الفني: {e}")
        return text

# ✅ تبسيط تحديث صفقة
def simplify_trade_update(text):
    try:
        real_strike_match = re.search(r"📍\s*Strike:\s*(\d+)", text)
        strike = real_strike_match.group(1) if real_strike_match else "غير معروف"

        date_match = re.search(r"(\d{1,2})\s+(\w+)\s+(202\d)", text)
        if date_match:
            day, month_name_ar, year = date_match.groups()
            month_map = {
                'يناير': 1, 'فبراير': 2, 'مارس': 3, 'أبريل': 4, 'ابريل': 4,
                'مايو': 5, 'يونيو': 6, 'يوليو': 7, 'أغسطس': 8, 'اغسطس': 8,
                'سبتمبر': 9, 'أكتوبر': 10, 'اكتوبر': 10, 'نوفمبر': 11, 'ديسمبر': 12
            }
            month = month_map.get(month_name_ar, 1)
            date_obj = datetime(int(year), month, int(day))
            day_name_ar = {
                'Monday': 'الاثنين', 'Tuesday': 'الثلاثاء', 'Wednesday': 'الأربعاء',
                'Thursday': 'الخميس', 'Friday': 'الجمعة', 'Saturday': 'السبت', 'Sunday': 'الأحد'
            }[date_obj.strftime('%A')]
            full_date = f"{day_name_ar} – {day} {month_name_ar} {year}"
        else:
            full_date = "غير معروف"

        simplified_message = f"""🎯 تحديث صفقة | (SPXW {strike}P)
<b>📅 اليوم:</b> {full_date}
<b>⏳ تاريخ الانتهاء:</b> نفس اليوم
                                                               ⸻
<b>🔻 نوع العقد:</b> خيار بيع (بوت – PUT)
<b>📍 سعر التنفيذ (Strike):</b> {strike}
<b>💵 سعر الدخول المقترح:</b> لا يتجاوز $20 – $30 من الطرح المعروض
                                                               ⸻
🎯 <b>الأهداف المحققة:</b>
• ✅ الهدف الأول: ربح بين 15٪ – 20٪ من قيمة العقد
• ✅ الهدف الثاني: يتم التنويه عنه لاحقًا
                                                               ⸻
🔐 <b>مبدؤنا:</b> التداول بحذر لأجل إنماء المحفظة بثبات – دون طمع
                                                               ⸻
BOT_TOPSPX1"""
        return simplified_message
    except Exception as e:
        print(f"❌ خطأ أثناء تبسيط الرسالة: {e}")
        return text

# ✅ تبسيط صفقة ناجحة
def simplify_successful_trade(text):
    try:
        strike_match = re.search(r"SPXW\s*(\d+)", text)
        strike = strike_match.group(1) if strike_match else "غير معروف"

        date_match = re.search(r"(\d{1,2})\s+([A-Za-z]+)\s+(\d{2})", text)
        if date_match:
            day, month_eng, year = date_match.groups()
            year = "20" + year
            day = str(int(day))

            month_map = {
                'Jan': ('يناير', 1), 'Feb': ('فبراير', 2), 'Mar': ('مارس', 3), 'Apr': ('أبريل', 4),
                'May': ('مايو', 5), 'Jun': ('يونيو', 6), 'Jul': ('يوليو', 7), 'Aug': ('أغسطس', 8),
                'Sep': ('سبتمبر', 9), 'Oct': ('أكتوبر', 10), 'Nov': ('نوفمبر', 11), 'Dec': ('ديسمبر', 12)
            }
            month_ar, month_num = month_map.get(month_eng, ("غير معروف", 1))
            date_obj = datetime(int(year), month_num, int(day))
            day_name_map = {
                'Monday': 'الاثنين', 'Tuesday': 'الثلاثاء', 'Wednesday': 'الأربعاء',
                'Thursday': 'الخميس', 'Friday': 'الجمعة', 'Saturday': 'السبت', 'Sunday': 'الأحد'
            }
            day_name_ar = day_name_map[date_obj.strftime('%A')]
            full_date_line = f"{day} {month_ar} {year}"
            formatted_date = f"{day_name_ar} – {day} {month_ar}"
        else:
            full_date_line = "غير معروف"
            formatted_date = "غير معروف"

        simplified = f"""🎯 صفقة ناجحة | (SPXW {strike}P) – {full_date_line}

🔻 نوع العقد: خيار بيع (بوت – Put)
📆 التاريخ: {formatted_date}
                                                               ⸻

💵 سعر التنفيذ: تم الدخول عند السعر المطروح
📈 النتيجة: ربح مميز تجاوز +30٪ خلال نفس الجلسة
                                                               ⸻
✨ صفقة دقيقة تم تنفيذها بثقة بعد مراقبة حركة السوق واختيار مثالي للعقد.
📌 نجاح يعكس الانضباط وفعالية إدارة المخاطر
                                                               ⸻
BOT_TOPSPX1"""
        return simplified
    except Exception as e:
        print(f"❌ خطأ أثناء تبسيط صفقة ناجحة: {e}")
        return text

# ✅ استبدال كلمات
def replace_keywords(text):
    if not text:
        return ""
    replacements = {
        "هيرو زيرو": "هيرو خطير استمرار فيه قرارك",
        "هيرو": "هيرو خطير استمرار فيه قرارك",
        "OPTON X": "BOT_TOPSPX1",
        "نتايج طرح اليوم ولله الحمد 🤑🤑": "✅ نتائج تداول اليوم – والحمد لله على التوفيق والنجاح",
        "بوت مضاربي دون المنطقة": " 🔻 بوت مضاربي دون المنطقة "
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"من\s+(?:ال)?ارباح", "العقد عالي الخطورة\n💰 الدخول فقط من أرباح سابقة\n👁‍🗨 المتابعة الحذرة مطلوب", text, flags=re.IGNORECASE)
    return text

# ✅ علامة مائية
def add_image_watermark(base_image_path, watermark_image_path, output_path, opacity=135):
    base_image = Image.open(base_image_path).convert("RGBA")
    watermark = Image.open(watermark_image_path).convert("RGBA")
    scale_factor = 0.75
    new_size = (int(base_image.width * scale_factor), int(base_image.height * scale_factor))
    watermark = watermark.resize(new_size, Image.Resampling.LANCZOS)
    alpha = watermark.getchannel("A")
    alpha = alpha.point(lambda p: int(p * (opacity / 255)))
    watermark.putalpha(alpha)
    x = (base_image.width - watermark.width) // 2
    y = (base_image.height - watermark.height) // 2
    transparent_layer = Image.new("RGBA", base_image.size, (0, 0, 0, 0))
    transparent_layer.paste(watermark, (x, y), watermark)
    combined = Image.alpha_composite(base_image, transparent_layer)
    combined.convert("RGB").save(output_path, "JPEG")

# ✅ التعامل مع الرسائل الجديدة
@client.on(events.NewMessage(chats=source_channel))
async def forward_handler(event):
    try:
        original_text = event.text or ""
        modified_caption = replace_keywords(original_text)

        if "🎯 تحديث صفقة |" in original_text:
            modified_caption = simplify_trade_update(original_text)
        elif "🎯 صفقة ناجحة |" in original_text:
            modified_caption = simplify_successful_trade(original_text)
        elif "خطير ومتابعه تحت" in original_text:
            modified_caption = simplify_alert_message(original_text)

        if event.photo:
            file_path = await event.download_media()
            output_path = "watermarked.jpg"
            watermark_path = "watermark.png"
            add_image_watermark(file_path, watermark_path, output_path)
            await client.send_file(destination_channel, output_path, caption=modified_caption, parse_mode='html')
            os.remove(file_path)
            os.remove(output_path)
        elif event.message:
            await client.send_message(destination_channel, modified_caption, parse_mode='html')

        await client.send_message(destination_channel, "\n\n.")
        await client.send_message(destination_channel, "───  BOT_TOPSPX1 ───\n")

    except Exception as e:
        print(f"❌ خطأ أثناء التعامل مع الرسالة: {e}")

# ✅ الرسالة اليومية الثابتة
daily_message = """بسم الله الرحمن الرحيم

🤖 نظام إدارة مجموعة BOT_TOPSPX
تدار المجموعة بواسطة روبوت ذكي مبني على خوارزميات تحليل متقدمة،
وتحت إشراف مباشر من قبل تسعة اشخاص خبراء ماليين محترفين لضمان دقة الأداء واتخاذ القرارات المُثلى.

⚙ آلية اختيار العقود وتنفيذ الصفقات
اختيار العقد الأنسب يتم عبر تحليل شامل لـ:
    • 📊 حجم السيولة اليومية
    • 🌀 حركة السوق اللحظية (Volatility)
    • 📈 التحليل الفني الدقيق للعقد

قواعد تنفيذ الصفقة:
    • ✅ يتم طرح العقد عند مستوى دخول محسوب مسبقًا بدقة.
    • ⛔ يُمنع الدخول إذا ارتفع السعر أكثر من 20 دولار عن سعر الطرح ومحاولة إسراع في الدخول عند طرح العقد
    • 🛑 يتم تحديد مستوى وقف الخسارة بوضوح على الشارت قبل أي تنفيذ.

استراتيجية الخروج:
    • 🎯 هدفنا تحقيق ربح 60 دولار أي 15٪ إلى 20٪ لتضمن الربح وتنمي محفظتك والاستمرار بقرارك، ويتم توضيح إذا هناك فرصة قوية لعقد في ارتفاع واستمرار
    • عند دخولك بأكثر من عقد يُنصح بالخروج إذا تم ربح 15‎% إلى 20‎%‎ من قيمة كل عقد

🎯 نظام المجموعة
    • لا نُكثر من الصفقات. نُركز على:
        - ✔ أقصى ربح ممكن
        - 🛡 أقل خسارة محتملة

📊 نظام تتبع الأداء
نقيس كفاءة الروبوت وفق:
    • 📈 أعلى ربح تم تحقيقه للعقد الواحد
    • 📉 أقصى خسارة مسجلة للعقد الواحد
    • 📆 تقارير أسبوعية وشهرية لأداء المجموعة (ربح / خسارة)

🔔 تنبيه مهم:
الأرقام المعروضة لا تمثل أداء كل متداول بدقة، إذ يختلف الأداء حسب:
    • 🔢 عدد العقود المنفذة
    • ⏱ توقيت الدخول والخروج

⚠ إخلاء مسؤولية ضروري
    • 🎓 هذه المجموعة تُستخدم لأغراض تعليمية فقط عبر الحسابات التجريبية.
    • 🧾 المعلومات المعروضة ليست توصيات.
    • ⚠ التداول يتم على مسؤوليتك الشخصية."""

# ✅ جدولة الرسالة اليومية الساعة 3 فجراً بتوقيت السعودية
scheduler = AsyncIOScheduler(timezone="Asia/Riyadh")
@scheduler.scheduled_job('cron', hour=3, minute=0)
async def send_daily_info():
    await client.send_message(destination_channel, daily_message)

# ✅ التشغيل
async def main():
    await client.start()
    print("✅ البوت متصل بـ Telegram")
    scheduler.start()
    await client.run_until_disconnected()

# ✅ بدء البوت
if __name__ == "__main__":
    asyncio.run(main())
