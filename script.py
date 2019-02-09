#!/usr/bin/env python3

import argparse
import pandas as pd
from datetime import date
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

import life
import strong

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('life',     help='ATimeLogger csv')
    parser.add_argument('strong',   help='Strong csv')
    args = vars(parser.parse_args())

    life_data = life.parse_life(args['life'])
    strong_data = strong.parse_strong(args['strong'])

    print('\nLife data\n{}\n{}\n--------\n'.format(
        life_data.head(10), life_data.info()))
    #print('\nStrong data\n{}\n{}\n--------\n'.format(
    #    strong_data.drop('Workout', axis=1).head(10), strong_data.info()))

    #print('Plotting some graphs...\n')
    #strong.plot_exercises(strong_data, 'Weight', 'data/strong_weight1.png', exercises=['Bench Press', 'Squat', 'Deadlift'])
    #strong.plot_exercises(strong_data, 'Weight', 'data/strong_weight2.png')
    #strong.plot_exercises(strong_data, 'Sets', 'data/strong_sets.png')
    #strong.plot_exercises(strong_data, 'Reps', 'data/strong_reps.png')
    #strong.plot_exercises(strong_data, 'Volume', 'data/strong_volume.png')


if __name__ == '__main__':
    main()
