# Database Documentation

This utility collects schema metadata from a MariaDB database and exports it to
an Excel workbook. It reads metadata from `information_schema`; it does not
export application-table records.

The generated workbook contains:

- **Table Catalog** — table type, engine, approximate row count, business
  domain, domain description, table description, and documentation status.
- **Column Dictionary** — column names, data types, nullability, defaults,
  keys, and database comments.
- **Declared Foreign Keys** — foreign-key constraints declared in MySQL.
  Relationships are not inferred from column names or application conventions.
- **Indexes** — index names, columns, uniqueness, order, and type.

All registry descriptions are provisional and require business-owner review.

## Requirements

- Python 3.13 (the version used to validate this project)
- A MySQL-compatible database reachable from this machine
- A database account with permission to read the target schema metadata

## Setup

Run these commands from the `database-documentation` directory:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create `config/.env` with the connection settings:

```dotenv
DB_USER=your_read_only_user
DB_PASSWORD=your_password
DB_HOST=your_database_host
DB_PORT=3306
DB_NAME=your_database_name
```

Use a read-only database account. Do not commit `config/.env`; it is excluded
by `.gitignore`.

## Generate the workbook

From the `database-documentation` directory, run:

```powershell
python main.py
```

The workbook is written to:

```text
output/database_documentation.xlsx
```

The command needs to run from this directory because the database connection
loader and output paths are relative to the current working directory.

## Maintain the table registry

Edit `config/table_metadata.json`:

- Add or update domain definitions in `domains`.
- Add one entry under `tables` for each database table. The key must exactly
  match the MySQL table name.
- Set `domain` to a key defined in `domains`, and provide an English
  `description`.
- Update `schema_snapshot_date` when the registry is reviewed against a new
  schema snapshot.
- Keep classifications provisional until confirmed by a business owner.

Tables missing from the registry appear as **Unclassified** in the workbook
with a **Missing registry entry** status.

## Scope note

The current `main.py` pipeline generates the Excel workbook only. Any ER
diagram files already present in `output` are not refreshed by this command.