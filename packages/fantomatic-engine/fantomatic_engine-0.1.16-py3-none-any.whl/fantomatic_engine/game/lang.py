from .config import GameConfig
import json


class Translator:
    def __init__(self, conf: GameConfig):
        self.lang = conf.lang
        self.translations = self.load_translations(conf)

    def load_translations(self, conf: GameConfig) -> dict:
        return (json.load(open(conf.translations_file, encoding="utf-8")).get(self.lang, dict())
                if conf.translations_available()
                else dict())

    def trad(self, key):
        return self.translations.get(key, key)
