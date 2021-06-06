from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import globals


def main_menu(update, context):
    buttons = [
        [
            KeyboardButton(text=globals.btn_fast_food), KeyboardButton(text=globals.btn_card),
        ],
        [
            KeyboardButton(text=globals.btn_order)
        ]
    ]
    update.message.reply_text(
        text="Menu",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )


def fast_food(update, context, categories):
    buttons = []
    row = []
    count = 0
    for category in categories:
        row.append(
            InlineKeyboardButton(
                text=f"{category['title']}",
                callback_data=f"category_{category['id']}"
            )
        )
        count += 1
        if count == 2:
            buttons.append(row)
            row = []
            count = 0
    if len(categories) % 2 == 1:
        buttons.append(row)

    update.message.reply_text(
        text="Kategoriyalarni tanglang!",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


def back_to_fast_food(update, context, categories, chat_id, message_id):
    buttons = []
    row = []
    count = 0
    for category in categories:
        row.append(
            InlineKeyboardButton(
                text=f"{category['title']}",
                callback_data=f"category_{category['id']}"
            )
        )
        count += 1
        if count == 2:
            buttons.append(row)
            row = []
            count = 0
    if len(categories) % 2 == 1:
        buttons.append(row)

    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text="Kategoriyalarni tanglang!",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


def category_products(update, context, products, chat_id, message_id):
    buttons = []
    row = []
    count = 0
    for product in products:
        row.append(
            InlineKeyboardButton(
                text=f"{product['title']}",
                callback_data=f"category_product_{product['id']}"
            )
        )
        count += 1
        if count == 2:
            buttons.append(row)
            row = []
            count = 0
    if len(products) % 2 == 1:
        buttons.append(row)

    buttons.append(
        [
            InlineKeyboardButton(
                text="Orqaga",
                callback_data="category_back"
            )
        ]
    )

    context.bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text="Mahsulotlarni tanglang!",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


def send_product(update, context, product, chat_id, message_id):
    caption = f"<b>{product['title']}</b>\nNarxi: {product['price']}\n{product['description']}"
    buttons = [
        [
            InlineKeyboardButton(
                text="Savatchaga qo'shish",
                callback_data=f"category_product_card_{product['id']}"
            )
        ],
        [
            InlineKeyboardButton(
                text="Orqaga",
                callback_data=f"category_product_back_{product['category_id']}"
            )
        ]
    ]
    context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    context.bot.send_photo(
        chat_id=chat_id,
        photo=open(f"{product['image']}", "rb"),
        caption=caption,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="HTML"
    )


def back_to_category_products(update, context, products, chat_id, message_id):
    buttons = []
    row = []
    count = 0
    for product in products:
        row.append(
            InlineKeyboardButton(
                text=f"{product['title']}",
                callback_data=f"category_product_{product['id']}"
            )
        )
        count += 1
        if count == 2:
            buttons.append(row)
            row = []
            count = 0
    if len(products) % 2 == 1:
        buttons.append(row)

    buttons.append(
        [
            InlineKeyboardButton(
                text="Orqaga",
                callback_data="category_back"
            )
        ]
    )

    context.bot.send_message(
        chat_id=chat_id,
        text="Mahsulotlarni tanglang!",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


def product_amount(update, context, chat_id, message_id, product_id, count=1):
    buttons = [
        [
            InlineKeyboardButton(
                text="-",
                callback_data=f"category_product_card_{product_id}_minus_{count}"
            ),
            InlineKeyboardButton(
                text=f"{count}",
                callback_data=f"category_product_card_{product_id}_count"
            ),
            InlineKeyboardButton(
                text="+",
                callback_data=f"category_product_card_{product_id}_plus_{count}"
            )
        ],
        [
            InlineKeyboardButton(
                text="Tasdiqlash",
                callback_data=f"category_product_card_{product_id}_submit_{count}"
            )
        ],
        [
            InlineKeyboardButton(
                text="Orqaga",
                callback_data=f"category_product_card_{product_id}_back"
            )
        ]
    ]
    context.bot.edit_message_reply_markup(
        chat_id=chat_id,
        message_id=message_id,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


def submit_product(update, context, user, chat_id, product_id, message_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="Orqaga",
                callback_data=f"category_product_card_{product_id}_back"
            )
        ]
    ]
    context.bot.edit_message_caption(
        chat_id=chat_id,
        message_id=message_id,
        caption="Text",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    context.bot.send_message(
        chat_id=chat_id,
        text="Savatchaga qoshildi!"
    )


def my_card(update, context, products, chat_id):
    if products:
        text = "Savatchada\n\n"
        total_price = 0
        for product in products:
            price = int(product['product_price'].split(" ")[0])
            total_price += product['amount'] * price
            text += f"{product['product_title']} = {product['amount']} x {product['product_price']} = {price * product['amount']} so'm\n"
        text += f"\nUmumiy narx: {total_price} so'm"
        buttons = [
            [
                InlineKeyboardButton(
                    text="Savatchani bo'shatish",
                    callback_data="card_clear"
                ),
                InlineKeyboardButton(
                    text="Buyurtma berish",
                    callback_data="card_order"
                )
            ]
        ]
        context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text="Savatcha bo'sh"
        )


def send_order(update, context, chat_id):
    buttons = [
        [
            InlineKeyboardButton("Buyurtma tarixi", callback_data=f"card_order_history"),
            InlineKeyboardButton("Yetkazib berish", callback_data=f"card_order_active")
        ]
    ]
    context.bot.send_message(
        chat_id=chat_id, text="Quyidagilardan birini tanlang",
        reply_markup=InlineKeyboardMarkup(buttons))
