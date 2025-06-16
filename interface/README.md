# Tender Monitor Interface

A modern, reactive web interface for visualizing scraped tender data. Built with React and Material-UI, this application provides an intuitive way to explore and analyze tender data from various sources.

## Features

- 📊 Interactive dashboard with key metrics
- 📋 Searchable and filterable tender list
- 📈 Statistical visualizations using Chart.js
- 🎨 Modern UI with Material Design
- 🔄 Real-time data updates
- 📱 Responsive design for all devices

## Prerequisites

- Node.js (v14 or later)
- npm or yarn
- Python (v3.8 or later)
- Django (v4.2 or later)

## Setup

1. Install frontend dependencies:
   ```bash
   cd interface
   npm install
   ```

2. Install Django REST framework if not already installed:
   ```bash
   pip install djangorestframework
   ```

3. Add 'rest_framework' to INSTALLED_APPS in your Django settings.py:
   ```python
   INSTALLED_APPS = [
       ...
       'rest_framework',
   ]
   ```

## Running the Application

1. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

2. In a separate terminal, start the React development server:
   ```bash
   cd interface
   npm start
   ```

3. Access the application:
   - Frontend: http://localhost:3000
   - API: http://localhost:8000/api/tenders/

## API Endpoints

- `GET /api/tenders/`: Get all tenders
- `GET /api/tenders/statistics/`: Get tender statistics

## Project Structure

```
interface/
├── src/
│   ├── components/      # Reusable UI components
│   ├── pages/           # Page components
│   ├── App.js           # Main application component
│   └── index.js         # Application entry point
├── package.json         # Project dependencies
└── README.md           # Project documentation
```

## Development

- The frontend uses proxy configuration to forward API requests to the Django backend
- All API calls use relative paths (e.g., `/api/tenders/`)
- The application is configured for development with hot reloading

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request