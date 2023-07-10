
import streamlit as st
from fundamentals import Fundamentals
from graph import Graph
from dividends import Dividends

# Page configs
st.set_page_config(
    page_title="Pymycode Stock Screener",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

class App:

    def __init__(self) -> None:    
        
        "Imput Stock Symbol"
        self.stock = st.sidebar.text_input('Enter Stock Symbol').upper()
        self.overview = st.sidebar.selectbox(
                            'Select the overview?',
                            ('Fundamentals','Dividends', 'Graph'))
        
        if self.overview == "Fundamentals":
            Fundamentals(self.stock)
        if self.overview == "Graph":
            Graph(self.stock)
        if self.overview == "Dividends":
            Dividends(self.stock)

def main():
    App()

if __name__ == "__main__":
    main()