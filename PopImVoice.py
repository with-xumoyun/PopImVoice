import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.client.default import DefaultBotProperties


# =========================================================
# SETTINGS
# =========================================================

TOKEN = "8861059885:AAGxXYaBCdsIFXpEx_Wd_gNEUiZaT0zzbWg"

# SHIKOYAT VA TAKLIFLAR SHU ID GA KELADI
ADMIN_ID = 6630112784

logging.basicConfig(level=logging.INFO)

router = Router()

users_db = {}


# =========================================================
# SARDORLAR
# =========================================================

SARDORS = {
    "maktab": {
        "name": "🏫 Maktab sardori",
        "description": "Maktab sardori — o‘quvchilar manfaatlarini ifodalash va tashabbuslarni muvofiqlashtirishga yordam beradi."
    },

    "eco": {
        "name": "🌿 Ekologiya sardori",
        "description": "Ekologiya sardori — ekologik madaniyat, tozalik va atrof-muhitni asrash tashabbuslarini rivojlantiradi."
    },

    "sport": {
        "name": "⚽️ Sport sardori",
        "description": "Sport sardori — sport musobaqalari va sog‘lom turmush tarzi tadbirlarini tashkil etishga yordam beradi."
    },

    "talim": {
        "name": "📚 Ta’lim sardori",
        "description": "Ta’lim sardori — ta’lim sifatini yaxshilash va bilim olishga qiziqishni oshirishga yordam beradi."
    },

    "media": {
        "name": "📸 Media sardori",
        "description": "Media sardori — maktab yangiliklari, tadbirlar va loyihalarni yoritadi."
    },

    "madaniyat": {
        "name": "🎭 Madaniyat sardori",
        "description": "Madaniyat sardori — madaniy tadbirlar va ijodiy loyihalarni tashkil etishga yordam beradi."
    },

    "kamalak": {
        "name": "🌟 Kamalak sardori",
        "description": "Kamalak sardori — do‘stlik, hamjihatlik va ijtimoiy faollikni rivojlantirishga yordam beradi."
    }
}


# =========================================================
# STATES
# =========================================================

class RegStates(StatesGroup):
    language = State()
    full_name = State()
    grade = State()
    phone = State()


class MenuStates(StatesGroup):
    main_menu = State()

    complaint_sardor = State()
    complaint_text = State()

    suggestion_sardor = State()
    suggestion_text = State()

    edit_name = State()


# =========================================================
# TEXTS
# =========================================================

