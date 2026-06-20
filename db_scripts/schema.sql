-- AI-Enhanced Flight Booking System Database Schema (Supabase PostgreSQL)

-- 1. Users Table (Handles Passengers and Administrators)
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'User' CHECK (role IN ('User', 'Admin')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Flights Table (Maintains Flight Schedule and Availability)
CREATE TABLE IF NOT EXISTS flights (
    flight_id SERIAL PRIMARY KEY,
    flight_number VARCHAR(20) UNIQUE NOT NULL,
    airline VARCHAR(100) NOT NULL,
    source VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    departure_time TIMESTAMP NOT NULL,
    arrival_time TIMESTAMP NOT NULL,
    seats INTEGER NOT NULL,
    booked_seats INTEGER DEFAULT 0,
    price DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'Scheduled' CHECK (status IN ('Scheduled', 'Delayed', 'Cancelled', 'Completed'))
);

-- 3. Bookings Table (Manages Flight Tickets and Passenger Names)
CREATE TABLE IF NOT EXISTS bookings (
    booking_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    flight_id INTEGER NOT NULL REFERENCES flights(flight_id) ON DELETE CASCADE,
    pnr VARCHAR(10) UNIQUE NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    travel_date DATE NOT NULL,
    passenger_name VARCHAR(100) NOT NULL,
    passenger_age INTEGER,
    passenger_gender VARCHAR(20),
    status VARCHAR(20) DEFAULT 'Booked' CHECK (status IN ('Booked', 'Cancelled'))
);

-- 4. Seat Reservations Table (Tracks Reserved Seat Numbers per Booking)
CREATE TABLE IF NOT EXISTS seat_reservations (
    reservation_id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL REFERENCES bookings(booking_id) ON DELETE CASCADE,
    flight_id INTEGER NOT NULL REFERENCES flights(flight_id) ON DELETE CASCADE,
    seat_number VARCHAR(5) NOT NULL
);

-- 5. Payments Table (Simulates Payment Gateways and Transaction History)
CREATE TABLE IF NOT EXISTS payments (
    payment_id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL REFERENCES bookings(booking_id) ON DELETE CASCADE,
    amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    transaction_id VARCHAR(100) UNIQUE NOT NULL,
    payment_status VARCHAR(20) NOT NULL CHECK (payment_status IN ('Success', 'Failed'))
);

-- 6. Recommendations Table (Saves Historical ML Inference Predictions)
CREATE TABLE IF NOT EXISTS recommendations (
    recommendation_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    predicted_airline VARCHAR(100) NOT NULL,
    confidence_score DECIMAL(5, 2) NOT NULL,
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Database Performance Indexes
CREATE INDEX IF NOT EXISTS idx_source_destination ON flights(source, destination);
CREATE INDEX IF NOT EXISTS idx_booking_user ON bookings(user_id);
CREATE INDEX IF NOT EXISTS idx_flight_number ON flights(flight_number);
