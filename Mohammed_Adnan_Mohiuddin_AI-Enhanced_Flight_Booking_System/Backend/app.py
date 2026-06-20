import os
import random
import re
from datetime import datetime, date, timedelta
from io import BytesIO

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import cast, Date
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import joblib
import pandas as pd
import numpy as np

# ReportLab imports for PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Configuration & Models
from config import Config
from models import db, User, Flight, Booking, SeatReservation, Payment, Recommendation

# Initialize Flask app
app = Flask(__name__, template_folder='../Frontend/templates', static_folder='../Frontend/static')
app.config.from_object(Config)

# Initialize Database
db.init_app(app)

# Initialize Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'error'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- MACHINE LEARNING MODEL LOADING ---
ml_model = None
ml_encoders = None

def load_ml_components():
    global ml_model, ml_encoders
    try:
        model_path = os.path.join(os.path.dirname(__file__), 'ml', 'flight_recommendation_model.joblib')
        encoders_path = os.path.join(os.path.dirname(__file__), 'ml', 'label_encoders.joblib')
        if os.path.exists(model_path) and os.path.exists(encoders_path):
            ml_model = joblib.load(model_path)
            ml_encoders = joblib.load(encoders_path)
            print("Successfully loaded ML model and encoders.")
        else:
            print("ML model files not found. Recommendations will run in fallback simulation mode.")
    except Exception as e:
        print(f"Error loading ML components: {e}")

# --- HELPER FUNCTIONS ---

def generate_pnr():
    """Generates a unique 8-character alphanumeric PNR."""
    while True:
        pnr = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
        if not Booking.query.filter_by(pnr=pnr).first():
            return pnr

def markdown_to_html(md_text):
    """Converts basic markdown syntax to HTML for AI summary rendering."""
    html = md_text
    # Headers
    html = re.sub(r'^\s*###\s+(.*?)$', r'<h5 class="text-white mt-3">\1</h5>', html, flags=re.MULTILINE)
    html = re.sub(r'^\s*##\s+(.*?)$', r'<h4 class="text-white mt-3">\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^\s*#\s+(.*?)$', r'<h3 class="text-white mt-3">\1</h3>', html, flags=re.MULTILINE)
    # Bold
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    # Bullet Lists
    html = re.sub(r'^\s*[-*]\s+(.*?)$', r'<li class="text-muted ml-3">\1</li>', html, flags=re.MULTILINE)
    # Paragraph spaces
    html = html.replace('\n', '<br>')
    return html

def setup_database():
    """Initializes tables and seeds base records (runs on first request)."""
    with app.app_context():
        db.create_all()
        # Seed default Admin and User if users table is empty
        if not User.query.first():
            print("Seeding default database records...")
            # Create Admin
            admin = User(
                name="System Administrator",
                email="admin@flight.com",
                phone="+15550199",
                role="Admin"
            )
            admin.set_password("admin123")
            db.session.add(admin)
            
            # Create default User
            passenger = User(
                name="John Doe",
                email="passenger@example.com",
                phone="+15550122",
                role="User"
            )
            passenger.set_password("passenger123")
            db.session.add(passenger)
            
            # Seed base flights
            base_flights = [
                Flight(flight_number="EK-201", airline="Emirates", source="JFK", destination="DXB", departure_time=datetime(2026, 7, 15, 8, 30), arrival_time=datetime(2026, 7, 16, 5, 30), seats=350, booked_seats=0, price=1250.00, status="Scheduled"),
                Flight(flight_number="EK-202", airline="Emirates", source="DXB", destination="JFK", departure_time=datetime(2026, 7, 20, 14, 0), arrival_time=datetime(2026, 7, 20, 20, 30), seats=350, booked_seats=0, price=1100.00, status="Scheduled"),
                Flight(flight_number="DL-142", airline="Delta Air Lines", source="JFK", destination="LAX", departure_time=datetime(2026, 7, 15, 9, 0), arrival_time=datetime(2026, 7, 15, 12, 15), seats=180, booked_seats=0, price=350.00, status="Scheduled"),
                Flight(flight_number="DL-143", airline="Delta Air Lines", source="LAX", destination="JFK", departure_time=datetime(2026, 7, 18, 16, 30), arrival_time=datetime(2026, 7, 18, 23, 45), seats=180, booked_seats=0, price=380.00, status="Scheduled"),
                Flight(flight_number="SQ-308", airline="Singapore Airlines", source="LHR", destination="SIN", departure_time=datetime(2026, 7, 16, 11, 30), arrival_time=datetime(2026, 7, 17, 7, 30), seats=250, booked_seats=0, price=950.00, status="Scheduled"),
                Flight(flight_number="SQ-309", airline="Singapore Airlines", source="SIN", destination="LHR", departure_time=datetime(2026, 7, 22, 23, 5), arrival_time=datetime(2026, 7, 23, 5, 45), seats=250, booked_seats=0, price=1020.00, status="Scheduled"),
                Flight(flight_number="BA-117", airline="British Airways", source="LHR", destination="JFK", departure_time=datetime(2026, 7, 16, 8, 20), arrival_time=datetime(2026, 7, 16, 11, 5), seats=280, booked_seats=0, price=620.00, status="Scheduled"),
                Flight(flight_number="BA-118", airline="British Airways", source="JFK", destination="LHR", departure_time=datetime(2026, 7, 21, 18, 30), arrival_time=datetime(2026, 7, 22, 6, 30), seats=280, booked_seats=0, price=580.00, status="Scheduled"),
                Flight(flight_number="6E-5321", airline="IndiGo", source="BOM", destination="DEL", departure_time=datetime(2026, 7, 15, 6, 0), arrival_time=datetime(2026, 7, 15, 8, 10), seats=180, booked_seats=0, price=90.00, status="Scheduled"),
                Flight(flight_number="6E-5322", airline="IndiGo", source="DEL", destination="BOM", departure_time=datetime(2026, 7, 15, 18, 45), arrival_time=datetime(2026, 7, 15, 21, 0), seats=180, booked_seats=0, price=85.00, status="Scheduled"),
                Flight(flight_number="AI-101", airline="Air India", source="DEL", destination="JFK", departure_time=datetime(2026, 7, 17, 1, 45), arrival_time=datetime(2026, 7, 17, 7, 25), seats=300, booked_seats=0, price=850.00, status="Scheduled")
            ]
            for f in base_flights:
                db.session.add(f)
            
            db.session.commit()
            print("Database seeding completed.")

