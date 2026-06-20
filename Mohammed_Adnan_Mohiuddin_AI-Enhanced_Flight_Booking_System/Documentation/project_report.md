# COVER PAGE
**Project Title:** AI-Enhanced Flight Booking System
**Student Details:** Mohammed Adnan Mohiuddin
**Roll Number:** 237R1A6635
**Department:** Computer Science and Engineering (AIML)
**College:** CMR Technical Campus
**Academic Year:** 2025–2026

---

# CERTIFICATE
This is to certify that the project report entitled **"AI-Enhanced Flight Booking System"** submitted by **Mohammed Adnan Mohiuddin (Roll No: 237R1A6635)** in partial fulfillment of the requirements for the award of the degree of Bachelor of Technology in Computer Science and Engineering (AIML) at CMR Technical Campus, is a bonafide record of the work carried out under our guidance and supervision.

**Signature of Internal Guide**
**Signature of Head of Department**
**Signature of External Examiner**

---

# DECLARATION
I, **Mohammed Adnan Mohiuddin**, hereby declare that the project titled **"AI-Enhanced Flight Booking System"** is an original work done by me under the supervision of my project guide. This work has not been submitted previously in whole or in part to any other University or Institution for the award of any degree or diploma.

**Date:** 14-June-2026
**Signature:** Mohammed Adnan Mohiuddin

---

# ACKNOWLEDGEMENT
I would like to express my profound gratitude to my project guide and the faculty of the CSE (AIML) department at CMR Technical Campus for their continuous support, valuable feedback, and technical guidance throughout the development of this project. Their expertise has been instrumental in shaping this software from conception to deployment. 

---

# ABSTRACT
**Purpose:** The aviation industry generates massive amounts of data daily. Traditional flight booking systems allow users to search and book flights but fail to provide personalized, intelligent insights. The purpose of this project is to bridge the gap between standard CRUD web applications and advanced Artificial Intelligence by developing an AI-Enhanced Flight Booking System.

**Technologies:** The system is built using a modern technology stack. The frontend employs HTML5, CSS3, Bootstrap 5, and JavaScript to deliver a premium, glassmorphism-inspired UI. The backend is developed in Python using the Flask framework, communicating with a cloud-hosted PostgreSQL database (Supabase) via SQLAlchemy ORM.

**Machine Learning Integration:** A predictive Artificial Intelligence module is integrated using Scikit-Learn. A Random Forest Classifier was trained on historical flight datasets to predict the most optimal airline for a user based on their travel parameters (origin, destination, season).

**Generative AI Features:** To act as a digital travel agent, the system integrates the Google Gemini Large Language Model (LLM) API. By employing prompt engineering, the system dynamically generates comprehensive travel itineraries, packing tips, and route summaries tailored to the user's specific booking.

**Expected Outcomes:** The expected outcome is a fully functional, highly secure, and cloud-deployed web application that not only processes financial transactions (simulated) and generates dynamic PDF tickets via ReportLab, but fundamentally enhances the user experience through actionable AI intelligence.

---

# TABLE OF CONTENTS
1. Introduction
2. Literature Survey
3. System Analysis
4. System Design
5. Database Design
6. Implementation
7. Machine Learning Module
8. Generative AI Module
9. Testing
10. Results and Screenshots
11. Conclusion
12. Future Enhancements
13. References

---

# CHAPTER 1 – INTRODUCTION

### 1.1 Background
The rapid digitization of the travel industry has led to the proliferation of online booking platforms. However, most platforms operate as static databases. As the volume of air travel increases, users face "decision fatigue." They are required to manually research airlines, plan itineraries on third-party websites, and guess the best times to fly.

### 1.2 Need for Flight Booking Systems
A centralized flight booking system is essential for organizing global aviation logistics. It allows users to view available inventory, compare prices, and secure seats. For administrators, it provides a dashboard to manage flight schedules, monitor revenue, and track occupancy rates.

### 1.3 Problem Statement
*Existing travel platforms lack embedded intelligence.* Users must switch between a booking site to buy a ticket, a weather site to check the climate, and a travel blog to plan their itinerary. Furthermore, standard platforms do not analyze historical data to recommend the most reliable airlines for specific routes.

### 1.4 Objectives
1. To develop a robust, responsive full-stack flight reservation platform.
2. To integrate predictive Machine Learning (Random Forest) for airline recommendations.
3. To integrate Generative AI (Gemini) for automated itinerary generation.
4. To implement secure user authentication and dynamic PDF ticket generation.
5. To deploy the system to a scalable cloud environment.

