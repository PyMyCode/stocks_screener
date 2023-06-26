import streamlit as st
import yfinance as yf
import pandas as pd
import pickle

class Fundamentals:
    # Constructor
    def __init__(self, stock):

        print("\n\n\n"+"New")

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

        columns_selected = self._columns_selected(df)

        print("\n" + "After being called")
        print(columns_selected)
        print("\n")
        
        # display on streamlit
        df_display = df[columns_selected]

        st.table(data = df_display.T)

    def _columns_selected(self, df):

        "creating the kpi cluster selectbox"
        kpi_cluster = st.sidebar.selectbox(
                            'Select the KPI Cluster?',
                            ('n.a.', 'shareprice', 'dividend'))
        
        if kpi_cluster == "n.a.":
            columns_selected = []
        else:
            # extract list from pickle files
            file_name = kpi_cluster + ".pickle"
            with open(file_name, 'rb') as file:
                columns_selected = pickle.load(file)
            
        "Creating a filter"
        columns_all = list(df.columns)
        columns_all.sort()

        columns_selected_2 = st.sidebar.multiselect("Select columns", columns_all)

        # adding selected filter to the list
        if len(columns_selected_2) > 0:
            columns_selected = columns_selected + columns_selected_2
        
        return columns_selected