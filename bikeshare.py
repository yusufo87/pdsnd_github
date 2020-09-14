import time
import pandas as pd
import numpy as np

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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
        city = input("\n Write name of the city you want to check (Chicago, New York City or Washington?)\n").lower()
        if city not in ( 'chicago', 'new york city', 'washington'):
            print("Sorry, try again")
        else:   
            break
        

    # TO DO: get user input for month (all, january, february, ... , june)
    
    while True:
        month = input("\n Write name of the month you want to check (January, February, March, April, May, June or type all not to filter by month \n").lower()
        if month not in ( 'all', 'january', 'february', 'march', 'april', 'may', 'june'):
            print("Sorry, try again")
        else:
            break


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    
    while True:
        day = input("\n Write name of the day you want to check (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday) or type all not to filter by day \n").lower()
        if day not in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
            print("Sorry, try again")
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
    #load data file
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime and extract month ,day of week and hour from Start Time to create new columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    
    # filter by month
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

     # filter by day of week
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]    
        
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = df['month'].mode()[0]
    print('Most Common Month:', most_common_month )

    # TO DO: display the most common day of week
    mont_common_day_of_week = df['day_of_week'].mode()[0]
    print('Most Common Day of Week:', mont_common_day_of_week )

    # TO DO: display the most common start hour
    most_common_hour = df['hour'].mode()[0]
    print('Most Common start Hour:', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_commonly_used_start_station= df ['Start Station'].value_counts().idxmax()
    print('Most Commonly used start station:', most_commonly_used_start_station)

    # TO DO: display most commonly used end station
    most_commonly_used_end_station= df ['End Station'].value_counts().idxmax()
    print('Most Commonly used end station:', most_commonly_used_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df2 = df.groupby ( ['Start Station', 'End Station']).size().reset_index(name='counts')
    df2 = df2[df2['counts']==df2['counts'].max()] 
    print('most_frequent_combination_of_start_and_end_station_trip : \n', df2)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('total travel time :', total_travel_time, 'minutes' )

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('mean travel time :', mean_travel_time, 'minutes' )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
   
    # TO DO: Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print(gender)
    except KeyError:
        print('gender : no data for this option' )
    # TO DO: Display earliest, most recent, and most common year of birth
    
    # display earliest birth
    try:
        earliest_birth = df['Birth Year'].min()
        print('earliest_birth : ', earliest_birth)
    except KeyError:
        print('earliest_birth : no data for this option' )
        
    # display most recent birth    
    try:
        most_recent_birth = df['Birth Year'].max()
        print('most_recent_birth : ', most_recent_birth)
    except KeyError:
        print('most_recent_birth : no data for this option' )
        
    # display most common birth    
    try:
        most_common_birth = df['Birth Year'].mode()[0]
        print('most_common_birth : ', most_common_birth)
    except KeyError:
        print('most_common_birth : no data for this option' )
        
        
     # TO DO:  calculate average travel time of people with in same birth year
    def average_travel_time(birth_year): 
        average_travel_time = df.loc[(df ['Birth Year'] == birth_year) ]['Trip Duration'].mean()
        return (average_travel_time)
    
     # compare average travel time of oldest and youngest people 
    try:    
        earliest_birth_average_travel_time = average_travel_time(earliest_birth)
        most_recent_birth_average_travel_time = average_travel_time(most_recent_birth)
        print("average travel time of people with in earliest birth: {} minutes, \naverage travel time of people with in most recent birth:  {} minutes\n".format(earliest_birth_average_travel_time, most_recent_birth_average_travel_time))
    except UnboundLocalError:
        print('avarage travel time of oldest and youngest people : no data for this option')    
       
     
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
   
  
def display_data(df):
    index=0
    user_input=input('would you like to display 5 rows of raw data? ').lower()
    while user_input in ['yes','y','yep','yea'] and index+5 < df.shape[0]:
        print(df.iloc[index:index+5])
        index += 5
        user_input = input('would you like to display more 5 rows of raw data? ').lower()
        

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