### 1.5 Scope
The scope of this project encompasses the complete Software Development Life Cycle (SDLC) from UI/UX design to cloud deployment. It simulates the core functionalities of a commercial airline aggregator, including seat selection, payment simulation, and ticket generation, augmented with AI.

### 1.6 Existing System
Traditional systems utilize standard SQL queries to filter flights based on user input. They rely heavily on manual user research and do not utilize user data beyond the immediate transaction. 
**Disadvantages:**
* No personalized recommendations.
* Lacks destination insights.
* Static, unengaging user interfaces.

### 1.7 Proposed System
The proposed "AI-Enhanced Flight Booking System" integrates both Predictive AI and Generative AI directly into the booking workflow.
**Advantages:**
* Provides instant, data-driven airline recommendations.
* Generates custom travel guides on demand.
* Interactive UI with dynamic data visualization (Chart.js).
* Automated infrastructure using cloud databases (Supabase).

---

# CHAPTER 2 – LITERATURE SURVEY

### 2.1 Traditional Flight Booking Systems
Early Computer Reservation Systems (CRS) like Sabre revolutionized the 1960s. Modern iterations transitioned to web-based platforms using MVC architectures. However, literature shows these systems have plateaued in innovation, primarily focusing on speed rather than user intelligence.

### 2.2 AI in Aviation
Recent studies highlight the use of AI in aviation primarily for backend logistics (fuel optimization, predictive maintenance). The application of AI in customer-facing booking interfaces is a novel area of research, focusing on improving conversion rates through personalization.

### 2.3 Recommendation Systems
Collaborative filtering and content-based filtering are standard in e-commerce. In travel, researchers advocate for context-aware recommendation systems. This project adopts a content-based approach using Random Forest to analyze contextual factors (route, month).

### 2.4 Generative AI Applications
With the advent of Transformers, LLMs like GPT and Gemini have demonstrated human-level text generation. Literature suggests integrating LLMs via APIs into microservices to reduce customer support loads by providing instant, automated answers to user queries (e.g., packing lists).

### 2.5 Machine Learning in Travel Platforms
Decision Trees and Random Forests are heavily cited in literature for their robustness against overfitting in categorical datasets. Given that flight data (Origin, Destination, Airline) is primarily categorical, Random Forest was identified as the optimal algorithm for this project.

---

# CHAPTER 3 – SYSTEM ANALYSIS

### 3.1 Functional Requirements
* **User Module:** Register, Login, Search Flights, Book Flights, Download PDF Ticket, View AI Recommendations, View Dashboard.
* **Admin Module:** Login, View Analytics Dashboard, Add Flights, Edit Flights, Delete Flights.
* **AI Module:** Request ML Prediction, Request GenAI Summary.

### 3.2 Non-Functional Requirements
* **Security:** Passwords must be hashed using Scrypt. Routes must be protected by Role-Based Access Control.
* **Performance:** AI predictions must resolve in under 500ms.
* **Availability:** Deployed on Vercel for 99.9% uptime.
* **Usability:** Fully responsive UI compatible with mobile devices.

### 3.3 Feasibility Study
* **Technical:** Highly feasible. Python Flask integrates perfectly with Scikit-Learn.
* **Economic:** Feasible. Cloud hosting (Vercel) and database hosting (Supabase) offer free tiers sufficient for academic demonstration.
* **Operational:** Feasible. The UI is intuitive, requiring minimal user training.

### 3.4 Use Cases
* *Use Case 1:* Passenger searches for flights and filters by price.
* *Use Case 2:* Passenger requests an AI travel summary for their destination.
* *Use Case 3:* Admin logs in to view total revenue generated via Chart.js graphs.

---

# CHAPTER 4 – SYSTEM DESIGN

*(Note: Diagrams to be inserted by the student using tools like draw.io or Lucidchart)*

### 4.1 Architecture Diagram
**Explanation:** The system follows a Client-Server Architecture. The Client (Browser) renders HTML/CSS. It sends HTTP requests to the Flask Backend. The Backend communicates with three external entities: The Supabase PostgreSQL Database, the Local ML serialized model (`rf_model.pkl`), and the external Google Gemini API over HTTPS.

### 4.2 Data Flow Diagram (DFD)
**Explanation:** 
*   *Level 0:* User -> System -> Ticket.
*   *Level 1:* User inputs search -> System queries DB -> DB returns Flights -> System displays flights. User selects flight -> System processes payment -> System generates PDF -> Returns to User.

### 4.3 ER Diagram
**Explanation:** Represents the entities defined in Chapter 5 and their relations. A One-to-Many relationship connects `Users` to `Bookings`, and `Flights` to `Bookings`.

### 4.4 UML Use Case Diagram
**Explanation:** Two actors: Admin and Passenger. Passenger use cases include Search, Book, Download, AI Insights. Admin use cases include Manage Inventory, View Analytics.

