PROJECT_QUERIES = [
    # -------------------------------------------------------------
    # SECTION 1: CRUD & DATA MANIPULATION
    # -------------------------------------------------------------
    {
        "id": "q1_1",
        "question_num": "1.1",
        "title": "1.1 Insert New Event",
        "category": "1. Data Manipulation (CRUD)",
        "description": "Inserts a new event ('Ahmedabad Business Expo') into the Events table with venue and organizer associations.",
        "concepts": ["INSERT INTO", "VALUES", "Relational Integrity"],
        "pg_sql": """INSERT INTO Events
(event_id, event_name, event_date, venue_id, organizer_id,
 ticket_price, total_seats, available_seats)
VALUES
(11, 'Ahmedabad Business Expo', '2026-12-20 10:00:00',
 1, 1, 1800.00, 1000, 1000);""",
        "sql": """INSERT OR REPLACE INTO Events
(event_id, event_name, event_date, venue_id, organizer_id,
 ticket_price, total_seats, available_seats)
VALUES
(11, 'Ahmedabad Business Expo', '2026-12-20 10:00:00',
 1, 1, 1800.00, 1000, 1000);""",
        "visualize_as": None
    },
    {
        "id": "q1_2",
        "question_num": "1.2",
        "title": "1.2 Pattern Search with LIKE",
        "category": "1. Data Manipulation (CRUD)",
        "description": "Searches for all events whose names contain the substring 'Ahmedabad' using pattern matching.",
        "concepts": ["SELECT", "WHERE", "LIKE", "Pattern Matching"],
        "pg_sql": "SELECT * FROM Events WHERE event_name LIKE '%Ahmedabad%';",
        "sql": "SELECT * FROM Events WHERE event_name LIKE '%Ahmedabad%';",
        "visualize_as": "table"
    },
    {
        "id": "q1_3",
        "question_num": "1.3",
        "title": "1.3 Update Event Ticket Price",
        "category": "1. Data Manipulation (CRUD)",
        "description": "Updates the ticket price to 2000.00 for the newly inserted event (event_id = 11).",
        "concepts": ["UPDATE", "SET", "WHERE"],
        "pg_sql": "UPDATE Events SET ticket_price = 2000.00 WHERE event_id = 11;",
        "sql": "UPDATE Events SET ticket_price = 2000.00 WHERE event_id = 11;",
        "visualize_as": None
    },
    {
        "id": "q1_4",
        "question_num": "1.4",
        "title": "1.4 Delete Event Record",
        "category": "1. Data Manipulation (CRUD)",
        "description": "Safely removes event 11 from the Events table using primary key filtering.",
        "concepts": ["DELETE FROM", "WHERE"],
        "pg_sql": "DELETE FROM Events WHERE event_id = 11;",
        "sql": "DELETE FROM Events WHERE event_id = 11;",
        "visualize_as": None
    },

    # -------------------------------------------------------------
    # SECTION 2: BASIC QUERIES & JOINS
    # -------------------------------------------------------------
    {
        "id": "q2_1",
        "question_num": "2.1",
        "title": "2.1 Upcoming Ahmedabad Events with Venue Info",
        "category": "2. Basic Queries & Joins",
        "description": "Performs an INNER JOIN between Events and Venues to filter for upcoming events located in Ahmedabad.",
        "concepts": ["INNER JOIN", "WHERE", "Date Filtering", "NOW()"],
        "pg_sql": """SELECT e.event_id, e.event_name, e.event_date, v.venue_name, v.location 
FROM Events e 
INNER JOIN Venues v ON e.venue_id = v.venue_id 
WHERE v.location = 'Ahmedabad' AND e.event_date > NOW();""",
        "sql": """SELECT e.event_id, e.event_name, e.event_date, v.venue_name, v.location 
FROM Events e 
INNER JOIN Venues v ON e.venue_id = v.venue_id 
WHERE v.location = 'Ahmedabad' AND e.event_date > NOW();""",
        "visualize_as": "table"
    },
    {
        "id": "q2_2",
        "question_num": "2.2",
        "title": "2.2 Top 5 Events by Confirmed Revenue",
        "category": "2. Basic Queries & Joins",
        "description": "Aggregates confirmed ticket sales per event and calculates total revenue, ordering descending to show top 5 performers.",
        "concepts": ["INNER JOIN", "GROUP BY", "SUM", "COUNT", "ORDER BY", "LIMIT"],
        "pg_sql": """SELECT e.event_name, e.ticket_price, COUNT(t.ticket_id) AS tick_sold, SUM(e.ticket_price) AS total_revenue 
FROM Events e
INNER JOIN Tickets t ON e.event_id = t.event_id
WHERE t.status = 'Confirmed'
GROUP BY e.event_id, e.event_name, e.ticket_price
ORDER BY total_revenue DESC
LIMIT 5;""",
        "sql": """SELECT e.event_name, e.ticket_price, COUNT(t.ticket_id) AS tick_sold, SUM(e.ticket_price) AS total_revenue 
FROM Events e
INNER JOIN Tickets t ON e.event_id = t.event_id
WHERE t.status = 'Confirmed'
GROUP BY e.event_id, e.event_name, e.ticket_price
ORDER BY total_revenue DESC
LIMIT 5;""",
        "visualize_as": "bar"
    },
    {
        "id": "q2_3",
        "question_num": "2.3",
        "title": "2.3 Recent Ticket Bookings (Last 7 Days)",
        "category": "2. Basic Queries & Joins",
        "description": "Retrieves attendee names and booking dates for tickets reserved within the past 7 days relative to the audit timestamp.",
        "concepts": ["INNER JOIN", "Date Math", "INTERVAL", "ORDER BY DESC"],
        "pg_sql": """SELECT a.name, t.ticket_id, t.booking_date 
FROM Attendees a
INNER JOIN Tickets t ON a.attendee_id = t.attendee_id
WHERE t.booking_date >= NOW() - INTERVAL '7 day'
ORDER BY t.booking_date DESC;""",
        "sql": """SELECT a.name, t.ticket_id, t.booking_date 
FROM Attendees a
INNER JOIN Tickets t ON a.attendee_id = t.attendee_id
WHERE t.booking_date >= datetime('2026-08-08 23:59:59', '-7 days')
ORDER BY t.booking_date DESC;""",
        "visualize_as": "table"
    },

    # -------------------------------------------------------------
    # SECTION 3: FILTERING & CONDITIONAL RETRIEVAL
    # -------------------------------------------------------------
    {
        "id": "q3_1",
        "question_num": "3.1",
        "title": "3.1 December Events with > 50% Available Seats",
        "category": "3. Filtering & Conditions",
        "description": "Extracts events scheduled in December that have more than half of their total seating capacity still unsold.",
        "concepts": ["EXTRACT", "MONTH", "Arithmetic Comparison", "WHERE"],
        "pg_sql": """SELECT e.event_id, e.event_name, e.event_date, e.total_seats, e.available_seats 
FROM Events e
WHERE EXTRACT(MONTH FROM e.event_date) = 12 AND e.available_seats > (e.total_seats * 0.50);""",
        "sql": """SELECT e.event_id, e.event_name, e.event_date, e.total_seats, e.available_seats 
FROM Events e
WHERE CAST(strftime('%m', e.event_date) AS INTEGER) = 12 AND e.available_seats > (e.total_seats * 0.50);""",
        "visualize_as": "bar"
    },
    {
        "id": "q3_2",
        "question_num": "3.2",
        "title": "3.2 Distinct Attendees with Active or Pending Bookings",
        "category": "3. Filtering & Conditions",
        "description": "Uses DISTINCT and multi-table LEFT JOINS to identify all attendees who have a ticket assigned or pending payment.",
        "concepts": ["DISTINCT", "LEFT JOIN", "OR Condition", "IS NOT NULL"],
        "pg_sql": """SELECT DISTINCT a.attendee_id, a.name 
FROM Attendees a
LEFT JOIN Tickets t ON a.attendee_id = t.attendee_id
LEFT JOIN Payments p ON t.ticket_id = p.ticket_id
WHERE t.ticket_id IS NOT NULL OR p.payment_status = 'Pending';""",
        "sql": """SELECT DISTINCT a.attendee_id, a.name 
FROM Attendees a
LEFT JOIN Tickets t ON a.attendee_id = t.attendee_id
LEFT JOIN Payments p ON t.ticket_id = p.ticket_id
WHERE t.ticket_id IS NOT NULL OR p.payment_status = 'Pending';""",
        "visualize_as": "table"
    },
    {
        "id": "q3_3",
        "question_num": "3.3",
        "title": "3.3 Events Not Sold Out (Available Seats > 0)",
        "category": "3. Filtering & Conditions",
        "description": "Filters for events that still have seats open using the logical NOT operator on zero availability.",
        "concepts": ["WHERE NOT", "Filtering", "Capacity Check"],
        "pg_sql": """SELECT event_id, event_name, total_seats, available_seats
FROM Events 
WHERE NOT available_seats = 0;""",
        "sql": """SELECT event_id, event_name, total_seats, available_seats
FROM Events 
WHERE NOT available_seats = 0;""",
        "visualize_as": "bar"
    },

    # -------------------------------------------------------------
    # SECTION 4: SORTING & GROUPING
    # -------------------------------------------------------------
    {
        "id": "q4_1",
        "question_num": "4.1",
        "title": "4.1 Chronologically Ordered Events Calendar",
        "category": "4. Sorting & Grouping",
        "description": "Presents all scheduled events sorted chronologically by earliest occurrence date.",
        "concepts": ["SELECT", "ORDER BY ASC"],
        "pg_sql": """SELECT event_name, event_date, ticket_price
FROM Events 
ORDER BY event_date ASC;""",
        "sql": """SELECT event_name, event_date, ticket_price
FROM Events 
ORDER BY event_date ASC;""",
        "visualize_as": "line"
    },
    {
        "id": "q4_2",
        "question_num": "4.2",
        "title": "4.2 Total Attendees per Event (Descending)",
        "category": "4. Sorting & Grouping",
        "description": "Groups tickets by event to count attendee attendance, ordering descending to highlight popularity.",
        "concepts": ["LEFT JOIN", "GROUP BY", "COUNT", "ORDER BY DESC"],
        "pg_sql": """SELECT e.event_id, e.event_name, COUNT(t.attendee_id) AS total_attendees 
FROM Events e
LEFT JOIN Tickets t ON e.event_id = t.event_id
GROUP BY e.event_id, e.event_name 
ORDER BY total_attendees DESC;""",
        "sql": """SELECT e.event_id, e.event_name, COUNT(t.attendee_id) AS total_attendees 
FROM Events e
LEFT JOIN Tickets t ON e.event_id = t.event_id
GROUP BY e.event_id, e.event_name 
ORDER BY total_attendees DESC;""",
        "visualize_as": "bar"
    },
    {
        "id": "q4_3",
        "question_num": "4.3",
        "title": "4.3 Total Successful Revenue Generated per Event",
        "category": "4. Sorting & Grouping",
        "description": "Aggregates only successful payment transactions per event to calculate exact realized revenue, ordered ascending.",
        "concepts": ["3-Table Join", "SUM", "Conditional Join", "GROUP BY"],
        "pg_sql": """SELECT e.event_id, e.event_name, SUM(p.amount_paid) AS total_revenue 
FROM Events e
LEFT JOIN Tickets t ON e.event_id = t.event_id
LEFT JOIN Payments p ON t.ticket_id = p.ticket_id AND p.payment_status = 'Success'
GROUP BY e.event_id, e.event_name
ORDER BY total_revenue;""",
        "sql": """SELECT e.event_id, e.event_name, COALESCE(SUM(p.amount_paid), 0) AS total_revenue 
FROM Events e
LEFT JOIN Tickets t ON e.event_id = t.event_id
LEFT JOIN Payments p ON t.ticket_id = p.ticket_id AND p.payment_status = 'Success'
GROUP BY e.event_id, e.event_name
ORDER BY total_revenue;""",
        "visualize_as": "bar"
    },

    # -------------------------------------------------------------
    # SECTION 5: AGGREGATE FUNCTIONS
    # -------------------------------------------------------------
    {
        "id": "q5_1",
        "question_num": "5.1",
        "title": "5.1 Overall Successful Revenue Across Platform",
        "category": "5. Aggregate Functions",
        "description": "Calculates the grand total of all successful payment transactions across all events.",
        "concepts": ["SUM", "WHERE Filter", "Financial Metric"],
        "pg_sql": "SELECT SUM(amount_paid) AS total_revenue FROM Payments WHERE payment_status = 'Success';",
        "sql": "SELECT SUM(amount_paid) AS total_revenue FROM Payments WHERE payment_status = 'Success';",
        "visualize_as": "metric"
    },
    {
        "id": "q5_2",
        "question_num": "5.2",
        "title": "5.2 Event Attendance Counts (Ascending)",
        "category": "5. Aggregate Functions",
        "description": "Calculates total attendee counts per event, sorted from least attended to most attended.",
        "concepts": ["COUNT", "GROUP BY", "ORDER BY ASC"],
        "pg_sql": """SELECT e.event_id, e.event_name, COUNT(t.attendee_id) AS total_attendance 
FROM Events e
LEFT JOIN Tickets t ON e.event_id = t.event_id
GROUP BY e.event_id, e.event_name 
ORDER BY total_attendance;""",
        "sql": """SELECT e.event_id, e.event_name, COUNT(t.attendee_id) AS total_attendance 
FROM Events e
LEFT JOIN Tickets t ON e.event_id = t.event_id
GROUP BY e.event_id, e.event_name 
ORDER BY total_attendance;""",
        "visualize_as": "bar"
    },
    {
        "id": "q5_3",
        "question_num": "5.3",
        "title": "5.3 Overall Average Ticket Price",
        "category": "5. Aggregate Functions",
        "description": "Computes the global average ticket price across all events listed in the catalog.",
        "concepts": ["AVG", "Pricing Analytics"],
        "pg_sql": "SELECT AVG(ticket_price) AS avg_ticket_pri FROM Events;",
        "sql": "SELECT ROUND(AVG(ticket_price), 2) AS avg_ticket_pri FROM Events;",
        "visualize_as": "metric"
    },

    # -------------------------------------------------------------
    # SECTION 7: JOINS LABORATORY
    # -------------------------------------------------------------
    {
        "id": "q7_1",
        "question_num": "7.1",
        "title": "7.1 INNER JOIN: Events & Venues",
        "category": "7. Joins Laboratory",
        "description": "Retrieves only events that have a matching venue record defined in the database.",
        "concepts": ["INNER JOIN", "Relational Intersection"],
        "pg_sql": """SELECT e.event_name, e.event_date, v.venue_name, v.location
FROM Events e 
INNER JOIN Venues v ON e.venue_id = v.venue_id;""",
        "sql": """SELECT e.event_name, e.event_date, v.venue_name, v.location
FROM Events e 
INNER JOIN Venues v ON e.venue_id = v.venue_id;""",
        "visualize_as": "table"
    },
    {
        "id": "q7_2",
        "question_num": "7.2",
        "title": "7.2 LEFT JOIN: Events & Venues",
        "category": "7. Joins Laboratory",
        "description": "Retrieves all events regardless of whether a matching venue exists.",
        "concepts": ["LEFT JOIN", "Preserving Left Table"],
        "pg_sql": """SELECT e.event_name, e.event_date, v.venue_name, v.location
FROM Events e 
LEFT JOIN Venues v ON e.venue_id = v.venue_id;""",
        "sql": """SELECT e.event_name, e.event_date, v.venue_name, v.location
FROM Events e 
LEFT JOIN Venues v ON e.venue_id = v.venue_id;""",
        "visualize_as": "table"
    },
    {
        "id": "q7_3",
        "question_num": "7.3",
        "title": "7.3 RIGHT JOIN: Events & Venues",
        "category": "7. Joins Laboratory",
        "description": "Retrieves all venues, including those that currently have no scheduled events.",
        "concepts": ["RIGHT JOIN", "Preserving Right Table", "Unutilized Venues"],
        "pg_sql": """SELECT e.event_name, e.event_date, v.venue_name, v.location
FROM Events e 
RIGHT JOIN Venues v ON e.venue_id = v.venue_id;""",
        "sql": """SELECT e.event_name, e.event_date, v.venue_name, v.location
FROM Events e 
RIGHT JOIN Venues v ON e.venue_id = v.venue_id;""",
        "visualize_as": "table"
    },
    {
        "id": "q7_4",
        "question_num": "7.4",
        "title": "7.4 FULL OUTER JOIN: Events & Venues",
        "category": "7. Joins Laboratory",
        "description": "Demonstrates full outer join, returning all events and all venues, pairing where possible and filling NULLs otherwise.",
        "concepts": ["FULL OUTER JOIN", "Complete Set Union"],
        "pg_sql": """SELECT e.event_name, e.event_date, v.venue_name, v.location
FROM Events e 
FULL OUTER JOIN Venues v ON e.venue_id = v.venue_id;""",
        "sql": """SELECT e.event_name, e.event_date, v.venue_name, v.location
FROM Events e 
FULL OUTER JOIN Venues v ON e.venue_id = v.venue_id;""",
        "visualize_as": "table"
    },

    # -------------------------------------------------------------
    # SECTION 8: SUBQUERIES & NESTED LOGIC
    # -------------------------------------------------------------
    {
        "id": "q8_1",
        "question_num": "8.1",
        "title": "8.1 Events Priced Above Platform Average",
        "category": "8. Subqueries & Nested Logic",
        "description": "Uses a scalar subquery in the WHERE clause to filter for premium events priced higher than the platform average.",
        "concepts": ["Scalar Subquery", "AVG", "WHERE Comparison"],
        "pg_sql": """SELECT event_id, event_name, ticket_price 
FROM Events
WHERE ticket_price > (SELECT AVG(ticket_price) FROM Events);""",
        "sql": """SELECT event_id, event_name, ticket_price 
FROM Events
WHERE ticket_price > (SELECT AVG(ticket_price) FROM Events);""",
        "visualize_as": "bar"
    },
    {
        "id": "q8_2",
        "question_num": "8.2",
        "title": "8.2 Attendees Booked for Multiple Distinct Events",
        "category": "8. Subqueries & Nested Logic",
        "description": "Identifies loyal attendees who have booked tickets for more than one distinct event using a nested GROUP BY with HAVING.",
        "concepts": ["Nested Subquery", "IN Operator", "HAVING COUNT(DISTINCT)"],
        "pg_sql": """SELECT attendee_id, name, email 
FROM Attendees
WHERE attendee_id IN (
    SELECT attendee_id 
    FROM Tickets 
    GROUP BY attendee_id 
    HAVING COUNT(DISTINCT event_id) > 1
);""",
        "sql": """SELECT attendee_id, name, email 
FROM Attendees
WHERE attendee_id IN (
    SELECT attendee_id 
    FROM Tickets 
    GROUP BY attendee_id 
    HAVING COUNT(DISTINCT event_id) > 1
);""",
        "visualize_as": "table"
    },
    {
        "id": "q8_3",
        "question_num": "8.3",
        "title": "8.3 Active Organizers Managing Over 3 Events",
        "category": "8. Subqueries & Nested Logic",
        "description": "Filters for major event production companies managing more than 3 events in the catalog.",
        "concepts": ["Nested Subquery", "GROUP BY", "HAVING", "IN Operator"],
        "pg_sql": """SELECT organizer_id, organizer_name, contact_email 
FROM Organizers
WHERE organizer_id IN (
    SELECT organizer_id 
    FROM Events 
    GROUP BY organizer_id 
    HAVING COUNT(event_id) > 3
);""",
        "sql": """SELECT organizer_id, organizer_name, contact_email 
FROM Organizers
WHERE organizer_id IN (
    SELECT organizer_id 
    FROM Events 
    GROUP BY organizer_id 
    HAVING COUNT(event_id) > 3
);""",
        "visualize_as": "table"
    },

    # -------------------------------------------------------------
    # SECTION 9: DATE & TIME MANIPULATION
    # -------------------------------------------------------------
    {
        "id": "q9_1",
        "question_num": "9.1",
        "title": "9.1 Event Month Extraction",
        "category": "9. Date & Time Functions",
        "description": "Extracts the numerical month value from the event timestamp column for temporal grouping.",
        "concepts": ["EXTRACT", "MONTH", "Date Parsing"],
        "pg_sql": """SELECT event_id, event_name, event_date, 
EXTRACT(MONTH FROM event_date) AS event_month 
FROM Events;""",
        "sql": """SELECT event_id, event_name, event_date, 
CAST(strftime('%m', event_date) AS INTEGER) AS event_month 
FROM Events;""",
        "visualize_as": "table"
    },
    {
        "id": "q9_2",
        "question_num": "9.2",
        "title": "9.2 Days Remaining Countdown to Events",
        "category": "9. Date & Time Functions",
        "description": "Calculates the exact number of days remaining until each upcoming event date.",
        "concepts": ["Date Arithmetic", "Type Casting", "Countdown"],
        "pg_sql": """SELECT event_id, event_name, event_date, 
(event_date::date - current_date) AS days_remaining
FROM Events 
WHERE event_date::date >= current_date
ORDER BY event_date;""",
        "sql": """SELECT event_id, event_name, event_date, 
CAST(julianday(date(event_date)) - julianday('2026-08-08') AS INTEGER) AS days_remaining
FROM Events 
WHERE date(event_date) >= '2026-08-08'
ORDER BY event_date;""",
        "visualize_as": "bar"
    },
    {
        "id": "q9_3",
        "question_num": "9.3",
        "title": "9.3 Formatted Payment Timestamps",
        "category": "9. Date & Time Functions",
        "description": "Formats payment timestamps into standardized 'YYYY-MM-DD HH24:MI:SS' string representations.",
        "concepts": ["TO_CHAR", "String Formatting", "Timestamps"],
        "pg_sql": """SELECT payment_id, ticket_id, payment_status, 
TO_CHAR(payment_date, 'yyyy-mm-dd hh24:mi:ss') AS formatted_payment_date 
FROM Payments;""",
        "sql": """SELECT payment_id, ticket_id, payment_status, 
strftime('%Y-%m-%d %H:%M:%S', payment_date) AS formatted_payment_date 
FROM Payments;""",
        "visualize_as": "table"
    },

    # -------------------------------------------------------------
    # SECTION 10: STRING MANIPULATION
    # -------------------------------------------------------------
    {
        "id": "q10_1",
        "question_num": "10.1",
        "title": "10.1 Uppercase Organizer Names",
        "category": "10. String Functions",
        "description": "Applies the UPPER() function to standardize organizer company names in capital letters.",
        "concepts": ["UPPER", "String Normalization"],
        "pg_sql": "SELECT organizer_id, UPPER(organizer_name) AS organizer_name FROM Organizers;",
        "sql": "SELECT organizer_id, UPPER(organizer_name) AS organizer_name FROM Organizers;",
        "visualize_as": "table"
    },
    {
        "id": "q10_2",
        "question_num": "10.2",
        "title": "10.2 Trim Whitespace from Attendee Names",
        "category": "10. String Functions",
        "description": "Removes leading and trailing spaces from attendee name strings (e.g., '  Aarav Sharma  ' -> 'Aarav Sharma').",
        "concepts": ["TRIM", "Data Cleansing"],
        "pg_sql": "SELECT attendee_id, TRIM(name) AS attendee_name FROM Attendees;",
        "sql": "SELECT attendee_id, TRIM(name) AS attendee_name FROM Attendees;",
        "visualize_as": "table"
    },
    {
        "id": "q10_3",
        "question_num": "10.3",
        "title": "10.3 Coalesce Missing Email Addresses",
        "category": "10. String Functions",
        "description": "Replaces NULL values in attendee email fields with the fallback label 'Not Provided' using COALESCE().",
        "concepts": ["COALESCE", "NULL Handling", "Defensive Querying"],
        "pg_sql": "SELECT attendee_id, name, COALESCE(email, 'Not Provided') AS email FROM Attendees;",
        "sql": "SELECT attendee_id, name, COALESCE(email, 'Not Provided') AS email FROM Attendees;",
        "visualize_as": "table"
    },

    # -------------------------------------------------------------
    # SECTION 11: ANALYTICAL WINDOW FUNCTIONS
    # -------------------------------------------------------------
    {
        "id": "q11_1",
        "question_num": "11.1",
        "title": "11.1 Event Revenue Ranking with RANK()",
        "category": "11. Analytical Window Functions",
        "description": "Calculates revenue per event and ranks them dynamically using the RANK() analytical window function.",
        "concepts": ["RANK() OVER", "CASE WHEN", "COALESCE", "Window Functions"],
        "pg_sql": """SELECT e.event_id, e.event_name,
RANK() OVER (ORDER BY COALESCE(SUM(
    CASE
        WHEN p.payment_status = 'Success' THEN p.amount_paid
        ELSE 0
    END), 0) DESC) AS revenue_rank
FROM Events e
LEFT JOIN Tickets t ON e.event_id = t.event_id
LEFT JOIN Payments p ON t.ticket_id = p.ticket_id
GROUP BY e.event_id, e.event_name
ORDER BY revenue_rank;""",
        "sql": """SELECT e.event_id, e.event_name,
RANK() OVER (ORDER BY COALESCE(SUM(
    CASE
        WHEN p.payment_status = 'Success' THEN p.amount_paid
        ELSE 0
    END), 0) DESC) AS revenue_rank
FROM Events e
LEFT JOIN Tickets t ON e.event_id = t.event_id
LEFT JOIN Payments p ON t.ticket_id = p.ticket_id
GROUP BY e.event_id, e.event_name
ORDER BY revenue_rank;""",
        "visualize_as": "bar"
    },
    {
        "id": "q11_2",
        "question_num": "11.2",
        "title": "11.2 Cumulative Ticket Sales Over Time",
        "category": "11. Analytical Window Functions",
        "description": "Calculates the running cumulative count of tickets booked in chronological order using COUNT(*) OVER.",
        "concepts": ["COUNT(*) OVER", "Cumulative Metrics", "Time Series Analysis"],
        "pg_sql": """SELECT t.ticket_id, t.event_id, t.booking_date, t.status,
COUNT(*) OVER (ORDER BY t.booking_date) AS cumulative_ticket_sales
FROM Tickets t
ORDER BY t.booking_date;""",
        "sql": """SELECT t.ticket_id, t.event_id, t.booking_date, t.status,
COUNT(*) OVER (ORDER BY t.booking_date) AS cumulative_ticket_sales
FROM Tickets t
ORDER BY t.booking_date;""",
        "visualize_as": "line"
    },
    {
        "id": "q11_3",
        "question_num": "11.3",
        "title": "11.3 Running Total of Attendees Across Events",
        "category": "11. Analytical Window Functions",
        "description": "Calculates running totals of attendees across events using a subquery and SUM(...) OVER (ORDER BY event_id).",
        "concepts": ["SUM() OVER", "Subquery", "Running Total"],
        "pg_sql": """SELECT event_id, event_name, total_attendees, 
SUM(total_attendees) OVER (ORDER BY event_id) AS running_total_attendees
FROM (
    SELECT e.event_id, e.event_name, COUNT(t.attendee_id) AS total_attendees 
    FROM Events e
    LEFT JOIN Tickets t ON e.event_id = t.event_id
    GROUP BY e.event_id, e.event_name
) AS event_attendees
ORDER BY event_id;""",
        "sql": """SELECT event_id, event_name, total_attendees, 
SUM(total_attendees) OVER (ORDER BY event_id) AS running_total_attendees
FROM (
    SELECT e.event_id, e.event_name, COUNT(t.attendee_id) AS total_attendees 
    FROM Events e
    LEFT JOIN Tickets t ON e.event_id = t.event_id
    GROUP BY e.event_id, e.event_name
) AS event_attendees
ORDER BY event_id;""",
        "visualize_as": "line"
    },

    # -------------------------------------------------------------
    # SECTION 12: CONDITIONAL CLASSIFICATION (CASE)
    # -------------------------------------------------------------
    {
        "id": "q12_1",
        "question_num": "12.1",
        "title": "12.1 Dynamic Seat Demand Tiers",
        "category": "12. Conditional Logic (CASE)",
        "description": "Classifies events into 'high demand' (<20% seats left), 'moderate demand' (<50%), or 'low demand' dynamically.",
        "concepts": ["CASE WHEN", "Capacity Thresholds", "Business Tiers"],
        "pg_sql": """SELECT event_id, event_name, total_seats, available_seats,
CASE
    WHEN available_seats < (total_seats * 0.20) THEN 'high demand'
    WHEN available_seats < (total_seats * 0.50) THEN 'moderate demand'
    ELSE 'low demand'
END AS demand_category 
FROM Events;""",
        "sql": """SELECT event_id, event_name, total_seats, available_seats,
CASE
    WHEN available_seats < (total_seats * 0.20) THEN 'high demand'
    WHEN available_seats < (total_seats * 0.50) THEN 'moderate demand'
    ELSE 'low demand'
END AS demand_category 
FROM Events;""",
        "visualize_as": "pie"
    },
    {
        "id": "q12_2",
        "question_num": "12.2",
        "title": "12.2 Payment Health Status Categorization",
        "category": "12. Conditional Logic (CASE)",
        "description": "Maps raw payment status values into readable business categories ('successful', 'failed', 'pending') using CASE.",
        "concepts": ["CASE WHEN", "Data Categorization", "Status Normalization"],
        "pg_sql": """SELECT payment_id, ticket_id, amount_paid, payment_status,
CASE
    WHEN payment_status = 'Success' THEN 'successful'
    WHEN payment_status = 'Failed' THEN 'failed'
    ELSE 'pending'
END AS payment_category 
FROM Payments;""",
        "sql": """SELECT payment_id, ticket_id, amount_paid, payment_status,
CASE
    WHEN payment_status = 'Success' THEN 'successful'
    WHEN payment_status = 'Failed' THEN 'failed'
    ELSE 'pending'
END AS payment_category 
FROM Payments;""",
        "visualize_as": "pie"
    }
]
