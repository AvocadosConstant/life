#!/usr/bin/env python3

import argparse
import pandas as pd
from datetime import date
from datetime import datetime
from datetime import timedelta
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


def parse_strong(csv):
    strong = pd.read_csv(csv, sep=';',
            usecols=list(range(6)),
            parse_dates=['Date'],
            header=0,
            names='Date Workout Exercise Order Weight Reps'.split(),
            dtype={'Exercise': 'category'})

    # Build number of sets column
    for workout, exercise in strong.groupby(['Date', 'Exercise']):
        strong.loc[exercise.index.values, 'Sets'] = int(exercise.Order.max())
    strong['Sets'] = strong['Sets'].astype(int)

    # Build volume column
    strong['Volume'] = strong.Weight * strong.Sets * strong.Reps

    # Reorder cols for clarity
    strong = strong['Date Workout Exercise Order Weight Sets Reps Volume'.split()]

    return strong


def plot_exercises(data, metric, out_file, exercises=None):
    valid = {'Weight', 'Sets', 'Reps', 'Volume'}
    if metric not in valid:
        raise ValueError(
            'plot_exercises: metric must be one of {}'.format(valid))

    sns.set()
    sns.set_style('whitegrid')
    sns.set_palette(sns.color_palette('hls', data.Exercise.nunique()))

    plt.figure()
    fig, ax = plt.subplots()

    for exercise, grp in data.groupby(['Exercise']):
        if not exercises or exercise in exercises:
            filtered = grp.groupby(['Date'])[metric]
            points = filtered.sum() if metric in ['Reps', 'Volume'] else filtered.max()
            ax = points.plot(
                ax=ax, kind='line', marker='o', linestyle='-',
                alpha=0.7, linewidth=2, label=exercise)

    # Styling graph
    plt.title('Strength Training {}'.format(metric), fontsize=20)
    ax.set_xlabel('Date', fontsize=12)

    units = '' if metric in {'Sets', 'Reps'} else ' (lbs)'
    ax.set_ylabel(metric + units, fontsize=12)

    ax.margins(.8, .2)
    fig.set_size_inches(16, 12)
    plt.legend(loc='best')

    day_offset = timedelta(days=2)
    ax.set_ylim(0, ax.get_ylim()[1] * 1.1)
    ax.set_xlim(data.Date.min() - day_offset,
                data.Date.max() + day_offset)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %-d'))

    plt.savefig(out_file)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('life',     help='ATimeLogger csv')
    parser.add_argument('strong',   help='Strong csv')
    args = vars(parser.parse_args())

    life = parse_life(args['life'])
    strong = parse_strong(args['strong'])

    print('\nLife data\n{}\n{}\n--------\n'.format(
        life.head(10), life.info()))
    print('\nStrong data\n{}\n{}\n--------\n'.format(
        strong.drop('Workout', axis=1).head(10), strong.info()))

    print('Plotting some graphs...\n')
    plot_exercises(strong, 'Weight', 'data/strong_weight1.png', exercises=['Bench Press', 'Squat', 'Deadlift'])
    plot_exercises(strong, 'Weight', 'data/strong_weight2.png')
    plot_exercises(strong, 'Sets', 'data/strong_sets.png')
    plot_exercises(strong, 'Reps', 'data/strong_reps.png')
    plot_exercises(strong, 'Volume', 'data/strong_volume.png')


if __name__ == '__main__':
    main()
