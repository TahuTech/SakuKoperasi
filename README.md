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

## Docker Setup (Django + PostgreSQL)

1. Copy environment template:

```bash
cp .env.example .env
```

2. Build and start containers:

```bash
docker-compose up --build
```

3. Open API/app:

```text
http://localhost:8000
```

Useful commands:

```bash
# stop containers
docker-compose down

# stop and remove database volume
docker-compose down -v

# run Django command inside web container
docker-compose exec web python manage.py createsuperuser
```

## Docker Shortcut: tahu

This project containt script `tahu` for important shortcut for docker.

1. Grant permission to execute (once time):

```bash
chmod +x tahu
```

2. Run Command:

```bash
./tahu install
./tahu up
./tahu migrate
./tahu logs
```

Important actions:

```text
up         Build and start containers
down       Stop and remove containers
reset      Stop containers and remove volumes
logs       Show service logs
ps         Show service status
install    Install Docker + Compose (Ubuntu/Debian/Arch/CachyOS)
migrate    Run Django migrate
check      Run Django check
shell      Open Django shell
superuser  Create Django superuser
dump       Export data to sakukoperasi/data.json
loaddata   Import sakukoperasi/data.json
```

Note: `./tahu install` need root access/sudo

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
