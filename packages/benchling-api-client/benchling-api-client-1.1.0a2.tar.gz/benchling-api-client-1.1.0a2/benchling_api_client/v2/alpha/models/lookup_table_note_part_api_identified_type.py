from enum import Enum
from functools import lru_cache
from typing import cast

from ..extensions import Enums


class LookupTableNotePartApiIdentifiedType(Enums.KnownString):
    LOOKUP_TABLE = "lookup_table"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    @lru_cache(maxsize=None)
    def of_unknown(val: str) -> "LookupTableNotePartApiIdentifiedType":
        if not isinstance(val, str):
            raise ValueError(
                f"Value of LookupTableNotePartApiIdentifiedType must be a string (encountered: {val})"
            )
        newcls = Enum("LookupTableNotePartApiIdentifiedType", {"_UNKNOWN": val}, type=Enums.UnknownString)  # type: ignore
        return cast(LookupTableNotePartApiIdentifiedType, getattr(newcls, "_UNKNOWN"))
