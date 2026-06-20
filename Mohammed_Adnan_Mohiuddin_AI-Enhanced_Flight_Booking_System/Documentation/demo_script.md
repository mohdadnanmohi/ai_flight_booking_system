# Demo Video Presentation Script
**Project:** AI-Enhanced Flight Booking System

## [0:00 - 1:00] 1. Introduction
*Camera ON - Face clearly visible*

"Hello everyone, my name is Mohammed Adnan Mohiuddin, Roll Number 237R1A6635 from the CSE AIML Department at CMR Technical Campus. Today, I am excited to present my final year project: the **AI-Enhanced Flight Booking System**."

"Traditional flight booking platforms only allow users to search for flights. My project revolutionizes this by integrating a **Machine Learning predictive engine** to recommend the best airlines based on historical data, and a **Generative AI module** powered by Google Gemini to act as an automated travel agent."

## [1:00 - 2:30] 2. User Registration & Login (Frontend & Authentication)
*Share Screen - Show Homepage*

"Let's start with the user flow. The frontend is built using HTML5, CSS3, Bootstrap 5, and JavaScript, featuring a modern glassmorphism design. I will now register a new user."
*(Perform Registration)*
"The backend uses Python Flask. Notice that passwords are not stored as plain text. I've implemented Werkzeug's Scrypt algorithm to securely hash passwords in our Supabase PostgreSQL database."
*(Log in as the new user)*
"Upon successful login, Flask-Login manages the user session, redirecting us to the user dashboard."

## [2:30 - 4:00] 3. Flight Search & Booking (Database Integration)
*Navigate to Flight Search*

"Now, I'll search for a flight from New York (JFK) to Los Angeles (LAX). When I submit this form, SQLAlchemy ORM queries our live Supabase PostgreSQL database and fetches the scheduled flights."
*(Select a flight and proceed to booking)*
"Here is the interactive seat selection grid. The system dynamically checks the `seat_reservations` table and disables seats that are already booked to prevent double-booking."
*(Fill passenger details, pick a seat, and click Book)*
"We proceed to the payment gateway simulation. Once the payment is marked successful, the transaction is committed to the database using an atomic transaction to ensure data integrity."

## [4:00 - 5:00] 4. Ticket Download (PDF Generation)
*Show the Success Page*

"The booking is confirmed. I can now download my ticket. This PDF is not a static file; it is generated dynamically in real-time using Python's `ReportLab` library, pulling my specific PNR and flight details from the database."
*(Open the downloaded PDF to show it)*

## [5:00 - 6:30] 5. Machine Learning Prediction (AI Feature 1)
*Navigate to 'AI Predictions' tab*

"One of the core features of this project is the Machine Learning module. I trained a Random Forest Classifier using Scikit-Learn on a dataset of historical flight patterns."
*(Enter parameters: e.g., JFK to LHR in July)*
"When I click Predict, the Flask backend loads the serialized `.pkl` model and label encoders, processes these inputs in milliseconds, and predicts that British Airways is the most optimal airline for this specific route and season based on historical reliability and pricing trends."

## [6:30 - 8:00] 6. Generative AI Summary (AI Feature 2)
*Go back to Flight Search Results*

"The second AI feature utilizes Large Language Models. When viewing flight results, users can click 'Generate AI Route Summary'."
*(Click the button and wait for the AI response)*
"This triggers a backend call to the Google Gemini API. I engineered a prompt that passes the user's origin, destination, and travel class. Gemini generates a highly personalized travel itinerary, packing tips, and destination insights. The Markdown response is parsed into clean HTML using JavaScript."

## [8:00 - 9:30] 7. Admin Dashboard & Code Walkthrough
*Log out and log in as Admin*

"Finally, let's look at the Admin role. The Admin Dashboard features real-time analytics using Chart.js. The backend aggregates total revenue and bookings from PostgreSQL and feeds them to the frontend."
*(Show the Code Editor briefly)*
"In terms of code structure, `app.py` handles the routing, `models.py` defines the SQLAlchemy database schema, and `config.py` manages environment variables. The ML folder contains the dataset and training scripts, keeping the architecture clean and modular."

## [9:30 - 10:00] 8. Conclusion
"In conclusion, this project successfully bridges traditional full-stack development with modern AI integration. It is fully responsive, secure, and currently deployed live on Vercel."

"Thank you for your time and evaluation."
