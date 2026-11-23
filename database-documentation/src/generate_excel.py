import pandas as pd
from pathlib import Path

OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)

COMMENT_TRANSLATIONS = {
    "0: attesa invio 1: invio in corso 2: attesa ricevuta 3: inviato 4: errore":
        "0: Waiting to send; 1: Sending; 2: Awaiting delivery receipt; 3: Sent; 4: Error",
    "0: attesa invio 1: invio in corso 2: inviata 3: errore":
        "0: Waiting to send; 1: Sending; 2: Sent; 3: Error",
    "0: attesa iscrizione 1: iscritto 2: frequentato 3: disdetto":
        "0: Awaiting enrollment; 1: Enrolled; 2: Attended; 3: Cancelled",
    "0: attivo 1: bounce soft 2: bounce hard 3: disiscritto":
        "0: Active; 1: Soft bounce; 2: Hard bounce; 3: Unsubscribed",
    "1: facebook 2: linkedin":
        "1: Facebook; 2: LinkedIn",
    "1: ins 2: ins doppione 3: upd 4: warning":
        "1: Inserted; 2: Duplicate insert; 3: Updated; 4: Warning",
    "1: standard2: ab_test":
        "1: Standard; 2: A/B test",
    "workspace_id della licenza AudienceRate che alimenta brainlead con un connettore dedicato":
        "Workspace ID of the AudienceRate license that feeds Brainlead through a dedicated connector.",
}


def generate_excel(
    tables,
    columns,
    foreign_keys,
    indexes,
    table_registry
):
    # Table Catalog
    catalog = tables.copy()

    registry_tables = table_registry["tables"]
    domains = table_registry["domains"]

    def metadata_for(table_name):
        return registry_tables.get(table_name, {})

    catalog["Business Domain"] = catalog["TABLE_NAME"].map(
        lambda table_name: metadata_for(table_name).get(
            "domain",
            "Unclassified"
        )
    )
    catalog["Domain Description"] = catalog["Business Domain"].map(
        lambda domain: domains.get(
            domain,
            "No domain description in registry"
        )
    )
    catalog["Description"] = catalog["TABLE_NAME"].map(
        lambda table_name: metadata_for(table_name).get(
            "description",
            "No description in registry"
        )
    )
    catalog["Documentation Status"] = catalog["TABLE_NAME"].map(
        lambda table_name: (
            table_registry["classification_status"]
            if table_name in registry_tables
            else "Missing registry entry"
        )
    )

    catalog = catalog.rename(columns={
        "TABLE_NAME": "Table",
        "TABLE_TYPE": "Type",
        "TABLE_ROWS": "Approx. Rows",
        "ENGINE": "Engine",
        "TABLE_COMMENT": "Comment"
    })

    # Column Dictionary
    dictionary = columns.copy()

    dictionary["Description"] = "Needs business validation"
    dictionary["COLUMN_COMMENT"] = dictionary["COLUMN_COMMENT"].map(
        lambda comment: COMMENT_TRANSLATIONS.get(
            " ".join(comment.split()),
            comment
        )
        if isinstance(comment, str)
        else comment
    )

    dictionary = dictionary.rename(columns={
        "TABLE_NAME": "Table",
        "COLUMN_NAME": "Column",
        "COLUMN_TYPE": "Data Type",
        "COLUMN_KEY": "Key",
        "IS_NULLABLE": "Nullable",
        "COLUMN_DEFAULT": "Default",
        "COLUMN_COMMENT": "Comment"
    })

    # Declared foreign key constraints
    relationships = foreign_keys.rename(columns={
        "TABLE_NAME": "Child Table",
        "COLUMN_NAME": "Child Column",
        "REFERENCED_TABLE_NAME": "Parent Table",
        "REFERENCED_COLUMN_NAME": "Parent Column"
    })

    # Export
    path = OUTPUT / "database_documentation.xlsx"

    with pd.ExcelWriter(
        path,
        engine="openpyxl"
    ) as writer:

        catalog.to_excel(
            writer,
            sheet_name="Table Catalog",
            index=False
        )

        dictionary.to_excel(
            writer,
            sheet_name="Column Dictionary",
            index=False
        )

        relationships.to_excel(
            writer,
            sheet_name="Declared Foreign Keys",
            index=False
        )

        indexes.to_excel(
            writer,
            sheet_name="Indexes",
            index=False
        )

    print(f"Created: {path}")