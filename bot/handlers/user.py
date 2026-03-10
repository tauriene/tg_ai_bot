import asyncio

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
import time

from bot.keyboards import main_kb, get_ai_models_kb
from bot.db import (
    add_user,
    get_requests_count,
    add_request,
    MAX_REQUESTS_PER_DAY,
    set_user_ai_model,
    get_user_ai_model,
)
from bot.utils import generate_text, send_answer_parts

REQUEST_COOLDOWN = 5
router = Router()


@router.message(CommandStart())
async def cmd_start(msg: Message):
    await add_user(tg_id=msg.from_user.id)
    await msg.answer(
        "Привет! 🤖\nЯ бот с искуственным интеллектом — могу помочь с учёбой, разработкой, текстами, идеями и любыми вопросами.\n\n"
        "Как пользоваться ботом?\n\n"
        "📝ЗАПРОС: просто напишите вопрос в чат\n"
        "⭐️МОДЕЛИ: отправьте команду /model\n"
        "👤АККАУНТ: отправьте команду /account",
        reply_markup=main_kb,
    )


@router.message(F.text == "Аккаунт")
@router.message(Command("account"))
async def cmd_account(msg: Message):
    user_req_count = await get_requests_count(
        tg_id=msg.from_user.id,
    )
    selected_ai_model = await get_user_ai_model(tg_id=msg.from_user.id)
    await msg.answer(
        f"👤 Подписка: стандартная\nМодель: {selected_ai_model.name} /model\n\n📊 Статистика использования\n"
        f"Осталось запросов на сегодня: {MAX_REQUESTS_PER_DAY - user_req_count}/5\n"
    )


@router.message(F.text == "Модель")
@router.message(Command("model"))
async def cmd_model(msg: Message):
    selected_ai_model = await get_user_ai_model(tg_id=msg.from_user.id)
    await msg.answer(
        f"⭐️ У вас выбрана модель: {selected_ai_model.name}.\n\n",
        reply_markup=await get_ai_models_kb(selected_ai_model.name),
    )


@router.callback_query(F.data.startswith("model_"))
async def cb_model(cb_q: CallbackQuery):
    _, ai_model_id, ai_model_name = cb_q.data.split("_")
    if cb_q.message.text != f"⭐️ Вы выбрали модель: {ai_model_name}":
        await set_user_ai_model(tg_id=cb_q.from_user.id, ai_model_id=int(ai_model_id))
        await cb_q.message.edit_text(
            f"⭐️ Вы выбрали модель: {ai_model_name}",
            reply_markup=await get_ai_models_kb(ai_model_name),
        )
    await cb_q.answer()


active_users: set[int] = set()
last_request_time: dict[int, float] = {}


async def handle_ai_request(msg: Message):
    user_id = msg.from_user.id
    status_msg = await msg.answer("🤔 Думаю...")
    try:
        user_ai_model = await get_user_ai_model(tg_id=user_id)
        response = await generate_text(req=msg.text, user_ai_model=user_ai_model.name)

        if response["ok"]:
            await add_request(tg_id=user_id)
            await send_answer_parts(msg, response["text"])

            user_req_count = await get_requests_count(tg_id=user_id)
            await msg.answer(
                f"Ваш ответ. Осталось текстовых запросов на сегодня: "
                f"{MAX_REQUESTS_PER_DAY - user_req_count}/5."
            )

            last_request_time[user_id] = time.time()

        else:
            await msg.answer("😬 Произошла ошибка! Попробуйте позже.")

    finally:
        active_users.discard(user_id)
        await status_msg.delete()


@router.message(F.text)
async def process_request(msg: Message):
    user_id = msg.from_user.id
    now = time.time()

    if user_id in active_users:
        await msg.answer("⏳ Подождите, предыдущий запрос ещё выполняется.")
        return

    last_time = last_request_time.get(user_id, 0)
    if now - last_time < REQUEST_COOLDOWN:
        await msg.answer(
            f"⏱️ Подождите {int(REQUEST_COOLDOWN - (now - last_time))} секунд перед следующим запросом."
        )
        return

    user_req_count = await get_requests_count(tg_id=user_id)
    if user_req_count >= MAX_REQUESTS_PER_DAY:
        await msg.answer(
            "🙁 У вас осталось 0/5 текстовых запросов на сегодня. Попробуйте завтра."
        )
        return

    active_users.add(user_id)
    asyncio.create_task(handle_ai_request(msg))
