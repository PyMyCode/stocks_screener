
        
import streamlit as st
from fundamentals import Fundamentals
from graph import Graph

class App:
    def __init__(self) -> None:    
        
        "Imput Stock Symbol"
        self.stock = st.sidebar.text_input('Enter Stock Symbol').upper()
        self.overview = st.sidebar.selectbox(
                            'Select the overview?',
                            ('Fundamentals', 'Graph'))
        
        if self.overview == "Fundamentals":
            Fundamentals(self.stock)
        if self.overview == "Graph":
            Graph(self.stock)

def main():
    App()

if __name__ == "__main__":
    main()