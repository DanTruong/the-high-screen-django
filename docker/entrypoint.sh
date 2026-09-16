#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."

until python -c "
import os
import psycopg

psycopg.connect(
    dbname=os.environ['POSTGRES_DB'],
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    host=os.environ['POSTGRES_HOST'],
    port=os.environ.get('POSTGRES_PORT', '5432'),
).close()
" 2>/dev/null
do
    sleep 1
done

echo "PostgreSQL is ready."

echo "Applying Django migrations..."
python manage.py migrate --noinput

echo "Checking for existing THS content..."

POST_COUNT=$(python manage.py shell --no-imports -c \
    "from blog.models import Post; print(Post.objects.count())")

echo "Current post count: $POST_COUNT"

if [ "$POST_COUNT" -eq 0 ]; then
    echo "Empty database detected."
    echo "Importing The High Screen archive..."

    python manage.py import_posts data/all-posts.json
else
    echo "Existing content detected. Skipping article import."
fi

echo "Ensuring site configuration exists..."

python manage.py shell --no-imports -c \
    "from blog.models import SiteSettings; SiteSettings.objects.get_or_create(site_name='The High Screen')"

echo "Starting Django..."

exec python manage.py runserver 0.0.0.0:8000