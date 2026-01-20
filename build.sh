#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Remove old SQLite database if it exists (for fresh start on each deploy)
if [ -f db.sqlite3 ]; then
    echo "Removing old SQLite database..."
    rm db.sqlite3
fi

# Apply database migrations
echo "Running migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Build completed successfully!"