### 4.5 Sequence Diagram
**Explanation:** Traces the booking flow. User -> UI -> Controller -> Database -> Controller -> UI. Demonstrates the synchronous nature of the booking transaction.

---

# CHAPTER 5 – DATABASE DESIGN

The database is highly normalized and hosted on Supabase (PostgreSQL). SQLAlchemy ORM is used for schema definition.

### 5.1 Users Table
Stores authentication and profile data.
*   `user_id` (Integer, Primary Key)
*   `name` (String)
*   `email` (String, Unique)
*   `phone` (String)
*   `password` (String - Scrypt Hash)
*   `role` (String - 'User' or 'Admin')

### 5.2 Flights Table
Stores the aviation inventory.
*   `flight_id` (Integer, Primary Key)
*   `flight_number` (String, Unique)
*   `airline` (String)
*   `source` (String)
*   `destination` (String)
*   `departure_time` (DateTime)
*   `arrival_time` (DateTime)
*   `price` (Numeric)

### 5.3 Bookings Table
The central junction table linking users to flights.
*   `booking_id` (Integer, Primary Key)
*   `user_id` (Foreign Key -> Users)
*   `flight_id` (Foreign Key -> Flights)
*   `pnr` (String, Unique)
*   `travel_date` (Date)
*   `status` (String)

### 5.4 Seat Reservations Table
Prevents double-booking of specific physical seats.
*   `reservation_id` (Integer, Primary Key)
*   `booking_id` (Foreign Key -> Bookings)
*   `flight_id` (Foreign Key -> Flights)
*   `seat_number` (String)

### 5.5 Payments Table
Records financial transactions.
*   `payment_id` (Integer, Primary Key)
*   `booking_id` (Foreign Key -> Bookings)
*   `amount` (Numeric)
*   `transaction_id` (String, Unique)

---

# CHAPTER 6 – IMPLEMENTATION

### 6.1 Frontend
The UI was constructed using **HTML5** and **CSS3**, leveraging the **Bootstrap 5** framework for responsive grid layouts. Custom CSS was written to implement "Glassmorphism," utilizing `backdrop-filter: blur(10px)` with semi-transparent rgba backgrounds to create a modern, premium aesthetic. **JavaScript** was used for client-side form validation and DOM manipulation (e.g., interactive seat selection grids).

### 6.2 Backend
**Python Flask** was chosen as the WSGI framework. It routes HTTP requests to specific controller functions. **Flask-Login** manages user sessions via secure cookies. **SQLAlchemy** serves as the ORM, abstracting raw SQL into Python classes, preventing SQL injection vulnerabilities.

### 6.3 Database
**Supabase PostgreSQL** provides the cloud database infrastructure. During implementation, a specific issue regarding IPv6 timeout limits on Vercel was encountered and resolved by implementing an ephemeral SQLite fallback specifically for the Vercel serverless environment.

### 6.4 ML & Generative AI Integration
The backend utilizes `joblib.load()` to pull the trained **Random Forest** model into RAM during server startup to eliminate cold-start latency during predictions. The **Gemini API** is implemented using the `google.generativeai` SDK, utilizing `try-except` blocks for resilience.

### 6.5 PDF Generation
The `ReportLab` library is used to construct a `canvas` object. The implementation calculates X/Y coordinates to draw text (PNR, Passenger Name, Flight Number) and lines onto the canvas. It is saved to an `io.BytesIO()` memory buffer and streamed to the user via Flask's `send_file`.

---

# CHAPTER 7 – MACHINE LEARNING MODULE

### 7.1 Dataset & Features
A custom dataset was synthesized mirroring real-world aviation patterns.
**Features:**
*   `Source`: Origin airport code (Categorical).
*   `Destination`: Arrival airport code (Categorical).
*   `Travel Month`: Integer (1-12) to account for seasonal variations.
*   `Target Variable`: `Airline` (The optimal airline to fly).

### 7.2 Preprocessing
Machine Learning algorithms cannot process strings (e.g., 'JFK'). Scikit-Learn's `LabelEncoder` was utilized to map unique strings to integer values (e.g., JFK -> 0, LAX -> 1). Three separate encoders were created and saved for Source, Destination, and Airline to ensure input data during production is transformed identically to training data.

### 7.3 Training & Algorithm
The dataset was divided using `train_test_split` (80% training, 20% testing). A **Random Forest Classifier** was instantiated with `n_estimators=100`. Random Forest was selected because it builds an ensemble of decision trees, minimizing the risk of overfitting common in categorical datasets.

