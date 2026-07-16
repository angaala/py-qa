def test_google_search(page):
    """Тест проверяет базовый поиск в Google"""
    
    # 1. Открываем главную страницу Google
    page.goto("https://google.com")
    
    # 2. Проверяем, что заголовок вкладки (Title) содержит слово "Google"
    assert "Google" in page.title(), f"Ожидали заголовок Google, но получили {page.title()}"
    
    # 3. Находим строку поиска по её имени (атрибуту name="q")
    search_box = page.locator("textarea[name='q']")
    
    # 4. Вводим поисковый запрос и нажимаем клавишу Enter
    search_box.fill("pytest")
    search_box.press("Enter")
    
    # 5. Ожидаем, пока страница загрузит результаты поиска
    page.wait_for_load_state("networkidle")
    
    # 6. Проверяем, что в адресе страницы (URL) появилось наше поисковое слово
    assert "pytest" in page.url, f"Слово 'pytest' не найдено в URL: {page.url}"