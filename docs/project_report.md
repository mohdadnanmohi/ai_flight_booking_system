# Project Report: AI-Enhanced Flight Booking System

## 1. Executive Summary
The AI-Enhanced Flight Booking System is a full-stack, enterprise-grade travel platform designed to automate flight searches, bookings, passenger reservations, seat selection, and payment simulations. It integrates a **Random Forest Classifier** machine learning model to recommend airlines based on user travel histories and budget parameters, and leverages the **Google Gemini API** to generate travel summaries and traveler advice.

---

## 2. Problem Statement
Traditional travel reservation sites are transactional, requiring users to manually compare airline policies, cost patterns, and routes. This project addresses these shortcomings by:
1. **Intelligent Personalization**: Recommending carriers using machine learning models trained on seasonal booking factors.
2. **Generative Insights**: Synthesizing context-sensitive traveler suggestions (layover alerts, checked baggage guides) via LLMs.
3. **Structured UI/UX**: Creating a modern, airline-inspired, glassmorphic layout displaying real-time analytics.

---

## 3. Database Architecture (Supabase PostgreSQL)
The schema is designed to enforce relational integrity and maximize search speed.

### Tables Overview
- **`users`**: Manages customer details and divides credentials into `User` and `Admin` roles.
- **`flights`**: Holds route listings, scheduled timings, capacity bounds, and real-time status.
- **`bookings`**: Connects users to flights, storing passenger-specific info for group bookings.
- **`seat_reservations`**: Tracks occupied seats to prevent double-booking.
- **`payments`**: Records simulated gateway transactions with generated IDs.
- **`recommendations`**: Logs historical predictions to track model usage.

### Optimization Indexes
We created the following indexes on Supabase to optimize performance:
- `idx_source_destination` on `flights(source, destination)` - Speeds up flight search queries.
- `idx_booking_user` on `bookings(user_id)` - Accelerates dashboard history fetching.
- `idx_flight_number` on `flights(flight_number)` - Optimizes schedule lookups.

---

## 4. Machine Learning Module
We implemented a **Random Forest Classifier** to predict the recommended airline.

### Feature Selection
The feature vector contains 10 dimensions:
1. **Source** (Categorical, Label Encoded)
2. **Destination** (Categorical, Label Encoded)
3. **Ticket Price** (Numerical)
4. **Travel Month** (Numerical)
5. **Airline** (Categorical, Label Encoded)
6. **Travel Time** (Categorical, Label Encoded)
7. **Booking Frequency** (Numerical)
8. **Preferred Airline** (Categorical, Label Encoded)
9. **Travel Class** (Categorical, Label Encoded)
10. **Previous Bookings** (Numerical)

### Model Mechanics & Accuracy
- **Algorithm**: The Random Forest Classifier aggregates decision trees, which reduces overfitting on categorical label mappings.
- **Accuracy**: The model achieves >80% accuracy during cross-validation due to generated correlation parameters (budget class matching, seasonal preferences).

---

## 5. Generative AI Module (Gemini API)
- **Model**: `gemini-1.5-flash`
- **Utility**: Generates unstructured traveler recommendations.
- **Fallback Design**: A mock generator compiles matching structured advice if no API key is configured, ensuring the application remains robust.

---

## 6. System Walkthrough
1. **E2E Booking**: Search $\rightarrow$ Select Flight $\rightarrow$ Input Passengers $\rightarrow$ Pick Seats $\rightarrow$ Simulate UPI/Card Payment $\rightarrow$ Download PDF Boarding Pass.
2. **Admin Flow**: Dashboard charts (Revenue, Occupancy, Top Airlines) $\rightarrow$ Add/Update/Delete flights in real time.
3. **ML Prediction**: Enter parameters $\rightarrow$ View predicted airline with a confidence meter.
