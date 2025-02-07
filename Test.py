import pandas as pd

# Define parameters
base_threshold = 600  # Base threshold for queue length 3
decay_factor = 2  # Decay factor
max_queue_length = 10  # Simulating up to queue length 10

# Initialize counters and thresholds
counters = {i: 0 for i in range(2, max_queue_length + 1)}
thresholds = {i: base_threshold // (decay_factor ** (i - 3)) if i >= 3 else 0 for i in range(2, max_queue_length + 1)}

# Simulate queue length changes over 15 frames
simulation_steps = 15  # Number of frames to simulate
queue_lengths = [3, 4, 5, 6, 5, 4, 3, 5, 6, 7, 5, 4, 3, 4, 5]  # Sample queue length pattern
queue = ["F1", "F2", "F3", "F4", "F5"]  # Initial queue

# Track the simulation results
simulation_results = []

for step in range(simulation_steps):
    current_length = queue_lengths[step]

    # Increment counters for queue lengths 2 to (m-1)
    for i in range(2, current_length):
        counters[i] += 1

    # Reset other counters
    for i in range(2, max_queue_length + 1):
        if i < 2 or i >= current_length:
            counters[i] = 0

    # Check if any counter exceeds its threshold and discard a frame if needed
    discarded_frame = None
    for i in range(3, current_length):
        if counters[i] > thresholds[i]:
            for j in range(2, max_queue_length + 1):
                counters[j] = 0  # Reset all counters

            if queue:
                discarded_frame = queue.pop(0)  # Discard the oldest frame
            break

    # Store the simulation step results
    simulation_results.append({
        "Step": step + 1,
        "Queue Length": current_length,
        "Counters": counters.copy(),
        "Thresholds": thresholds.copy(),
        "Discarded Frame": discarded_frame if discarded_frame else "None",
        "Current Queue": queue.copy()
    })

# Convert to DataFrame for visualization
df_simulation = pd.DataFrame([{
    "Step": result["Step"],
    "Queue Length": result["Queue Length"],
    "Counters": result["Counters"],
    "Thresholds": result["Thresholds"],
    "Discarded Frame": result["Discarded Frame"],
    "Current Queue": result["Current Queue"]
} for result in simulation_results])

# Display the simulation results
print(df_simulation)

# Optionally, save to CSV
df_simulation.to_csv("QM_600_2_Simulation.csv", index=False)
print("Simulation saved to QM_600_2_Simulation.csv")
