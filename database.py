import sqlite3
import os
import time
import re
from datetime import datetime
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "event_management.db")

def register_custom_functions(conn: sqlite3.Connection):
    """Registers PostgreSQL and SQL-standard helper functions inside SQLite."""
    # NOW()
    conn.create_function("now", 0, lambda: "2026-08-08 23:59:59")
    
    # YEAR, MONTH, DAY extractors
    conn.create_function("year", 1, lambda d: int(str(d).split("-")[0]) if d and "-" in str(d) else None)
    conn.create_function("month", 1, lambda d: int(str(d).split("-")[1]) if d and "-" in str(d) else None)
    conn.create_function("day", 1, lambda d: int(str(d).split("-")[2][:2]) if d and "-" in str(d) else None)
    
    # CONCAT
    conn.create_function("concat", -1, lambda *args: "".join(str(a) for a in args if a is not None))
    
    # TO_CHAR emulation
    def _to_char(val, fmt=None):
        if val is None:
            return ""
        val_str = str(val)
        if fmt and "yyyy" in fmt.lower():
            # Return standard formatted string YYYY-MM-DD HH:MM:SS
            try:
                dt = datetime.fromisoformat(val_str.replace("Z", "+00:00"))
                return dt.strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                return val_str
        return val_str
    
    conn.create_function("to_char", 2, _to_char)

def preprocess_pg_to_sqlite(sql: str) -> str:
    """
    Translates common PostgreSQL-specific syntax into SQLite-compatible SQL
    so that queries from finalexam.sql execute cleanly.
    """
    s = sql.strip()
    
    # Remove leading comment markers if any line starts with '- ' or '--'
    s = re.sub(r'^\s*-\s+(\d+\.\d+)', r'-- \1', s)
    
    # 1. EXTRACT(month FROM col) -> CAST(strftime('%m', col) AS INTEGER)
    s = re.sub(
        r'(?i)extract\s*\(\s*month\s+from\s+([a-zA-Z0-9_.]+)\s*\)',
        r"CAST(strftime('%m', \1) AS INTEGER)",
        s
    )
    
    # 2. NOW() - INTERVAL 'X day' -> datetime('2026-08-08 23:59:59', '-X days')
    s = re.sub(
        r"(?i)now\(\)\s*-\s*interval\s*'(\d+)\s*day'",
        r"datetime('2026-08-08 23:59:59', '-\1 days')",
        s
    )
    
    # 3. (event_date::date - current_date) or event_date::date - current_date
    s = re.sub(
        r"(?i)\(?\s*([a-zA-Z0-9_.]+)::date\s*-\s*current_date\s*\)?",
        r"CAST(julianday(date(\1)) - julianday('2026-08-08') AS INTEGER)",
        s
    )
    
    # 4. col::date -> date(col)
    s = re.sub(r'(?i)([a-zA-Z0-9_.]+)::date', r'date(\1)', s)
    
    # 5. to_char(col, 'yyyy-mm-dd hh24:mi:ss')
    s = re.sub(
        r"(?i)to_char\s*\(\s*([^,]+)\s*,\s*'yyyy-mm-dd hh24:mi:ss'\s*\)",
        r"strftime('%Y-%m-%d %H:%M:%S', \1)",
        s
    )
    
    return s

