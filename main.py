from app.home_page import home_page
from app.utils import initialize_session_state

if __name__ == "__main__":
    initialize_session_state()  # Initialize session state before app starts
    home_page()