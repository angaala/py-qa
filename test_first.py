import urllib.parse

def test_fm18_search(page):
    """Тест проверяет базовый поиск в fm18"""
    
    # 1. Открываем главную страницу fm18
    page.goto("https://fm18.ru/")
    
    # 2. Проверяем, что заголовок вкладки (Title) содержит слово "fm18"
    assert "Фабрика" in page.title(), f"Ожидали заголовок Фабрика, но получили {page.title()}"
    
    # 3. Находим строку поиска по её имени (атрибуту name="q")
    search_box = page.locator("input[name='search']")
    
    # 4. Вводим поисковый запрос и нажимаем клавишу Enter
    search_box.fill("стул")
    page.locator(".button-search").click()
    
    # 5. Ожидаем, пока страница загрузит результаты поиска
    page.wait_for_load_state("networkidle")
    
    decoded_url = urllib.parse.unquote(page.url)
    
    # 6. Проверяем, что в адресе страницы (URL) появилось наше поисковое слово
    assert "стул" in decoded_url, f"Слово 'стул' не найдено в URL: {page.url}"