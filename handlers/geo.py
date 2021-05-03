from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType


class GeoTag(StatesGroup):
    waiting_for_geo = State()
    # waiting_for_description = State()


async def geo_start(message: types.Message):
    await message.answer('Отправьте геометку')
    await GeoTag.waiting_for_geo.set()


async def geo_sent(message: types.Message, state: FSMContext):
    if not message.location:
        await message.answer("Это не геометка, отправьте снова")
        return
    answer = await message.answer(text="%s, %s" % (message.location.latitude, message.location.longitude))
    # await state.update_data(location=message.location)
    poll = await answer.reply_poll(question="%s, %s" % (message.location.latitude, message.location.longitude),
                              options=["+", "-"])
    await state.finish()


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


def register_handlers_geo(dp: Dispatcher):
    dp.register_message_handler(geo_start, commands="geo", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(geo_sent, state=GeoTag.waiting_for_geo)
    dp.register_message_handler(geo_sent, content_types=ContentType.LOCATION, state="*")
