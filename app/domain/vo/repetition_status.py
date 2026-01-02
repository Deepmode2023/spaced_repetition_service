from app.domain.common.models import EnumABC


class RepetitionStatusEnum(str, EnumABC):
    SUCCESSFUL = 1
    UNSUCCESSFUL = 0
    STARTING = -1

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
        return "repetitionstatusenum"
