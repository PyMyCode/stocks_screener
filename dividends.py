from math import nan
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as sty

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
        df, df_sp, df_div = self._extraction_data()

        # calling method to convert data to yearly
        df_yearly = self._data_conversion_yearly(df_sp, df_div)

        # calling method create dividend history graph
        self._dividend_history_graph(df)

        # calculating dividend yield and dividend growth
        self._dividend_parameters(df_yearly)


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

        return df, df_sp, df_div

    def _data_conversion_yearly(self, df_sp, df_div):
        
        print("Converting data to yearly")

        # taking yearly means sp data
        df_sp_yearly = df_sp.groupby(df_sp.index.year).agg('mean')
        df_sp_yearly.index.name = "Year"

        # taking yearly sums div data
        df_div_yearly = df_div.groupby(df_div.index.year).agg("sum")

        # joining div and sp yearly data
        df_yearly = df_sp_yearly.join(df_div_yearly)

        print("FINAL")
        print(df_yearly.head(11))

        return df_yearly
    
    def _dividend_parameters(self, df_yearly):

        # calculating div growth based on Close sp
        df_yearly["DY"] = df_yearly.Dividends / df_yearly.Close

        # calculating dividend growth based on div
        df_yearly["DG"] = df_yearly.Dividends.pct_change()

        print("Yearly Div data")
        print(df_yearly.head(11))


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
        
        # Graph heading
        st.write("Dividend History")
        # Display the plot
        st.pyplot(fig)