def get_connection() -> sqlite3.Connection:
    """Creates a connection with custom functions registered."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    register_custom_functions(conn)
    return conn

def init_db(force_reset: bool = False):
    """Initializes the database schema and sample data if not already existing or if reset requested."""
    if force_reset and os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception:
            pass

    conn = get_connection()
    cursor = conn.cursor()

    # Check if tables already exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Events';")
    if cursor.fetchone() and not force_reset:
        conn.close()
        return

    # 1. Create Tables
    cursor.executescript("""
    DROP TABLE IF EXISTS Payments;
    DROP TABLE IF EXISTS Tickets;
    DROP TABLE IF EXISTS Events;
    DROP TABLE IF EXISTS Attendees;
    DROP TABLE IF EXISTS Organizers;
    DROP TABLE IF EXISTS Venues;

    CREATE TABLE Venues (
        venue_id INT PRIMARY KEY,
        venue_name VARCHAR(100) NOT NULL,
        location VARCHAR(100) NOT NULL,
        capacity INT NOT NULL
    );

    CREATE TABLE Organizers (
        organizer_id INT PRIMARY KEY,
        organizer_name VARCHAR(100) NOT NULL,
        contact_email VARCHAR(100),
        phone_number VARCHAR(15)
    );

    CREATE TABLE Events (
        event_id INT PRIMARY KEY,
        event_name VARCHAR(100) NOT NULL,
        event_date TIMESTAMP,
        venue_id INT,
        organizer_id INT,
        ticket_price DECIMAL(10,2) NOT NULL,
        total_seats INT NOT NULL,
        available_seats INT NOT NULL,
        FOREIGN KEY (venue_id) REFERENCES Venues(venue_id),
        FOREIGN KEY (organizer_id) REFERENCES Organizers(organizer_id)
    );

    CREATE TABLE Attendees (
        attendee_id INT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100),
        phone_number VARCHAR(15)
    );

    CREATE TABLE Tickets (
        ticket_id INT PRIMARY KEY,
        event_id INT NOT NULL,
        attendee_id INT NOT NULL,
        booking_date TIMESTAMP NOT NULL,
        status VARCHAR(20) NOT NULL CHECK(status IN ('Confirmed', 'Cancelled', 'Pending')),
        FOREIGN KEY (event_id) REFERENCES Events(event_id),
        FOREIGN KEY (attendee_id) REFERENCES Attendees(attendee_id),
        UNIQUE (event_id, attendee_id)
    );

    CREATE TABLE Payments (
        payment_id INT PRIMARY KEY,
        ticket_id INT NOT NULL,
        amount_paid DECIMAL(10,2) NOT NULL,
        payment_status VARCHAR(20) NOT NULL CHECK(payment_status IN ('Success', 'Failed', 'Pending')),
        payment_date TIMESTAMP,
        FOREIGN KEY (ticket_id) REFERENCES Tickets(ticket_id)
    );
    """)

    # 2. Insert Venues
    cursor.executescript("""
    INSERT INTO Venues (venue_id, venue_name, location, capacity) VALUES
    (1, 'Riverfront Convention Centre', 'Ahmedabad', 1000),
    (2, 'Grand Palace Hall', 'Mumbai', 800),
    (3, 'Tech Arena', 'Bangalore', 1200),
    (4, 'City Auditorium', 'Delhi', 600),
    (5, 'Royal Garden', 'Pune', 500),
    (6, 'Sunrise Hall', 'Ahmedabad', 400);
    """)

    # 3. Insert Organizers
    cursor.executescript("""
    INSERT INTO Organizers (organizer_id, organizer_name, contact_email, phone_number) VALUES
    (1, '  Raj Events  ', 'raj@events.com', '9876543210'),
    (2, 'Dream Productions', 'dream@events.com', '9876543211'),
    (3, 'TechConnect', 'tech@events.com', '9876543212'),
    (4, 'Global Events', NULL, '9876543213'),
    (5, 'Elite Management', 'elite@events.com', '9876543214');
    """)

    # 4. Insert Events
    cursor.executescript("""
    INSERT INTO Events (event_id, event_name, event_date, venue_id, organizer_id, ticket_price, total_seats, available_seats) VALUES
    (1, 'Ahmedabad Music Festival', '2026-12-05 18:00:00', 1, 1, 1500.00, 1000, 150),
    (2, 'Mumbai Business Summit', '2026-11-20 10:00:00', 2, 2, 2500.00, 800, 450),
    (3, 'Bangalore Tech Conference', '2026-12-15 09:00:00', 3, 3, 3000.00, 1200, 900),
    (4, 'Delhi Startup Expo', '2026-10-10 11:00:00', 4, 4, 1200.00, 600, 500),
    (5, 'Pune Food Carnival', '2026-12-25 17:00:00', 5, 5, 800.00, 500, 80),
    (6, 'Ahmedabad Art Exhibition', '2026-09-18 16:00:00', 6, 1, 500.00, 400, 300),
    (7, 'Mumbai Concert Night', '2026-12-30 19:00:00', 2, 2, 2000.00, 800, 100),
    (8, 'Delhi Cultural Festival', '2026-12-12 18:00:00', 4, 4, 1000.00, 600, 350),
    (9, 'Bangalore AI Summit', '2027-01-20 09:30:00', 3, 3, 3500.00, 1200, 1100),
    (10, 'Pune Business Meetup', '2026-08-30 14:00:00', 5, 5, 600.00, 500, 450);
    """)

    # 5. Insert Attendees
    cursor.executescript("""
    INSERT INTO Attendees (attendee_id, name, email, phone_number) VALUES
    (1, '  Aarav Sharma  ', 'aarav@gmail.com', '9000000001'),
    (2, 'Priya Patel', 'priya@gmail.com', '9000000002'),
    (3, 'Rohan Mehta', 'rohan@gmail.com', '9000000003'),
    (4, 'Ananya Shah', NULL, '9000000004'),
    (5, 'Kabir Joshi', 'kabir@gmail.com', '9000000005'),
    (6, 'Neha Desai', 'neha@gmail.com', '9000000006'),
    (7, 'Arjun Verma', NULL, '9000000007'),
    (8, 'Isha Kapoor', 'isha@gmail.com', '9000000008'),
    (9, 'Vivaan Shah', 'vivaan@gmail.com', '9000000009'),
    (10, 'Meera Patel', 'meera@gmail.com', '9000000010'),
    (11, 'Aditya Singh', 'aditya@gmail.com', '9000000011'),
    (12, 'Kavya Joshi', 'kavya@gmail.com', '9000000012');
    """)

    # 6. Insert Tickets
    cursor.executescript("""
    INSERT INTO Tickets (ticket_id, event_id, attendee_id, booking_date, status) VALUES
    (1, 1, 1, '2026-08-01 10:30:00', 'Confirmed'),
    (2, 1, 2, '2026-08-02 11:00:00', 'Confirmed'),
    (3, 2, 3, '2026-08-03 12:00:00', 'Confirmed'),
    (4, 2, 4, '2026-08-04 14:30:00', 'Pending'),
    (5, 3, 5, '2026-08-05 09:15:00', 'Confirmed'),
    (6, 3, 6, '2026-08-05 16:00:00', 'Confirmed'),
    (7, 5, 7, '2026-08-06 10:00:00', 'Confirmed'),
    (8, 5, 8, '2026-08-06 11:30:00', 'Confirmed'),
    (9, 7, 9, '2026-08-07 13:00:00', 'Pending'),
    (10, 7, 10, '2026-08-07 15:30:00', 'Confirmed'),
    (11, 8, 1, '2026-08-08 09:00:00', 'Confirmed'),
    (12, 8, 11, '2026-08-08 10:00:00', 'Confirmed'),
    (13, 3, 12, '2026-08-08 11:00:00', 'Pending'),
    (14, 6, 3, '2026-08-08 12:00:00', 'Confirmed'),
    (15, 2, 5, '2026-08-08 13:00:00', 'Cancelled');
    """)

    # 7. Insert Payments
    cursor.executescript("""
    INSERT INTO Payments (payment_id, ticket_id, amount_paid, payment_status, payment_date) VALUES
    (1, 1, 1500.00, 'Success', '2026-08-01 10:35:00'),
    (2, 2, 1500.00, 'Success', '2026-08-02 11:05:00'),
    (3, 3, 2500.00, 'Success', '2026-08-03 12:10:00'),
    (4, 4, 2500.00, 'Pending', '2026-08-04 14:35:00'),
    (5, 5, 3000.00, 'Success', '2026-08-05 09:20:00'),
    (6, 6, 3000.00, 'Success', '2026-08-05 16:05:00'),
    (7, 7, 800.00, 'Success', '2026-08-06 10:05:00'),
    (8, 8, 800.00, 'Success', '2026-08-06 11:35:00'),
    (9, 9, 2000.00, 'Pending', '2026-08-07 13:05:00'),
    (10, 10, 2000.00, 'Success', '2026-08-07 15:35:00'),
    (11, 11, 1000.00, 'Success', '2026-08-08 09:05:00'),
    (12, 12, 1000.00, 'Success', '2026-08-08 10:05:00'),
    (13, 13, 3000.00, 'Pending', '2026-08-08 11:05:00'),
    (14, 14, 500.00, 'Success', '2026-08-08 12:05:00'),
    (15, 15, 2500.00, 'Failed', '2026-08-08 13:05:00');
    """)

    conn.commit()
    conn.close()

def run_query(sql_query: str):
    """
    Executes a SQL query and returns:
    (DataFrame or None, execution_time_in_ms, error_string_or_None)
    """
    start_time = time.time()
    conn = get_connection()
    try:
        # Translate dialect if needed
        executable_sql = preprocess_pg_to_sqlite(sql_query)
        sql_stripped = executable_sql.strip().lower()
        
        # Check if SELECT / WITH or modifying query
        if sql_stripped.startswith("select") or sql_stripped.startswith("with"):
            df = pd.read_sql_query(executable_sql, conn)
            elapsed_ms = (time.time() - start_time) * 1000
            conn.close()
            return df, elapsed_ms, None
        else:
            cursor = conn.cursor()
            cursor.execute(executable_sql)
            conn.commit()
            rows_affected = cursor.rowcount
            elapsed_ms = (time.time() - start_time) * 1000
            conn.close()
            df = pd.DataFrame([{"Status": "Success", "Message": "Statement executed successfully", "Rows Affected": rows_affected}])
            return df, elapsed_ms, None
    except Exception as e:
        conn.close()
        elapsed_ms = (time.time() - start_time) * 1000
        return None, elapsed_ms, str(e)

def get_kpis():
    """Returns high-level KPI metrics for the executive dashboard."""
    conn = get_connection()
    cur = conn.cursor()
    
    total_events = cur.execute("SELECT COUNT(*) FROM Events").fetchone()[0]
    total_venues = cur.execute("SELECT COUNT(*) FROM Venues").fetchone()[0]
    total_organizers = cur.execute("SELECT COUNT(*) FROM Organizers").fetchone()[0]
    total_attendees = cur.execute("SELECT COUNT(*) FROM Attendees").fetchone()[0]
    total_tickets = cur.execute("SELECT COUNT(*) FROM Tickets").fetchone()[0]
    confirmed_tickets = cur.execute("SELECT COUNT(*) FROM Tickets WHERE status = 'Confirmed'").fetchone()[0]
    
    total_revenue_res = cur.execute("SELECT SUM(amount_paid) FROM Payments WHERE payment_status = 'Success'").fetchone()[0]
    total_revenue = float(total_revenue_res) if total_revenue_res else 0.0
    
    avg_ticket_res = cur.execute("SELECT AVG(ticket_price) FROM Events").fetchone()[0]
    avg_ticket_price = round(float(avg_ticket_res), 2) if avg_ticket_res else 0.0
    
    total_capacity = cur.execute("SELECT SUM(total_seats) FROM Events").fetchone()[0] or 0
    available_seats = cur.execute("SELECT SUM(available_seats) FROM Events").fetchone()[0] or 0
    booked_seats = total_capacity - available_seats

    conn.close()
    return {
        "events": total_events,
        "venues": total_venues,
        "organizers": total_organizers,
        "attendees": total_attendees,
        "tickets": total_tickets,
        "confirmed_tickets": confirmed_tickets,
        "total_revenue": total_revenue,
        "avg_ticket_price": avg_ticket_price,
        "total_capacity": total_capacity,
        "available_seats": available_seats,
        "booked_seats": booked_seats
    }

def get_table_names():
    """Returns the ordered list of primary application tables."""
    return ["Venues", "Organizers", "Events", "Attendees", "Tickets", "Payments"]

def get_table_data(table_name: str) -> pd.DataFrame:
    """Fetches all records for a given table."""
    conn = get_connection()
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

def get_table_schema(table_name: str) -> pd.DataFrame:
    """Fetches the schema column details for a given table."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table_name});")
    rows = cur.fetchall()
    conn.close()
    return pd.DataFrame(rows, columns=["CID", "Column Name", "Data Type", "Not Null", "Default Value", "Primary Key"])

