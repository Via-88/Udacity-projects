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
    print("Which city's data would you like to know? Chicago, New York City or Washington?")
    city=input().lower()
    while city not in CITY_DATA:
        print('Please choose a city from Chicago, New York City or Washington!')
        city=input().lower()
    print("Great! Let's see some data from {}!".format(city.title()))
        
    # TO DO: get user input for month (all, january, february, ... , june)
    print("Would like to filter the data by month? 'All' means no month filter. Jan=1,Feb=2,Mar=3,Apr=4,May=5,June=6")
    month = input().lower()
 
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print("Would like to filter the data by day? You can choose Monday, Tuesday, Wednesday, Thursday, Friday, Saturday and Sunday. 'All' means no day filter.")
    day = input().lower()
    
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
    #filename='city.csv'
    city=city.lower()
 #   df=pd.read_csv('{}.csv'.format(city))
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        #months = ['january', 'february', 'march', 'april', 'may', 'june']
        #month = months.index(month) + 1
        month=int(month)

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    month_counts= df[df['month']== popular_month].shape[0]
    print('Most Frequent Month:', popular_month, " "*4,'Counts:', month_counts)



    # TO DO: display the most common day of week
    popular_day_of_week=df['day_of_week'].mode()[0]
    day_counts= df[df['day_of_week']== popular_day_of_week].shape[0]
    print('Most Frequent Day of Week:', popular_day_of_week, " "*4,'Counts:', day_counts)
    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]
    hour_counts= df[df['hour']== popular_hour].shape[0]
    print('Most Frequent Start Hour:', popular_hour, " "*4,'Counts:', hour_counts)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station=df['Start Station'].mode()[0]
    start_station_counts=df[df['Start Station']== most_common_start_station].shape[0]
    print('Most Common Start Station: {}\nCounts: {}'.format(most_common_start_station, start_station_counts))

    # TO DO: display most commonly used end station
    most_common_end_station=df['End Station'].mode()[0]
    end_station_counts=df[df['End Station']== most_common_end_station].shape[0]
    print('Most Common End Station: {}\nCounts: {}'.format(most_common_end_station, end_station_counts))

    # TO DO: display most frequent combination of start station and end station trip
    most_common_trip=df.groupby(['Start Station','End Station']).size().idxmax()
    count=df.groupby(['Start Station','End Station']).size()[most_common_trip]
    print('Most Common Trip:\n','Start Station: {}\n End   Station: {}\n'.format(*most_common_trip),'Count:',count)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    def second_to_hour(n):# a function converting seconds to hours
        h = n//3600
        m = (n%3600)//60
        s=n-3600*h-60*m
        return '{} hours {} mins {} seconds'.format(h,m,int(s))

    # TO DO: display total travel time
    total_trip_time = df['Trip Duration'].sum()
    print('The total trip time is {}.'.format(total_trip_time),'It is about {}'.format(second_to_hour(total_trip_time)))


    # TO DO: display mean travel time
    ave_travel_time = df['Trip Duration'].mean()
    print('The average travel time is {}.'.format(ave_travel_time),'It is about {}'.format(second_to_hour(ave_travel_time)))
    
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
        gender_counts = df['Gender'].value_counts()
        print(gender_counts)
    except:
        print("The breakdown of user gender is not available!")


    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_year_of_birth = df['Birth Year'].min()
        print('The earliest year of birth is ', earliest_year_of_birth)
        most_recent_year_of_birth = df['Birth Year'].max()
        print('The most recent year of birth is ', most_recent_year_of_birth)
        most_common_year_of_birth = df['Birth Year'].mode()[0]
        print('The most common year of birth is ', most_common_year_of_birth)
    except:
        print("The users's birth year is not available!")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        # To display the raw data upon request by user 
        print("\nWould you like to see some previous user data samples? Enter yes or no.\n")
        answer = input()
        n = 0
        while answer.lower() == 'yes':
            print('\nHow many samples would you like to see?\n')
            m = int(input()) + n
            print(df.iloc[n:m])
            print('\nWould like to see more? Enter yes or no.\n')
            answer = input()
            n = m
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()


