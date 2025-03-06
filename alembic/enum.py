from typing import Iterable, Sequence, Tuple
from alembic import op
import sqlalchemy as sa
from app.domain.models import EnumABC
from app.domain.exceptions.internal import WrongEnumInstError, WrongEntityError
from collections import namedtuple


Reference = namedtuple("Reference", ["table", "column"])


def enum_key_gen(values: Iterable[str]) -> str:
    return ", ".join(f"'{value}'" for value in values)


def create_enum_values(
    enums: dict[str, EnumABC],
    references: Iterable[Reference],
):
    """
    @param enum: EnumABC
    @param references: Iterable[Reference]

    Example:
        create_enum_values(('promo_type_enum', promo_type_enum1'), (('advertisement_sale_package', 'promo_type'), ('advertisement_sale_package', 'promo_type')))
    """

    for reference in references:
        _, column = reference
        enum = enums.get(column, None)
        create_enum_value(enum=enum, reference=reference)


def create_enum_value(
    enum: EnumABC,
    reference: Reference,
):
    try:
        table, column = reference
        sa.Enum(
            enum_key_gen(enum.fields().values()),
            name=enum.get_name,
        ).create(op.get_bind())

        op.execute(
            f"ALTER TABLE {table} ALTER COLUMN {column} TYPE {enum.get_name} USING {column}::{enum.get_name};"
        )
    except Exception:
        raise WrongEntityError(
            entity="reference",
            entity_type="Iterable[str,str]",
            place="'create_enum_values functions'",
        )


def set_enum_values(
    enum_name: str,
    new_values: Iterable[str],
    references: Tuple[Reference],
):
    """
    @param enum_name: Системное наименование enum
    @param new_values: Новые значения enum
    @param references: Упоминания enum в моделях

    Example:
        set_enum_values('promo_type_enum', (
            'BEST_OFFER',
            'NEW_PRODUCT',
            'NO_PROMOTION',
        ), [('advertisement_sale_package', 'promo_type')])
    """
    query_str = f"""
        ALTER TYPE {enum_name} RENAME TO {enum_name}_old;
        CREATE TYPE {enum_name} AS ENUM({enum_key_gen(new_values)});
    """
    query_str += "\n".join(
        f"""
        ALTER TABLE {table_name} ALTER COLUMN {column_name} DROP DEFAULT;
        ALTER TABLE {table_name} ALTER COLUMN {column_name} TYPE {enum_name} USING {column_name}::text::{enum_name};
        """
        for table_name, column_name in references
    )
    query_str += f"DROP TYPE {enum_name}_old;"

    for q in query_str.split(";")[:-1]:
        op.execute(q)
