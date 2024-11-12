import pandas as pd

# Load the CSV file
file_path = "./data/1"  # Update with the actual file path
raw_data = pd.read_csv(file_path, header=None)

# Assign column names
raw_data.columns = [
    'timer', 'enqueue_interval', 'deque_timer', 'dequeue_interval',
    'frames_in_queue', 'running_avg_5', 'queue_size(D)',
    'time_taken_update', 'expected_sleep', 'sleep_difference', 'start_time_interval'
]

# Focus on the 'dequeue_interval' column for magnitude and interrupts
dequeue_times = raw_data['dequeue_interval']

# Define constants
expected_frame_time_ms = 16.67  # Expected time for 60 FPS
interrupt_threshold_ms = 33.34  # Double the expected time

# Calculate interrupts and magnitude
interrupt_count = 0
magnitude_sum = 0

for dequeue_time in dequeue_times:
    if dequeue_time > interrupt_threshold_ms:
        interrupt_count += 1
        magnitude_sum += (dequeue_time - interrupt_threshold_ms) # frame time - double the frame time

# Calculate run duration in seconds
run_duration_seconds = len(dequeue_times) * (expected_frame_time_ms / 1000)  # Convert to seconds

# Calculate metrics
interrupts_per_second = interrupt_count / run_duration_seconds
magnitude_per_second = magnitude_sum / run_duration_seconds

# Print results
print(f"Interrupts per second: {interrupts_per_second}")
print(f"Magnitude (ms/s): {magnitude_per_second}")
