import os
import random
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from openai import OpenAI

# Initialize OpenAI API
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

def load_destinations():
    try:
        df = pd.read_csv('destinations.csv')
        st.write("Dataframe loaded successfully:")
        st.write(df.head())  # Display the first few rows of the DataFrame to ensure it loaded correctly
        return df
    except FileNotFoundError:
        st.error("The destinations.csv file was not found. Please ensure it is in the same directory as this script.")
        return pd.DataFrame()  # Return an empty DataFrame if file is not found
    except pd.errors.EmptyDataError:
        st.error("The destinations.csv file is empty. Please provide a valid CSV file with data.")
        return pd.DataFrame()  # Return an empty DataFrame if file is empty

def match_preferences(climate, activities, budget, duration):
    df = load_destinations()
    if df.empty:
        return df
    if 'cost_per_day' not in df.columns:
        st.error("'cost_per_day' column is missing in the CSV file.")
        return pd.DataFrame()  # Return an empty DataFrame if 'cost_per_day' column is missing
    df = df[df['climate'] == climate]
    df = df[df['cost_per_day'] <= budget]
    df['activity_match'] = df['activities'].apply(lambda x: any(activity in x.split(';') for activity in activities))
    df = df[df['activity_match']]
    return df

def get_random_suggestion(df):
    if df.empty:
        return None
    random_index = random.randint(0, len(df) - 1)
    return df.iloc[random_index]

def generate_description(api_key, destination):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=1,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides travel advice."},
            {"role": "user", "content": f"Write a brief travel guide for {destination}. Include key attractions and activities."}
        ]
    )
    return response.choices[0].message.content

# Streamlit app layout
st.title("Travel Destination Suggestion")
st.write("Tell us about your travel preferences and we'll suggest one destination for you!")

# User inputs
climate = st.selectbox("Preferred Climate", ["Tropical", "Temperate", "Cold"])
activities = st.multiselect("Preferred Activities", ["Beaches", "Hiking", "Museums", "Nightlife", "Shopping"])
budget = st.slider("Budget per Day (USD)", 50, 500, 150)
duration = st.slider("Duration of Trip (Days)", 3, 30, 7)

if st.button("Get Suggestions"):
    if not activities:
        st.write("Please select at least one activity.")
    else:
        suggestions = match_preferences(climate, activities, budget, duration)
        if suggestions.empty:
            st.write("No destinations match your preferences. Please adjust your criteria.")
        else:
            random_suggestion = get_random_suggestion(suggestions)
            st.write(f"### Destination: {random_suggestion['destination']}")
            st.write(f"Cost per Day: ${random_suggestion['cost_per_day']}")
            description = generate_description(api_key, random_suggestion['destination'])
            st.write(f"Description: {description}")
