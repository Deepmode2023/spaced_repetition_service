from app.domain.common.models import EnumABC


class RepetitionContentTypeEnum(str, EnumABC):
    BASE = "REPETITION"
    MD = "MD"
    WORD = "WORD"
    TEXT = "TEXT"

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
        return "repetitioncontenttypeenum"