TEXTS = {
    "uz": {
        "language": "🌐 Tilni tanlang:",
        "name": "👤 Ism va familiyangizni kiriting:",
        "grade": "🎓 Sinfingizni kiriting:\n\nMasalan: 9.01",
        "phone": "📱 Telefon raqamingizni yuboring:",
        "send_phone": "📱 Telefon raqamimni yuborish",

        "success": (
            "✅ <b>Ro‘yxatdan o‘tish yakunlandi!</b>\n\n"
            "👤 Ism: {name}\n"
            "🎓 Sinf: {grade}\n"
            "📞 Telefon: {phone}\n\n"
            "🏠 Asosiy menyu:"
        ),

        "complaint": "📝 Shikoyat yuborish",
        "suggestion": "💡 Taklif yuborish",
        "profile": "👤 Profilim",
        "sardors": "👥 Sardorlar haqida",
        "news": "📰 Yangiliklar",
        "settings": "⚙️ Sozlamalar",
        "back": "🔙 Orqaga",

        "choose_complaint": (
            "📝 <b>Shikoyat yuborish</b>\n\n"
            "Shikoyat qaysi sardorga tegishli?\n"
            "Sardorni tanlang:"
        ),

        "choose_suggestion": (
            "💡 <b>Taklif yuborish</b>\n\n"
            "Taklif qaysi sardorga tegishli?\n"
            "Sardorni tanlang:"
        ),

        "write_complaint": (
            "✍️ <b>Shikoyatingizni yozing:</b>\n\n"
            "Batafsil yozib yuboring."
        ),

        "write_suggestion": (
            "✍️ <b>Taklifingizni yozing:</b>\n\n"
            "Batafsil yozib yuboring."
        ),

        "complaint_sent": (
            "✅ <b>Shikoyatingiz yuborildi!</b>\n\n"
            "Rahmat."
        ),

        "suggestion_sent": (
            "✅ <b>Taklifingiz yuborildi!</b>\n\n"
            "Rahmat."
        ),

        "profile_title": "👤 <b>Profilim</b>\n\n",

        "news_empty": "📰 Hozircha yangiliklar mavjud emas.",

        "edit_name": "✏️ Yangi ism va familiyangizni kiriting:",

        "name_updated": "✅ Ismingiz yangilandi.",

        "settings": "⚙️ Sozlamalar",

        "yes": "✅ Ha",
        "no": "❌ Yo‘q",

        "reset": (
            "⚠️ Ro‘yxatdan o‘tish ma’lumotlari o‘chiriladi.\n\n"
            "Qaytadan ro‘yxatdan o‘tasizmi?"
        )
    },

    "ru": {
        "language": "🌐 Выберите язык:",
        "name": "👤 Введите имя и фамилию:",
        "grade": "🎓 Введите класс:\n\nНапример: 9.01",
        "phone": "📱 Отправьте номер телефона:",
        "send_phone": "📱 Отправить мой номер",

        "success": (
            "✅ <b>Регистрация завершена!</b>\n\n"
            "👤 Имя: {name}\n"
            "🎓 Класс: {grade}\n"
            "📞 Телефон: {phone}\n\n"
            "🏠 Главное меню:"
        ),

        "complaint": "📝 Отправить жалобу",
        "suggestion": "💡 Отправить предложение",
        "profile": "👤 Мой профиль",
        "sardors": "👥 О старших",
        "news": "📰 Новости",
        "settings": "⚙️ Настройки",
        "back": "🔙 Назад",

        "choose_complaint": "📝 Выберите старшего для жалобы:",
        "choose_suggestion": "💡 Выберите старшего для предложения:",

        "write_complaint": "✍️ Напишите вашу жалобу:",
        "write_suggestion": "✍️ Напишите ваше предложение:",

        "complaint_sent": "✅ Жалоба отправлена!",
        "suggestion_sent": "✅ Предложение отправлено!",

        "profile_title": "👤 <b>Мой профиль</b>\n\n",

        "news_empty": "📰 Новостей пока нет.",

        "edit_name": "✏️ Введите новое имя и фамилию:",

        "name_updated": "✅ Имя обновлено.",

        "yes": "✅ Да",
        "no": "❌ Нет",

        "reset": "⚠️ Удалить данные регистрации?"
    },

    "en": {
        "language": "🌐 Choose your language:",
        "name": "👤 Enter your full name:",
        "grade": "🎓 Enter your grade:\n\nExample: 9.01",
        "phone": "📱 Send your phone number:",
        "send_phone": "📱 Send my phone",

        "success": (
            "✅ <b>Registration completed!</b>\n\n"
            "👤 Name: {name}\n"
            "🎓 Grade: {grade}\n"
            "📞 Phone: {phone}\n\n"
            "🏠 Main menu:"
        ),

        "complaint": "📝 Send a complaint",
        "suggestion": "💡 Send a suggestion",
        "profile": "👤 My profile",
        "sardors": "👥 About leaders",
        "news": "📰 News",
        "settings": "⚙️ Settings",
        "back": "🔙 Back",

        "choose_complaint": "📝 Choose a leader for your complaint:",
        "choose_suggestion": "💡 Choose a leader for your suggestion:",

        "write_complaint": "✍️ Write your complaint:",
        "write_suggestion": "✍️ Write your suggestion:",

        "complaint_sent": "✅ Complaint sent!",
        "suggestion_sent": "✅ Suggestion sent!",

        "profile_title": "👤 <b>My profile</b>\n\n",

        "news_empty": "📰 No news yet.",

        "edit_name": "✏️ Enter your new full name:",

        "name_updated": "✅ Name updated.",

        "yes": "✅ Yes",
        "no": "❌ No",

        "reset": "⚠️ Delete registration data?"
    }
}


