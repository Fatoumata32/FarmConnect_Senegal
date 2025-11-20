# FarmConnect Senegal

A comprehensive agricultural platform designed to help Senegalese farmers with weather forecasts, crop advice, market prices, and community features.

## Features

- **Weather Forecasts**: 3-day weather predictions for all 14 regions of Senegal
- **Crop Advice**: Detailed agricultural advice for 15+ popular crops
- **Market Prices**: Real-time market price information
- **Community**: Forum and networking features for farmers
- **Investor Portal**: Information for potential investors
- **Multi-language Support**: French and Wolof
- **PWA Support**: Works offline with service worker caching

## Tech Stack

- **Backend**: Django 4.2+
- **Frontend**: Bootstrap 5, JavaScript
- **Database**: SQLite (development), PostgreSQL (production)
- **Cache**: Redis 
- **Task Queue**: Celery 

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10+** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **Redis** (optional, for caching) - [Download Redis](https://redis.io/download)

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/FarmConnect_Senegal.git
cd FarmConnect_Senegal
```

### Step 2: Create a Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root directory:


**.env file contents:**
```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True

# API Keys
OPENWEATHER_API_KEY=your-openweather-api-key
WEATHERAPI_KEY=your-weatherapi-key-optional
SMS_API_KEY=your-sms-api-key-optional

# Database (optional - for PostgreSQL in production)
# DB_NAME=farmconnect
# DB_USER=your-db-user
# DB_PASSWORD=your-db-password
# DB_HOST=localhost
# DB_PORT=5432
```

**Getting API Keys:**

1. **OpenWeather API Key** (Required for weather features):
   - Go to [OpenWeatherMap](https://openweathermap.org/api)
   - Create a free account
   - Get your API key from the dashboard
   - Add it to your `.env` file

### Step 5: Run Database Migrations

```bash
python manage.py migrate
```

### Step 6: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 7: Run the Development Server

```bash
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000/**

## Accessing the Application

### Main Pages

- **Home Page**: http://127.0.0.1:8000/
- **Login**: http://127.0.0.1:8000/accounts/login/
- **Register**: http://127.0.0.1:8000/register/
- **Dashboard**: http://127.0.0.1:8000/dashboard/
- **Community**: http://127.0.0.1:8000/community/
- **Crop Advice Guide**: http://127.0.0.1:8000/guide-cultures/
- **Investors**: http://127.0.0.1:8000/investors/
- **Tools**: http://127.0.0.1:8000/tools/

### Admin Panel

- **Admin Dashboard**: http://127.0.0.1:8000/admin-dashboard/
- **Django Admin**: http://127.0.0.1:8000/admin/

Login with 
Username: farmconnect_admin
Email: admin@farmconnect.sn
Password: FarmConnect@2024 to access the **admin** areas.

## Project Structure

```
FarmConnect_Senegal/
├── advice/                 # Crop advice app
├── community/              # Community/forum app
├── crops/                  # Crops management app
├── farmconnect_app/        # Main application
├── farmconnect_project/    # Project settings
├── marketplace/            # Marketplace app
├── weather/                # Weather service app
├── static/                 # Static files (CSS, JS, images)
├── templates/              # HTML templates
├── locale/                 # Translation files
├── logs/                   # Log files
├── media/                  # User uploaded files
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
└── .env                    # Environment variables (create this)
```

## Configuration Options

### Debug Mode

For development, keep `DEBUG=True` in your `.env` file. For production, set `DEBUG=False`.

### Database

**SQLite (Default - Development):**
No additional configuration needed. The database file `farmconnect.sqlite3` will be created automatically.

**PostgreSQL (Production):**
1. Install PostgreSQL
2. Create a database
3. Update `.env` with database credentials
4. Modify `settings.py` to use PostgreSQL

### Redis Cache (Optional)

If you want to enable Redis caching:

1. Install and start Redis server
2. The application will automatically use Redis when available


## Running Tests

```bash
python manage.py test
```

## Common Issues & Solutions

### Issue: "No module named 'decouple'"
```bash
pip install python-decouple
```

### Issue: "Static files not loading"
```bash
python manage.py collectstatic --noinput
```

### Issue: "Database errors after pulling new code"
```bash
python manage.py migrate
```

### Issue: "Weather not loading"
Make sure you have a valid `OPENWEATHER_API_KEY` in your `.env` file.

### Issue: "Permission denied" on Windows
Run your terminal as Administrator.

### Issue: Redis connection error
If Redis is not installed, the app will use a dummy cache. This is fine for development.

## API Endpoints

### Public APIs

- `GET /api/crops/` - List all crops
- `GET /api/soil-types/` - List soil types
- `GET /api/recommendations/` - Get crop recommendations
- `GET /api/weather/?region=dakar` - Get weather for a region
- `GET /api/crop-advice/crops_with_advice/` - Get crops with advice

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is proprietary software. All rights reserved.

## Support

For support, email: support@farmconnect.sn

## Authors

- **FarmConnect Senegal Team - Fatoumata NDIAYE**

