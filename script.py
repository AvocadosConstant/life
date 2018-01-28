#!/usr/bin/env python3

import argparse
import pandas as pd
from datetime import date
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')


def convert_date(raw):
    return datetime.strptime(raw, '%b %d, %I:%M %p').replace(year=2018)

def calc_duration(row):
    return (row['To'] - row['From']).total_seconds() / 60

def parse_life(life):
    life = life.drop('Comment', axis=1)

    # Transform dates into datetime objects
    life['From'] = life['From'].apply(convert_date)
    life['To'] = life['To'].apply(convert_date)

    # Create duration column
    life['Duration'] = life.apply(calc_duration, axis=1)

    return life

def parse_fit(fit):
    fit = fit.drop(['Distance', 'Distance Unit', 'Time'], axis=1)

    # Transform dates into datetime.date objects
    fit['Date'] = fit['Date'].apply(lambda d : datetime.strptime(d, "%Y-%m-%d").date())
    fit.rename(columns={'Weight (lbs)': 'Weight'}, inplace=True)

    return fit

def plot_exercises(fit, out_file):

    fig, ax = plt.subplots()
    ax.set_autoscale_on(False)
    fig.set_size_inches(16, 12)

    for exercise, grp in fit.groupby(['Exercise']):
        ax = grp.plot(ax=ax, kind='line', x='Date', y='Weight',
                      linewidth=5, label=exercise)

    # Name labels
    plt.title('Exercise Trends', fontsize=36)
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('Weight (lbs)', fontsize=18)

    # Tweak dates
    ax.axis([date(2018, 1, 19), date.today(), 20, 160])
    xfmt = mdates.DateFormatter('%b %-d')
    ax.xaxis.set_major_formatter(xfmt)

    plt.legend(loc='best')

    plt.savefig(out_file, bbox_inches='tight')

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('life', help='ATimeLogger csv')
    parser.add_argument('fit',  help='FitNotes csv')
    args = vars(parser.parse_args())

    life = parse_life(pd.read_csv(args['life']))
    fit = parse_fit(pd.read_csv(args['fit']))

    print(life)
    print(fit)

    plot_exercises(fit, 'data/fit.png')

if __name__ == '__main__':
    main()
