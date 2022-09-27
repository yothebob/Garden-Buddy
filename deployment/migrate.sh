cd /var/www/garden-tracker;
source venv/bin/activate;
python3 -c "from main import app_migrate;app_migrate()";
