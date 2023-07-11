from Modules import recently_played,monthly_report,weekly_report,yearly_report
import streamlit as st

st.set_page_config(page_title="Spotify Analytics Dashboard",layout="wide")

@st.cache_data()
def user_specific():
    """
    A function that retrieves the recently played data specific to the user.

    Returns:
        The recently played data specific to the user.
    """
    return recently_played.get()

st.title("Spotify Analytics Dashboard")
recently_played_df = user_specific()

available_types = ('Weekly','Monthly','Yearly')
option = st.selectbox("Select Type Of Report",available_types)

if option == available_types[0]:
    weekly_report.get(recently_played_df)
elif option == available_types[1]:
    monthly_report.get(recently_played_df)
elif option == available_types[2]:
    yearly_report.get(recently_played_df)