import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Load the CSV file
file_path = './data/server/log_20241113T220727405Z.csv'  # Update with your file path
data = pd.read_csv(file_path)

# Assign appropriate column names
data.columns = ['interval','timer']

# Convert string columns to numeric (if applicable)
data['timer'] = pd.to_numeric(data['timer'], errors='coerce')
data['interval'] = pd.to_numeric(data['interval'], errors='coerce')

# Drop any rows with missing values after conversion
data.dropna(inplace=True)


# Function to plot and save the graphs without scientific notation
def plot_and_save_graph(x, y, xlabel, ylabel, title, color, filename, xlim=(2, 60)):
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label=ylabel, color=color)
    plt.xlim(xlim)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    # Disable scientific notation for the Y-axis
    ax = plt.gca()  # Get the current axis
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))
    ax.yaxis.get_major_formatter().set_scientific(False)

    plt.legend()
    plt.grid(True)
    plt.savefig(filename)  # Save the figure to a file
    plt.show()  # Close the plot to avoid display


# 1. Enqueue timer vs Enqueue interval (in nanoseconds)
plot_and_save_graph(data['timer'], data['interval'],
                    'Timer (A) [seconds]', 'Interval (B) [ns]',
                    'Frame Send Interval From Server', 'b',
                    'server_interval.png')
