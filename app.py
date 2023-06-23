
        
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

class App:
    def __init__(self) -> None:    
        
        "Imput Stock Symbol"
        self.stock = st.sidebar.text_input('Enter Stock Symbol').upper()
        self.period = st.sidebar.selectbox(
            'Period?',
            ("1d","5d","1mo","3mo","6mo","1y","2y","5y","10y","ytd","max"))
        self.interval = st.sidebar.selectbox(
            'Interval?',
            ("1m","2m","5m","15m","30m","60m","90m","1h","1d","5d","1wk","1mo","3mo"))
        
        "Saving the Symbols in a list"
        self.stock_list = self.stock.split()
        
        if self.stock:
            self._check_extraction()
        else:
            exit() 

        # display graph
        if st.sidebar.button("Generate Graph"):

            self._stock_price_graph()

    def _check_extraction(self):
        "Trying to extract data from yfinance"
        try:
            t = yf.Ticker(self.stock)
            st.write("Works")
        except:
            st.write("Invalid Symbol")
            exit()

    def _stock_price_graph(self):

        st.line_chart(self._stock_price_data())
        
    def _stock_price_data(self):

        # fetching data
        df = yf.download(
        tickers = self.stock,
        period = self.period,
        interval = self.interval,
        group_by = 'ticker',
        prepost = False,
        repair = True
        )

        # collecting only closing information
        columns_list = []

        for col_name in df:
            if col_name[1] == "Close":
                columns_list.append(pd.DataFrame(df[col_name]))
                
        df_close = pd.concat(columns_list, axis=1)

        return df_close

def main():
    App()

if __name__ == "__main__":
    main()