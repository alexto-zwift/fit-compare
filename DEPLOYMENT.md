# Fit Compare

A Flask web application that allows you to compare your fitness activities using data from the Strava API.

## Features

- Strava OAuth 2.0 authentication
- View your fitness activities
- Compare activities with other users
- Responsive web interface

## Local Development

### Prerequisites
- Python 3.9+
- pip or virtualenv

### Setup

1. Clone the repository:
```bash
git clone https://github.com/alexto-zwift/fit-compare.git
cd fit-compare
```

2. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
```

5. Add your Strava API credentials:
   - Go to https://www.strava.com/settings/api
   - Create an application
   - Copy your Client ID and Client Secret to `.env`

6. Run the development server:
```bash
python3 app.py
```

The app will be available at `http://localhost:5001`

## Deployment to Vercel

1. Push your code to GitHub
2. Visit [Vercel](https://vercel.com)
3. Create a new project and import this repository
4. Add environment variables in Vercel dashboard:
   - `STRAVA_CLIENT_ID`
   - `STRAVA_CLIENT_SECRET`
   - `STRAVA_REDIRECT_URI` (set to your Vercel domain)
   - `SECRET_KEY`
5. Deploy!

## Project Structure

```
fit-compare/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel deployment config
├── api/
│   └── index.py         # Serverless function handler
├── routes/              # Blueprint route handlers
├── services/            # External API clients
├── static/              # CSS, JavaScript
├── templates/           # HTML templates
└── models/              # Database models
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `STRAVA_CLIENT_ID` | Your Strava API Client ID |
| `STRAVA_CLIENT_SECRET` | Your Strava API Client Secret |
| `STRAVA_REDIRECT_URI` | OAuth redirect URL (localhost:5001 for local) |
| `SECRET_KEY` | Flask session secret key |
| `DEBUG` | Debug mode (True/False) |

## License

MIT
