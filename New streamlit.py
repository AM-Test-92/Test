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
if 'itinerary_generated' not in st.session_state:
    st.session_state.itinerary_generated = False

# System prompts
def get_ai_response(user_input):
    """Generate AI responses based on conversation stage"""
    
    # Check what information we still need
    missing_info = [k for k, v in st.session_state.user_info.items() if v is None or v == []]
    
    if not missing_info:
        return "I have all the information I need! Would you like me to generate your itinerary now?"
    
    # First question - destination
    if not st.session_state.user_info['destination']:
        return "Great! I can help plan your trip. Where would you like to go?"
    
    # Subsequent questions
    if not st.session_state.user_info['duration']:
        return f"How many days will you be in {st.session_state.user_info['destination']}?"
    
    if not st.session_state.user_info['dates']:
        return "Do you have specific travel dates in mind? (e.g., July 15-20, 2023)"
    
    if not st.session_state.user_info['origin']:
        return "Where will you be traveling from?"
    
    if not st.session_state.user_info['budget']:
        return "What's your approximate budget for this trip? (e.g., low/medium/high or specific amount)"
    
    if not st.session_state.user_info['purpose']:
        return "What's the main purpose of your trip? (vacation, business, honeymoon, etc.)"
    
    if not st.session_state.user_info['preferences']:
        return "What kind of activities do you enjoy? (e.g., cultural sites, nature, nightlife, shopping)"
    
    if not st.session_state.user_info['dietary']:
        return "Do you have any dietary preferences or restrictions?"
    
    if not st.session_state.user_info['interests']:
        return "Any specific interests within those preferences? (e.g., if you said 'culture', do you prefer museums or historical sites?)"
    
    if not st.session_state.user_info['mobility']:
        return "Do you have any mobility concerns or preferences about walking distances?"
    
    if not st.session_state.user_info['accommodation']:
        return "What type of accommodation do you prefer? (hotel, Airbnb, luxury, budget, etc.)"
    
    if not st.session_state.user_info['must_see']:
        return "Are there any must-see attractions or activities you already know you want to include?"

def generate_itinerary():
    """Generate a sample itinerary based on user info"""
    info = st.session_state.user_info
    
    itinerary = f"""
# {info['destination']} Travel Itinerary ({info['duration']} days)

**Travel Dates:** {info['dates'] or 'Not specified'}  
**Budget:** {info['budget']}  
**Travel Style:** {', '.join(info['preferences']) if info['preferences'] else 'Not specified'}

## Day 1: Arrival and Exploration
- **Morning:** Arrive in {info['destination']}, check into accommodation
- **Afternoon:** Walking tour of downtown area
- **Evening:** Dinner at a local restaurant ({info['dietary'] or 'no'} dietary restrictions noted)

## Day 2: Cultural Highlights
- **Morning:** Visit main museums and historical sites
- **Afternoon:** Local cuisine tasting
- **Evening:** {info['preferences'][0] if info['preferences'] else 'Leisure'} activities

## Day 3: Nature and Relaxation
- **Full Day:** Excursion to nearby natural attractions
- **Evening:** Free time to explore at your own pace

## Additional Notes:
- Mobility considerations: {info['mobility'] or 'none noted'}
- Accommodation type: {info['accommodation'] or 'not specified'}
- Must-see attractions included: {info['must_see'] or 'none specified'}
"""
    return itinerary

def main():
    st.title("✈️ AI Travel Itinerary Planner")
    st.caption("Plan your perfect trip with AI assistance")
    
    # Sidebar for user info summary
    with st.sidebar:
        st.subheader("Your Trip Details")
        if st.session_state.user_info['destination']:
            st.write(f"**Destination:** {st.session_state.user_info['destination']}")
        if st.session_state.user_info['duration']:
            st.write(f"**Duration:** {st.session_state.user_info['duration']} days")
        if st.session_state.user_info['budget']:
            st.write(f"**Budget:** {st.session_state.user_info['budget']}")
        
        if st.button("Reset Conversation"):
            st.session_state.conversation = []
            st.session_state.user_info = {k: None for k in st.session_state.user_info}
            st.session_state.itinerary_generated = False
            st.rerun()
    
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
        
        # Update user info based on conversation
        if not st.session_state.user_info['destination']:
            st.session_state.user_info['destination'] = prompt
        elif not st.session_state.user_info['duration'] and prompt.isdigit():
            st.session_state.user_info['duration'] = int(prompt)
        elif not st.session_state.user_info['dates'] and "-" in prompt:
            st.session_state.user_info['dates'] = prompt
        # Add more conditions for other fields...
        
        # Get AI response
        ai_response = get_ai_response(prompt)
        st.session_state.conversation.append(("ai", ai_response))
        
        # Rerun to update the display
        st.rerun()
    
    # Generate itinerary if all info is collected
    if all(st.session_state.user_info.values()) and not st.session_state.itinerary_generated:
        if st.button("✨ Generate Itinerary"):
            itinerary = generate_itinerary()
            st.session_state.conversation.append(("ai", "Here's your personalized itinerary!"))
            st.session_state.itinerary_generated = True
            st.session_state.conversation.append(("ai", itinerary))
            st.rerun()
    
    # Display generated itinerary if available
    if st.session_state.itinerary_generated:
        st.divider()
        st.subheader("Your Personalized Itinerary")
        st.write(st.session_state.conversation[-1][1])
        
        # Add download option
        itinerary_json = json.dumps(st.session_state.user_info, indent=2)
        st.download_button(
            label="📥 Download Itinerary",
            data=itinerary_json,
            file_name=f"{st.session_state.user_info['destination']}_itinerary.json",
            mime="application/json"
        )

if __name__ == "__main__":
    main()