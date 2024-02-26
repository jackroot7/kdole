#!/bin/bash

# Start Streamlit Dashboard
echo "Starting Streamlit Dashboard..."
streamlit run app.py &
STREAMLIT_PID=$!
echo "Streamlit Dashboard running in background with PID: $STREAMLIT_PID"
# Wait a bit for Streamlit to fully start
sleep 10

# Assuming user input is handled through the dashboard and available to the channel service
echo "Running Channel Service..."
python extractors/channels.py
echo "Channel Service completed."

echo "Running Videos Information Extraction..."
python extractors/main.py
echo "Videos Information Extraction completed."

echo "Performing Sentiment Analysis..."
python sentimental_analysis/sentimental.py
echo "Sentiment Analysis completed."

echo "Running Database Service to save data..."
# Assuming the database service script is ready to pick up and save the data
# Add the database service command here if it's a script or a command to start a service
# For the sake of example, I'm assuming a script named `save_to_db.py`
python database_service/save_to_db.py
echo "Data saved to database."

echo "All processes completed."

# Optionally, you can kill the Streamlit process if needed
# kill $STREAMLIT_PID
# echo "Streamlit Dashboard has been stopped."
