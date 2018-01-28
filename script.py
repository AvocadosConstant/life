#!/usr/bin/env python3

import argparse
import pandas as pd
from datetime import datetime

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
    return fit

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('life', help='ATimeLogger csv')
    parser.add_argument('fit',  help='FitNotes csv')
    args = vars(parser.parse_args())

    life = parse_life(pd.read_csv(args['life']))
    fit = parse_fit(pd.read_csv(args['fit']))

    print(life)
    print(fit)


if __name__ == '__main__':
    main()
