import pandas as pd


def predict_qoe(ftsd, interrupt_freq, interrupt_magnitude,delay):
    """
    Predicts QoE using three different models from Table 7.
    :param ftsd: Frame Time Standard Deviation (ms)
    :param interrupt_freq: Interrupt Frequency (/s)
    :param interrupt_magnitude: Interrupt Magnitude (ms/s)
    :return: QoE predictions for each model
    """
    qoe_ftsd = -0.056 * ftsd + 4.6
    qoe_if = -0.023 * interrupt_freq + 3.7
    qoe_im = -0.004 * interrupt_magnitude + 4.0
    qoe_delay = -0.0148 * delay + 4.76

    # Ensure QoE is within range [1, 5]
    qoe_ftsd = max(1.0, min(5.0, qoe_ftsd))
    qoe_if = max(1.0, min(5.0, qoe_if))
    qoe_im = max(1.0, min(5.0, qoe_im))
    qoe_delay = max(1.0, min(5.0, qoe_delay))
    return qoe_ftsd, qoe_if, qoe_im, qoe_delay


def process_qoe_csv(input_csv, output_per_run_csv, output_grouped_csv):
    """
    Reads a CSV, computes QoE per run and per setting, and saves results.
    """
    df = pd.read_csv(input_csv)

    # Ensure correct column names
    required_columns = ['Average Queue Size','Std Dev Frame Time', 'Interrupt Frequency (/s)', 'Interrupt Mag (ms/s)',
                        'Buffer Size', 'Jitter Magnitude', 'Policy', 'Base Length for Thresholding','Threshold', 'Decay']

    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Convert necessary columns to numeric
    numeric_columns = ['Average Queue Size','Std Dev Frame Time', 'Interrupt Frequency (/s)', 'Interrupt Mag (ms/s)']
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # Compute QoE for each row (Per Run)
    df['QoE_FTSD'] = df.apply(lambda row: predict_qoe(row['Std Dev Frame Time'], 0, 0,0)[0], axis=1)
    df['QoE_IF'] = df.apply(lambda row: predict_qoe(0, row['Interrupt Frequency (/s)'], 0,0)[1], axis=1)
    df['QoE_IM'] = df.apply(lambda row: predict_qoe(0, 0, row['Interrupt Mag (ms/s)'],0)[2], axis=1)
    df['QoE_Delay'] = df.apply(lambda row: predict_qoe(0, 0,0, row['Average Queue Size'])[3], axis=1)

    # Keep only required columns for per-run QoE
    per_run_df = df[['Buffer Size', 'Jitter Magnitude', 'Policy', 'Base Length for Thresholding', 'Threshold', 'Decay',
                     'Std Dev Frame Time', 'Interrupt Frequency (/s)', 'Interrupt Mag (ms/s)',
                     'QoE_FTSD', 'QoE_IF', 'QoE_IM', 'QoE_Delay']]

    # Save per-run QoE file
    per_run_df.to_csv(output_per_run_csv, index=False)
    print(f"QoE per run saved to {output_per_run_csv}")

    # Group by settings and compute mean values
    grouped_df = per_run_df.groupby(
        ['Buffer Size', 'Jitter Magnitude', 'Policy', 'Base Length for Thresholding','Threshold','Decay']).mean()

    # Save grouped QoE file
    grouped_df.to_csv(output_grouped_csv)
    print(f"Grouped QoE results saved to {output_grouped_csv}")

# Example usage
if __name__ == "__main__":
    input_csv = "./data/2025-03-04_22-24-12//iteration_summary.csv"
    output_per_run_csv = "./data/2025-03-04_22-24-12//qoe_results_per_iteration.csv"
    output_grouped_csv = "./data/2025-03-04_22-24-12//qoe_results_grouped.csv"

    process_qoe_csv(input_csv, output_per_run_csv, output_grouped_csv)
