import streamlit as st
import json
from datetime import datetime

# Initialize session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'user_info' not in st.session_state:
    st.session_state.user_info = {
        'destination': None,
        'duration': None,
        'dates': None,
        'origin': None,
        'budget': None,
        'purpose': None,
        'preferences': [],
        'dietary': None,
        'interests': [],
        'mobility': None,
        'accommodation': None,
        'must_see': None
    }
    st.session_state.current_question = 'destination'  # Track which question we're asking
if 'itinerary_generated' not in st.session_state:
    st.session_state.itinerary_generated = False

def get_ai_response(user_input):
    """Generate AI responses based on conversation stage"""
    # Update user info based on current question
    if st.session_state.current_question:
        if st.session_state.current_question == 'duration' and user_input.isdigit():
            st.session_state.user_info['duration'] = int(user_input)
        elif st.session_state.current_question == 'dates' and '-' in user_input:
            st.session_state.user_info['dates'] = user_input
        else:
            st.session_state.user_info[st.session_state.current_question] = user_input
    
    # Determine next question
    questions_order = [
        'destination', 'duration', 'dates', 'origin', 
        'budget', 'purpose', 'preferences', 'dietary',
        'interests', 'mobility', 'accommodation', 'must_see'
    ]
    
    for question in questions_order:
        if not st.session_state.user_info[question]:
            st.session_state.current_question = question
            break
    else:
        st.session_state.current_question = None
    
    # Return appropriate response
    if not st.session_state.current_question:
        return "I have all the information I need! Would you like me to generate your itinerary now?"
    
    question_texts = {
        'destination': "Great! I can help plan your trip. Where would you like to go?",
        'duration': f"How many days will you be in {st.session_state.user_info['destination']}?",
        'dates': "Do you have specific travel dates in mind? (e.g., July 15-20, 2023)",
        'origin': "Where will you be traveling from?",
        'budget': "What's your approximate budget for this trip? (e.g., low/medium/high or specific amount)",
        'purpose': "What's the main purpose of your trip? (vacation, business, honeymoon, etc.)",
        'preferences': "What kind of activities do you enjoy? (e.g., cultural sites, nature, nightlife, shopping)",
        'dietary': "Do you have any dietary preferences or restrictions?",
        'interests': "Any specific interests within those preferences?",
        'mobility': "Do you have any mobility concerns or preferences about walking distances?",
        'accommodation': "What type of accommodation do you prefer? (hotel, Airbnb, luxury, budget, etc.)",
        'must_see': "Are there any must-see attractions or activities you already know you want to include?"
    }
    
    return question_texts[st.session_state.current_question]

def main():
    st.title("✈️ AI Travel Itinerary Planner")
    
    # Chat interface
    st.header("Let's Plan Your Trip")
    
    # Display conversation history
    for sender, message in st.session_state.conversation:
        with st.chat_message(sender):
            st.write(message)
    
    # User input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to conversation
        st.session_state.conversation.append(("user", prompt))
        
        # Get AI response
        ai_response = get_ai_response(prompt)
        st.session_state.conversation.append(("ai", ai_response))
        
        # Rerun to update the display
        st.rerun()
    
    # Generate itinerary if all info is collected
    if all(st.session_state.user_info.values()) and not st.session_state.itinerary_generated:
        if st.button("✨ Generate Itinerary"):
            st.session_state.itinerary_generated = True
            st.rerun()

if __name__ == "__main__":
    main()
