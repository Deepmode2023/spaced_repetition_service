from app.domain.common.models import EnumABC


class LanguageEnum(EnumABC):
    ENGLISH_US = "EN-US"
    ENGLISH_BR = "EN_GB"
    SPANISH = "ES"
    FRENCH = "FR"
    GERMANY = "DE"
    POLAND = "PL"

    @classmethod
    def fields(cls):
        """
        Returns all fields of the enum as a dictionary.

        Returns:
            dict: A dictionary with enum names as keys and values as enum values.
        """
        return {item.name: item.value for item in cls}

    @classmethod
    def get_name(self):
        return "languageenum"
