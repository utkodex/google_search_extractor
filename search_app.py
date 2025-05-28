from GLSE import GoogleScraper
import os
import sys
import streamlit as st

def run_streamlit_app():

    # Set up the Streamlit app
    st.title("Search Linkedin Profiles")
    st.write("Enter a query and click the search button.")
    st.write("Check this sheet link: https://docs.google.com/spreadsheets/d/1MV3GXRFBeEUnZ9YxlgJIOlW6y7HOWWC80ugLc_zZPKM/edit?gid=169399261#gid=169399261")

    # Input field for the search query
     # Input fields for search queries
    position_query = st.text_input("Position Search", placeholder="Enter positions to search...")
    industry_query = st.text_input("Industry Search", placeholder="Enter industries to search...")

    # Input fields for page numbers (small-sized and side-by-side)
    col1, col2 = st.columns([1, 1])  # Create two equal columns

    with col1:
        from_page = st.number_input("From page no.", min_value=1, step=1, format="%d")
    with col2:
        to_page = st.number_input("To page no.", min_value=1, step=1, format="%d")

    # Button for searching
    if st.button("Search"):
        if position_query.strip() or industry_query.strip():
            if from_page > to_page:
                st.warning("The 'From page no.' should not be greater than 'To page no.'")
            else:
                st.info("Initializing scraper...")

                # Create an instance of GoogleScraper
                scraper = GoogleScraper()
                scraper.position = position_query
                scraper.industry = industry_query
                scraper.from_page = from_page
                scraper.to_page = to_page

            try:
                scraper.data_scraper()  # Start the scraping process
                st.success("Scraping completed successfully! Data has been uploaded to the Google Sheet.")
            except Exception as e:
                st.error(f"An error occurred during scraping: {e}")
        else:
            st.warning("Please enter a search query before clicking the button.")

if __name__ == "__main__":
    # Check if the script is executed directly or by Streamlit
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        # If Streamlit started this script, run the app
        run_streamlit_app()
    else:
        # Otherwise, launch Streamlit with this script
        os.system(f'streamlit run "{os.path.abspath(__file__)}" run')