# =========================================================
# HELPERS
# =========================================================

def lang(user_id):
    return users_db.get(
        user_id,
        {}
    ).get(
        "language",
        "uz"
    )


def text(user_id, key):
    language = lang(user_id)

    return TEXTS[language].get(
        key,
        TEXTS["uz"].get(key, key)
    )


def main_keyboard(user_id):

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=text(user_id, "complaint")
                ),
                KeyboardButton(
                    text=text(user_id, "suggestion")
                )
            ],
            [
                KeyboardButton(
                    text=text(user_id, "profile")
                ),
                KeyboardButton(
                    text=text(user_id, "sardors")
                )
            ],
            [
                KeyboardButton(
                    text=text(user_id, "news")
                ),
                KeyboardButton(
                    text=text(user_id, "settings")
                )
            ]
        ],
        resize_keyboard=True
    )


def language_keyboard():

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🇺🇿 O‘zbekcha"
                ),
                KeyboardButton(
                    text="🇷🇺 Русский"
                ),
                KeyboardButton(
                    text="🇬🇧 English"
                )
            ]
        ],
        resize_keyboard=True
    )


def phone_keyboard(user_id):

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=text(
                        user_id,
                        "send_phone"
                    ),
                    request_contact=True
                )
            ]
        ],
        resize_keyboard=True
    )


def back_keyboard(user_id):

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=text(
                        user_id,
                        "back"
                    )
                )
            ]
        ],
        resize_keyboard=True
    )


def sardor_keyboard(user_id, prefix):

    buttons = []

    for key, sardor in SARDORS.items():

        buttons.append(
            [
                KeyboardButton(
                    text=prefix + sardor["name"]
                )
            ]
        )

    buttons.append(
        [
            KeyboardButton(
                text=text(
                    user_id,
                    "back"
                )
            )
        ]
    )

    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )


def get_sardor(text_value):

    for key, sardor in SARDORS.items():

        if sardor["name"] in text_value:
            return key

    return None


# =========================================================
# START
# =========================================================

@router.message(CommandStart())
async def start(
    message: Message,
    state: FSMContext
):

    user_id = message.from_user.id

    if user_id in users_db:

        await state.clear()

        await state.set_state(
            MenuStates.main_menu
        )

        await message.answer(
            text(
                user_id,
                "main_menu"
            ),
            reply_markup=main_keyboard(
                user_id
            )
        )

        return

    await state.clear()

    await state.set_state(
        RegStates.language
    )

    await message.answer(
        TEXTS["uz"]["language"],
        reply_markup=language_keyboard()
    )


# =========================================================
# REGISTRATION
# =========================================================

