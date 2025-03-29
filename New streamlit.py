import streamlit as st
import json

# Initialize session state
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
    st.session_state.conversation.append(("ai", "Hello! I'm your travel planning assistant. Where would you like to go?"))
    
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
    st.session_state.current_question = 'destination'
    
if 'itinerary_generated' not in st.session_state:
    st.session_state.itinerary_generated = False

def get_ai_response(user_input):
    """Generate AI responses based on conversation stage"""
    # Store the user's response to the current question
    if st.session_state.current_question:
        # Special handling for duration (convert to number)
        if st.session_state.current_question == 'duration' and user_input.isdigit():
            st.session_state.user_info['duration'] = int(user_input)
        else:
            st.session_state.user_info[st.session_state.current_question] = user_input
    
    # Determine next question to ask
    questions_order = [
        'destination', 'duration', 'dates', 'origin', 
        'budget', 'purpose', 'preferences', 'dietary',
        'interests', 'mobility', 'accommodation', 'must_see'
    ]
    
    # Find the next unanswered question
    next_question = None
    for question in questions_order:
        if not st.session_state.user_info[question]:
            next_question = question
            break
    
    st.session_state.current_question = next_question
    
    # Return appropriate response or offer to generate itinerary
    if not next_question:
        return "I have all the information I need! Click the 'Generate Itinerary' button when you're ready."
    
    question_texts = {
        'destination': "Great! Where would you like to go?",
        'duration': "How many days will you be there?",
        'dates': "What are your travel dates? (e.g., July 15-20, 2023)",
        'origin': "Where will you be traveling from?",
        'budget': "What's your approximate budget? (low/medium/high or specific amount)",
        'purpose': "What's the main purpose of your trip? (vacation, business, etc.)",
        'preferences': "What kind of activities do you enjoy? (culture, nature, nightlife, etc.)",
        'dietary': "Any dietary preferences or restrictions?",
        'interests': "Any specific interests within those preferences?",
        'mobility': "Any mobility concerns or walking preferences?",
        'accommodation': "What type of accommodation do you prefer?",
        'must_see': "Any must-see attractions you want included?"
    }
    
    return question_texts[next_question]

def generate_itinerary():
    """Generate a sample itinerary based on user info"""
    info = st.session_state.user_info
    itinerary = f"""
# {info['destination']} Travel Itinerary ({info['duration']} days)

**Travel Dates:** {info['dates'] or 'Not specified'}  
**Budget:** {info['budget']}  
**Travel Style:** {', '.join(info['preferences']) if info['preferences'] else 'Not specified'}

## Day 1: Arrival and Exploration
- Morning: Arrive in {info['destination']}, check into accommodation
- Afternoon: Walking tour of downtown area
- Evening: Dinner at a local restaurant

## Day 2: Cultural Highlights
- Morning: Visit main museums and historical sites
- Afternoon: Local cuisine tasting
- Evening: Leisure time

## Day 3-{info['duration']}: [Custom activities based on your preferences]
"""
    return itinerary

def main():
    st.title("✈️ AI Travel Itinerary Planner")
    
    # Sidebar with collected info
    with st.sidebar:
        st.subheader("Your Trip Details")
        for key, value in st.session_state.user_info.items():
            if value:
                st.write(f"**{key.capitalize()}:** {value}")
        
        if st.button("Reset Conversation"):
            st.session_state.conversation = []
            st.session_state.user_info = {k: None for k in st.session_state.user_info}
            st.session_state.current_question = 'destination'
            st.session_state.itinerary_generated = False
            st.session_state.conversation.append(("ai", "Hello! Where would you like to go?"))
            st.rerun()
    
    # Chat interface
    st.header("Let's Plan Your Trip")
    
    # Display conversation
    for sender, message in st.session_state.conversation:
        with st.chat_message(sender):
            st.write(message)
    
    # User input
    if prompt := st.chat_input("Type your message here..."):
        st.session_state.conversation.append(("user", prompt))
        ai_response = get_ai_response(prompt)
        st.session_state.conversation.append(("ai", ai_response))
        st.rerun()
    
    # Generate itinerary button
    if all(st.session_state.user_info.values()) and not st.session_state.itinerary_generated:
        if st.button("✨ Generate Itinerary"):
            itinerary = generate_itinerary()
            st.session_state.conversation.append(("ai", "Here's your personalized itinerary:"))
            st.session_state.conversation.append(("ai", itinerary))
            st.session_state.itinerary_generated = True
            st.rerun()

if __name__ == "__main__":
    main()
