from math import nan
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as sty

# Page configs
st.set_page_config(layout="wide") # streamlit pag uses compltet width

# containers
dividend_history_container = st.container()

class Dividends:
    # Constructor
    def __init__(self, stock):
        
        # getting stock smbol as str
        self.stock = stock
        self.stock_list = self.stock.split()
        
        # Only 1 Input
        if len(self.stock_list) > 1:
            st.write("WARNING!Only give 1 Ticker")
            exit()
        
        if self.stock:
            self.t = self._extraction_ticker()
            # splitting stock names
        else:
            exit()
        # calling method to extract data
        df = self._extraction_data()

        # calling method create dividend history graph
        self._dividend_history_graph(df)


    def _extraction_ticker(self):

        "Trying to extract data from yfinance"
        try:
            t = yf.Ticker(self.stock)
            
            print("\nExtraction Working\n")
            return t

        except:
            print("\nInvalid Symbol\n")
            exit()

    def _extraction_data(self):
        
        # historical share price
        try:
            df_sp = yf.download(
            tickers = self.stock,
            period = "max",
            interval = "1d",
            group_by = 'ticker',
            prepost = False,
            repair = True
            )
        except:
            st.write("could not historical share price data")
            exit()

        # dividend data
        try:
            df_div = self.t.dividends
        except:
            st.write("dividend data could not be extracted")
            exit()
        
        # removing localize times
        df_div = df_div.tz_localize(None)

        # joining dataframes
        df = df_sp.join(df_div)
        
        print("Dividend Dates")
        print(df[df["Dividends"].notnull()])

        return df

    def _dividend_history_graph(self, df):

        # setting the graph style
        sty.use(['dark_background'])
        st.set_option('deprecation.showPyplotGlobalUse', False)

        # setting overall font size
        plt.rcParams['font.size'] = 8

        # creating the subplot
        fig, ax = plt.subplots(figsize=(20, 6))
        #fig, ax = plt.subplots()

        # Plot the line chart
        ax.plot(df.index, df.Close, label='Line Chart')

        # Set labels and title
        ax.set_xlabel('Year')
        ax.set_ylabel('Dividend Rate')

        # Collecting dividend annotations
        annotations = df[df['Dividends'].notnull()]

        # Add annotations based on the 'label' column
        for i, row in annotations.iterrows():
            x = i
            y = row["Close"]
            # adding date of distr.
            label = str(round(row['Dividends'],2)) + "\n" + i.strftime(('%m/%Y'))
            # adding annotation
            ax.annotate(label, (x, y), textcoords="offset points", xytext=(0,50), ha='center',
                        arrowprops=dict(arrowstyle = '-', connectionstyle = 'arc3',facecolor='red'))

        with dividend_history_container:
            
            st.write("Dividend History")
            # Display the plot
            st.pyplot(fig)
