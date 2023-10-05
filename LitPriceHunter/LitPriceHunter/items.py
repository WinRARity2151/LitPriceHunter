import scrapy

class LitpricehunterItem(scrapy.Item):
    # Поле для хранения заголовка книги
    title = scrapy.Field()
    # Поле для хранения имени автора книги
    author = scrapy.Field()
    # Поле для хранения информации о цене книги
    price = scrapy.Field()
    # Поле для хранения ссылки на книгу
    link = scrapy.Field()
