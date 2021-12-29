from signal import Signal


class PeriodicSignal(Signal):
    """
        Derived class which inherits of the base Signal class.
        It represents the periodic physiological signals and contains variables, features and processing methods
        that are specific only for this type of signal.
    """

    def __init__(self, signal_file_name, signal_type, columns, windowing_attr=None):
        super().__init__(signal_file_name, signal_type, columns, windowing_attr)
