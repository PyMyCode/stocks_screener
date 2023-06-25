import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

class Fundamentals:
    # Constructor
    def __init__(self, stock):

        self.stock = stock

        self.stock_list = self.stock.split()
        if len(self.stock_list) > 1:
            self.multiple_stocks = True
        else:
            self.multiple_stocks = False
        

        if self.stock:
            self.t = self._extraction()
            # splitting stock names
        else:
            exit()
        
        self._table()
    
    def _extraction(self):
        "Trying to extract data from yfinance"
        try:
            if self.multiple_stocks:
                t = yf.Tickers(self.stock)
            else:
                t = yf.Ticker(self.stock)
            
            print("\nExtraction Working\n")
            return t

        except:
            print("\nInvalid Symbol\n")
            exit()
    
    def _table(self):

        if not self.multiple_stocks:
            info = self.t.info
            df = pd.DataFrame.from_dict(info).head(1) # taking only first element

        else:
            for s in self.stock_list:
                info = self.t.tickers[s].info
                try:
                    df = pd.concat([df, pd.DataFrame.from_dict(info).head(1)])
                except:
                    df = pd.DataFrame.from_dict(info).head(1)
        
        #setting the index
        df = df.set_index('symbol')

        print(df)

        # column list all

        columns_all = list(df.columns)
        columns_all.sort()
        
        columns_selected = st.sidebar.multiselect("Select columns", columns_all)
        columns_selected_size = len(columns_selected)
        
        # display on streamlit
        df_display = df[columns_selected]
        st.dataframe(data = df_display)

        # TODO: Switch Rows with columns while displaying