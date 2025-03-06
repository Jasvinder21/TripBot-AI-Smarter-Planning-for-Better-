import os
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from datetime import date

# Load API Key securely
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Google Gemini API
genai.configure(api_key=API_KEY)

# Streamlit App Configuration
st.set_page_config(page_title="Plan Your Dream Adventure Trip!", layout="wide")

# Custom CSS for Styling
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #2E86C1;
    }
    .sidebar-title {
        font-size: 22px;
        font-weight: bold;
        color: #154360;
    }
    .stButton>button {
        background-color: #2E86C1;
        color: white;
        font-size: 16px;
        padding: 10px;
        border-radius: 8px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #1B4F72;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown("<h1 class='main-title'>TripBot AI: Smarter Planning for Better Journeys!!</h1>", unsafe_allow_html=True)

# Sidebar Navigation with Image
st.sidebar.image(r"E:\Tripbot.ai Project 1\tripbot.jpg", use_container_width=True)
#st.sidebar.markdown("<h2 class='sidebar-title'>Navigation</h2>", unsafe_allow_html=True)
section_choice = st.sidebar.radio("Choose Section:", 
                                  ("Location Finder", "Trip Planner", "Budget Planner", "Transportation Guide", "Restaurant & Hotel Planner"))

# Function to get text-based responses from Gemini
def get_text_response(prompt, user_input):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content([prompt, user_input])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Function to analyze images using Gemini Vision
def get_image_response(image, prompt):
    try:
        img = Image.open(image)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([prompt, img])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Location Finder
if section_choice == "Location Finder":
    st.subheader("Find a Place by Image 🏞️")
    upload_file = st.file_uploader("Upload an image of a place", type=["jpeg", "jpg", "png"])
    
    if upload_file is not None:
        # Open and display the image in its original size
        img = Image.open(upload_file)
        st.image(img, caption="Uploaded Image (Original Size)", use_container_width=False)  # Keep original size
    
    input_prompt_loc = "Describe this place with its location details and attractions."
    
    if st.button("Find Location!"):
        response = get_image_response(upload_file, input_prompt_loc)
        st.subheader("Tour Bot:")
        st.write(response)

# Trip Planner
elif section_choice == "Trip Planner":
    st.subheader("Plan Your Dream Trip 🏖️")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Select Start Date", date.today())
    with col2:
        end_date = st.date_input("Select End Date", date.today())
    
    input_location = st.text_area("Enter destination and trip details (e.g., 'Goa, 5 days'):")
    input_prompt_planner = f"Provide a detailed itinerary for a trip to {input_location} from {start_date} to {end_date}."
    
    if st.button("Plan my Trip!"):
        response = get_text_response(input_prompt_planner, input_location)
        st.subheader("Trip Planner:")
        st.write(response)

# Budget Planner
elif section_choice == "Budget Planner":
    st.subheader("Plan Your Trip Budget 💰")
    budget = st.number_input("Enter your total budget (INR/USD):", min_value=1000, step=500)
    input_location = st.text_area("Enter your destination:")
    
    input_prompt_budget = f"Suggest a budget plan for a trip to {input_location} within {budget} INR/USD, including accommodation, food, transport, and sightseeing."
    
    if st.button("Plan My Budget!"):
        response = get_text_response(input_prompt_budget, input_location)
        st.subheader("Budget Guide:")
        st.write(response)

# Transportation Guide
elif section_choice == "Transportation Guide":
    st.subheader("Find Best Transportation Options 🚆🚖")
    input_location = st.text_area("Enter your travel destination:")
    
    input_prompt_transport = f"Provide travel options for reaching {input_location}, including flights, trains, buses, and rental services with estimated costs."
    
    if st.button("Find Transport!"):
        response = get_text_response(input_prompt_transport, input_location)
        st.subheader("Transport Guide:")
        st.write(response)
        
        st.markdown("""
        **Direct Booking Links:**
        - [Book Flights](https://www.skyscanner.com)
        - [Train Tickets](https://www.irctc.co.in)
        - [Bus Booking](https://www.redbus.in)
        - [Car Rentals](https://www.uber.com)
        """, unsafe_allow_html=True)

# Restaurant & Hotel Planner
elif section_choice == "Restaurant & Hotel Planner":
    st.subheader("Find Best Restaurants & Hotels 🍽️🏨")
    input_location = st.text_area("Enter location to find hotels & restaurants:")
    
    input_prompt_hotel = f"Provide top restaurants and hotels in {input_location} with ratings and pricing."
    
    if st.button("Find Hotels & Restaurants!"):
        response = get_text_response(input_prompt_hotel, input_location)
        st.subheader("Accommodation Bot:")
        st.write(response)
        
        st.markdown("""
        **Useful Booking Links:**
        - [Find Hotels](https://www.booking.com)
        - [Best Restaurants](https://www.zomato.com)
        """, unsafe_allow_html=True)
