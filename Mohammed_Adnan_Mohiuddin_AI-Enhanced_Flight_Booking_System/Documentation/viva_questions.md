# Viva Questions and Answers
**Project:** AI-Enhanced Flight Booking System

## Python Flask & Backend
**1. What is Flask and why did you choose it for this project?**
Flask is a lightweight WSGI web application framework for Python. I chose it because it is highly modular, easy to integrate with AI libraries like Scikit-Learn, and provides fine-grained control over routing compared to heavier frameworks like Django.

**2. Explain the concept of routing in Flask.**
Routing maps specific URLs to Python functions. In my app, `@app.route('/flights')` binds the `/flights` URL to the `search_flights()` function, which executes the backend logic and returns the HTML template.

**3. How is user authentication handled in your project?**
I used the `Flask-Login` extension to manage user sessions. It handles logging in, logging out, and restricting access to certain pages using the `@login_required` decorator.

**4. What is Werkzeug and how is it used here?**
Werkzeug is a comprehensive WSGI web application library that Flask is built upon. In my project, I used its `security` module (`generate_password_hash` and `check_password_hash`) to securely hash passwords using the Scrypt algorithm before storing them in the database.

**5. How did you manage environment variables?**
I used the `python-dotenv` package to load sensitive configuration variables, like the `DATABASE_URL` and `GEMINI_API_KEY`, from a `.env` file so they are not hardcoded into the source code.

## Database (PostgreSQL & SQLAlchemy)
**6. What is SQLAlchemy?**
SQLAlchemy is an Object Relational Mapper (ORM). It allows me to interact with my PostgreSQL database using Python classes and objects instead of writing raw SQL queries, which prevents SQL injection and makes the code more maintainable.

**7. Why use Supabase PostgreSQL instead of MySQL?**
Supabase provides a scalable, cloud-hosted PostgreSQL database. PostgreSQL offers advanced JSONB support, strict data integrity, and excellent integration with modern serverless deployment platforms like Vercel compared to traditional MySQL setups.

**8. Explain the relationships in your database.**
The database uses One-to-Many relationships. A `User` can have multiple `Bookings`. A `Flight` can have multiple `Bookings` and `SeatReservations`. The `Booking` table acts as a central hub linking Users, Flights, and Payments via Foreign Keys.

**9. How do you handle database migrations?**
I used SQLAlchemy's `db.create_all()` during initialization. For structural changes, tools like Flask-Migrate (Alembic) are used to upgrade the database schema without losing existing data.

**10. What happens when a flight is deleted?**
Because I configured the foreign keys with `ondelete='CASCADE'`, deleting a flight will automatically delete all associated bookings and seat reservations, preventing orphaned records.

## Machine Learning (Random Forest)
**11. What is the purpose of the Machine Learning module in your project?**
The ML module analyzes a user's travel parameters (origin, destination, travel month) and predicts the most optimal airline for them based on historical booking patterns.

**12. Why did you choose Random Forest?**
Random Forest is an ensemble learning method that creates multiple decision trees and merges them together. I chose it because it handles non-linear categorical data well, is highly accurate, and is resistant to overfitting compared to single decision trees.

**13. How did you preprocess the data?**
I used Scikit-Learn's `LabelEncoder` to convert categorical text data (like airport codes and airline names) into numerical values that the Random Forest algorithm can process mathematically.

**14. What is the Train-Test Split?**
I divided the dataset into 80% training data (to teach the model) and 20% testing data (to evaluate its accuracy on unseen data) using `train_test_split()`.

**15. How is the ML model integrated into the Flask app?**
After training, I serialized the model and encoders using `joblib` into `.pkl` files. When the Flask app starts, it loads these files into memory, allowing it to make real-time predictions without retraining.

## Generative AI (Gemini API)
**16. What is the role of the Gemini API in this project?**
The Gemini API is used to dynamically generate intelligent travel summaries. When a user searches for a route, Gemini acts as an AI travel agent, providing packing tips, destination highlights, and cultural insights.

**17. How do you construct the prompt for the AI?**
I use "Prompt Engineering" by injecting variables from the user's search (Source, Destination, Travel Class) into a predefined text template, instructing the AI to act as a professional travel agent and format the output in Markdown.

**18. What happens if the Gemini API fails or times out?**
The application implements a "Fallback Mock Mode." If the API request fails due to network issues or invalid keys, the app catches the exception and returns a pre-written, generic travel summary so the user experience is not disrupted.

**19. How is the AI output rendered on the frontend?**
The Gemini API returns Markdown text. In the frontend, I used the `marked.js` library to parse the Markdown into formatted HTML (bolding, lists, headers) dynamically in the browser.

## Frontend & PDF Generation
**20. How did you make the UI responsive?**
I used Bootstrap 5, which utilizes a mobile-first flexbox grid system. This ensures the application looks perfect on both desktop monitors and mobile devices.

**21. What is Glassmorphism?**
Glassmorphism is a UI design trend I implemented using CSS `backdrop-filter: blur()`. It creates a frosted-glass effect on panels, giving the application a modern, premium look.

**22. How are the charts generated on the Admin Dashboard?**
I used `Chart.js`, a JavaScript library. The Flask backend queries the database for statistics, passes the raw numbers to the HTML template, and Chart.js renders them as interactive bar and doughnut charts.

**23. How are PDF tickets generated?**
I used the `ReportLab` Python library. It creates a PDF canvas in memory, draws text, lines, and passenger data onto it, and returns the binary data directly to the user as a downloadable file via Flask's `send_file`.

## Deployment & Vercel
**24. Where is the project hosted?**
The backend is hosted on Vercel as Serverless Functions, and the database is hosted on Supabase.

**25. What is a Serverless Function?**
Instead of running a continuous server, Vercel spins up a micro-container to execute the Python Flask code only when an HTTP request is received, and shuts it down afterward. This makes it highly scalable and cost-effective.

**26. How did you solve the Supabase IPv6 timeout issue on Vercel?**
Since Vercel's free tier lacks IPv6 support, I programmed the application to detect the `VERCEL` environment variable. If true, it dynamically generates an ephemeral SQLite database in Vercel's `/tmp` memory directory to ensure the app remains functional for demonstration purposes.

*(Note: Provide the remaining 24 questions discussing general HTTP methods, REST architecture, normalization, session hijacking prevention, and future scopes as needed by the examiner).*
