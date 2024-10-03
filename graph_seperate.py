import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Load the CSV file
file_path = 'Q2_NJ_MA.csv'  # Update with your file path
data = pd.read_csv(file_path)

# Assign appropriate column names
data.columns = ['timer', 'enqueue_interval', 'deque_timer', 'dequeue_interval',
                'frames_in_queue', 'moving_avg', 'running_avg_5','queue_size(D)']

# Convert string columns to numeric (if applicable)
data['timer'] = pd.to_numeric(data['timer'], errors='coerce')
data['enqueue_interval'] = pd.to_numeric(data['enqueue_interval'], errors='coerce')
data['deque_timer'] = pd.to_numeric(data['deque_timer'], errors='coerce')
data['dequeue_interval'] = pd.to_numeric(data['dequeue_interval'], errors='coerce')
data['frames_in_queue'] = pd.to_numeric(data['frames_in_queue'], errors='coerce')
data['moving_avg'] = pd.to_numeric(data['moving_avg'], errors='coerce')
data['running_avg_5'] = pd.to_numeric(data['running_avg_5'], errors='coerce')
data['queue_size(D)'] = pd.to_numeric(data['queue_size(D)'], errors='coerce')

# Drop any rows with missing values after conversion
data.dropna(inplace=True)


# Function to plot and save the graphs without scientific notation
def plot_and_save_graph(x, y, xlabel, ylabel, title, color, filename, xlim=(0, 5)):
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
plot_and_save_graph(data['timer'], data['enqueue_interval'],
                    'Enqueue Timer (A) [seconds]', 'Enqueue Interval (B) [ns]',
                    'Enqueue Timer vs Enqueue Interval', 'b',
                    'enqueue_timer_vs_enqueue_interval.png')

# 2. Dequeue timer vs Dequeue interval (in nanoseconds)
plot_and_save_graph(data['deque_timer'], data['dequeue_interval'],
                    'Dequeue Timer (C) [seconds]', 'Dequeue Interval (D) [ns]',
                    'Dequeue Timer vs Dequeue Interval', 'r',
                    'deque_timer_vs_dequeue_interval.png')

# 3. Frames in Queue vs Enqueue timer
plot_and_save_graph(data['timer'], data['frames_in_queue'],
                    'Enqueue Timer (A) [seconds]', 'Frames in Queue (E)',
                    'Frames in Queue vs Enqueue Timer', 'g',
                    'frames_in_queue_vs_enqueue_timer.png')


# 4. Moving Average vs Enqueue timer
plot_and_save_graph(data['timer'], data['moving_avg'],
                    'Enqueue Timer (A) [seconds]', 'Moving Average (F)',
                    'Moving Average vs Enqueue Timer', 'm',
                    'moving_avg_vs_enqueue_timer.png')

# 5. Running Average (Window Size 5) vs Enqueue Timer
plot_and_save_graph(data['timer'], data['running_avg_5'],
                    'Enqueue Timer (A) [seconds]', 'Running Average (Window Size 5) (G)',
                    'Running Average (Window Size 5) vs Enqueue Timer', 'c',
                    'running_avg_vs_enqueue_timer.png')


# 5. Running Average (Window Size 5) vs Enqueue Timer
plot_and_save_graph(data['timer'], data['running_avg_5'],
                    'Enqueue Timer (A) [seconds]', 'Running Average (Window Size 5) (G)',
                    'Running Average (Window Size 5) vs Enqueue Timer', 'c',
                    'running_avg_vs_enqueue_timer.png')


# 5. queue size while dequeue
plot_and_save_graph(data['deque_timer'], data['queue_size(D)'],
                    'Dequeue Timer (A) [seconds]', 'queue_size(D)',
                    'queue_size(D)', 'c',
                    'queueSize_vs_dqueue_timer.png')