import json
from typing import Dict, Union, List


def read_states() -> Dict[
    str,
    Dict[
        str,
        Union[
            Dict[
                int,
                List[str]
                ],
            int
            ]
        ]
    ]:
    with open('states/states.json', 'r', encoding='utf-8') as file:
        result: dict = json.load(file)
        result = dict(zip(map(int, result.keys()), result.values()))
    return result


def write_states(new_states: Dict[
    str,
    Dict[
        str,
        Union[
            Dict[
                int,
                List[str]
                ],
            int
            ]
        ]
    ]) -> None:
    with open('states/states.json', 'w', encoding='utf-8') as file:
        json.dump(new_states, file, indent=4, ensure_ascii=False)


def read_facts(category: str) -> List[str]:
    with open('database/facts.json', 'r', encoding='utf-8') as file:
        result: Dict[str, List[str]] = json.load(file)
    
    if category == 'stars':
        category = 'Звёзды'
    elif category == 'planets':
        category = 'Планеты'
    elif category == 'galaxies':
        category = 'Галактики'

    return result[category]