# --- WEB APP PATH ROUTES ---

@app.route('/')
def home():
    return render_template('index.html')

# User Registration API
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role', 'User')

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
            
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address is already registered.', 'error')
            return render_template('register.html')
            
        new_user = User(name=name, email=email, phone=phone, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

# User Login API
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash('Invalid email or password.', 'error')
            return render_template('login.html')
            
        login_user(user, remember=remember)
        
        if user.role == 'Admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('dashboard'))
        
    return render_template('login.html')

# User Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('home'))

# Flight Searching API
@app.route('/flights', methods=['GET'])
def search_flights():
    source = request.args.get('source', '').upper()
    destination = request.args.get('destination', '').upper()
    departure_date_str = request.args.get('departure_date', '')
    passengers = int(request.args.get('passengers', 1))
    travel_class = request.args.get('travel_class', 'Economy')
    
    if not source or not destination:
        flash('Please fill in both origin and destination airports.', 'error')
        return redirect(url_for('home'))
        
    query = Flight.query.filter_by(source=source, destination=destination)
    
    # Filter by departure date if specified
    if departure_date_str:
        try:
            dep_date = datetime.strptime(departure_date_str, '%Y-%m-%d').date()
            start_of_day = datetime.combine(dep_date, datetime.min.time())
            end_of_day = start_of_day + timedelta(days=1)
            # Find flights matching date using range query (100% compatible across SQLite/PostgreSQL)
            query = query.filter(Flight.departure_time >= start_of_day, Flight.departure_time < end_of_day)
        except ValueError:
            pass
            
    flights = query.all()
    
    # Calculate price adjustments based on travel class
    # Base price is stored in DB. We adjust based on selection:
    # Economy = 1.0x, Premium Eco = 1.6x, Business = 3.0x, First = 5.0x
    class_multiplier = 1.0
    if travel_class == 'Premium Economy':
        class_multiplier = 1.6
    elif travel_class == 'Business':
        class_multiplier = 3.0
    elif travel_class == 'First Class':
        class_multiplier = 5.0
        
    for f in flights:
        f.price = float(f.price) * class_multiplier

    return render_template('search_results.html', 
                           flights=flights, 
                           source=source, 
                           destination=destination,
                           travel_date=departure_date_str,
                           passengers=passengers,
                           travel_class=travel_class)

# Flight Booking Module View
@app.route('/book-flight', methods=['GET'])
@login_required
def booking_view():
    flight_id = int(request.args.get('flight_id'))
    passengers = int(request.args.get('passengers', 1))
    travel_class = request.args.get('travel_class', 'Economy')
    travel_date = request.args.get('travel_date')

    flight = Flight.query.get_or_404(flight_id)
    
    # Fetch all occupied seat numbers for this flight to block them in the grid
    occupied_reservations = SeatReservation.query.filter_by(flight_id=flight_id).all()
    occupied_seats = [res.seat_number for res in occupied_reservations]

    return render_template('booking.html', 
                           flight=flight, 
                           passengers=passengers, 
                           travel_class=travel_class,
                           travel_date=travel_date,
                           occupied_seats=occupied_seats)

# Process Booking -> Go to Payment Gate
@app.route('/process-booking', methods=['POST'])
@login_required
def process_booking():
    flight_id = int(request.form.get('flight_id'))
    travel_class = request.form.get('travel_class')
    travel_date = request.form.get('travel_date')
    passengers = int(request.form.get('passengers', 1))
    
    passenger_name = request.form.get('passenger_name')
    passenger_age = int(request.form.get('passenger_age', 0))
    passenger_gender = request.form.get('passenger_gender')
    passenger_email = request.form.get('passenger_email')
    passenger_phone = request.form.get('passenger_phone')
    seat_number = request.form.get('seat_number')
    
    flight = Flight.query.get_or_404(flight_id)
    
    # Verify seat isn't already occupied
    is_seat_taken = SeatReservation.query.filter_by(flight_id=flight_id, seat_number=seat_number).first()
    if is_seat_taken:
        flash('Seat is already occupied. Please select another seat.', 'error')
        return redirect(url_for('booking_view', flight_id=flight_id, passengers=passengers, travel_class=travel_class, travel_date=travel_date))
        
    # Calculate price adjustments based on travel class
    class_multiplier = 1.0
    if travel_class == 'Premium Economy':
        class_multiplier = 1.6
    elif travel_class == 'Business':
        class_multiplier = 3.0
    elif travel_class == 'First Class':
        class_multiplier = 5.0
        
    final_amount = float(flight.price) * class_multiplier * passengers
    
    # Render Payment Simulator
    return render_template('payment.html',
                           flight_id=flight_id,
                           travel_class=travel_class,
                           travel_date=travel_date,
                           passenger_name=passenger_name,
                           passenger_age=passenger_age,
                           passenger_gender=passenger_gender,
                           passenger_email=passenger_email,
                           passenger_phone=passenger_phone,
                           seat_number=seat_number,
                           amount=final_amount)

# Payment API Simulation
@app.route('/process-payment', methods=['POST'])
@login_required
def process_payment():
    flight_id = int(request.form.get('flight_id'))
    travel_class = request.form.get('travel_class')
    travel_date_str = request.form.get('travel_date')
    passenger_name = request.form.get('passenger_name')
    passenger_age = int(request.form.get('passenger_age'))
    passenger_gender = request.form.get('passenger_gender')
    seat_number = request.form.get('seat_number')
    amount = float(request.form.get('amount'))
    payment_method = request.form.get('payment_method')
    simulated_status = request.form.get('simulated_status') # 'Success' or 'Failed'

    flight = Flight.query.get_or_404(flight_id)
    travel_date = datetime.strptime(travel_date_str, '%Y-%m-%d').date()

    if simulated_status == 'Success':
        # Generate PNR and complete booking insertion
        pnr_code = generate_pnr()
        booking = Booking(
            user_id=current_user.user_id,
            flight_id=flight_id,
            pnr=pnr_code,
            travel_date=travel_date,
            passenger_name=passenger_name,
            passenger_age=passenger_age,
            passenger_gender=passenger_gender,
            status='Booked'
        )
        db.session.add(booking)
        db.session.flush() # Populate booking_id
        
        # Create seat reservation
        reservation = SeatReservation(
            booking_id=booking.booking_id,
            flight_id=flight_id,
            seat_number=seat_number
        )
        db.session.add(reservation)

        # Record successful payment transaction
        txn_id = 'TXN-' + str(random.randint(100000000, 999999999))
        payment = Payment(
            booking_id=booking.booking_id,
            amount=amount,
            payment_method=payment_method,
            transaction_id=txn_id,
            payment_status='Success'
        )
        db.session.add(payment)

        # Increment flight's booked_seats counter
        flight.booked_seats += 1
        db.session.commit()
        
        flash('Booking successful!', 'success')
        return render_template('payment_status.html',
                               status='Success',
                               pnr=pnr_code,
                               passenger_name=passenger_name,
                               travel_date=travel_date_str,
                               seat_number=seat_number,
                               travel_class=travel_class,
                               flight=flight)
    else:
        # Failure response
        flash('Payment transaction failed. Reservation discarded.', 'error')
        return render_template('payment_status.html',
                               status='Failed',
                               flight_id=flight_id,
                               seat_number=seat_number)

# Booking Cancellation API
@app.route('/cancel-booking', methods=['POST'])
@login_required
def cancel_booking():
    booking_id = int(request.form.get('booking_id'))
    booking = Booking.query.get_or_404(booking_id)

    # Security check: User can only cancel their own bookings unless admin
    if booking.user_id != current_user.user_id and current_user.role != 'Admin':
        flash('Unauthorized action.', 'error')
        return redirect(url_for('dashboard'))
        
    if booking.status == 'Cancelled':
        flash('Booking is already cancelled.', 'error')
        return redirect(url_for('dashboard'))

    # Mark as Cancelled
    booking.status = 'Cancelled'
    
    # Delete seat reservations associated with booking to release capacity
    SeatReservation.query.filter_by(booking_id=booking_id).delete()

    # Decrement flight's booked seats
    flight = Flight.query.get(booking.flight_id)
    if flight and flight.booked_seats > 0:
        flight.booked_seats -= 1
        
    db.session.commit()
    flash('Booking cancelled successfully. Seat reservation released.', 'success')
    
    if current_user.role == 'Admin':
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('dashboard'))

