# API Documentation
**Project:** AI-Enhanced Flight Booking System
**Author:** Mohammed Adnan Mohiuddin

---

## 1. Authentication Endpoints

### 1.1 User Registration
*   **Endpoint**: `/register`
*   **Method**: `POST`
*   **Description**: Registers a new user (Passenger or Admin) and encrypts the password.
*   **Parameters (Form Data)**:
    *   `name` (string): Full name of the user.
    *   `email` (string): Unique email address.
    *   `phone` (string): Contact number.
    *   `password` (string): User password.
    *   `confirm_password` (string): Password confirmation.
*   **Response**: 
    *   Success: Redirects to `/login` with success flash message.
    *   Failure: Renders `register.html` with error flash message.

### 1.2 User Login
*   **Endpoint**: `/login`
*   **Method**: `POST`
*   **Description**: Authenticates user credentials using Werkzeug's security hashing.
*   **Parameters (Form Data)**:
    *   `email` (string): Registered email address.
    *   `password` (string): User password.
    *   `remember` (boolean): Remember me session toggle.
*   **Response**:
    *   Success: Redirects to `/dashboard` (User) or `/admin/dashboard` (Admin).
    *   Failure: Renders `login.html` with error flash message.

---

## 2. Flight Search and Booking Endpoints

### 2.1 Search Flights
*   **Endpoint**: `/flights`
*   **Method**: `GET`
*   **Description**: Queries the PostgreSQL database for flights matching the search criteria.
*   **Query Parameters**:
    *   `source` (string): Origin airport code (e.g., JFK).
    *   `destination` (string): Destination airport code (e.g., LAX).
    *   `departure_date` (date string): Format YYYY-MM-DD.
    *   `travel_class` (string): Economy, Premium Economy, Business, or First Class.
    *   `passengers` (integer): Number of passengers.
*   **Response**: Renders `search_results.html` containing flight objects and dynamic price calculations based on travel class.

### 2.2 Initialize Booking
*   **Endpoint**: `/book-flight`
*   **Method**: `GET`
*   **Description**: Prepares the booking UI for a specific flight. Fetches occupied seats to block them on the seat map.
*   **Query Parameters**:
    *   `flight_id` (integer): ID of the selected flight.
*   **Response**: Renders `booking.html` passing the flight details and an array of `occupied_seats`.

### 2.3 Process Booking
*   **Endpoint**: `/process-booking`
*   **Method**: `POST`
*   **Description**: Validates the seat selection and prepares the transaction for the payment gateway.
*   **Parameters (Form Data)**:
    *   `flight_id`, `seat_number`, `passenger_name`, `passenger_age`, `passenger_gender`.
*   **Response**: Renders `payment.html` with the calculated total amount.

### 2.4 Finalize Payment
*   **Endpoint**: `/confirm-payment`
*   **Method**: `POST`
*   **Description**: Processes the mock payment, commits the Booking, SeatReservation, and Payment records to the database.
*   **Response**: Redirects to `/success` with the generated PNR number.

### 2.5 Cancel Booking
*   **Endpoint**: `/cancel-booking`
*   **Method**: `POST`
*   **Description**: Cancels an active booking, frees the reserved seat, and updates the flight occupancy.
*   **Parameters (Form Data)**:
    *   `booking_id` (integer).
*   **Response**: Redirects to `/dashboard` with cancellation success message.

---

## 3. Artificial Intelligence Endpoints

### 3.1 Machine Learning Flight Recommendation
*   **Endpoint**: `/recommend-flight`
*   **Method**: `POST`
*   **Description**: Utilizes a trained Scikit-Learn Random Forest model to predict the most suitable airline for a user based on context.
*   **Parameters (JSON / Form Data)**:
    *   `source` (string), `destination` (string), `travel_month` (integer).
*   **Response**: 
    *   Returns the predicted `airline` string via the UI.

### 3.2 Generative AI Travel Summary
*   **Endpoint**: `/generate-summary`
*   **Method**: `POST`
*   **Description**: Calls the Google Gemini API to generate a professional travel itinerary, packing tips, and destination highlights.
*   **Parameters (Form Data)**:
    *   `source` (string), `destination` (string), `travel_class` (string).
*   **Response**: Renders `ai_recommendations.html` injecting the markdown-formatted AI response.

---

## 4. Utility Endpoints

### 4.1 Download PDF Ticket
*   **Endpoint**: `/download-ticket/<pnr>`
*   **Method**: `GET`
*   **Description**: Dynamically generates a PDF boarding pass using ReportLab.
*   **Response**: Triggers an HTTP file download (`attachment; filename=Ticket_<pnr>.pdf`).

---

## 5. Admin Endpoints

### 5.1 Admin Dashboard
*   **Endpoint**: `/admin/dashboard`
*   **Method**: `GET`
*   **Description**: Fetches aggregate statistics (total revenue, active flights, total bookings) for the Chart.js visualizations.
*   **Response**: Renders `admin_dashboard.html`.

### 5.2 Manage Flights
*   **Endpoint**: `/admin/flights`
*   **Method**: `GET`, `POST`
*   **Description**: CRUD operations for managing the flight inventory. Only accessible to users with the 'Admin' role.
