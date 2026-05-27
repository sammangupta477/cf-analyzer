import requests
import pandas as pd
import streamlit as st

def fetch_failed_tags(handle):
    """Fetches user submissions and extracts tags from failed attempts."""
    url = f"https://codeforces.com/api/user.status?handle={handle}"
    
    try:
        response = requests.get(url)
        data = response.json()     
        if data['status'] != 'OK':
            return None, "Error: User not found or API issue."
        failed_tags = []
        for submission in data['result']:
            if submission.get('verdict') != 'OK':
                tags = submission.get('problem', {}).get('tags', [])
                failed_tags.extend(tags)
        return failed_tags, None
    except Exception as e:
        return None, f"An error occurred: {e}"

# --- Streamlit UI ---
st.set_page_config(page_title="Algorithmic Wrong Submissions Analyzer", page_icon="📊")
st.title("📊 Codeforces Wrong Submissions Analyzer")
st.write("Enter a Codeforces handle to analyze which problem topics they fail on the most.")
handle = st.text_input("Codeforces Handle:", placeholder="e.g., tourist")
if st.button("Analyze"):
    if handle:
        with st.spinner(f"Fetching data for {handle}..."):
            tags, error = fetch_failed_tags(handle)     
            if error:
                st.error(error)
            elif not tags:
                st.success(f"{handle} has no failed submissions!")
            else:
                df = pd.Series(tags).value_counts().reset_index()
                df.columns = ['Topic', 'Failed Submissions']
                top_10 = df.head(10)
                st.subheader(f"Top 10 Weakest Topics for '{handle}'")
                st.bar_chart(data=top_10, x='Topic', y='Failed Submissions', color="#ff4b4b")
                with st.expander("View Raw Data"):
                    st.dataframe(df)
    else:
        st.warning("Please enter a valid handle.")