@router.message(RegStates.language)
async def registration_language(
    message: Message,
    state: FSMContext
):

    value = message.text or ""

    if "O‘zbekcha" in value or "O'zbekcha" in value:
        language = "uz"

    elif "Русский" in value:
        language = "ru"

    elif "English" in value:
        language = "en"

    else:

        await message.answer(
            TEXTS["uz"]["language"],
            reply_markup=language_keyboard()
        )

        return

    user_id = message.from_user.id

    users_db[user_id] = {
        "language": language
    }

    await state.set_state(
        RegStates.full_name
    )

    await message.answer(
        TEXTS[language]["name"],
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(RegStates.full_name)
async def registration_name(
    message: Message,
    state: FSMContext
):

    user_id = message.from_user.id

    name = (
        message.text or ""
    ).strip()

    if len(name) < 3:

        await message.answer(
            text(user_id, "name")
        )

        return

    users_db[user_id][
        "full_name"
    ] = name

    await state.set_state(
        RegStates.grade
    )

    await message.answer(
        text(user_id, "grade")
    )


@router.message(RegStates.grade)
async def registration_grade(
    message: Message,
    state: FSMContext
):

    user_id = message.from_user.id

    grade = (
        message.text or ""
    ).strip()

    if not grade:

        await message.answer(
            text(user_id, "grade")
        )

        return

    users_db[user_id][
        "grade"
    ] = grade

    await state.set_state(
        RegStates.phone
    )

    await message.answer(
        text(user_id, "phone"),
        reply_markup=phone_keyboard(
            user_id
        )
    )


@router.message(RegStates.phone)
async def registration_phone(
    message: Message,
    state: FSMContext
):

    user_id = message.from_user.id

    if message.contact:
        phone = message.contact.phone_number

    else:
        phone = (
            message.text or ""
        ).strip()

    if not phone:

        await message.answer(
            text(user_id, "phone"),
            reply_markup=phone_keyboard(
                user_id
            )
        )

        return

    users_db[user_id][
        "phone"
    ] = phone

    name = users_db[user_id].get(
        "full_name",
        "Noma'lum"
    )

    grade = users_db[user_id].get(
        "grade",
        "Noma'lum"
    )

    await state.set_state(
        MenuStates.main_menu
    )

    await message.answer(
        text(
            user_id,
            "success"
        ).format(
            name=name,
            grade=grade,
            phone=phone
        ),
        reply_markup=main_keyboard(
            user_id
        )
    )


# =========================================================
# MAIN MENU
# =========================================================

@router.message(MenuStates.main_menu)
async def menu(
    message: Message,
    state: FSMContext
):

    user_id = message.from_user.id
    value = message.text or ""

    # SHIKOYAT
    if value == text(
        user_id,
        "complaint"
    ):

        await state.set_state(
            MenuStates.complaint_sardor
        )

        await message.answer(
            text(
                user_id,
                "choose_complaint"
            ),
            reply_markup=sardor_keyboard(
                user_id,
                "📝 "
            )
        )

        return

    # TAKLIF
    if value == text(
        user_id,
        "suggestion"
    ):

        await state.set_state(
            MenuStates.suggestion_sardor
        )

        await message.answer(
            text(
                user_id,
                "choose_suggestion"
            ),
            reply_markup=sardor_keyboard(
                user_id,
                "💡 "
            )
        )

        return

    # PROFIL
    if value == text(
        user_id,
        "profile"
    ):

        user = users_db[user_id]

        name = user.get(
            "full_name",
            "Noma'lum"
        )

        grade = user.get(
            "grade",
            "Noma'lum"
        )

        phone = user.get(
            "phone",
            "Telefon yo‘q"
        )

        profile = (
            f"{text(user_id, 'profile_title')}"
            f"👤 <b>Ism:</b> {name}\n"
            f"🎓 <b>Sinf:</b> {grade}\n"
            f"📞 <b>Telefon:</b> {phone}"
        )

        await message.answer(
            profile,
            reply_markup=main_keyboard(
                user_id
            )
        )

        return

    # SARDORLAR
    if value == text(
        user_id,
        "sardors"
    ):

        result = "👥 <b>SARDORLAR</b>\n\n"

        for number, sardor in enumerate(
            SARDORS.values(),
            start=1
        ):

            result += (
                f"<b>{number}. "
                f"{sardor['name']}</b>\n"
                f"{sardor['description']}\n\n"
            )

        await message.answer(
            result,
            reply_markup=main_keyboard(
                user_id
            )
        )

        return

    # NEWS
    if value == text(
        user_id,
        "news"
    ):

        await message.answer(
            text(
                user_id,
                "news_empty"
            ),
            reply_markup=main_keyboard(
                user_id
            )
        )

        return

    # SETTINGS
    if value == text(
        user_id,
        "settings"
    ):

        settings = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text="✏️ Ismni o‘zgartirish"
                    )
                ],
                [
                    KeyboardButton(
                        text="🌐 Tilni o‘zgartirish"
                    )
                ],
                [
                    KeyboardButton(
                        text="🔄 Qayta ro‘yxatdan o‘tish"
                    )
                ],
                [
                    KeyboardButton(
                        text=text(
                            user_id,
                            "back"
                        )
                    )
                ]
            ],
            resize_keyboard=True
        )

        await message.answer(
            "⚙️ <b>Sozlamalar</b>",
            reply_markup=settings
        )

        return


