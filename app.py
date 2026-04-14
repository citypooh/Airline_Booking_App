from flask import Flask, render_template, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)


def get_db():
    return psycopg2.connect(
        host="localhost", dbname="airline", user="postgres", password="",
        cursor_factory=RealDictCursor
    )


@app.route("/")
def index():
    with get_db() as conn, conn.cursor() as cur:
        cur.execute("SELECT airport_code, name FROM Airport ORDER BY airport_code")
        airports = cur.fetchall()
    return render_template("index.html", airports=airports)


@app.route("/search")
def search():
    origin = request.args["origin"]
    destination = request.args["destination"]
    start_date = request.args["start_date"]
    end_date = request.args["end_date"]

    with get_db() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT f.flight_number, f.departure_date,
                   fs.origin_code, fs.dest_code, fs.departure_time, fs.airline_name
            FROM Flight f
            JOIN FlightService fs ON f.flight_number = fs.flight_number
            WHERE fs.origin_code = %s AND fs.dest_code = %s
              AND f.departure_date BETWEEN %s AND %s
            ORDER BY f.departure_date, fs.departure_time
        """, (origin, destination, start_date, end_date))
        flights = cur.fetchall()

    return render_template("results.html", flights=flights,
                           origin=origin, destination=destination,
                           start_date=start_date, end_date=end_date)


@app.route("/flight/<flight_number>/<departure_date>")
def flight_detail(flight_number, departure_date):
    with get_db() as conn, conn.cursor() as cur:
        cur.execute("""
            SELECT f.flight_number, f.departure_date,
                   fs.airline_name, fs.origin_code, fs.dest_code, fs.departure_time,
                   a.capacity,
                   a.capacity - COUNT(b.pid) AS available_seats,
                   COUNT(b.pid) AS booked_seats
            FROM Flight f
            JOIN FlightService fs ON f.flight_number = fs.flight_number
            JOIN Aircraft a ON f.plane_type = a.plane_type
            LEFT JOIN Booking b ON f.flight_number = b.flight_number
                               AND f.departure_date = b.departure_date
            WHERE f.flight_number = %s AND f.departure_date = %s
            GROUP BY f.flight_number, f.departure_date,
                     fs.airline_name, fs.origin_code, fs.dest_code,
                     fs.departure_time, a.capacity
        """, (flight_number, departure_date))
        flight = cur.fetchone()

    return render_template("flight_detail.html", flight=flight)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
