source ./server/venv/bin/activate
(cd server ; flask db upgrade)
exec gunicorn -b :5000 --access-logfile - --error-logfile - reader:app