# =========================================================
# COMPLAINT — SARDOR
# =========================================================

@router.message(
    MenuStates.complaint_sardor
)
async def complaint_sardor(
    message: Message,
    state: FSMContext
):

    user_id = message.from_user.id

    value = message.text or ""

    # ORQAGA
    if value == text(
        user_id,
        "back"
    ):

        await state.set_state(
            MenuStates.main_menu
        )

        await message.answer(
            text(
                user_id,
                "main_menu"
            ),
            reply_markup=main_keyboard(
                user_id
            )
        )

        return

    sardor_key = get_sardor(
        value
    )

    if sardor_key is None:

        await message.answer(
            "❗ Sardorlardan birini tanlang.",
            reply_markup=sardor_keyboard(
                user_id,
                "📝 "
            )
        )

        return

    # TANLANGAN SARDORNI SAQLAYMIZ
    await state.update_data(
        selected_sardor=sardor_key
    )

    # KEYINGI BOSQICH
    await state.set_state(
        MenuStates.complaint_text
    )

    selected = SARDORS[
        sardor_key
    ]["name"]

    await message.answer(
        f"✅ Tanlandi: <b>{selected}</b>\n\n"
        f"{text(user_id, 'write_complaint')}",
        reply_markup=back_keyboard(
            user_id
        )
    )


# =========================================================
# COMPLAINT — TEXT
# =========================================================

@router.message(
    MenuStates.complaint_text
)
async def complaint_text(
    message: Message,
    state: FSMContext
):

    user_id = message.from_user.id

    complaint = (
        message.text or ""
    ).strip()

    if complaint == text(
        user_id,
        "back"
    ):

        await state.set_state(
            MenuStates.complaint_sardor
        )

        await message.answer(
            text(
                user_id,
                "choose_complaint"
            ),
            reply_markup=sardor_keyboard(
                user_id,
                "📝 "
            )
        )

        return

    if not complaint:

        await message.answer(
            text(
                user_id,
                "write_complaint"
            )
        )

        return

    data = await state.get_data()

    sardor_key = data.get(
        "selected_sardor"
    )

    sardor = SARDORS.get(
        sardor_key
    )

    if not sardor:

        await message.answer(
            "❌ Sardor ma'lumoti topilmadi.",
            reply_markup=main_keyboard(
                user_id
            )
        )

        await state.set_state(
            MenuStates.main_menu
        )

        return

    user = users_db.get(
        user_id,
        {}
    )

    name = user.get(
        "full_name",
        "Noma'lum"
    )

    grade = user.get(
        "grade",
        "Noma'lum"
    )

    phone = user.get(
        "phone",
        "Telefon yo‘q"
    )

    username = message.from_user.username

    if username:
        username_text = "@" + username
    else:
        username_text = "Username yo‘q"

    admin_message = (
        "🚨 <b>YANGI SHIKOYAT</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"

        f"👤 <b>Ism:</b> {name}\n"
        f"🎓 <b>Sinf:</b> {grade}\n"
        f"📞 <b>Telefon:</b> {phone}\n"
        f"🔗 <b>Username:</b> {username_text}\n"
        f"🆔 <b>Telegram ID:</b> {user_id}\n\n"

        f"👥 <b>TANLANGAN SARDOR:</b>\n"
        f"{sardor['name']}\n\n"

        f"📝 <b>SHIKOYAT:</b>\n"
        f"{complaint}\n\n"

        "━━━━━━━━━━━━━━━━━━━━"
    )

    try:

        await message.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_message
        )

        await message.answer(
            text(
                user_id,
                "complaint_sent"
            ),
            reply_markup=main_keyboard(
                user_id
            )
        )

    except Exception as error:

        logging.exception(
            "Complaint error"
        )

        await message.answer(
            "❌ Xabar yuborishda xatolik.\n\n"
            f"<code>{error}</code>",
            reply_markup=main_keyboard(
                user_id
            )
        )

    await state.set_state(
        MenuStates.main_menu
    )


