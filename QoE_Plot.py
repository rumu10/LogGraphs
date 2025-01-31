import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your QoE per iteration results file
qoe_file_path = "./data/2025-01-29_23-15-39/qoe_results_per_iteration.csv"
df_qoe = pd.read_csv(qoe_file_path)

# Convert necessary columns to numeric
numeric_columns = ['Jitter Magnitude', 'Policy', 'QoE_FTSD', 'QoE_IF', 'QoE_IM']
df_qoe[numeric_columns] = df_qoe[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Set up the plotting style
sns.set(style="whitegrid")

# 1️⃣ QoE vs Jitter Magnitude (Grouped by Policy)
plt.figure(figsize=(10, 6))
sns.lineplot(data=df_qoe, x='Jitter Magnitude', y='QoE_FTSD', hue='Policy', marker="o", linewidth=2.5)
plt.title("QoE vs Jitter Magnitude (Grouped by Policy)")
plt.xlabel("Jitter Magnitude")
plt.ylabel("QoE (FTSD Model)")
plt.legend(title="Policy")
plt.grid(True)
plt.show()

# 2️⃣ QoE per Policy (Grouped by Jitter Magnitude)
plt.figure(figsize=(10, 6))
sns.boxplot(data=df_qoe, x='Policy', y='QoE_FTSD', hue='Jitter Magnitude')
plt.title("QoE per Policy (Grouped by Jitter Magnitude)")
plt.xlabel("Policy")
plt.ylabel("QoE (FTSD Model)")
plt.legend(title="Jitter Magnitude")
plt.grid(True)
plt.show()
