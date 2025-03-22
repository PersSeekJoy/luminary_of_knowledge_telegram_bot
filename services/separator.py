from math import ceil
from typing import Dict, List

def separator(search_result: Dict[str, str]) -> Dict[int, List[Dict[str, str]]]:
    result_dict: Dict[int, List[Dict[str, str]]] = {}
    pages_number = ceil(len(search_result) / 10)
    
    # Создаем страницы
    for page in range(1, pages_number + 1):
        result_dict[page] = []
    
    # Заполняем страницы
    for idx, (link, title) in enumerate(search_result.items()):
        page_number = (idx // 10) + 1
        result_dict[page_number].append({link: title})
    
    return result_dict