# User Dashboard (Booking History)
@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'Admin':
         return redirect(url_for('admin_dashboard'))
         
    # Query current user's bookings, ordered by booking date
    bookings = Booking.query.filter_by(user_id=current_user.user_id).order_by(Booking.booking_date.desc()).all()
    return render_template('dashboard.html', bookings=bookings)

# --- MACHINE LEARNING MODEL RECOMMENDATION API ---

@app.route('/recommend-flight', methods=['GET', 'POST'])
@login_required
def recommend_flights_view():
    prediction = None
    confidence = 0
    matching_flights = []
    form_data = {
        'source': 'JFK',
        'destination': 'LAX',
        'budget': 800,
        'travel_class': 'Economy',
        'travel_time': 'Morning',
        'preferred_airline': 'Delta Air Lines'
    }

    if request.method == 'POST':
        source = request.form.get('source', 'JFK')
        destination = request.form.get('destination', 'LAX')
        budget = int(request.form.get('budget', 800))
        travel_class = request.form.get('travel_class', 'Economy')
        travel_time = request.form.get('travel_time', 'Morning')
        preferred_airline = request.form.get('preferred_airline', 'Delta Air Lines')

        form_data = {
            'source': source,
            'destination': destination,
            'budget': budget,
            'travel_class': travel_class,
            'travel_time': travel_time,
            'preferred_airline': preferred_airline
        }

        # Check if Random Forest Classifier model is loaded
        if ml_model and ml_encoders:
            try:
                # Features list to feed the model:
                # ['Source', 'Destination', 'Ticket_Price', 'Travel_Month', 'Airline', 
                #  'Travel_Time', 'Booking_Frequency', 'Preferred_Airline', 'Travel_Class', 'Previous_Bookings']
                
                # Transform categorical variables using loaded encoders. Fallback to 0 if class isn't in encoder.
                def safe_encode(encoder, value):
                    try:
                        return encoder.transform([value])[0]
                    except Exception:
                        return 0

                enc_source = safe_encode(ml_encoders['Source'], source)
                enc_dest = safe_encode(ml_encoders['Destination'], destination)
                enc_time = safe_encode(ml_encoders['Travel_Time'], travel_time)
                enc_pref_airline = safe_encode(ml_encoders['Preferred_Airline'], preferred_airline)
                enc_class = safe_encode(ml_encoders['Travel_Class'], travel_class)
                
                # Assume default month is current month, airline matches preference for feature input, and default frequency settings
                current_month = datetime.now().month
                enc_airline = safe_encode(ml_encoders['Airline'], preferred_airline)
                booking_freq = 5
                prev_bookings = 4
                
                # Form target features array
                features_array = [[
                    enc_source, enc_dest, budget, current_month, enc_airline,
                    enc_time, booking_freq, enc_pref_airline, enc_class, prev_bookings
                ]]

                # Predict
                pred_encoded = ml_model.predict(features_array)[0]
                prediction = ml_encoders['Target'].inverse_transform([pred_encoded])[0]

                # Get confidence score
                probabilities = ml_model.predict_proba(features_array)[0]
                confidence = float(np.max(probabilities)) * 100
                confidence = round(confidence, 1)

                # Store Recommendation History
                rec_record = Recommendation(
                    user_id=current_user.user_id,
                    predicted_airline=prediction,
                    confidence_score=confidence
                )
                db.session.add(rec_record)
                db.session.commit()

                # Query database flights that match the predicted airline
                matching_flights = Flight.query.filter_by(
                    source=source, 
                    destination=destination, 
                    airline=prediction
                ).all()

            except Exception as e:
                print(f"ML Inference error: {e}")
                # Fallback static logic
                prediction = preferred_airline
                confidence = 85.4
                matching_flights = Flight.query.filter_by(source=source, destination=destination, airline=prediction).all()
        else:
            # Fallback static logic if model is not loaded/trained
            prediction = preferred_airline
            confidence = 78.5
            matching_flights = Flight.query.filter_by(source=source, destination=destination, airline=prediction).all()

    return render_template('ai_recommendations.html',
                           prediction=prediction,
                           confidence=confidence,
                           matching_flights=matching_flights,
                           form_data=form_data)

