import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Make sure the ml directory exists
os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)

def generate_synthetic_data(num_samples=1200):
    """Generates a realistic travel dataset for flight recommendation model training."""
    np.random.seed(42)
    
    # Predefined lists of values
    sources = ['JFK', 'LAX', 'LHR', 'DXB', 'SIN', 'BOM', 'DEL', 'SFO', 'HND', 'SYD']
    destinations = ['LAX', 'JFK', 'DXB', 'LHR', 'BOM', 'SIN', 'SFO', 'DEL', 'SYD', 'HND']
    airlines = ['Delta Air Lines', 'Emirates', 'British Airways', 'Singapore Airlines', 'IndiGo', 'United Airlines', 'Air India', 'Qantas', 'Japan Airlines', 'Southwest Airlines']
    travel_times = ['Morning', 'Afternoon', 'Evening', 'Night']
    travel_classes = ['Economy', 'Premium Economy', 'Business', 'First Class']
    
    data = []
    
    for _ in range(num_samples):
        source = np.random.choice(sources)
        # Ensure source and destination are different
        dest = np.random.choice([d for d in destinations if d != source])
        
        travel_class = np.random.choice(travel_classes, p=[0.6, 0.2, 0.15, 0.05])
        preferred_airline = np.random.choice(airlines)
        
        # Price correlates with travel class
        if travel_class == 'Economy':
            price = np.random.randint(150, 600)
        elif travel_class == 'Premium Economy':
            price = np.random.randint(600, 1200)
        elif travel_class == 'Business':
            price = np.random.randint(1200, 3000)
        else: # First Class
            price = np.random.randint(3000, 7000)
            
        travel_month = np.random.randint(1, 13)
        travel_time = np.random.choice(travel_times)
        booking_frequency = np.random.randint(1, 15)
        previous_bookings = np.random.randint(0, 50)
        
        # Define recommendation rules (simulate realistic choices)
        # 1. 60% chance of choosing preferred airline
        if np.random.rand() < 0.6:
            rec_airline = preferred_airline
        else:
            # Otherwise, pick based on budget and route
            if price < 400:
                # Budget airlines
                rec_airline = np.random.choice(['IndiGo', 'Southwest Airlines'])
            elif price > 2000:
                # Premium long haul
                rec_airline = np.random.choice(['Emirates', 'Singapore Airlines', 'Japan Airlines'])
            else:
                # Major airlines
                rec_airline = np.random.choice(['Delta Air Lines', 'British Airways', 'United Airlines', 'Air India', 'Qantas'])
                
        # To make it a classification target, let's also output a realistic flight index or label
        data.append({
            'Source': source,
            'Destination': dest,
            'Ticket_Price': price,
            'Travel_Month': travel_month,
            'Airline': rec_airline, # The actual airline booked
            'Travel_Time': travel_time,
            'Booking_Frequency': booking_frequency,
            'Preferred_Airline': preferred_airline,
            'Travel_Class': travel_class,
            'Previous_Bookings': previous_bookings,
            'Recommended_Airline': rec_airline # Target
        })
        
    df = pd.DataFrame(data)
    # Save the raw dataset
    df.to_csv(os.path.join(os.path.dirname(__file__), 'sample_dataset.csv'), index=False)
    print(f"Generated {num_samples} synthetic dataset rows and saved to ml/sample_dataset.csv")
    return df

def train_model():
    # Load dataset
    df = generate_synthetic_data()
    
    # Categorical columns to encode
    categorical_cols = ['Source', 'Destination', 'Airline', 'Travel_Time', 'Preferred_Airline', 'Travel_Class']
    
    # Dictionary to hold label encoders
    encoders = {}
    
    # Apply Label Encoding
    encoded_df = df.copy()
    for col in categorical_cols:
        le = LabelEncoder()
        encoded_df[col] = le.fit_transform(df[col])
        encoders[col] = le
        
    # We also need to encode the target variable 'Recommended_Airline'
    target_le = LabelEncoder()
    encoded_df['Target'] = target_le.fit_transform(df['Recommended_Airline'])
    encoders['Target'] = target_le
    
    # Save Label Encoders
    encoders_path = os.path.join(os.path.dirname(__file__), 'label_encoders.joblib')
    joblib.dump(encoders, encoders_path)
    print("Label encoders saved to ml/label_encoders.joblib")
    
    # Split into features (X) and target (y)
    feature_cols = ['Source', 'Destination', 'Ticket_Price', 'Travel_Month', 'Airline', 
                    'Travel_Time', 'Booking_Frequency', 'Preferred_Airline', 'Travel_Class', 'Previous_Bookings']
    
    X = encoded_df[feature_cols]
    y = encoded_df['Target']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Random Forest Classifier
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=12)
    rf_model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = rf_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel Evaluation:")
    print(f"Accuracy: {accuracy * 100:.2f}%")
    
    # Check accuracy threshold
    target_names = [str(c) for c in target_le.classes_]
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=target_names, zero_division=0))
    
    # Save Model
    model_path = os.path.join(os.path.dirname(__file__), 'flight_recommendation_model.joblib')
    joblib.dump(rf_model, model_path)
    print(f"Model saved to {model_path}")
    
if __name__ == '__main__':
    train_model()
