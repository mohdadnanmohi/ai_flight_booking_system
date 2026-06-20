-- Seed Data for AI-Enhanced Flight Booking System (Supabase PostgreSQL)

-- 1. Insert Default Users (Passwords are pre-hashed using scrypt/pbkdf2 for 'admin123' and 'passenger123')
-- Admin Password hash corresponds to 'admin123'
-- User Password hash corresponds to 'passenger123'
INSERT INTO users (name, email, phone, password, role, created_at)
VALUES 
('System Admin', 'admin@flight.com', '+15550199', 'scrypt:32768:8:1$yXk02G7h$bf6164d1f2e032128cebf9ee5108d4b3b3a32f913d80339d27376e3381a3d906e5d8ec11cfcfb7d07936a28723f5b081beeb4fde7a652c79f976a47de02c8c69', 'Admin', CURRENT_TIMESTAMP),
('John Doe', 'passenger@example.com', '+15550122', 'scrypt:32768:8:1$yXk02G7h$bf6164d1f2e032128cebf9ee5108d4b3b3a32f913d80339d27376e3381a3d906e5d8ec11cfcfb7d07936a28723f5b081beeb4fde7a652c79f976a47de02c8c69', 'User', CURRENT_TIMESTAMP)
ON CONFLICT (email) DO NOTHING;

-- 2. Insert Default Flights
INSERT INTO flights (flight_number, airline, source, destination, departure_time, arrival_time, seats, booked_seats, price, status)
VALUES
('EK-201', 'Emirates', 'JFK', 'DXB', '2026-07-15 08:30:00', '2026-07-16 05:30:00', 350, 4, 1250.00, 'Scheduled'),
('EK-202', 'Emirates', 'DXB', 'JFK', '2026-07-20 14:00:00', '2026-07-20 20:30:00', 350, 0, 1100.00, 'Scheduled'),
('DL-142', 'Delta Air Lines', 'JFK', 'LAX', '2026-07-15 09:00:00', '2026-07-15 12:15:00', 180, 2, 350.00, 'Scheduled'),
('DL-143', 'Delta Air Lines', 'LAX', 'JFK', '2026-07-18 16:30:00', '2026-07-18 23:45:00', 180, 0, 380.00, 'Scheduled'),
('SQ-308', 'Singapore Airlines', 'LHR', 'SIN', '2026-07-16 11:30:00', '2026-07-17 07:30:00', 250, 1, 950.00, 'Scheduled'),
('SQ-309', 'Singapore Airlines', 'SIN', 'LHR', '2026-07-22 23:05:00', '2026-07-23 05:45:00', 250, 0, 1020.00, 'Scheduled'),
('BA-117', 'British Airways', 'LHR', 'JFK', '2026-07-16 08:20:00', '2026-07-16 11:05:00', 280, 1, 620.00, 'Scheduled'),
('BA-118', 'British Airways', 'JFK', 'LHR', '2026-07-21 18:30:00', '2026-07-22 06:30:00', 280, 0, 580.00, 'Scheduled'),
('6E-5321', 'IndiGo', 'BOM', 'DEL', '2026-07-15 06:00:00', '2026-07-15 08:10:00', 180, 2, 90.00, 'Scheduled'),
('6E-5322', 'IndiGo', 'DEL', 'BOM', '2026-07-15 18:45:00', '2026-07-15 21:00:00', 180, 0, 85.00, 'Scheduled'),
('AI-101', 'Air India', 'DEL', 'JFK', '2026-07-17 01:45:00', '2026-07-17 07:25:00', 300, 1, 850.00, 'Scheduled'),
('QF-11', 'Qantas', 'SYD', 'LAX', '2026-07-16 09:50:00', '2026-07-16 06:40:00', 320, 0, 1400.00, 'Scheduled'),
('JL-006', 'Japan Airlines', 'HND', 'JFK', '2026-07-16 10:40:00', '2026-07-16 10:45:00', 240, 0, 1280.00, 'Scheduled')
ON CONFLICT (flight_number) DO NOTHING;

-- 3. Insert Sample Bookings for User 2 (passenger@example.com)
-- Assume User 2 ID is 2, Flight 1 (EK-201) ID is 1, Flight 3 (DL-142) ID is 3
INSERT INTO bookings (booking_id, user_id, flight_id, pnr, booking_date, travel_date, passenger_name, passenger_age, passenger_gender, status)
VALUES
(1, 2, 1, 'PNR55421', '2026-06-10 11:30:00', '2026-07-15', 'John Doe', 32, 'Male', 'Booked'),
(2, 2, 3, 'PNR32014', '2026-06-11 09:15:00', '2026-07-15', 'Jane Doe', 28, 'Female', 'Booked')
ON CONFLICT (pnr) DO NOTHING;

-- 4. Insert Seat Reservations
INSERT INTO seat_reservations (booking_id, flight_id, seat_number)
VALUES
(1, 1, '12A'),
(1, 1, '12B'),
(2, 3, '04C')
ON CONFLICT DO NOTHING;

-- 5. Insert Sample Payments
INSERT INTO payments (booking_id, amount, payment_method, transaction_id, payment_status)
VALUES
(1, 2500.00, 'Credit Card', 'TXN-998877112', 'Success'),
(2, 350.00, 'UPI', 'TXN-334455667', 'Success')
ON CONFLICT (transaction_id) DO NOTHING;