# --- GENERATIVE AI MODULE ---

@app.route('/generate-summary', methods=['POST'])
@login_required
def generate_summary_view():
    source = request.form.get('source')
    destination = request.form.get('destination')
    travel_class = request.form.get('travel_class', 'Economy')

    api_key = app.config['GEMINI_API_KEY']
    summary_text = ""

    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            # Use lightweight recommended model
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = (
                f"You are a professional travel assistant. Provide a brief, structured, beautiful markdown report "
                f"for a travel itinerary from {source} to {destination} in {travel_class} class. "
                f"Include sections on Route Recommendations, layover durations, destination insights, cost-effective travel options, "
                f"and passenger-friendly suggestions (e.g. check-in times, packing tips). Make it realistic and concise."
            )
            response = model.generate_content(prompt)
            summary_text = response.text
        except Exception as e:
            print(f"Gemini API invocation error: {e}")
            summary_text = None
            
    if not api_key or not summary_text:
        # Graceful fallback mock generation matching structure
        summary_text = (
            f"### Route Overview: {source} to {destination}\n"
            f"This flight path represents a popular route with multiple carriers offering daily non-stop runs. "
            f"Traveling in **{travel_class}** class provides an optimized balance of cabin service and check-in speed.\n\n"
            f"### Flight & Budget Insights\n"
            f"- **Cost-Effective Option**: Standard tickets fluctuate seasonally. Booking 4-6 weeks in advance yields high price savings.\n"
            f"- **Direct Duration**: Average flight duration is approximately 6-12 hours depending on headwinds. Layovers are minimal.\n\n"
            f"### Passenger Friendly Suggestions\n"
            f"- **Airport Logistics**: Consider arriving at the airport **3 hours prior to departure** for international connections.\n"
            f"- **Baggage Allowance**: Double-check your cabin weight limit to avoid queue delays at check-in.\n"
            f"- **Preferred Travel Season**: Check destination local forecasts; summer months tend to occupy high passenger load factors."
        )

    # Convert markdown structure to HTML for templates
    summary_html = markdown_to_html(summary_text)

    return render_template('travel_summary.html',
                           source=source,
                           destination=destination,
                           summary_html=summary_html)

