# Airline Flight Search Web Application

## Setup

### 1. Create the database

pgAdmin: create a database, then open Query Tool and run the contents of `setup_db.sql`.

### 2. Install Python dependencies

```bash
pip3 install -r requirements.txt
```

### 3. Run the application

```bash
python app.py
```

Open [http://localhost:5001](http://localhost:5001) in your browser.

## Features

- **Search page**: enter origin/destination airport codes and a date range
- **Results page**: displays all matching flights (flight number, airline, departure date/time, origin, destination, duration)
- **Flight detail page**: click any flight to see plane capacity, booked seats, and available seats with an occupancy bar

## Structure

```
Airline_Booking_App/
├── app.py              # Flask application
├── setup_db.sql        # Database schema + sample data
├── requirements.txt    # Python dependencies
├── .gitignore
├── README.md
└── templates/
    ├── base.html           # Base template
    ├── index.html          # Search form (start page)
    ├── results.html        # Flight search results
    └── flight_detail.html  # Seat availability detail
```