# =========================================================
# SUGGESTION — SARDOR
# =========================================================

@router.message(
    MenuStates.suggestion_sardor
)
async def suggestion_sardor(
    message: Message,
    state: FSMContext
):

    user_id = message.from_user.id

    value = message.text or ""

    if value == text(
        user_id,
        "back"
    ):

        await state.set_state(
            MenuStates.main_menu
        )

        await message.answer(
            text(
                user_id,
                "main_menu"
            ),
            reply_markup=main_keyboard(
                user_id
            )
        )

        return

    sardor_key = get_sardor(
        value
    )

    if sardor_key is None:

        await message.answer(
            "❗ Sardorlardan birini tanlang.",
            reply_markup=sardor_keyboard(
                user_id,
                "💡 "
            )
        )

        return

    await state.update_data(
        selected_sardor=sardor_key
    )

    await state.set_state(
        MenuStates.suggestion_text
    )

    selected = SARDORS[
        sardor_key
    ]["name"]

    await message.answer(
        f"✅ Tanlandi: <b>{selected}</b>\n\n"
        f"{text(user_id, 'write_suggestion')}",
        reply_markup=back_keyboard(
            user_id
        )
    )


# =========================================================
# SUGGESTION — TEXT
# =========================================================

@router.message(
    MenuStates.suggestion_text
)
async def suggestion_text(
    message: Message,
    state: FSMContext
):

    user_id = message.from_user.id

    suggestion = (
        message.text or ""
    ).strip()

    if suggestion == text(
        user_id,
        "back"
    ):

        await state.set_state(
            MenuStates.suggestion_sardor
        )

        await message.answer(
            text(
                user_id,
                "choose_suggestion"
            ),
            reply_markup=sardor_keyboard(
                user_id,
                "💡 "
            )
        )

        return

    if not suggestion:

        await message.answer(
            text(
                user_id,
                "write_suggestion"
            )
        )

        return

    data = await state.get_data()

    sardor_key = data.get(
        "selected_sardor"
    )

    sardor = SARDORS.get(
        sardor_key
    )

    if not sardor:

        await message.answer(
            "❌ Sardor ma'lumoti topilmadi.",
            reply_markup=main_keyboard(
                user_id
            )
        )

        await state.set_state(
            MenuStates.main_menu
        )

        return

    user = users_db.get(
        user_id,
        {}
    )

    name = user.get(
        "full_name",
        "Noma'lum"
    )

    grade = user.get(
        "grade",
        "Noma'lum"
    )

    phone = user.get(
        "phone",
        "Telefon yo‘q"
    )

    username = message.from_user.username

    if username:
        username_text = "@" + username
    else:
        username_text = "Username yo‘q"

    admin_message = (
        "💡 <b>YANGI TAKLIF</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"

        f"👤 <b>Ism:</b> {name}\n"
        f"🎓 <b>Sinf:</b> {grade}\n"
        f"📞 <b>Telefon:</b> {phone}\n"
        f"🔗 <b>Username:</b> {username_text}\n"
        f"🆔 <b>Telegram ID:</b> {user_id}\n\n"

        f"👥 <b>TANLANGAN SARDOR:</b>\n"
        f"{sardor['name']}\n\n"

        f"💡 <b>TAKLIF:</b>\n"
        f"{suggestion}\n\n"

        "━━━━━━━━━━━━━━━━━━━━"
    )

    try:

        await message.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_message
        )

        await message.answer(
            text(
                user_id,
                "suggestion_sent"
            ),
            reply_markup=main_keyboard(
                user_id
            )
        )

    except Exception as error:

        logging.exception(
            "Suggestion error"
        )

        await message.answer(
            "❌ Xabar yuborishda xatolik.\n\n"
            f"<code>{error}</code>",
            reply_markup=main_keyboard(
                user_id
            )
        )

    await state.set_state(
        MenuStates.main_menu
    )


