from playwright.sync_api import sync_playwright
import time
import os

def run_e2e_test():
    # Ensure the videos directory exists
    os.makedirs("videos", exist_ok=True)
    
    print("Starting automated E2E test and video recording...")
    
    with sync_playwright() as p:
        # Launch browser. Set headless=False so you can watch it happen live!
        browser = p.chromium.launch(headless=False, slow_mo=500) 
        
        # Create a new context and configure video recording
        context = browser.new_context(
            record_video_dir="videos/",
            record_video_size={"width": 1280, "height": 720}
        )
        
        page = context.new_page()
        
        try:
            # 1. Go to homepage
            print("Navigating to homepage...")
            BASE_URL = "https://ai-flight-booking-system.vercel.app"
            page.goto(f"{BASE_URL}/")
            
            # 2. Login directly with seeded account
            print("Logging in...")
            page.click("text=Login")
            page.fill("input[name='email']", "passenger@example.com")
            page.fill("input[name='password']", "passenger123")
            page.click("button[type='submit']")
            
            # 3. Search for a flight
            print("Searching for flights...")
            page.click("text=Search Flights")
            page.select_option("select[name='source']", "JFK")
            page.select_option("select[name='destination']", "LAX")
            
            # Select specific date from database seeds
            page.fill("input[name='departure_date']", "2026-07-15")
            
            page.select_option("select[name='travel_class']", "Economy")
            page.click("button[type='submit']")
            
            # 4. Book the first available flight
            print("Selecting a flight...")
            page.wait_for_selector(".flight-card")
            page.click("a.btn-primary-custom >> text='Book Now'")
            
            # 5. Fill passenger details and select seat
            print("Filling passenger info and selecting a seat...")
            page.fill("input[name='passenger_name']", "Automated Tester")
            page.fill("input[name='passenger_age']", "28")
            page.select_option("select[name='passenger_gender']", "Other")
            page.fill("input[name='passenger_email']", "tester@example.com")
            page.fill("input[name='passenger_phone']", "+15550000000")
            
            # Click an available seat (one that doesn't have the 'occupied' class)
            page.click(".seat:not(.occupied)")
            
            page.click("button#submitBookingBtn")
            
            # 6. Simulate Payment
            print("Simulating payment...")
            page.click("text=Credit Card")
            page.click("button#simulateSuccessBtn")
            
            # 7. Verify Success
            print("Verifying success page...")
            page.wait_for_selector("text=Booking Confirmed!")
            print("Test completed successfully!")
            
            # Let it rest for a moment so the video captures the success screen
            time.sleep(2)
            
        except Exception as e:
            print(f"Test failed: {e}")
            
        finally:
            # Close context to save the video
            context.close()
            browser.close()
            print("Video saved in the 'videos/' folder!")

if __name__ == "__main__":
    run_e2e_test()
