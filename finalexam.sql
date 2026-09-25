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

CREATE TYPE ticket_status_type AS ENUM ('Confirmed', 'Cancelled', 'Pending');

CREATE TABLE Tickets (
    ticket_id INT PRIMARY KEY,
    event_id INT NOT NULL,
    attendee_id INT NOT NULL,
    booking_date TIMESTAMP NOT NULL,
    status ticket_status_type NOT NULL,

    FOREIGN KEY (event_id) REFERENCES Events(event_id),
    FOREIGN KEY (attendee_id) REFERENCES Attendees(attendee_id),

    UNIQUE (event_id, attendee_id)
);

CREATE TYPE payment_status_type AS ENUM ('Success', 'Failed', 'Pending');

CREATE TABLE Payments (
    payment_id INT PRIMARY KEY,
    ticket_id INT NOT NULL,
    amount_paid DECIMAL(10,2) NOT NULL,
    payment_status payment_status_type NOT NULL,
    payment_date TIMESTAMPTZ,

    FOREIGN KEY (ticket_id) REFERENCES Tickets(ticket_id)
);

INSERT INTO Venues
(venue_id, venue_name, location, capacity)
VALUES
(1, 'Riverfront Convention Centre', 'Ahmedabad', 1000),
(2, 'Grand Palace Hall', 'Mumbai', 800),
(3, 'Tech Arena', 'Bangalore', 1200),
(4, 'City Auditorium', 'Delhi', 600),
(5, 'Royal Garden', 'Pune', 500),
(6, 'Sunrise Hall', 'Ahmedabad', 400);

INSERT INTO Organizers
(organizer_id, organizer_name, contact_email, phone_number)
VALUES
(1, '  Raj Events  ', 'raj@events.com', '9876543210'),
(2, 'Dream Productions', 'dream@events.com', '9876543211'),
(3, 'TechConnect', 'tech@events.com', '9876543212'),
(4, 'Global Events', NULL, '9876543213'),
(5, 'Elite Management', 'elite@events.com', '9876543214');

INSERT INTO Events
(event_id, event_name, event_date, venue_id, organizer_id,
 ticket_price, total_seats, available_seats)
VALUES

(1, 'Ahmedabad Music Festival', '2026-12-05 18:00:00',
 1, 1, 1500.00, 1000, 150),

(2, 'Mumbai Business Summit', '2026-11-20 10:00:00',
 2, 2, 2500.00, 800, 450),

(3, 'Bangalore Tech Conference', '2026-12-15 09:00:00',
 3, 3, 3000.00, 1200, 900),

(4, 'Delhi Startup Expo', '2026-10-10 11:00:00',
 4, 4, 1200.00, 600, 500),

(5, 'Pune Food Carnival', '2026-12-25 17:00:00',
 5, 5, 800.00, 500, 80),

(6, 'Ahmedabad Art Exhibition', '2026-09-18 16:00:00',
 6, 1, 500.00, 400, 300),

(7, 'Mumbai Concert Night', '2026-12-30 19:00:00',
 2, 2, 2000.00, 800, 100),

(8, 'Delhi Cultural Festival', '2026-12-12 18:00:00',
 4, 4, 1000.00, 600, 350),

(9, 'Bangalore AI Summit', '2027-01-20 09:30:00',
 3, 3, 3500.00, 1200, 1100),

(10, 'Pune Business Meetup', '2026-08-30 14:00:00',
 5, 5, 600.00, 500, 450);


 INSERT INTO Attendees
(attendee_id, name, email, phone_number)
VALUES

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


INSERT INTO Tickets
(ticket_id, event_id, attendee_id, booking_date, status)
VALUES

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



INSERT INTO Payments
(payment_id, ticket_id, amount_paid, payment_status, payment_date)
VALUES

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





select * from Venues

SELECT * FROM Organizers;

SELECT * FROM Events;

SELECT * FROM Attendees;

SELECT * FROM Tickets;

SELECT * FROM Payments;



-- 1.1
insert into Events
(event_id, event_name, event_date, venue_id, organizer_id,
 ticket_price, total_seats, available_seats)
values
(11, 'Ahmedabad Business Expo', '2026-12-20 10:00:00',
 1, 1, 1800.00, 1000, 1000)

 -- 1.2
select * from Events where event_name like '%Ahmedabad%'

-- 1.3
update Events set ticket_price = 2000.00 where event_id = 11

-- 1.4
delete from Events where event_id = 11



-- 2.1
select e.event_id,e.event_name,e.event_date,v.venue_name,v.location from events e 
inner join venues v on e.venue_id = v.venue_id 
where v.location = 'Ahmedabad' and e.event_date > now()

-- 2.2
select e.event_name,e.ticket_price,count(t.ticket_id) as tick_sold,sum(e.ticket_price) as total_revenue from events e
inner join tickets t on e.event_id = t.event_id
where t.status = 'Confirmed'
group by e.event_id,e.event_name,e.ticket_price
order by total_revenue desc
limit 5