# =========================================================
# EDIT NAME
# =========================================================

@router.message(
    F.text == "✏️ Ismni o‘zgartirish"
)
async def edit_name_start(
    message: Message,
    state: FSMContext
):

    user_id = message.from_user.id

    await state.set_state(
        MenuStates.edit_name
    )

    await message.answer(
        text(
            user_id,
            "edit_name"
        ),
        reply_markup=back_keyboard(
            user_id
        )
    )


@router.message(
    MenuStates.edit_name
)
async def edit_name(
    message: Message,
    state: FSMContext
):

    user_id = message.from_user.id

    value = (
        message.text or ""
    ).strip()

    if value == text(
        user_id,
        "back"
    ):

        await state.set_state(
            MenuStates.main_menu
        )

        await message.answer(
            text(
                user_id,
                "main_menu"
            ),
            reply_markup=main_keyboard(
                user_id
            )
        )

        return

    if len(value) < 3:

        await message.answer(
            text(
                user_id,
                "edit_name"
            )
        )

        return

    users_db[user_id][
        "full_name"
    ] = value

    await state.set_state(
        MenuStates.main_menu
    )

    await message.answer(
        text(
            user_id,
            "name_updated"
        ),
        reply_markup=main_keyboard(
            user_id
        )
    )


# =========================================================
# CHANGE LANGUAGE
# =========================================================

@router.message(
    F.text == "🌐 Tilni o‘zgartirish"
)
async def change_language(
    message: Message,
    state: FSMContext
):

    await state.set_state(
        RegStates.language
    )

    await message.answer(
        TEXTS["uz"]["language"],
        reply_markup=language_keyboard()
    )


# =========================================================
# RESET
# =========================================================

@router.message(
    F.text == "🔄 Qayta ro‘yxatdan o‘tish"
)
async def reset_start(
    message: Message,
    state: FSMContext
):

    user_id = message.from_user.id

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=text(
                        user_id,
                        "yes"
                    )
                ),
                KeyboardButton(
                    text=text(
                        user_id,
                        "no"
                    )
                )
            ]
        ],
        resize_keyboard=True
    )

    await message.answer(
        text(
            user_id,
            "reset"
        ),
        reply_markup=keyboard
    )


# =========================================================
# GENERAL
# =========================================================

@router.message()
async def general(
    message: Message,
    state: FSMContext
):

    user_id = message.from_user.id

    value = message.text or ""

    if value == text(
        user_id,
        "yes"
    ):

        users_db.pop(
            user_id,
            None
        )

        await state.clear()

        await state.set_state(
            RegStates.language
        )

        await message.answer(
            TEXTS["uz"]["language"],
            reply_markup=language_keyboard()
        )

        return

    if value == text(
        user_id,
        "no"
    ):

        await state.set_state(
            MenuStates.main_menu
        )

        await message.answer(
            text(
                user_id,
                "main_menu"
            ),
            reply_markup=main_keyboard(
                user_id
            )
        )

        return

    if value == text(
        user_id,
        "back"
    ):

        await state.set_state(
            MenuStates.main_menu
        )

        await message.answer(
            text(
                user_id,
                "main_menu"
            ),
            reply_markup=main_keyboard(
                user_id
            )
        )


# =========================================================
# MAIN
# =========================================================

async def main():

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    dp = Dispatcher()

    dp.include_router(
        router
    )

    await bot.delete_webhook(
        drop_pending_updates=True
    )

    print("================================")
    print("🤖 PopImVoice_bot ISHLADI")
    print(f"📩 ADMIN ID: {ADMIN_ID}")
    print("================================")

    try:

        await dp.start_polling(
            bot
        )

    finally:

        await bot.session.close()


if __name__ == "__main__":

    try:

        asyncio.run(
            main()
        )

    except KeyboardInterrupt:

        print("🛑 Bot to‘xtatildi.")

    except Exception as error:

        print("❌ XATO:")
        print(error)