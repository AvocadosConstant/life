#!/usr/bin/env python3

import argparse
import pandas as pd
from datetime import date
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def calc_duration(row):
    return (row['To'] - row['From']).total_seconds() / 60


def parse_life(csv):
    life = pd.read_csv(csv, dtype={'Type': 'category'})
    life.drop('Comment', axis=1, inplace=True)

    # TODO: Handle years
    life['From'] = pd.to_datetime(life['From'], format='%b %d, %I:%M %p')
    life['From'] = life['From'].apply(lambda dt: dt.replace(year=2018))
    life['To'] = pd.to_datetime(life['To'], format='%b %d, %I:%M %p')
    life['To'] = life['To'].apply(lambda dt: dt.replace(year=2018))

    life['Duration'] = life.apply(calc_duration, axis=1)

    return life


def parse_fit(csv):
    fit = pd.read_csv(csv, dtype={'Exercise': 'category', 'Category': 'category'})
    fit.drop(['Distance', 'Distance Unit', 'Time'], axis=1, inplace=True)

    # Transform dates into datetime.date objects
    fit['Date'] = fit['Date'].apply(lambda d : datetime.strptime(d, "%Y-%m-%d").date())
    fit.rename(columns={'Weight (lbs)': 'Weight'}, inplace=True)

    fit['Volume'] = fit.Weight * fit.Reps
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

    life = parse_life(args['life'])
    fit = parse_fit(args['fit'])

    print('\nLife data\n', life.head())
    print(life.info())
    print('\n-------------------\n')
    print('\nFit data\n', fit.head())
    print(fit.info())

    print('\n-------------------\n')
    plot_exercises(fit, 'data/fit.png')


if __name__ == '__main__':
    main()
