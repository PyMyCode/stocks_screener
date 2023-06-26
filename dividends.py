import streamlit as st
import yfinance as yf
import pandas as pd

class Dividends:
    # Constructor
    def __init__(self, stock):
        
        self.stock = stock

        self.stock_list = self.stock.split()
        
        # Only 1 Input
        if len(self.stock_list) > 1:
            st.write("WARNING!Only give 1 Ticker")
            exit()
        
        if self.stock:
            self.t = self._extraction()
            # splitting stock names
        else:
            exit()
    
        self._dividends_info()
    
    def _extraction(self):
        "Trying to extract data from yfinance"
        try:
            t = yf.Ticker(self.stock)
            
            print("\nExtraction Working\n")
            return t

        except:
            print("\nInvalid Symbol\n")
            exit()
    
    def _dividends_info(self):

        df = self.t.dividends

        df_yearly = df.groupby(df.index.year).agg('sum')

        st.bar_chart(df_yearly)
        st.dataframe(df_yearly)
        st.dataframe(df)
