from pathlib import Path
from typing import Any


class Config:
    __isinstance = None
    _dictionary = {}

    def __new__(cls):
        if cls.__isinstance is None:
            cls.__isinstance = super(Config, cls).__new__(cls)

            config_path = Path(__file__).parents[4] / 'resources' / 'urls.properties'

            if not config_path.exists():
                raise FileNotFoundError(
                    f'Config file not found at {config_path}'
                )

            with open(config_path, 'r') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.split('=')
                        cls._dictionary[key.strip()] = value.strip()

        return cls.__isinstance


    @staticmethod
    def fetch(key: str, default_value: Any = None) -> Any:
        Config()
        return Config._dictionary.get(key, default_value)





#                    Реализация Singleton обьект создается один раз и конфигурация загружается один раз


                     #          Config.fetch('backendUrl')
                     #                     │
                     #                     ▼
                     #                  Config()
                     #                     │
                     #                     ▼
                     #                  __new__()
                     #                     │
                     #                     ▼
                     #         __isinstance is None?
                     #             │              │
                     #             ДА            НЕТ
                     #             │              │
                     #             ▼              │
                     #       создать объект       │
                     #             │              │
                     #             │              │
                     #             ▼              │
                     # найти urls.properties      │
                     #             │              │
                     #             ▼              │
                     #   прочитать файл           │
                     #             │              │
                     #             ▼              │
                     #   заполнить словарь        │
                     #             │              │
                     #             └──────┬───────┘
                     #                    ▼
                     #            _dictionary.get(...)
                     #                    │
                     #                    ▼
                     #       http: // localhost: 4111 / api
                     #
                     #


