import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Generate sample data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Set up Streamlit
st.title('Multi-Line Interactive Graph')
st.write('Adjust the slider to change the frequency of the sine and cosine curves.')

# Create a slider for adjusting the frequency
frequency = st.slider('Frequency', 1, 10, 1)

# Create the figure and axes
fig, ax = plt.subplots()

# Plot the lines
line1, = ax.plot(x, y1, label='Sine')
line2, = ax.plot(x, y2, label='Cosine')

# Add legend
ax.legend()

# Function to update the plot
def update_plot():
    # Update the y-values based on the frequency slider
    line1.set_ydata(np.sin(frequency * x))
    line2.set_ydata(np.cos(frequency * x))
    
    # Redraw the plot
    fig.canvas.draw()

# Update the plot initially
update_plot()

# Display the plot in Streamlit
st.pyplot(fig)

# Add a button to update the plot
if st.button('Update Plot'):
    update_plot()
