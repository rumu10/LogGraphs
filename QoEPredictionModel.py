def predict_qoe(ftsd=None, interrupt_magnitude=None):
    """
    Predicts QoE using either Frame Time Standard Deviation (FTSD) or Interrupt Magnitude.
    :param ftsd: Frame Time Standard Deviation (ms)
    :param interrupt_magnitude: Interrupt Magnitude (ms/s)
    :return: Predicted QoE value
    """
    if ftsd is not None:
        qoe = -0.056 * ftsd + 4.6
    elif interrupt_magnitude is not None:
        qoe = -0.004 * interrupt_magnitude + 4.0
    else:
        raise ValueError("Either ftsd or interrupt_magnitude must be provided.")

    return max(1.0, min(5.0, qoe))  # Ensures QoE stays within the 1-5 range
