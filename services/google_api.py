from googleapiclient.discovery import build

# Кортеж с сайтами, на которых нужно искать
SITES = (
    'https://iki.cosmos.ru',
    'https://www.nasa.gov',
    'https://www.esa.int',
    'https://www.roscosmos.ru',
    'https://www.cfa.harvard.edu',
    'https://www.caltech.edu',
    'https://www.mit.edu',
    'https://hubblesite.org',
    'http://www.sai.msu.ru/',
    'https://mipt.ru/',
    'http://www.ras.ru/'
)

def google_search(search_term,
                  api_key='AIzaSyCSDwE2P62j8o0VjhgtkSKQGNPCCeWuPMw',
                  cse_id='e36e6be4605a54665',
                  num_results=100,
                  sites=SITES,
                  **kwargs):
    # Создаем сервис для работы с API
    service = build("customsearch", "v1", developerKey=api_key)
    
    # Формируем фильтр по сайтам
    site_filter = " OR ".join(f'site:{site}' for site in sites)
    full_query = f'{search_term} ({site_filter})'

    # Словарь для хранения результатов {ссылка: заголовок}
    final_results = {}
    
    # Пагинация: Google API возвращает по 10 результатов за запрос
    start = 1
    while len(final_results) < num_results:
        try:
            # Выполняем поисковый запрос
            res = service.cse().list(
                q=full_query,  # Поисковый запрос
                cx=cse_id,     # Идентификатор поисковой системы
                num=10,        # Количество результатов за запрос (максимум 10)
                start=start,   # Начальная позиция
                **kwargs       # Дополнительные параметры
            ).execute()

            # Добавляем результаты в словарь
            for item in res.get('items', []):
                link = item.get('link')
                title = item.get('title')
                if link and title:
                    final_results[link] = title

            # Проверяем, есть ли ещё результаты
            if 'nextPage' not in res.get('queries', {}):
                break  # Если следующей страницы нет, выходим из цикла

            # Увеличиваем start для следующей страницы
            start += 10

        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")
            break

    return final_results
