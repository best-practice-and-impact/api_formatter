from enum import Enum

class SafeEnum(Enum):
    """
    A base class for Enums that provides a safe way to handle missing values.
    """
    @classmethod
    def _missing_(cls, value) -> Enum | None:
        """
        This method is called when a value is not found in the Enum.
        """
        return None

    @classmethod
    def values(cls) -> list[str]:
        """
        Returns a list of all values in the Enum.
        """
        return [item.value for item in cls]


    @classmethod
    def names(cls) -> list[str]:
        """
        Returns a list of all names in the Enum.
        """
        return [item.name for item in cls]


    @classmethod
    def has_value(cls, value) -> bool:
        """
        Checks if the given value exists in the Enum.
        """
        return value in cls._value2member_map_