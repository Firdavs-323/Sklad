import os
import polib

strings = {
    "Warehouse Management System": {"uz": "Omborxona Boshqaruvi Tizimi", "ru": "Система Управления Складом"},
    "Efficient inventory control and real-time monitoring": {"uz": "Inventarizatsiyani samarali nazorat qilish va real vaqtda monitoring", "ru": "Эффективный контроль запасов и мониторинг в реальном времени"},
    "Products": {"uz": "Mahsulotlar", "ru": "Товары"},
    "Manage your product inventory": {"uz": "Mahsulotlar zaxirasini boshqaring", "ru": "Управляйте запасами товаров"},
    "View Products": {"uz": "Mahsulotlarni ko'rish", "ru": "Посмотреть товары"},
    "Transactions": {"uz": "Tranzaksiyalar", "ru": "Транзакции"},
    "Track incoming and outgoing movements": {"uz": "Kirim va chiqim harakatlarini kuzatish", "ru": "Отслеживайте входящие и исходящие движения"},
    "View Transactions": {"uz": "Tranzaksiyalarni ko'rish", "ru": "Посмотреть транзакции"},
    "Reports": {"uz": "Hisobotlar", "ru": "Отчеты"},
    "Generate detailed analytics": {"uz": "Batafsil tahlillarni yaratish", "ru": "Генерация детальной аналитики"},
    "View Reports": {"uz": "Hisobotlarni ko'rish", "ru": "Посмотреть отчеты"},
    "Quick Actions": {"uz": "Tezkor amallar", "ru": "Быстрые действия"},
    "Add New Product": {"uz": "Yangi mahsulot qo'shish", "ru": "Добавить новый товар"},
    "Add Transaction": {"uz": "Tranzaksiya qo'shish", "ru": "Добавить транзакцию"},
    "Admin Panel": {"uz": "Admin paneli", "ru": "Панель администратора"},
    "System Status": {"uz": "Tizim holati", "ru": "Статус системы"},
    "Database": {"uz": "Ma'lumotlar bazasi", "ru": "База данных"},
    "Connected": {"uz": "Ulangan", "ru": "Подключено"},
    "API": {"uz": "API", "ru": "API"},
    "Active": {"uz": "Faol", "ru": "Активен"},
    "Telegram Bot": {"uz": "Telegram Bot", "ru": "Telegram Бот"},
    "Configuring": {"uz": "Sozlanmoqda", "ru": "Настраивается"},
    "Warehouse Management": {"uz": "Omborxona boshqaruvi", "ru": "Управление складом"},
    "Warehouse": {"uz": "Omborxona", "ru": "Склад"},
    "Categories": {"uz": "Kategoriyalar", "ru": "Категории"},
    "Welcome": {"uz": "Xush kelibsiz", "ru": "Добро пожаловать"},
    "Admin": {"uz": "Admin", "ru": "Админ"},
    "Login": {"uz": "Kirish", "ru": "Войти"},
    "Go": {"uz": "O'tish", "ru": "Перейти"},
    "Price": {"uz": "Narx", "ru": "Цена"},
    "Quantity": {"uz": "Miqdor", "ru": "Количество"},
    "Category": {"uz": "Kategoriya", "ru": "Категория"},
    "SKU": {"uz": "SKU", "ru": "Артикул"},
    "Barcode": {"uz": "Shtrix-kod", "ru": "Штрих-код"},
    "View Details": {"uz": "Tafsilotlarni ko'rish", "ru": "Посмотреть детали"},
    "No products found.": {"uz": "Mahsulotlar topilmadi.", "ru": "Товары не найдены."},
    "Add your first product": {"uz": "Birinchi mahsulotingizni qo'shing", "ru": "Добавьте ваш первый товар"},
    "Add New Category": {"uz": "Yangi kategoriya qo'shish", "ru": "Добавить новую категорию"},
    "Edit": {"uz": "Tahrirlash", "ru": "Изменить"},
    "No categories found.": {"uz": "Kategoriyalar topilmadi.", "ru": "Категории не найдены."},
    "Add your first category": {"uz": "Birinchi kategoriyangizni qo'shing", "ru": "Добавьте вашу первую категорию"},
    "Product Details": {"uz": "Mahsulot tafsilotlari", "ru": "Детали товара"},
    "Home": {"uz": "Bosh sahifa", "ru": "Главная"},
    "Product Information": {"uz": "Mahsulot haqida ma'lumot", "ru": "Информация о товаре"},
    "Name": {"uz": "Nomi", "ru": "Название"},
    "Recent Transactions": {"uz": "So'nggi tranzaksiyalar", "ru": "Последние транзакции"},
    "By": {"uz": "Tomonidan", "ru": "От"},
    "No transactions yet.": {"uz": "Hozircha tranzaksiyalar yo'q.", "ru": "Пока нет транзакций."},
    "Edit Product": {"uz": "Mahsulotni tahrirlash", "ru": "Изменить товар"},
    "Admin Dashboard": {"uz": "Admin Boshqaruvi", "ru": "Панель администратора"},
    "Dashboard": {"uz": "Boshqaruv", "ru": "Панель"},
    "Daily Income": {"uz": "Kunlik Daromad", "ru": "Дневной доход"},
    "Monthly Income": {"uz": "Oylik Daromad", "ru": "Месячный доход"},
    "Yearly Income": {"uz": "Yillik Daromad", "ru": "Годовой доход"},
    "Expenses": {"uz": "Xarajatlar", "ru": "Расходы"},
    "Logout": {"uz": "Chiqish", "ru": "Выйти"},
    "Register": {"uz": "Ro'yxatdan o'tish", "ru": "Регистрация"},
    "Login to Sklad": {"uz": "Sklad-ga kirish", "ru": "Войти в Склад"},
    "Username": {"uz": "Foydalanuvchi nomi", "ru": "Имя пользователя"},
    "Password": {"uz": "Parol", "ru": "Пароль"},
    "Admin Secret Code (Optional)": {"uz": "Admin maxfiy kodi (ixtiyoriy)", "ru": "Секретный код админа (необязательно)"},
    "Don't have an account?": {"uz": "Akkauntingiz yo'qmi?", "ru": "Нет аккаунта?"},
    "Register here": {"uz": "Shu yerda ro'yxatdan o'ting", "ru": "Зарегистрируйтесь здесь"},
    "Register as Seller": {"uz": "Sotuvchi sifatida ro'yxatdan o'tish", "ru": "Зарегистрироваться как продавец"},
    "Already have an account?": {"uz": "Allaqachon akkauntingiz bormi?", "ru": "Уже есть аккаунт?"},
    "Login here": {"uz": "Shu yerda kiring", "ru": "Войдите здесь"},
    "Daily Sales (Income)": {"uz": "Kunlik Sotuvlar (Daromad)", "ru": "Дневные продажи (Доход)"},
    "Monthly Sales (Income)": {"uz": "Oylik Sotuvlar (Daromad)", "ru": "Месячные продажи (Доход)"},
    "Yearly Sales (Income)": {"uz": "Yillik Sotuvlar (Daromad)", "ru": "Годовые продажи (Доход)"},
    "Seller Dashboard": {"uz": "Sotuvchi Boshqaruvi", "ru": "Панель продавца"},
    "Add Category": {"uz": "Kategoriya qo'shish", "ru": "Добавить категорию"},
    "Add Product": {"uz": "Mahsulot qo'shish", "ru": "Добавить товар"},
}

base_dir = r"c:\Users\Acer\Desktop\Sklad\locale"

for lang in ["uz", "ru"]:
    lc_dir = os.path.join(base_dir, lang, "LC_MESSAGES")
    os.makedirs(lc_dir, exist_ok=True)
    
    po = polib.POFile()
    po.metadata = {
        'Project-Id-Version': '1.0',
        'Report-Msgid-Bugs-To': 'you@example.com',
        'POT-Creation-Date': '2026-04-23 12:00+0500',
        'PO-Revision-Date': '2026-04-23 12:00+0500',
        'Last-Translator': 'you <you@example.com>',
        'Language-Team': lang,
        'MIME-Version': '1.0',
        'Content-Type': 'text/plain; charset=utf-8',
        'Content-Transfer-Encoding': '8bit',
    }
    
    for en_text, translations in strings.items():
        entry = polib.POEntry(
            msgid=en_text,
            msgstr=translations.get(lang, en_text)
        )
        po.append(entry)
    
    po_path = os.path.join(lc_dir, "django.po")
    mo_path = os.path.join(lc_dir, "django.mo")
    po.save(po_path)
    po.save_as_mofile(mo_path)

print("Translations successfully generated and compiled!")
