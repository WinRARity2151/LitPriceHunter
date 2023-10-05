# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2

class LitpricehunterPipeline:
    def open_spider(self, spider):
        # Установите соединение с базой данных PostgreSQL
        self.conn = psycopg2.connect(
            database="",  # Замените на имя вашей базы данных
            user="",          # Замените на имя пользователя базы данных
            password="",  # Замените на пароль пользователя базы данных
            host="",          # Замените на хост базы данных (обычно "localhost")
            port="",         # Замените на порт базы данных (обычно 5432)
            client_encoding="UTF-8"
        )
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        # Закрываем соединение с базой данных PostgreSQL и сохраните изменения
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        # Вставляем данные в таблицу "books" в базе данных PostgreSQL

        # Запрос на вставку данных в таблицу "books" с использованием параметров
        insert_query = """
            INSERT INTO books (title, author, price, link)
            VALUES (%s, %s, %s, %s)
        """

        # Выполняем запрос на вставку данных, передавая значения из элемента item
        self.cursor.execute(insert_query, (item['title'], item['author'], item['price'], item['link']))

        # Возвращаем элемент item, чтобы он мог быть обработан дальше
        return item