# --- REPORTLAB PDF TICKET GENERATOR ---

@app.route('/download-ticket/<pnr>')
@login_required
def download_ticket(pnr):
    booking = Booking.query.filter_by(pnr=pnr).first_or_404()
    
    # Safety Check: User can only download their own tickets unless Admin
    if booking.user_id != current_user.user_id and current_user.role != 'Admin':
        flash('Access Denied.', 'error')
        return redirect(url_for('dashboard'))

    flight = booking.flight
    
    # Create in-memory buffer
    buffer = BytesIO()
    
    # Set document structure
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=colors.HexColor('#1e1b4b'), # Deep Indigo
        spaceAfter=15
    )
    
    meta_style = ParagraphStyle(
        'MetaText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.HexColor('#475569'),
        spaceAfter=5
    )
    
    bold_meta = ParagraphStyle(
        'BoldMeta',
        parent=meta_style,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#0f172a')
    )

    pnr_style = ParagraphStyle(
        'PnrStyle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=16,
        textColor=colors.HexColor('#06b6d4'), # Cyber Cyan
        alignment=2 # Right align
    )
    # Header Bar
    header_data = [
        [Paragraph("GRADIOUS FLIGHTS", title_style), Paragraph(f"PNR: {booking.pnr}", pnr_style)]
    ]
    header_table = Table(header_data, colWidths=[300, 220])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(header_table)
    
    # Colored dividing stripe
    stripe = Table([[""]], colWidths=[520], rowHeights=[4])
    stripe.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#06b6d4')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(stripe)
    story.append(Spacer(1, 20))
    
    # Ticket Content Grid
    # Seat number lookup
    seat_num = "None Assigned"
    if booking.seat_reservations:
        seat_num = ", ".join([res.seat_number for res in booking.seat_reservations])
        
    ticket_data = [
        [
            Paragraph("PASSENGER DETAILS", styles['Heading3']),
            Paragraph("FLIGHT DETAILS", styles['Heading3'])
        ],
        [
            Paragraph(f"<b>Name:</b> {booking.passenger_name}", meta_style),
            Paragraph(f"<b>Airline:</b> {flight.airline}", meta_style)
        ],
        [
            Paragraph(f"<b>Age:</b> {booking.passenger_age or 'N/A'}", meta_style),
            Paragraph(f"<b>Flight Number:</b> {flight.flight_number}", meta_style)
        ],
        [
            Paragraph(f"<b>Gender:</b> {booking.passenger_gender or 'N/A'}", meta_style),
            Paragraph(f"<b>Route:</b> {flight.source} → {flight.destination}", meta_style)
        ],
        [
            Paragraph(f"<b>Booker ID:</b> #{booking.user_id}", meta_style),
            Paragraph(f"<b>Departure Time:</b> {flight.departure_time.strftime('%b %d, %Y at %H:%M')}", meta_style)
        ],
        [
            Paragraph(f"<b>Travel Status:</b> Confirmed", meta_style),
            Paragraph(f"<b>Assigned Seat:</b> <font color='#4f46e5'><b>{seat_num}</b></font>", meta_style)
        ]
    ]
    
    grid_table = Table(ticket_data, colWidths=[260, 260])
    grid_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LINEBELOW', (0,0), (-1,0), 1, colors.HexColor('#cbd5e1')),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('TOPPADDING', (0,1), (-1,-1), 6),
    ]))
    story.append(grid_table)
    story.append(Spacer(1, 30))
    
    # Draw simulated ticket stub boundary (dotted lines)
    stub_line = Table([["------------------------------------------------- BOARDING PASS STUB -------------------------------------------------"]], colWidths=[520])
    stub_line.setStyle(TableStyle([
        ('TEXTCOLOR', (0,0), (0,0), colors.HexColor('#94a3b8')),
        ('ALIGN', (0,0), (0,0), 'CENTER'),
        ('FONTNAME', (0,0), (0,0), 'Courier'),
        ('FONTSIZE', (0,0), (0,0), 8),
    ]))
    story.append(stub_line)
    story.append(Spacer(1, 25))
    
    # Stub barcode representation
    # Draw simple vertical black lines to mock a 1D barcode
    barcode_cols = []
    barcode_colors = []
    random.seed(booking.booking_id)
    for i in range(45):
        w = random.choice([2, 4, 6])
        barcode_cols.append(w)
        # alternate black / white lines
        barcode_colors.append(colors.black if i % 2 == 0 else colors.white)
        
    barcode_table = Table([[""] * len(barcode_cols)], colWidths=barcode_cols, rowHeights=[35])
    barcode_style = [
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]
    for idx, c in enumerate(barcode_colors):
        barcode_style.append(('BACKGROUND', (idx, 0), (idx, 0), c))
        
    barcode_table.setStyle(TableStyle(barcode_style))
    
    story.append(barcode_table)
    story.append(Spacer(1, 5))
    
    # Footer notice
    footer_text = Paragraph(
        "<font color='#64748b'>Gates close 20 minutes before departure. Please present this printed pass along with a valid photo identity for security gates.</font>",
        meta_style
    )
    story.append(footer_text)
    
    # Build document
    doc.build(story)
    
    # Reset buffer seek pointer
    buffer.seek(0)
    
    # Return PDF response
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=Ticket_{booking.pnr}.pdf'
    return response

