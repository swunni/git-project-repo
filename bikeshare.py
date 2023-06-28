import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    cities = ['chicago', 'new york city', 'washington']
    while True:
        city = input("Would you like to see data for Chicago, New York City or Washington?").lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print("Please enter one of the provided cities.")
        else:
            break

    # get user input for month (all, january, february, ... , june)

    while True:
        month = input("Which Month you like to see?\nJanuary, February, March, April, May, June or all month?\n").lower()
        if month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
            print("Something went wrong. Please enter one of the given Month or all.")
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        day = input("Which day of the week?\nPlease typethe full name like Monady, etc. or all.").lower()
        if day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
            print("An unexpected mistake happe, please check that you write the day correct.")
        else:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time']= pd.to_datetime(df['Start Time'])
    df['year']= df['Start Time'].dt.year
    df['month']= df['Start Time'].dt.month
    df['day_of_week']= df['Start Time'].dt.day_name()
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    df['month'] = df['Start Time'].dt.month_name()
    common_month = df['month'].mode()[0]
    print('The most common month is: ', common_month)

    # display the most common day of week

    df['day'] = df['Start Time'].dt.day_name()
    common_day = df['day'].mode()[0]
    print('The most common day of the week is: ', common_day)

    # display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('The most common start hour is: ', common_hour, 'o\'clock')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is:', start_station)

    # display most commonly used end station

    end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is:', end_station)

    # display most frequent combination of start station and end station trip

    df['Combination Station'] = df['Start Station'] + " " + df['End Station']
    combination_stations = df['Combination Station'].mode()[0]
    print('The most frequent combination of start station and end station is: ', combination_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_time = df['Trip Duration'].sum()
    print('Total travel time: %s. '%str(datetime.timedelta(seconds = int(total_time))))

    # display mean travel time

    mean_time = df['Trip Duration'].mean()
    print('Mean travel time: %s. '%str(datetime.timedelta(seconds = mean_time)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_type_counts = df['User Type'].value_counts()
    print('Counts of user types:\n', user_type_counts)

    # Display counts of gender

    try:
        gender_count = df['Gender'].value_counts()
        print('Counts of gender:\n', gender_count)
    except KeyError:
        print('There is no data on the gender for the selected city.')

    # Display earliest, most recent, and most common year of birth

try:
        earliest_birth_year = df['Birth Year'].min()
        earliest_year = int(earliest_birth_year)
        print('Earliest year of birth: ', earliest_year)
        most_recent_year = df['Birth Year'].max()
        recent_year = int(most_recent_year)
        print('Most recent year of birth: ', recent_year)
        most_common_year = df['Birth Year'].mode()[0]
        common_year = int(most_common_year)
        print('Most common year of birth: ', common_year)
    except KeyError:
        print('There is no data on the year of birth for the selected city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(df):
    user_prompt = input('Would you like to see 5lines of raw data? Enter Yes or No:\n').lower()
    answer = ['yes']
    steps = 0
    while (user_prompt in answer):
        print(df.iloc[steps:steps+5])
        steps +=5
        user_prompt = input('Would you like to continue? Enter Yes or No:\n').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
