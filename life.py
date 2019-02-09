import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns


def calc_duration(row):
    return (row['To'] - row['From']).total_seconds() / 60


def parse_life(csv):
    life = pd.read_csv(
        csv,
        usecols=[0,1,2],
        dtype={'Type': 'category'})

    # TODO: Handle years
    life['From'] = pd.to_datetime(life['From'], format='%b %d, %I:%M %p')
    life['From'] = life['From'].apply(lambda dt: dt.replace(year=2018))
    life['To'] = pd.to_datetime(life['To'], format='%b %d, %I:%M %p')
    life['To'] = life['To'].apply(lambda dt: dt.replace(year=2018))

    life['Duration'] = life.apply(calc_duration, axis=1)

    return life


