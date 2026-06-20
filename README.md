# Project Title: AI-Enhanced Flight Booking System

![Project Banner](https://via.placeholder.com/1200x400?text=AI-Enhanced+Flight+Booking+System)

## Project Overview
The **AI-Enhanced Flight Booking System** is a comprehensive, full-stack web application designed to revolutionize the travel reservation experience. It moves beyond traditional CRUD operations by integrating Predictive Machine Learning to recommend optimal airlines and Generative AI (LLMs) to provide automated, intelligent travel itineraries and insights dynamically during the booking process.

## Technologies Used
*   **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript, Chart.js (for Analytics)
*   **Backend:** Python 3, Flask, Flask-Login, ReportLab (for PDF Generation)
*   **Database:** Supabase PostgreSQL, SQLAlchemy ORM, SQLite (Ephemeral Vercel fallback)
*   **Machine Learning:** Scikit-Learn (Random Forest Classifier), Pandas, NumPy, Joblib
*   **Generative AI:** Google Gemini API (`google-generativeai`)

## Setup Instructions
1. **Extract the Project:** Unzip the provided project folder.
2. **Open Terminal:** Navigate to the `Backend/` directory (or root directory depending on execution context).
3. **Virtual Environment:** 
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## GenAI/API Key Instructions
To enable the AI and database functionalities, create a `.env` file in the `Backend/` directory with the following credentials:
```ini
# Flask Security
SECRET_KEY=your_secure_secret_key

# Supabase PostgreSQL Database (IPv4 Pooler recommended for Vercel)
DATABASE_URL=postgresql://postgres:password@db.supabase.co:5432/postgres

# Google Gemini API Key
GEMINI_API_KEY=your_google_gemini_api_key
```

## Database Setup Details
1. Ensure your `DATABASE_URL` is properly set in the `.env` file.
2. The database schema uses SQLAlchemy ORM.
3. Run the initialization script to automatically create the tables and seed default users (Admin/Passenger) and flight inventory:
   ```bash
   python db_scripts/init_supabase.py
   ```

## ML Model Details
*   **Algorithm:** Random Forest Classifier.
*   **Purpose:** Predicts the most reliable airline based on historical route data and travel season.
*   **Setup:** The ML dataset (`dataset.csv`) is located in the `ML/` folder.
*   **Training:** Run the following command to train the model and generate the `.pkl` serialization files:
    ```bash
    python train_model.py
    ```

## Steps to Run the Backend
The backend serves both the APIs and the template rendering engine.
1. Ensure your virtual environment is activated and `.env` is configured.
2. Start the Flask server:
   ```bash
   python app.py
   ```
3. The backend will initialize and run on `http://127.0.0.1:5000/`.

## Steps to Run the Frontend
Because this application uses the Flask templating engine (Jinja2), the frontend is tightly integrated and served directly by the backend server.
1. Start the backend server as described above.
2. Open any modern web browser (Chrome, Edge, Firefox).
3. Navigate to: `http://127.0.0.1:5000/` to access the User Interface.
4. (Optional) Admin Dashboard can be accessed by logging in with Admin credentials and navigating to the Admin UI.
