# Fit Compare

Fit Compare is a web application built with Flask that allows users to connect to the Strava API and compare fitness activities. This project provides a modern user interface and facilitates the retrieval and display of user information from Strava.

## Features

- User authentication with Strava
- Dashboard displaying user activities
- Profile page showing user information
- Modern UI with responsive design

## Project Structure

```
fit-compare
├── app.py                # Entry point of the Flask application
├── config.py             # Configuration settings for the application
├── requirements.txt      # List of dependencies
├── .env.example          # Example environment variables
├── .gitignore            # Files and directories to ignore by Git
├── README.md             # Project documentation
├── static                # Static files (CSS, JS)
│   ├── css
│   │   └── styles.css    # CSS styles for the application
│   └── js
│       └── app.js        # JavaScript for client-side functionality
├── templates             # HTML templates
│   ├── base.html         # Base template for the application
│   ├── index.html        # Landing page
│   ├── dashboard.html     # User dashboard
│   ├── profile.html      # User profile page
│   └── error.html        # Error page
├── routes                # Application routes
│   ├── __init__.py       # Initializes the routes package
│   ├── auth.py           # Authentication routes
│   ├── dashboard.py      # Dashboard routes
│   └── profile.py        # Profile routes
├── services              # Services for API interactions
│   ├── __init__.py       # Initializes the services package
│   └── strava_client.py  # Functions to interact with the Strava API
├── models                # Data models
│   ├── __init__.py       # Initializes the models package
│   └── user.py           # User model
└── utils                 # Utility functions
    ├── __init__.py       # Initializes the utils package
    └── token_store.py    # Handles token storage for Strava API
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/fit-compare.git
   cd fit-compare
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env` and fill in your Strava API credentials.

## Usage

1. Run the application:
   ```
   python app.py
   ```

2. Open your browser and go to `http://127.0.0.1:5000`.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features.

## License

This project is licensed under the MIT License. See the LICENSE file for details.