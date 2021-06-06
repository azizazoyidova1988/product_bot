import sqlite3


class Database:
    def __init__(self, database):
        self.conn = sqlite3.connect(database, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS user(
                id INTEGER PRIMARY KEY AUTOINCREMENT, chat_id INTEGER NOT NULL,
                first_name TEXT NULL, last_name TEXT NULL,
                contact TEXT NULL, created_at DATETIME
            )
            """
        )
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS category(
                id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, 
                created_at DATETIME
            )
            """
        )
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS product(
                id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL,
                description TEXT NOT NULL, price TEXT NULL, image TEXT NULL, 
                category_id INTEGER NULL, created_at DATETIME,
                FOREIGN KEY (category_id) REFERENCES category (id) ON DELETE SET NULL
            )
            """
        )
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS user_card(
                id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NULL,
                product_id INTEGER NULL, amount INTEGER NOT NULL, 
                status INTEGER NOT NULL, created_at DATETIME,
                FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE SET NULL,
                FOREIGN KEY (product_id) REFERENCES product (id) ON DELETE SET NULL
            )
            """
        )
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS user_order(
                id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NULL,
                products TEXT NOT NULL, created_at DATETIME,
                FOREIGN KEY (user_id) REFERENCES user (id) ON DELETE SET NULL
            )
            """
        )
        self.conn.commit()

    def create_user(self, chat_id, first_name, last_name, created_at):
        self.cur.execute(
            """INSERT INTO user(chat_id, first_name, last_name, created_at) VALUES (?, ?, ?, ?)""",
            (chat_id, first_name, last_name, created_at)
        )
        self.conn.commit()

    def get_user_by_chat_id(self, chat_id):
        self.cur.execute(
            """SELECT * FROM user WHERE chat_id = ?""",
            (chat_id, )
        )
        user = dict_fetchone(self.cur)
        return user

    def update_user(self, state, chat_id, data):
        if state == 1:
            self.cur.execute(
                """UPDATE user SET first_name = ? WHERE chat_id = ?""",
                (data, chat_id)
            )

        elif state == 2:
            self.cur.execute(
                """UPDATE user SET last_name = ? WHERE chat_id = ?""",
                (data, chat_id)
            )

        elif state == 3:
            self.cur.execute(
                """UPDATE user SET contact = ? WHERE chat_id = ?""",
                (data, chat_id)
            )
        self.conn.commit()

    def get_all_categories(self):
        self.cur.execute(
            """SELECT * FROM category"""
        )
        categories = dict_fetchall(self.cur)
        return categories

    def get_category_by_id(self, category_id):
        self.cur.execute(
            """SELECT * FROM category WHERE id = ?""",
            (category_id, )
        )
        category = dict_fetchone(self.cur)
        return category

    def get_all_products_by_category(self, category_id):
        self.cur.execute(
            """SELECT * FROM product WHERE category_id = ?""",
            (category_id, )
        )
        products = dict_fetchall(self.cur)
        return products

    def get_product_by_id(self, product_id):
        self.cur.execute(
            """SELECT * FROM product WHERE id = ?""",
            (product_id, )
        )
        product = dict_fetchone(self.cur)
        return product

    def add_to_cart(self, user_id, product_id, amount, status, created_at):
        self.cur.execute(
            """INSERT INTO user_card(user_id, product_id, amount, status, created_at) VALUES (?, ?, ?, ?, ?)""",
            (user_id, product_id, amount, status, created_at)
        )
        self.conn.commit()

    def get_products_in_card(self, user_id):
        self.cur.execute(
            """select product.title as product_title, product.price as product_price, user_card.* from user_card 
            inner join product on user_card.product_id = product.id
            where user_id = ? and status = 1;""",
            (user_id, )
        )
        products = dict_fetchall(self.cur)
        return products

    def get_card_by_id(self, card_id):
        self.cur.execute("""select product.title as product_title, product.price as product_price, user_card.* from user_card 
            inner join product on user_card.product_id = product.id
            where user_card.id = ? and status = 2;""", (card_id, ))
        card = dict_fetchone(self.cur)
        return card


    def change_card_status(self, user_id, status):
        self.cur.execute(
            """UPDATE user_card SET status = ? WHERE user_id = ? AND status = 1""",
            (status, user_id)
        )
        self.conn.commit()

    def add_order(self, user_id, products, created_at):
        self.cur.execute(
            """INSERT INTO user_order(user_id, products, created_at) VALUES (?, ?, ?)""",
            (user_id, products, created_at)
        )
        self.conn.commit()

    def get_orders(self, user_id,status):
        self.cur.execute("""
            SELECT * FROM user_order WHERE user_id=? AND status = ?
        """, (user_id, status))

        orders = dict_fetchall(self.cur)
        return orders

    def change_status(self, order_id):
        self.cur.execute("""
            UPDATE user_order SET status = ? WHERE user_order.id =? 
        """, (2, order_id))
        self.conn.commit()


def dict_fetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def dict_fetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return False
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))
