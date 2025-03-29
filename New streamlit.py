import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import wikipedia

# Configure Wikipedia
wikipedia.set_lang("en")

def simple_web_search(query):
    """Fallback Google search via direct HTML scraping"""
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract top 3 results
        results = []
        for g in soup.find_all('div', class_='tF2Cxc')[:3]:
            title = g.find('h3').text if g.find('h3') else "No title"
            link = g.find('a')['href'] if g.find('a') else "#"
            results.append(f"- [{title}]({link})")
        
        return "\n".join(results) if results else "No web results found"
    except:
        return "Failed to fetch web results"

def get_wikipedia_content(destination):
    """Get Wikipedia summary without API"""
    try:
        page = wikipedia.page(destination, auto_suggest=True)
        return {
            "summary": wikipedia.summary(destination, sentences=3),
            "url": page.url,
            "attractions": [section.title for section in page.sections if "attraction" in section.title.lower()]
        }
    except:
        return None

def generate_itinerary(destination, days):
    """Generate itinerary using only web scraping"""
    wiki_data = get_wikipedia_content(destination)
    activities = simple_web_search(f"top things to do in {destination}")
    
    itinerary = f"""
# {destination} Itinerary ({days} days)

## 🌐 About (from Wikipedia)
{wiki_data['summary'] if wiki_data else simple_web_search(f"{destination} tourism")}

## 🗺️ Top Activities (from Web)
{activities}

## Sample Day Plan
1. **Morning:** Explore city center  
2. **Afternoon:** Visit top attraction  
3. **Evening:** Local cuisine experience
"""
    return itinerary

# Streamlit UI
st.title("🌍 Web-Based Travel Planner")
destination = st.text_input("Destination")
days = st.number_input("Days", min_value=1, max_value=30, value=5)

if st.button("Generate Itinerary"):
    with st.spinner(f"Researching {destination}..."):
        st.markdown(generate_itinerary(destination, days))
