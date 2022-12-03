import re


def resolve_table_name(name: str) -> str:
    """Resolves table names to their mapped names."""

    names = re.split("(?=[A-Z])", name)
    return "_".join([x.lower() for x in names if x])
