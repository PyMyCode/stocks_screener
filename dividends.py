import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as sty

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
        # grouping by year
        df_yearly = df.groupby(df.index.year).agg('sum')

        # create graph
        self._dividend_rate_graph(df_yearly)

        print(df_yearly)

    def _dividend_rate_graph(self, df):

        # setting the graph style
        sty.use(['dark_background'])

        # setting overall font size
        plt.rcParams['font.size'] = 8

        # creating the subplot
        fig, ax = plt.subplots()

        # creating a barplot
        ax.bar(df.index, df.values)
        ax.set_xlabel('Year')
        ax.set_ylabel('Dividend Rate')
        ax.set_title('Yearly Dividend Rate')
        
        # showing all years with dividends
        plt.xticks(df.index, rotation='vertical')

        # annotations
        ax.bar_label(ax.containers[0])
        
        st.pyplot(fig)