### 7.4 Model Serialization
To integrate the model into Flask, the trained model and all three `LabelEncoders` were serialized into binary `.pkl` files using the `joblib` library. This allows the web server to load the pre-trained intelligence without re-running the mathematical training process.

---

# CHAPTER 8 – GENERATIVE AI MODULE

### 8.1 Gemini API Integration
The project integrates Google's Gemini Large Language Model. An API key is secured within the `.env` file and loaded via `os.getenv()`. The `genai.configure()` method initializes the SDK.

### 8.2 Prompt Engineering
The intelligence of the module relies on dynamic string formatting. When a user clicks "Generate Summary", the backend constructs a prompt:
*"Act as a professional travel agent. Write a 3-paragraph travel summary for a flight from {Source} to {Destination} traveling in {Class} class. Include weather tips and packing advice."*

### 8.3 Output Parsing and Fallback
The Gemini API returns a Markdown-formatted string. The frontend uses `marked.js` to render this safely. To ensure enterprise-grade reliability, a **Fallback Mock Mode** is implemented. If the API fails due to rate-limiting, the `except` block catches the error and returns a hardcoded, generic travel summary, ensuring the application never crashes from an external dependency failure.

---

# CHAPTER 9 – TESTING

### 9.1 Testing Methodologies
*   **Unit Testing:** Verified individual functions (e.g., password hashing correctness).
*   **Integration Testing:** Ensured Flask properly queries the PostgreSQL database.
*   **System Testing:** End-to-End (E2E) UI testing using Playwright to automate a full booking flow.
*   **User Acceptance Testing (UAT):** Verified the UI is intuitive and responsive on mobile devices.

### 9.2 Test Cases Table

| Test Case ID | Description | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| TC-01 | Register with existing email | Display error message "Email registered" | Displayed error correctly | PASS |
| TC-02 | Login with invalid password | Display error "Invalid credentials" | Displayed error correctly | PASS |
| TC-03 | Search flight with valid dates | Return list of matching flights | Flights rendered dynamically | PASS |
| TC-04 | Seat Selection | Prevent selection of occupied seat | Seat disabled in UI | PASS |
| TC-05 | Download PDF Ticket | Browser downloads .pdf file | PDF generated and downloaded | PASS |
| TC-06 | ML Recommendation | Return an airline string | Returned optimal airline | PASS |
| TC-07 | Gemini API Call | Return Markdown travel summary | Returned valid HTML parsed text | PASS |

---

# CHAPTER 10 – RESULTS AND SCREENSHOTS

*(Note to Evaluator: Actual images are to be embedded in the final PDF submission. The UI features a dark, glassmorphism theme.)*

*   **Screenshot 1: Home Page & Flight Search** - Displays the responsive input forms.
*   **Screenshot 2: Search Results & Gemini Integration** - Shows the flight list and the AI-generated travel summary.
*   **Screenshot 3: Interactive Booking & Seat Selection** - Displays the CSS Grid seat map.
*   **Screenshot 4: Admin Dashboard** - Showcases the Chart.js visual analytics for revenue.
*   **Screenshot 5: Generated PDF Ticket** - Shows the ReportLab output.

---

# CHAPTER 11 – CONCLUSION
The "AI-Enhanced Flight Booking System" successfully achieves its objectives of bridging traditional web development with modern Artificial Intelligence. By integrating a secure Flask-PostgreSQL architecture with Scikit-Learn Predictive ML and Google Gemini Generative AI, the system provides a vastly superior user experience compared to traditional platforms. The project demonstrates full-stack software engineering proficiency, database optimization, and cloud deployment capabilities.

---

# CHAPTER 12 – FUTURE ENHANCEMENTS
1.  **Live Airline APIs:** Replace the internal static database with external aggregators like Amadeus or Skyscanner API for real-time global flight data.
2.  **Real Payment Gateways:** Integrate Stripe or Razorpay APIs to process real financial transactions instead of simulated success forms.
3.  **Real-Time Flight Tracking:** Add WebSocket integration to show live GPS tracking of flights on an interactive map.
4.  **Mobile Application:** Port the frontend to React Native or Flutter to provide native iOS and Android applications.

---

# REFERENCES
1.  Grinberg, M. (2018). *Flask Web Development: Developing Web Applications with Python*. O'Reilly Media.
2.  Pedregosa, F. et al. (2011). *Scikit-learn: Machine Learning in Python*. Journal of Machine Learning Research, 12, 2825-2830.
3.  Google Developers. (2024). *Gemini API Documentation*. Retrieved from https://ai.google.dev/
4.  PostgreSQL Global Development Group. (2024). *PostgreSQL Documentation*.
5.  ReportLab Inc. (2024). *ReportLab PDF Library User Guide*.
