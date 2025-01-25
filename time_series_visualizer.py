import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_clean_data():
    # Import data
    df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

    # Clean data
    lower_limit = df['value'].quantile(0.025)
    upper_limit = df['value'].quantile(0.975)
    df = df[(df['value'] >= lower_limit) & (df['value'] <= upper_limit)]

    return df

def draw_line_plot(df):
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot(df):
    # Prepare data for bar plot
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    
    # Group data and calculate the average
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()

    # Draw bar plot
    fig = df_bar.plot(kind='bar', figsize=(15, 7)).figure
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months', labels=[
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ])
    plt.title('Monthly Average Page Views Per Year')

    # Save image
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot(df):
    # Prepare data for box plots
    df_box = df.copy()
    df_box['year'] = df_box.index.year
    df_box['month'] = df_box.index.month_name()
    df_box['month'] = pd.Categorical(df_box['month'], categories=[
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ], ordered=True)

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(15, 7), sharey=True)

    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Save image
    fig.savefig('box_plot.png')
    return fig

if __name__ == "__main__":
    df = load_and_clean_data()

    # Generate plots
    draw_line_plot(df)
    draw_bar_plot(df)
    draw_box_plot(df)
