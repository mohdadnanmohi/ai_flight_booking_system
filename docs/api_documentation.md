# API Documentation

This document describes all API endpoints and page view routes implemented in the Flask backend server.

---

## Authentication & Authorization Gate
Several routes require user authentication session state. Authentication is verified using `Flask-Login` cookies. Admin routes enforce an additional check: `current_user.role == 'Admin'`.

---

## Endpoint List

### 1. User Authentication

#### `POST /register`
Creates a new customer account.
- **Request Type**: HTML Form Data
- **Fields**:
  - `name` (string): Full name
  - `email` (string): Unique email address
  - `phone` (string): Contact number
  - `password` (string): Raw password
  - `confirm_password` (string): Password confirmation check
  - `role` (string): 'User' or 'Admin'
- **Response**: Redirect to `/login` on success, or reload register page with error flash message.

#### `POST /login`
Authenticates user and begins session.
- **Request Type**: HTML Form Data
- **Fields**:
  - `email` (string): Registered email
  - `password` (string): Password
  - `remember` (checkbox value): Keep user session active
- **Response**: Redirect to `/admin/dashboard` for administrators, `/dashboard` for standard passengers, or reload login page on credential failure.

#### `GET /logout`
Terminates user session.
- **Response**: Redirect to `/` (Home page) with a success flash notice.

---

### 2. Flight Search & Booking

#### `GET /flights`
Searches scheduled flights matching route parameters.
- **Query Parameters**:
  - `source` (string): Origin airport code (e.g. JFK)
  - `destination` (string): Destination airport code (e.g. LAX)
  - `departure_date` (string): YYYY-MM-DD date filter
  - `passengers` (integer): Passengers count
  - `travel_class` (string): 'Economy', 'Premium Economy', 'Business', 'First Class'
- **Response**: Renders `search_results.html` showing matching flights with applied price multipliers.

#### `POST /process-booking`
Validates traveler details, selects seat number, and routes to payment gateway simulator.
- **Request Type**: HTML Form Data
- **Fields**:
  - `flight_id` (integer): Target flight ID
  - `travel_class` (string): Selected class
  - `travel_date` (string): YYYY-MM-DD
  - `passenger_name` (string): Passenger full name
  - `passenger_age` (integer): Passenger age
  - `passenger_gender` (string): 'Male', 'Female', or 'Other'
  - `passenger_email` (string): Contact email
  - `passenger_phone` (string): Contact number
  - `seat_number` (string): Alphanumeric seat identifier (e.g. 12A)
- **Response**: Renders `payment.html` with calculated pricing.

#### `POST /process-payment`
Simulates transaction approval and commits database records on successful execution.
- **Request Type**: HTML Form Data
- **Fields**:
  - `flight_id`, `travel_class`, `travel_date`, `passenger_name`, `passenger_age`, `passenger_gender`, `seat_number`, `amount`
  - `payment_method` (string): 'UPI', 'Credit Card', 'Debit Card', 'Net Banking'
  - `simulated_status` (string): 'Success' or 'Failed'
- **Response**: Renders `payment_status.html` with generated PNR on success, or a diagnostic page on failure.

#### `POST /cancel-booking`
Cancels booking status and releases reserved seat.
- **Fields**:
  - `booking_id` (integer): Booking ID to cancel
- **Response**: Releases seat reservation, decrements flight booked seats, and redirects to Dashboard with success confirmation.

#### `GET /download-ticket/<pnr>`
Generates and downloads a PDF ticket using ReportLab.
- **Parameters**:
  - `pnr` (string): Unique 8-character booking PNR
- **Response**: `application/pdf` binary download stream containing boarding pass formatting, PNR details, and vertical mock barcode.

---

### 3. Machine Learning & Generative AI

#### `GET /recommend-flight`
Renders predictions query panel.

#### `POST /recommend-flight`
Runs Random Forest inference.
- **Fields**:
  - `source`, `destination` (string): Origin/Dest codes
  - `budget` (integer): Maximum target ticket price
  - `travel_class` (string): Cabin class
  - `travel_time` (string): 'Morning', 'Afternoon', 'Evening', 'Night'
  - `preferred_airline` (string): Preferred airline option
- **Response**: Renders recommendation target label, model confidence score, logs record in DB, and queries actual matching flights.

#### `POST /generate-summary`
Invokes Generative AI advice using the Gemini API.
- **Fields**:
  - `source`, `destination` (string): Origin/Dest codes
  - `travel_class` (string): Cabin class
- **Response**: Invokes Gemini API (or Mock fallback), converts markdown tips to HTML elements, and renders `travel_summary.html`.

---

### 4. Admin Management Console

#### `GET /admin/dashboard`
Aggregates total counters, builds datasets for revenue/occupancy charts, and gathers transactions.
- **Response**: Renders Chart.js visuals and full bookings log table.

#### `POST /admin/add-flight`
Creates a flight schedule.
- **Fields**:
  - `flight_number` (string), `airline` (string), `source` (string), `destination` (string), `departure_time` (datetime-local), `arrival_time` (datetime-local), `seats` (integer), `price` (decimal)
- **Response**: Commits flight record and redirects to flight list.

#### `POST /admin/update-flight`
Updates flight scheduling, seat count, or status ('Scheduled', 'Delayed', 'Cancelled', 'Completed').
- **Fields**:
  - `flight_id` (integer) + updated flight fields
- **Response**: Saves modifications and updates status indicators.

#### `POST /admin/delete-flight`
Deletes a flight listing.
- **Fields**:
  - `flight_id` (integer)
- **Response**: Deletes flight, triggers cascading reservation deletion, and redirects.
