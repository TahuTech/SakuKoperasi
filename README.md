## Run Project

Activate virtual environment:

```bash
source venv/bin/activate
```

Start server:

```bash
cd sakukoperasi
python manage.py runserver
```

## PostgreSQL Configuration

This project now uses PostgreSQL instead of SQLite.

Set these environment variables before running the app:

```bash
export DB_NAME=sakukoperasi_db
export DB_USER=postgres
export DB_PASSWORD=postgres
export DB_HOST=localhost
export DB_PORT=5432
```

Install PostgreSQL driver (already installed in this workspace):

```bash
pip install "psycopg[binary]"
```

## Migrate Existing SQLite Data to PostgreSQL

From folder `sakukoperasi/`:

1. Export data from SQLite:

```bash
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > data.json
```

2. Make sure PostgreSQL server is running and database exists:

```bash
createdb -U "$DB_USER" "$DB_NAME"
```

3. Run migrations on PostgreSQL:

```bash
python manage.py migrate
```

4. Import old data into PostgreSQL:

```bash
python manage.py loaddata data.json
```