-- 2.3
select a.name,t.ticket_id,t.booking_date from attendees a
inner join tickets t on a.attendee_id = t.attendee_id
where t.booking_date >= NOW() - INTERVAL '7 day'
order by t.booking_date desc



-- 3.1
select e.event_id,e.event_name,e.event_date,e.total_seats,e.available_seats from events e
where extract(month from e.event_date) = 12 and e.available_seats > (e.total_seats * 0.50)

-- 3.2
select distinct a.attendee_id, a.name from attendees a
left join tickets t on a.attendee_id = t.attendee_id
left join payments p on t.ticket_id = p.ticket_id
where t.ticket_id is not null or p.payment_status = 'Pending'

-- 3.3
select event_id,event_name,total_seats,available_seats
from events where not available_seats = 0



-- 4.1
select event_name,event_date,ticket_price
from events order by event_date asc

-- 4.2
select e.event_id,e.event_name,count(t.attendee_id) as total_attendees from events e
left join tickets t on e.event_id = t.event_id
group by e.event_id,e.event_name order by total_attendees desc

-- 4.3
select e.event_id,e.event_name,sum(p.amount_paid)as total_revenue from events e
left join tickets t on e.event_id = t.event_id
left join payments p on t.ticket_id = p.ticket_id and p.payment_status = 'Success'
group by e.event_id,e.event_name
order by total_revenue



-- 5.1
select sum(amount_paid) as total_revenue from payments where payment_status = 'Success'

-- 5.2
select e.event_id,e.event_name, count(t.attendee_id) as total_attendance from events e
left join tickets t on e.event_id = t.event_id
group by e.event_id, e.event_name order by total_attendance

-- 5.3
select avg(ticket_price) as avg_ticket_pri from events



-- 6
-- query written on create table structure



-- 7.1
select e.event_name,e.event_date,v.venue_name,v.location
from events e inner join venues v on e.venue_id = v.venue_id;

-- 7.2
select e.event_name,e.event_date,v.venue_name,v.location
from events e left join venues v on e.venue_id = v.venue_id;

-- 7.3
select e.event_name,e.event_date,v.venue_name,v.location
from events e right join venues v on e.venue_id = v.venue_id;

--7.4
select e.event_name,e.event_date,v.venue_name,v.location
from events e full outer join venues v on e.venue_id = v.venue_id;




-- 8.1
select event_id,event_name,ticket_price from events
where ticket_price > (select avg(ticket_price) from events)

-- 8.2
select attendee_id,name,email from attendees
where attendee_id in
(select attendee_id from tickets group by attendee_id having count(distinct event_id) > 1)

-- 8.3
select organizer_id,organizer_name,contact_email from organizers
where organizer_id in 
(select organizer_id from events group by organizer_id having count(event_id) > 3)




-- 9.1
select event_id,event_name,event_date,extract(month from event_date) as event_month from events

-- 9.2
select event_id,event_name,event_date,(event_date::date - current_date) as days_remaining
from events where event_date::date >= current_date
order by event_date

-- 9.3
select payment_id,ticket_id,payment_status,to_char(payment_date, 'yyyy-mm-dd hh24:mi:ss') as formatted_payment_date from payments;




-- 10.1
select organizer_id,upper(organizer_name) as organizer_name from organizers

-- 10.2
select attendee_id,trim(name) as attendee_name from attendees

-- 10.3
select attendee_id,name,coalesce(email, 'Not Provided') as email from attendees





- 11.1
select e.event_id,e.event_name,
rank() over (order by coalesce(sum(
case
when p.payment_status = 'Success'
then p.amount_paid
else 0
end))) as revenue_rank
from events e
left join tickets t on e.event_id = t.event_id
left join payments p on t.ticket_id = p.ticket_id
group by e.event_id,e.event_name
order by revenue_rank 

-- 11.2
select t.ticket_id,t.event_id,t.booking_date,t.status,
count(*) over (order by t.booking_date) as cumulative_ticket_sales
from tickets t
order by t.booking_date

-- 11.3
select event_id,event_name,total_attendees,sum(total_attendees) 
over (order by event_id) as running_total_attendees
from (select e.event_id,e.event_name,count(t.attendee_id) as total_attendees from events e
left join tickets t on e.event_id = t.event_id
group by e.event_id,e.event_name) as event_attendees
order by event_id




-- 12.1
select event_id,event_name,total_seats,available_seats,
case
when available_seats < (total_seats * 0.20)
then 'high demand'
when available_seats < (total_seats * 0.50)
then 'moderate demand'
else 'low demand'
end as demand_category from events

-- 12.2
select payment_id,ticket_id,amount_paid,payment_status,
case
when payment_status = 'Success'
then 'successful'
when payment_status = 'Failed'
then 'failed'
else 'pending'
end as payment_category from payments



