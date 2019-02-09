from datetime import timedelta
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns


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
