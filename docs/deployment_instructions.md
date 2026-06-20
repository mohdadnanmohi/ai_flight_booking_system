# Deployment & Setup Instructions

Follow these instructions to configure and execute the AI-Enhanced Flight Booking System on your local server.

---

## 1. Prerequisites
- **Python**: Ensure you have Python 3.8 to 3.14 installed.
- **Supabase Account**: Set up a free project on [Supabase](https://supabase.com) to provision a cloud PostgreSQL database.
- **Google AI Studio Key**: Generate a free Gemini API Key from [Google AI Studio](https://aistudio.google.com/) for travel summary reports.

---

## 2. Directory Installation
Extract the project source code, navigate to the folder, and run:
```bash
pip install -r requirements.txt
```

---

## 3. Database Initialization (Supabase Cloud)

To configure your cloud database:
1. Log in to your **Supabase Dashboard**, open your project, and navigate to the **SQL Editor**.
2. Copy the contents of `db_scripts/schema.sql` and execute the query. This sets up all tables and optimization indexes.
3. Copy the contents of `db_scripts/seeds.sql` and execute the query to insert base flight lists and account placeholders.

---

## 4. Environment Variables (`.env`)
Create a file named `.env` in the root folder and add:
```env
SECRET_KEY=enter-a-random-secret-key-phrase
FLASK_ENV=development

# Database Connection (Get the Direct Connection String from Supabase -> Settings -> Database -> Connection String)
DATABASE_URL=postgresql://postgres.[YOUR-PROJECT-ID]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres

# Google Gemini API
GEMINI_API_KEY=your-gemini-api-key-here
```
> [!NOTE]
> If `DATABASE_URL` is omitted, the Flask backend will automatically fall back to creating a local SQLite file named `flights.db` so the system is fully runnable out-of-the-box.

---

## 5. Train the Machine Learning Model
Before launching the server, train and save the Random Forest Classifier by running:
```bash
python ml/train_model.py
```
This script will:
1. Compile a dataset `ml/sample_dataset.csv` with 1200 travel search records.
2. Fit the Random Forest model and print accuracy diagnostics (target accuracy > 80%).
3. Export `flight_recommendation_model.joblib` and `label_encoders.joblib` to the `ml/` subdirectory for real-time inference.

---

## 6. Running Locally
Launch the Flask application server:
```bash
python app.py
```
Once initialized, access the portal in your browser:
**URL**: [http://localhost:5000](http://localhost:5000)

---

## 7. Default Credentials for Testing
Use these credentials to sign in and evaluate dashboard permissions:

### Passenger Portal
- **Email**: `passenger@example.com`
- **Password**: `passenger123`

### Flight Control Center (Admin Portal)
- **Email**: `admin@flight.com`
- **Password**: `admin123`
