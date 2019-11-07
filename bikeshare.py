import time
import pandas as pd


CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}


def get_filters_from_user():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello there my beautiful friend! Let\'s explore some US bikeshare data!')

    # getting user input for city (chicago, new york city, washington)
    # and using while to check for validation
    while True:
        city = input("\nLet's begin with the city you want to explore about.\n"
                     "Which city you want to explore? "
                     "\nChose between chicago, new york city, washington.  \n").lower()
        if city not in CITY_DATA.keys():
            print("Check for your spelling or make sure to choose only from the given cities my friend! "
                  "Try again.")
            continue
        else:
            break

    # getting user input for month (all, january, february, ... , june)
    # and checking for validation
    while True:
        month = input("\nNow, do you want to explore data about particular month?\n"
                      "If so, choose between january, february, march, april, may, june.\n"
                      "If not, just type all  \n").lower()

        if month not in ('all', 'january', 'february', 'march', 'april', 'may', 'june'):
            print("Check for your spelling or make sure to choose only from the given months my friend! \n"
                  "Try again.")
            continue
        else:
            break

    # getting user input for day of week (all, monday, tuesday, ... sunday)
    # and checking for validation
    while True:
        day = input("\nYou are almost there dear :D \n"
                    "now, do you want to filter by a specific day? \n"
                    "If so, choose between monday, tuesday, ... sunday. \n"
                    "if not, just type all  \n")
        if day not in ("all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"):
            print("Check for your spelling , or make sure to write the day of week name \n"
                  "Try again")
            continue
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month_name(locale='English')
    df['day'] = df['Start Time'].dt.weekday_name

    # find the most common month, day, hour
    popular_month = df['month'].mode()[0]
    popular_day = df['day'].mode()[0]
    popular_hour = df['hour'].mode()[0]

    # Display the information about favorite times
    print("Most common month is : {}".format(popular_month))
    print()
    print("Most common day of week is : {}".format(popular_day))
    print()
    print("Most frequent start hour is : {}".format(popular_hour))
    print()
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # most common start station
    print("the most common start station is : {}".format(df["Start Station"].mode()[0]))
    print()

    # most common end station
    print("the most common end station is : {}".format(df["End Station"].mode()[0]))
    print()

    # most common trip
    df['full_destination'] = "starts from " + df["Start Station"] + " and ends in " + df["End Station"]
    print("The most common trip {}".format(df['full_destination'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    #  Display the  total travel time in hours and rounding it up to 2 decimal points
    print("The total travel time is : {} hours".format(round(sum(df["Trip Duration"]) / 3600, 2)))
    print()

    # Display the average travel time in minutes and rounding it up to 2 decimal points
    print("The average travel time is : {} minutes".format(round(df["Trip Duration"].mean() / 60), 2))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display the count of each user type
    count_user_types = df["User Type"].value_counts()
    print("The count of each user type is : \n{}".format(count_user_types))
    print()

    # display the count of each gender
    try:
        count_user_gender = df["Gender"].value_counts()
        print("The count of each gender is : \n{}".format(count_user_gender))
        print()
    except KeyError:
        print("The count of each gender is : sorry, No gender data available for this city")

    # display the most recent BY
    try:
        print("The most recent Birth Year is : {} ".format(int(df["Birth Year"].max())))
        print()
    except KeyError:
        print("The most recent Birth Year is : sorry, No birth year data available for this city")

    # display the earliest BY
    try:
        print("The earliest Birth Year is : {} ".format(int(df["Birth Year"].min())))
        print()
    except KeyError:
        print("The earliest Birth Year is : sorry, No birth year data available for this city")

    # display the most common BY
    try:
        print("The most common Birth Year is : {}".format(int(df["Birth Year"].mode()[0])))
    except KeyError:
        print("The most common Birth Year is : sorry, No birth year data available for this city")

    # display the count of user types along with the gender
    try:

        # replacing the NaN values in Gender column with "No specified gender for a"
        df["Gender"].fillna("No specified gender ", inplace=True)

        # create a new column with data indicates the user type with its gender
        df["User type gender"] = df["Gender"] + " " + df["User Type"]
        count_user_gender_type = df["User type gender"].value_counts()
        # display the stats
        print()
        print("Here is the stats about user types along with there gender : \n\n{}"
              .format(count_user_gender_type))
    except KeyError:
        print("the stats about user types along with there gender : sorry, No gender data available for this city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def longest_trip(df):
    """ display information about the longest trip used by a user """

    # finding the maximum trip duration and rounding it up
    max_duration_time = round((max(df["Trip Duration"]) / 3600), 1)

    # finding the index of the maximum trip duration
    max_duration_time_index = df["Trip Duration"].idxmax()

    # finding start station for the maximum trip duration
    start_point = df["Start Station"][max_duration_time_index]

    # finding end station for the maximum trip duration
    end_point = df["End Station"][max_duration_time_index]
    try:

        # replacing the NaN values in Gender column with "not specified gender"
        df["Gender"].fillna("not specified gender", inplace=True)

        # find the user type who made the longest trip
        df["User type gender"] = df["Gender"] + " " + df["User Type"]
        long_trip_user_type = df["User type gender"][max_duration_time_index]

        # display a information about the maximum trip duration
        print("The longest trip duration was nearly {} hours. \nIt was by a {} who took the bike from {}, \n"
              "and when the trip ended the bike was left at {} ."
              .format(max_duration_time, long_trip_user_type, start_point, end_point))

        if start_point == end_point:
            print("So the bike has returned to its original station again.")
    except KeyError:
        # display a information about the maximum trip duration
        print("The longest trip duration was nearly {} hours.started in {}, \n"
              "and when the trip ended the bike was left at {} ."
              .format(max_duration_time, start_point, end_point))

        if start_point == end_point:
            print("So the bike has returned to its original station again.")


def dispay_data (df):
    """
    this function displays five lines of data in a row if the user wanted,
    after displaying the data, ask the user if they want more, continue asking
    until they type no
    """
    lower_index = 0
    upper_index = 5
    while True:
        user_permission = input("\nDo you like to see 5 lines of raw data? type yes or no \n").lower()
        if user_permission not in ("yes", "no"):
            print("invalid input, please type yes of you want, no if you don't")
            continue

        elif user_permission == "yes":
            print(df[df.columns[0:-1]].iloc[lower_index:upper_index])
            lower_index += 5
            upper_index += 5
            print()
            while True:
                user_permission2 = input("\nDo you want to see more ? \n").lower()
                if user_permission2 not in ("yes", "no"):
                    print("invalid input, please type yes of you want, no if you don't")
                    continue
                elif user_permission2 != "no":
                    print(df[df.columns[0:-1]].iloc[lower_index:upper_index])
                    lower_index += 5
                    upper_index += 5
                    continue
                break
        break


def main():
    while True:
        city, month, day = get_filters_from_user()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        longest_trip(df)
        dispay_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        print()
        if restart.lower() != 'yes':
            print("It was a pleasure using me , bye bye <3")
            break


if __name__ == "__main__":

    main()
