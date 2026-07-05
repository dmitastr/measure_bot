import asyncio
import logging
import os
import random
from aiogram import Bot, Dispatcher
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(
    parse_mode=ParseMode.HTML))
dp = Dispatcher()


def get_random_measurement(choices: list[dict], min_value: int, max_value: int) -> str:
    value = random.randint(min_value, max_value)
    logger.info(f"DEBUG: min={min_value}, max={max_value}, value={value}")

    for choice in choices[::-1]:
        if value >= choice.get("value", 0):
            text = choice.get("text", "").format(value=value)
            return text

    return choices[0].get("text", "").format(value=value)


MEASURE_OPTIONS = [
    {
        "id": "1",
        "title": "Винрейт",
        "description": "Узнай свой винрейт в играх!",
        "choices": [
            {"value": 0, "text": "🎮 <b>Винрейт</b>\n\n✅ Ваш винрейт: {value}%. Надо поднажать!"},
            {"value": 50, "text": "🎮 <b>Винрейт</b>\n\n✅ Вы выиграли {value}% игр!"},
            {"value": 90, "text": "🎮 <b>Винрейт</b>\n\n✅ У вас {value}% побед!"},
        ],
        "min_value": 0,
        "max_value": 100,
    },
]


@dp.inline_query()
async def inline_measure_handler(inline_query: InlineQuery):
    """
    Показываем все варианты измерений в инлайн-режиме.
    Текст с подтверждением сразу зашит в сообщение — никакой задержки не нужно.
    """
    results = []

    for measure in MEASURE_OPTIONS:
        results.append(
            InlineQueryResultArticle(
                id=measure["id"],
                title=measure["title"],
                description=measure["description"],
                input_message_content=InputTextMessageContent(
                    message_text=get_random_measurement(
                        choices=measure.get("choices", []),
                        min_value=measure.get("min_value", 0),
                        max_value=measure.get("max_value", 100)
                    ),
                    parse_mode=ParseMode.HTML,
                ),
            )
        )

    await inline_query.answer(results,  is_personal=True)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