# --- ADMINISTRATOR MODULE CONTROLLER ---

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # Role gate security
    if current_user.role != 'Admin':
        flash('Unauthorized portal access.', 'error')
        return redirect(url_for('home'))
        
    # Query Dashboard Counters
    total_flights = Flight.query.count()
    total_users = User.query.count()
    total_bookings = Booking.query.count()
    
    # Calculate Total Revenue from payments
    successful_payments = Payment.query.filter_by(payment_status='Success').all()
    total_revenue = sum(float(p.amount) for p in successful_payments)
    
    # Query all bookings for monitoring grid
    all_bookings = Booking.query.order_by(Booking.booking_date.desc()).all()
    
    # --- PREPARE DATASET FOR GRAPH CHARTS ---
    # 1. Revenue & Bookings Trend (by date)
    revenue_trend_dict = {}
    bookings_trend_dict = {}
    
    for p in successful_payments:
        date_str = p.booking.booking_date.strftime('%Y-%m-%d')
        revenue_trend_dict[date_str] = revenue_trend_dict.get(date_str, 0) + float(p.amount)
        bookings_trend_dict[date_str] = bookings_trend_dict.get(date_str, 0) + 1
        
    revenue_trend = [{'date': k, 'amount': v} for k, v in sorted(revenue_trend_dict.items())]
    bookings_trend = [{'date': k, 'count': v} for k, v in sorted(bookings_trend_dict.items())]
    
    # 2. Popular Routes
    popular_routes = {}
    for b in all_bookings:
        route_str = f"{b.flight.source} - {b.flight.destination}"
        popular_routes[route_str] = popular_routes.get(route_str, 0) + 1
        
    # 3. Active Flight Occupancy
    active_flights = Flight.query.all()
    occupancy_data = []
    for f in active_flights:
        occupancy_rate = f.occupancy_rate
        occupancy_data.append({
            'flight_number': f.flight_number,
            'occupancy': round(occupancy_rate, 1)
        })
        
    # 4. Top Airlines Share
    airlines_share = {}
    for b in all_bookings:
        airline = b.flight.airline
        airlines_share[airline] = airlines_share.get(airline, 0) + 1

    return render_template('admin_dashboard.html',
                           total_flights=total_flights,
                           total_users=total_users,
                           total_bookings=total_bookings,
                           total_revenue=total_revenue,
                           all_bookings=all_bookings,
                           revenue_trend=revenue_trend,
                           bookings_trend=bookings_trend,
                           popular_routes=popular_routes,
                           occupancy_data=occupancy_data,
                           airlines_share=airlines_share)