# ----------------- CRUD HELPER FUNCTIONS -----------------

def add_event(event_id, event_name, event_date, venue_id, organizer_id, ticket_price, total_seats, available_seats):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Events (event_id, event_name, event_date, venue_id, organizer_id, ticket_price, total_seats, available_seats)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (event_id, event_name, event_date, venue_id, organizer_id, ticket_price, total_seats, available_seats))
    conn.commit()
    conn.close()

def add_attendee(attendee_id, name, email, phone_number):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Attendees (attendee_id, name, email, phone_number)
        VALUES (?, ?, ?, ?)
    """, (attendee_id, name, email if email else None, phone_number))
    conn.commit()
    conn.close()

def book_ticket(ticket_id, event_id, attendee_id, booking_date, status):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Tickets (ticket_id, event_id, attendee_id, booking_date, status)
        VALUES (?, ?, ?, ?, ?)
    """, (ticket_id, event_id, attendee_id, booking_date, status))
    if status == 'Confirmed':
        cur.execute("UPDATE Events SET available_seats = available_seats - 1 WHERE event_id = ? AND available_seats > 0", (event_id,))
    conn.commit()
    conn.close()

def record_payment(payment_id, ticket_id, amount_paid, payment_status, payment_date):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO Payments (payment_id, ticket_id, amount_paid, payment_status, payment_date)
        VALUES (?, ?, ?, ?, ?)
    """, (payment_id, ticket_id, amount_paid, payment_status, payment_date))
    conn.commit()
    conn.close()

def update_ticket_price(event_id, new_price):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE Events SET ticket_price = ? WHERE event_id = ?", (new_price, event_id))
    conn.commit()
    conn.close()

def delete_event(event_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Events WHERE event_id = ?", (event_id,))
    conn.commit()
    conn.close()
