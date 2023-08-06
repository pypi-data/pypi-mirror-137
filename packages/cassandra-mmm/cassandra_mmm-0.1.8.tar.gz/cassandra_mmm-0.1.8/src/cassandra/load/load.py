import os
def load_current_directory():
    import pathlib
    return pathlib.Path().resolve()

def load_holidays_csv():
    config_path = 'references/dataset_holidays.csv'
    return config_path