@app.route('/admin/flights')
@login_required
def admin_flights():
    if current_user.role != 'Admin':
        flash('Unauthorized portal access.', 'error')
        return redirect(url_for('home'))
        
    flights = Flight.query.order_by(Flight.departure_time.asc()).all()
    return render_template('admin_flights.html', flights=flights)

# Create Flight API (Admin)
@app.route('/admin/add-flight', methods=['POST'])
@login_required
def add_flight():
    if current_user.role != 'Admin':
        return jsonify({'error': 'Unauthorized'}), 403
        
    flight_number = request.form.get('flight_number').upper()
    airline = request.form.get('airline')
    source = request.form.get('source').upper()
    destination = request.form.get('destination').upper()
    dep_time_str = request.form.get('departure_time')
    arr_time_str = request.form.get('arrival_time')
    seats = int(request.form.get('seats'))
    price = float(request.form.get('price'))

    departure_time = datetime.strptime(dep_time_str, '%Y-%m-%dT%H:%M')
    arrival_time = datetime.strptime(arr_time_str, '%Y-%m-%dT%H:%M')

    # Double-check existing flight number
    exists = Flight.query.filter_by(flight_number=flight_number).first()
    if exists:
        flash('Flight number already exists.', 'error')
        return redirect(url_for('admin_flights'))

    new_flight = Flight(
        flight_number=flight_number,
        airline=airline,
        source=source,
        destination=destination,
        departure_time=departure_time,
        arrival_time=arrival_time,
        seats=seats,
        price=price,
        status='Scheduled'
    )
    db.session.add(new_flight)
    db.session.commit()
    
    flash('Flight scheduled successfully.', 'success')
    return redirect(url_for('admin_flights'))

# Update Flight API (Admin)
@app.route('/admin/update-flight', methods=['POST'])
@login_required
def update_flight():
    if current_user.role != 'Admin':
        return jsonify({'error': 'Unauthorized'}), 403
        
    flight_id = int(request.form.get('flight_id'))
    flight = Flight.query.get_or_404(flight_id)

    flight.flight_number = request.form.get('flight_number').upper()
    flight.airline = request.form.get('airline')
    flight.source = request.form.get('source').upper()
    flight.destination = request.form.get('destination').upper()
    
    dep_time_str = request.form.get('departure_time')
    arr_time_str = request.form.get('arrival_time')
    flight.departure_time = datetime.strptime(dep_time_str, '%Y-%m-%dT%H:%M')
    flight.arrival_time = datetime.strptime(arr_time_str, '%Y-%m-%dT%H:%M')
    
    flight.seats = int(request.form.get('seats'))
    flight.price = float(request.form.get('price'))
    flight.status = request.form.get('status')

    db.session.commit()
    flash('Flight settings updated successfully.', 'success')
    return redirect(url_for('admin_flights'))

