import urllib.parse
from playwright.sync_api import TimeoutError

def test_fm18_search(page):
    """Тест проверяет базовый поиск, открытие товара и добавление в корзину на fm18"""
    
    test_timeout = 6000
    
    page.route("**/{metrika,analytics,google,yandex,doubleclick}**", lambda route: route.abort())
    
    page.set_default_navigation_timeout(test_timeout)
    
    # Открываем главную страницу fm18
    try:
        page.goto("https://fm18.ru/")
    except TimeoutError:
        page.evaluate("window.stop()")
    
    # Проверяем, что заголовок вкладки (Title) содержит слово "fm18"
    assert "Фабрика" in page.title(), f"Ожидали заголовок Фабрика, но получили {page.title()}"
    
    # Находим строку поиска по её имени (атрибуту name="search")
    search_box = page.locator("input[name='search']")
    
    # Вводим поисковый запрос и кликаем по товару
    search_box.fill("стул")
    
    try:
        page.locator(".button-search").click(timeout=test_timeout)
        # Ожидаем, пока страница загрузит результаты поиска
        page.wait_for_load_state("networkidle")
    except TimeoutError:
        page.evaluate("window.stop()")    
    
    decoded_url = urllib.parse.unquote(page.url)
    
    # Проверяем, что в адресе страницы (URL) появилось наше поисковое слово
    assert "стул" in decoded_url, f"Слово 'стул' не найдено в URL: {page.url}"
    
    first_product = page.locator(".product-list a").first
    
    try:
        first_product.click(timeout=test_timeout)
        # Ожидаем загрузки страницы самого товара
        page.wait_for_load_state("networkidle")
    except TimeoutError:
        page.evaluate("window.stop()")      
    
    buy_button = page.locator('.printPrice .cart input[type="button"]').first
    buy_button.click() 

    page.wait_for_timeout(test_timeout / 3)
    
    # Переходим в саму корзину
    basket_icon = page.locator("#cart a").first
    
    try:
        basket_icon.click()    
        page.wait_for_load_state("networkidle")
    except TimeoutError:
        page.evaluate("window.stop()")      
    
    assert "simplecheckout" in page.url, "Не удалось перейти на страницу корзины"
    
    assert (
        page.locator(".product-line").is_visible()
    ), "Корзина пуста, товар не добавился!"    