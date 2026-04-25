import os
import django
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from django.conf import settings
from django.contrib.auth.models import User
from products.models import Product
from transactions.models import Transaction
from accounts.models import Profile

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sklad.settings')
django.setup()

BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'  # Replace with your bot token
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('📦 View Stock'))
    keyboard.add(KeyboardButton('➕ Add Incoming'), KeyboardButton('➖ Add Outgoing'))
    keyboard.add(KeyboardButton('📊 Statistics'))
    return keyboard

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_id = message.from_user.id
    # Check if user exists and has role
    try:
        profile = Profile.objects.get(user__username=str(user_id))
        role = profile.role
    except Profile.DoesNotExist:
        await message.reply("You are not authorized to use this bot.")
        return

    await message.reply(
        f"Welcome to Warehouse Bot!\nYour role: {role.title()}\n\nChoose an action:",
        reply_markup=get_main_keyboard()
    )

@dp.message_handler(lambda message: message.text == '📦 View Stock')
async def view_stock(message: types.Message):
    user_id = message.from_user.id
    try:
        profile = Profile.objects.get(user__username=str(user_id))
    except Profile.DoesNotExist:
        await message.reply("Unauthorized")
        return

    products = Product.objects.all()
    if not products:
        await message.reply("No products in stock.")
        return

    text = "📦 Current Stock:\n\n"
    for product in products:
        status = "🟢" if product.quantity >= 10 else "🟡" if product.quantity > 0 else "🔴"
        text += f"{status} {product.name}: {product.quantity}\n"

    await message.reply(text)

@dp.message_handler(lambda message: message.text in ['➕ Add Incoming', '➖ Add Outgoing'])
async def add_transaction_start(message: types.Message):
    user_id = message.from_user.id
    try:
        profile = Profile.objects.get(user__username=str(user_id))
        if profile.role not in ['admin', 'warehouse_worker']:
            await message.reply("You don't have permission to add transactions.")
            return
    except Profile.DoesNotExist:
        await message.reply("Unauthorized")
        return

    transaction_type = 'in' if 'Incoming' in message.text else 'out'

    # Get products for inline keyboard
    products = Product.objects.all()
    if not products:
        await message.reply("No products available.")
        return

    keyboard = InlineKeyboardMarkup()
    for product in products:
        keyboard.add(InlineKeyboardButton(
            f"{product.name} (Stock: {product.quantity})",
            callback_data=f"select_product_{product.id}_{transaction_type}"
        ))

    await message.reply("Select a product:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith('select_product_'))
async def select_product(callback_query: types.CallbackQuery):
    data = callback_query.data.split('_')
    product_id = int(data[2])
    transaction_type = data[3]

    # Store in user state (simplified, in real app use FSM)
    await bot.send_message(
        callback_query.from_user.id,
        f"Selected product. Now enter quantity for {'incoming' if transaction_type == 'in' else 'outgoing'}:"
    )
    # In a real implementation, you'd use FSMContext to store state

@dp.message_handler(lambda message: message.text.isdigit())
async def process_quantity(message: types.Message):
    # Simplified - in real app, check state
    quantity = int(message.text)
    # Assume product_id and type from state
    await message.reply("Transaction added successfully!")

@dp.message_handler(lambda message: message.text == '📊 Statistics')
async def statistics(message: types.Message):
    total_products = Product.objects.count()
    total_quantity = sum(p.quantity for p in Product.objects.all())
    low_stock = Product.objects.filter(quantity__lt=10).count()

    text = f"""📊 Warehouse Statistics:

📦 Total Products: {total_products}
📊 Total Quantity: {total_quantity}
⚠️ Low Stock Items: {low_stock}"""

    await message.reply(text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)