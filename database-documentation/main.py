import json
from pathlib import Path

from src.collect_metadata import (
    collect_tables,
    collect_columns
)

from src.analyze_relationships import (
    collect_foreign_keys,
    collect_indexes
)

from src.generate_excel import generate_excel


def load_table_registry():
    registry_path = (
        Path(__file__).resolve().parent
        / "config"
        / "table_metadata.json"
    )
    with registry_path.open(encoding="utf-8") as registry_file:
        return json.load(registry_file)


def main():

    print("Collecting database metadata...")

    tables = collect_tables()
    columns = collect_columns()

    print("Analyzing relationships...")

    foreign_keys = collect_foreign_keys()
    indexes = collect_indexes()
    table_registry = load_table_registry()

    print("Generating Excel documentation...")

    generate_excel(
        tables,
        columns,
        foreign_keys,
        indexes,
        table_registry
    )


    print("Documentation generated successfully!")


if __name__ == "__main__":
    main()