# Импортируем необходимые модули Scrapy и элемент (item) LitpricehunterItem
import scrapy
from ..items import LitpricehunterItem

# Создаем класс LphCgSpider, представляющий веб-паука
class LphCgSpider(scrapy.Spider):
    name = "LPH_cg"  # Уникальное имя паука
    allowed_domains = ["www.chitai-gorod.ru"]  # Домен, на котором будет выполняться сканирование
    start_urls = ["https://www.chitai-gorod.ru/catalog/books/klassicheskaya-proza-110003?page=1"]  # Стартовая URL-адрес

    def parse(self, response):
        allowed_pages = 3  # Максимальное количество страниц для сканирования
        items = LitpricehunterItem()  # Создаем экземпляр элемента LitpricehunterItem для хранения данных о книгах

        # Итерируемся по каждой книге на текущей странице
        for book in response.css('div .products-list article'):
            items['title'] = book.css('::attr(data-chg-product-name)').get()  # Извлекаем название книги
            items['author'] = book.css('div.product-title__author::text').get().strip()  # Извлекаем автора книги
            items['price'] = book.css('::attr(data-chg-product-price)').get()  # Извлекаем цену книги
            items['link'] = book.css('a::attr(href)').get()  # Извлекаем ссылку на книгу

            yield items  # Возвращаем элемент items, чтобы он был сохранен в результате сканирования

        current_page = int(response.url.split('=')[-1])  # Извлекаем текущий номер страницы

        # Проверяем, не достигли ли максимального разрешенного числа страниц
        if current_page <= allowed_pages:
            next_page = f'https://www.chitai-gorod.ru/catalog/books/klassicheskaya-proza-110003?page={current_page + 1}'
            # Переходим на следующую страницу и передаем управление обратно в функцию parse
            yield response.follow(next_page, callback=self.parse)