# Delete Flight API (Admin)
@app.route('/admin/delete-flight', methods=['POST'])
@login_required
def delete_flight():
    if current_user.role != 'Admin':
        return jsonify({'error': 'Unauthorized'}), 403
        
    flight_id = int(request.form.get('flight_id'))
    flight = Flight.query.get_or_404(flight_id)
    
    db.session.delete(flight)
    db.session.commit()
    
    flash('Flight cancelled and deleted successfully.', 'success')
    return redirect(url_for('admin_flights'))

# Start setup commands
def initialize_database():
    with app.app_context():
        db.create_all()
        # Seed tables if empty
        if not User.query.first():
            admin = User(name="System Administrator", email="admin@flight.com", phone="+15550199", role="Admin")
            admin.set_password("admin123")
            db.session.add(admin)
            
            passenger = User(name="John Doe", email="passenger@example.com", phone="+15550122", role="User")
            passenger.set_password("passenger123")
            db.session.add(passenger)
            
            base_flights = [
                Flight(flight_number="EK-201", airline="Emirates", source="JFK", destination="DXB", departure_time=datetime(2026, 7, 15, 8, 30), arrival_time=datetime(2026, 7, 16, 5, 30), seats=350, booked_seats=0, price=1250.00, status="Scheduled"),
                Flight(flight_number="EK-202", airline="Emirates", source="DXB", destination="JFK", departure_time=datetime(2026, 7, 20, 14, 0), arrival_time=datetime(2026, 7, 20, 20, 30), seats=350, booked_seats=0, price=1100.00, status="Scheduled"),
                Flight(flight_number="DL-142", airline="Delta Air Lines", source="JFK", destination="LAX", departure_time=datetime(2026, 7, 15, 9, 0), arrival_time=datetime(2026, 7, 15, 12, 15), seats=180, booked_seats=0, price=350.00, status="Scheduled"),
                Flight(flight_number="DL-143", airline="Delta Air Lines", source="LAX", destination="JFK", departure_time=datetime(2026, 7, 18, 16, 30), arrival_time=datetime(2026, 7, 18, 23, 45), seats=180, booked_seats=0, price=380.00, status="Scheduled"),
                Flight(flight_number="SQ-308", airline="Singapore Airlines", source="LHR", destination="SIN", departure_time=datetime(2026, 7, 16, 11, 30), arrival_time=datetime(2026, 7, 17, 7, 30), seats=250, booked_seats=0, price=950.00, status="Scheduled"),
                Flight(flight_number="SQ-309", airline="Singapore Airlines", source="SIN", destination="LHR", departure_time=datetime(2026, 7, 22, 23, 5), arrival_time=datetime(2026, 7, 23, 5, 45), seats=250, booked_seats=0, price=1020.00, status="Scheduled"),
                Flight(flight_number="BA-117", airline="British Airways", source="LHR", destination="JFK", departure_time=datetime(2026, 7, 16, 8, 20), arrival_time=datetime(2026, 7, 16, 11, 5), seats=280, booked_seats=0, price=620.00, status="Scheduled"),
                Flight(flight_number="BA-118", airline="British Airways", source="JFK", destination="LHR", departure_time=datetime(2026, 7, 21, 18, 30), arrival_time=datetime(2026, 7, 22, 6, 30), seats=280, booked_seats=0, price=580.00, status="Scheduled"),
                Flight(flight_number="6E-5321", airline="IndiGo", source="BOM", destination="DEL", departure_time=datetime(2026, 7, 15, 6, 0), arrival_time=datetime(2026, 7, 15, 8, 10), seats=180, booked_seats=0, price=90.00, status="Scheduled"),
                Flight(flight_number="6E-5322", airline="IndiGo", source="DEL", destination="BOM", departure_time=datetime(2026, 7, 15, 18, 45), arrival_time=datetime(2026, 7, 15, 21, 0), seats=180, booked_seats=0, price=85.00, status="Scheduled"),
                Flight(flight_number="AI-101", airline="Air India", source="DEL", destination="JFK", departure_time=datetime(2026, 7, 17, 1, 45), arrival_time=datetime(2026, 7, 17, 7, 25), seats=300, booked_seats=0, price=850.00, status="Scheduled")
            ]
            for f in base_flights:
                db.session.add(f)
            
            db.session.commit()

# Load model parameters at start
load_ml_components()

# Auto-initialize the temporary SQLite database on Vercel serverless cold-starts
import os
if os.getenv('VERCEL') == '1':
    initialize_database()

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True, host='0.0.0.0', port=5000)
