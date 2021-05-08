import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use("ggplot")
import sklearn
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures

import pymysql.cursors



df1 = pd.read_csv("https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv")
df2 = pd.read_csv("https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_recovered_global.csv&filename=time_series_covid19_recovered_global.csv")
df3 = pd.read_csv("https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_deaths_global.csv&filename=time_series_covid19_deaths_global.csv")
# Where df1 = cases file, df2 = recoveries file and df3 = deaths file 



def my_model_current_values():
    
    name_input = str(input("Enter the Country's name: ")).title()

    if name_input == "Us" or name_input == "Usa" or name_input == "United States Of America":
        name_input = "US"

    elif name_input == "North Korea":
        print("North Korea has no covid-19 data")
        print("\n")
        my_model_menu()

    elif name_input == "South Korea":
        name_input = "Korea, South"


    # To group the cases dataset by countries and fetch the country pertaining to the user's input
    grouped_cases = df1.groupby("Country/Region")
    fetched_cases = grouped_cases.get_group(name_input)
    new1 = pd.DataFrame(fetched_cases)
    new_cases = pd.DataFrame(new1.iloc[:, 4:])
    #To sum up the daily values. This caters fot situations where the country has multiple provinces
    new_cases_df = new_cases.sum(axis = "rows")


    # To group the recoveries dataset by countries and fetch the country pertaining to the user's input
    grouped_recoveries = df2.groupby("Country/Region")
    fetched_recoveries = grouped_recoveries.get_group(name_input)
    new2 = pd.DataFrame(fetched_recoveries)
    new_recoveries = pd.DataFrame(new2.iloc[:, 4:])
    #To sum up the daily values. This caters fot situations where the country has multiple provinces
    new_recoveries_df = new_recoveries.sum(axis = "rows")


    # To group the deaths dataset by countries and fetch the country pertaining to the user's input
    grouped_deaths = df3.groupby("Country/Region")
    fetched_deaths = grouped_deaths.get_group(name_input)
    new3 = pd.DataFrame(fetched_deaths)
    new_deaths = pd.DataFrame(new3.iloc[:, 4:])
     #To sum up the daily values. This caters fot situations where the country has multiple provinces
    new_deaths_df = new_deaths.sum(axis = "rows")


    # To access the last entry since the last entry is the sum(which is the current value)
    fetched_cases_total = new_cases_df.iloc[-1]
    fetched_recoveries_total = new_recoveries_df.iloc[-1]
    fetched_deaths_total = new_deaths_df.iloc[-1]


    # To print out the results
    print("The current number of cases in {} is {}".format(name_input, fetched_cases_total))
    print("The current number of recoveries in {} is {}".format(name_input, fetched_recoveries_total))
    print("The current number of deaths in {} is {}".format(name_input, fetched_deaths_total))



def my_model_line_chart():
    name_input = str(input("Enter name of Country: ")).title()


    # This is to convert the dates to a more common format
    the_dates = df1.columns[4:]
    standard_dates = []
    for _ in the_dates:

        "1/22/20" 
        month, day, year = _.split("/") 

        fixed_date = "/".join([day, month, year.replace('\n','')+'20'])
        "2020-1-22"
        standard_dates.append(fixed_date)

    
    if name_input == "Us" or name_input == "Usa" or name_input == "United States Of America":
        name_input = "US"
    

    elif name_input == "North Korea":
        print("North Korea has no covid-19 data")
        print("\n")
        my_model_menu()

    elif name_input == "South Korea":
        name_input = "Korea, South"

    grouped_cases = df1.groupby("Country/Region")
    fetched_cases = grouped_cases.get_group(name_input)
    new1 = pd.DataFrame(fetched_cases)
    new_cases = pd.DataFrame(new1.iloc[:, 4:])
    new_cases_df = new_cases.sum(axis = "rows")

    grouped_recoveries = df2.groupby("Country/Region")
    fetched_recoveries = grouped_recoveries.get_group(name_input)
    new2 = pd.DataFrame(fetched_recoveries)
    new_recoveries = pd.DataFrame(new2.iloc[:, 4:])
    new_recoveries_df = new_recoveries.sum(axis = "rows")

    grouped_deaths = df3.groupby("Country/Region")
    fetched_deaths = grouped_deaths.get_group(name_input)
    new3 = pd.DataFrame(fetched_deaths)
    new_deaths = pd.DataFrame(new3.iloc[:, 4:])
    new_deaths_df = new_deaths.sum(axis = "rows")

    # To set the intervals in which the data would be picked to show the trend
    dates_interval = "{0:.0f}".format(0.1 * len(standard_dates))

    k = int(dates_interval)
    
    
    dates_display = standard_dates[40::k]
    fetched_cases_display = new_cases_df[40::k]
    fetched_recoveries_display = new_recoveries_df[40::k]
    fetched_deaths_display = new_deaths_df[40::k]


    # This for the line plotting
    plt.rcParams["figure.figsize"] = [15,8]
    plt.plot(dates_display, fetched_cases_display, color = "yellow", label= "cases", alpha = 0.8, linewidth = 5)
    plt.plot(dates_display, fetched_recoveries_display, color = "green", label= "recoveries", alpha = 0.8, linewidth = 5)
    plt.plot(dates_display, fetched_deaths_display, color = "red", label= "deaths", alpha = 0.8, linewidth = 5)
    

    plt.xlabel("Dates(dd/mm/yy)")
    plt.ylabel("Figures")
    plt.title("Line chart for {}".format(name_input))
    plt.legend(loc = "best", shadow = True, fontsize = "large")

    
    plt.show()



def my_model_bar_chart():
    name_input = str(input("Enter name of Country (If there are two, use TRIPPLE BLANK SPACES as the separator): ")).title().split("   ")
    for d, e in enumerate(name_input):
        if e == "Us" or e == "Usa" or e == "United States Of America":
            name_input[d] = "US"
        
        elif e == "North Korea":
            print("North Korea has no covid-19 data")
            print("\n")
            my_model_bar_chart()

        elif e == "South Korea":
            name_input[d] = "Korea, South"



    yo = list(name_input[0])
    yoo = "".join(yo)
    yeah = []
    yeah.append(yoo)   #This returns exactly the input name if just one name is inputed by the user
    
    
    # A list of Countries having different Provinces
    

    if name_input == yeah:
        # To group the datasetes by the column we would use to search for the country with respect to the user's input 
        grouped_cases = df1.groupby("Country/Region")
        grouped_recoveries = df2.groupby("Country/Region")
        grouped_deaths = df3.groupby("Country/Region")        

        # To fetch the data from all three datasetes pertaining to the user's input country
        fetched_cases = grouped_cases.get_group(name_input[0])
        fetched_recoveries = grouped_recoveries.get_group(name_input[0])
        fetched_deaths = grouped_deaths.get_group(name_input[0])

        # Creating 3 new DataFrames with entries of only the desired  country
        new1 = pd.DataFrame(fetched_cases)
        new2 = pd.DataFrame(fetched_recoveries)
        new3 = pd.DataFrame(fetched_deaths)

        # To fetch all the data from the cases DataFrame. This comes in handy in situations where the country has multiple provinces
        new_cases_df = pd.DataFrame(new1.iloc[:, 4:])
        daily_cases_sum = new_cases_df.sum(axis = "rows")
        new_cases_display = daily_cases_sum[-1]

         # To fetch all the data from the recoveries DataFrame. This comes in handy in situations where the country has multiple provinces
        new_recoveries_df = pd.DataFrame(new2.iloc[:, 4:])
        daily_recoveries_sum = new_recoveries_df.sum(axis = "rows")
        new_recoveries_display = daily_recoveries_sum[-1]

         # To fetch all the data from the deaths DataFrame. This comes in handy in situations where the country has multiple provinces
        new_deaths_df = pd.DataFrame(new3.iloc[:, 4:])
        daily_deaths_sum = new_deaths_df.sum(axis = "rows")
        new_deaths_display = daily_deaths_sum[-1]


        # Defining the x and y axes
        fetched_total = [new_cases_display, new_deaths_display, new_recoveries_display]
        fetched_total_xaxis = ["Cases", "Deaths", "Recoveries"]

        # Plotting the bar chart
        plt.bar(fetched_total_xaxis, fetched_total, color = ["Yellow", "Red", "Green"], width = 0.3)
        plt.title("Bar Chart for {}".format(name_input[0]))
        plt.show()


    elif name_input[0] in name_input and name_input[1] in name_input:   # This caters for when the user inputs two countries
        # To group the datasetes by the column we would use to search for the country with respect to the user's first input  
        grouped_cases1 = df1.groupby("Country/Region")
        grouped_recoveries1 = df2.groupby("Country/Region")
        grouped_deaths1 = df3.groupby("Country/Region")        

        # To fetch the data from all three datasets pertaining to the user's first input country
        fetched_cases1 = grouped_cases1.get_group(name_input[0])
        fetched_recoveries1 = grouped_recoveries1.get_group(name_input[0])
        fetched_deaths1 = grouped_deaths1.get_group(name_input[0])

        # Creating 3 new DataFrames with entries of only the first country
        new1 = pd.DataFrame(fetched_cases1)
        new2 = pd.DataFrame(fetched_recoveries1)
        new3 = pd.DataFrame(fetched_deaths1)

        # To fetch all the data from the cases DataFrame. This comes in handy in situations where the country has multiple provinces
        new_cases_df1 = pd.DataFrame(new1.iloc[:, 4:])
        daily_cases_sum1 = new_cases_df1.sum(axis = "rows")
        new_cases_display1 = daily_cases_sum1[-1]

         # To fetch all the data from the recoveries DataFrame. This comes in handy in situations where the country has multiple provinces
        new_recoveries_df1 = pd.DataFrame(new2.iloc[:, 4:])
        daily_recoveries_sum1 = new_recoveries_df1.sum(axis = "rows")
        new_recoveries_display1 = daily_recoveries_sum1[-1]

         # To fetch all the data from the deaths DataFrame. This comes in handy in situations where the country has multiple provinces
        new_deaths_df1 = pd.DataFrame(new3.iloc[:, 4:])
        daily_deaths_sum1 = new_deaths_df1.sum(axis = "rows")
        new_deaths_display1 = daily_deaths_sum1[-1]



         # To group the datasetes by the column we would use to search for the country for the user's input 
        grouped_cases2 = df1.groupby("Country/Region")
        grouped_recoveries2 = df2.groupby("Country/Region")
        grouped_deaths2 = df3.groupby("Country/Region")        

        # To fetch the data from all three datasetes pertaining to the second country
        fetched_cases2 = grouped_cases2.get_group(name_input[1])
        fetched_recoveries2 = grouped_recoveries2.get_group(name_input[1])
        fetched_deaths2 = grouped_deaths2.get_group(name_input[1])

        # Creating 3 new DataFrames with entries of only the second country
        new11 = pd.DataFrame(fetched_cases2)
        new22 = pd.DataFrame(fetched_recoveries2)
        new33 = pd.DataFrame(fetched_deaths2)

        # To fetch all the data from the cases DataFrame. This comes in handy in situations where the country has multiple provinces
        new_cases_df2 = pd.DataFrame(new11.iloc[:, 4:])
        daily_cases_sum2 = new_cases_df2.sum(axis = "rows")
        new_cases_display2 = daily_cases_sum2[-1]


        # To fetch all the data from the recoveries DataFrame. This comes in handy in situations where the country has multiple provinces
        new_recoveries_df2 = pd.DataFrame(new22.iloc[:, 4:])
        daily_recoveries_sum2 = new_recoveries_df2.sum(axis = "rows")
        new_recoveries_display2 = daily_recoveries_sum2[-1]

        # To fetch all the data from the deaths DataFrame. This comes in handy in situations where the country has multiple provinces
        new_deaths_df2 = pd.DataFrame(new33.iloc[:, 4:])
        daily_deaths_sum2 = new_deaths_df2.sum(axis = "rows")
        new_deaths_display2 = daily_deaths_sum2[-1]

        # To get the list of the total number of cases, recoveries and deaths 
        fetched_total1 = [new_cases_display1, new_deaths_display1, new_recoveries_display1]
        fetched_total2 = [new_cases_display2, new_deaths_display2, new_recoveries_display2]


        # To plot the results
        N = 3
        ind = np.arange(N)
        width = 0.3
        dual_xaxis = ["Cases", "Deaths", "Recoveries"]
        plt.bar(ind - 0.35, fetched_total1, color = ["cyan"], width = 0.3, label = "{}".format(name_input[0]))
        plt.bar(ind - 0.05, fetched_total2, color = ["red"], width = 0.3, label = "{}".format(name_input[1]))
        

        plt.xticks(ind - 0.2, dual_xaxis, fontsize = "large")
        plt.legend(loc = "best", shadow = True, fontsize = "large")
        plt.title("Bar Chart for {} and {}".format(name_input[0], name_input[1]))
        plt.show()



def my_model_predictions():

    # To get the user's input
    name_input = str(input("Enter name of Country: ")).title()
    date_input = str(input("Enter desired date(s) in the format(yy-mm-dd). If multiple, use a SINGLE BLANK SPACE as the separator: ")).split(" ")
    print("\n")

    if name_input == "Us" or name_input == "Usa" or name_input == "United States Of America":
        name_input = "US"

    elif name_input == "North Korea":
        print("North Korea has no covid-19 data")
        print("\n")
        my_model_menu()
        
       

    elif name_input == "South Korea":
        name_input = "Korea, South"

    # Grouping and summing the daily cases data of the country requested by the user
    grouped_cases = df1.groupby("Country/Region")
    fetched_cases = grouped_cases.get_group(name_input)
    new1 = pd.DataFrame(fetched_cases)
    new_cases = pd.DataFrame(new1.iloc[:, 4:])
    new_cases_df = new_cases.sum(axis = "rows")

    # Creating another dataframe for cases only so I can feed data entries to  a final dataframe which would be created soon
    sub_final_cases_df = pd.DataFrame(new_cases_df)
    cases_entries = []
    for a in new_cases_df:
        cases_entries.append(a)

    # The final dataframe for cases ready to be passed into the model
    final_cases_df = pd.DataFrame([cases_entries], columns = [a for a in sub_final_cases_df.index])


    # Grouping and summing the daily recoveries data of the country requested by the user
    grouped_recoveries = df2.groupby("Country/Region")
    fetched_recoveries = grouped_recoveries.get_group(name_input)
    new2 = pd.DataFrame(fetched_recoveries)
    new_recoveries = pd.DataFrame(new2.iloc[:, 4:])
    new_recoveries_df = new_recoveries.sum(axis = "rows")

    # Creating another dataframe for recoveries only so I can feed data entries to  a final dataframe which would be created soon
    sub_final_recoveries_df = pd.DataFrame(new_recoveries_df)
    recoveries_entries = []
    for a in new_recoveries_df:
        recoveries_entries.append(a)

    # The final dataframe for recoveries ready to be passed into the model
    final_recoveries_df = pd.DataFrame([recoveries_entries], columns = [a for a in sub_final_recoveries_df.index])


    # Grouping and summing the daily deaths data of the country requested by the user
    grouped_deaths = df3.groupby("Country/Region")
    fetched_deaths = grouped_deaths.get_group(name_input)
    new3 = pd.DataFrame(fetched_deaths)
    new_deaths = pd.DataFrame(new3.iloc[:, 4:])
    new_deaths_df = new_deaths.sum(axis = "rows")

    # Creating another dataframe for deaths only so I can feed data entries to  a final dataframe which would be created soon
    sub_final_deaths_df = pd.DataFrame(new_deaths_df)
    deaths_entries = []
    for a in new_deaths_df:
        deaths_entries.append(a)

    # The final dataframe for deaths ready to be passed into the model
    final_deaths_df = pd.DataFrame([deaths_entries], columns = [a for a in sub_final_deaths_df.index])


    # I created this while to cater for cases only. Here, the data is passed into the model and the result is displayed
    # This while loop runs only once
    timer1 = 1
    while (timer1 <= 1):
        # Determining the index_iterator(i.e the point in which the model starts training on the data) in accordance with the country's current value
        fetched_cases_total = new_cases_df.iloc[-1]

        number_to_start_iteration1 = "{0:.0f}".format(0.7 * fetched_cases_total)

        index_iterator = 0
        zip_column_row = zip(final_cases_df.columns, final_cases_df.iloc[index_iterator, :])
        for c,d in enumerate(zip_column_row):
            if d[1] >= int(number_to_start_iteration1):
                index_iterator = c
                break

        # The process to define the predictor and target variables for each country's model
        y_axis = final_cases_df.iloc[0, index_iterator:]
        sub_x_axis = final_cases_df.columns.values.tolist()
        x_axis = sub_x_axis[index_iterator:]

        # This is to convert the predictor variables to the standard pandas datetime
        predictor_variables_to_series = pd.Series(x_axis)
        predictor_variables_to_datetime = pd.to_datetime(predictor_variables_to_series)

        # Finally defining the predictor and target variables
        X = predictor_variables_to_datetime
        Y = y_axis

        
        # Since the relationship is polynomial, we would convert the predictor variables to fit polynomial features
        poly = PolynomialFeatures(degree = 16)
        X_ = poly.fit_transform(X[:, np.newaxis])

        # Now, we split the predictor and target variables into training and testing data
        X_train1, x_test1, Y_train1, y_test1 = train_test_split(X_, Y, train_size = 0.9, random_state = 1)

        # We train the model by fitting the training data into the model
        lm = linear_model.LinearRegression()
        lm.fit(X_train1, Y_train1)

        # We would have to convert the date_input to the standard pandas datetime
        date_to_series = pd.Series(date_input)
        date_to_datetime = pd.to_datetime(date_to_series, errors = "coerce")

        # Now, we transorm it to fit the polynomial features requirement
        date_transformed = poly.fit_transform(date_to_datetime[:, np.newaxis])

        # The input_date can now be passed as a predictor
        predictions = lm.predict(date_transformed)
        
        #   The accuracy if the model is given as
        r_squared1 = lm.score(X_train1, Y_train1)
        r_squared1_display = "{0:.2f}%".format(r_squared1 * 100)

        predictions1 = [round(float(a)) for a in predictions]

        timer1 += 1



    # I created this while to cater for recoveries only. Here, the data is passed into the model and the result is displayed
    # This while loop runs only once
    timer2 = 1
    while (timer2 <= 1):
        fetched_recoveries_total = new_recoveries_df.iloc[-1]
        
        number_to_start_iteration2 = "{0:.0f}".format(0.7 * fetched_recoveries_total)

        index_iterator = 0
        zip_column_row = zip(final_recoveries_df.columns, final_recoveries_df.iloc[index_iterator, :])
        for c,d in enumerate(zip_column_row):
            if d[1] >= int(number_to_start_iteration2):
                index_iterator = c
                break



        # The process to define the predictor and target variables for each country's model
        y_axis = final_recoveries_df.iloc[0, index_iterator:]
        sub_x_axis = final_recoveries_df.columns.values.tolist()
        x_axis = sub_x_axis[index_iterator:]

        # This is to convert the predictor variables to the standard pandas datetime
        predictor_variables_to_series = pd.Series(x_axis)
        predictor_variables_to_datetime = pd.to_datetime(predictor_variables_to_series)

        # Finally defining the predictor and target variables
        X = predictor_variables_to_datetime
        Y = y_axis

        # Since the relationship is polynomial, we would convert the predictor variables to fit polynomial features
        poly = PolynomialFeatures(degree = 16)
        X_ = poly.fit_transform(X[:, np.newaxis])

        # Now, we split the predictor and target variables into training and testing data
        X_train2, x_test2, Y_train2, y_test2 = train_test_split(X_, Y, train_size = 0.9, random_state = 1)

        # We train the model by fitting the training data into the model
        lm = linear_model.LinearRegression()
        lm.fit(X_train2, Y_train2)

        # We would have to convert the date_input to the standard pandas datetime
        date_to_series = pd.Series(date_input)
        date_to_datetime = pd.to_datetime(date_to_series, errors = "coerce")

        # Now, we transorm it to fit the polynomial features requirement
        date_transformed = poly.fit_transform(date_to_datetime[:, np.newaxis])

        # The input_date can now be passed as a predictor
        predictions = lm.predict(date_transformed)
        
        #   The accuracy if the model is given as
        r_squared2 = lm.score(X_train2, Y_train2)
        r_squared2_display = "{0:.2f}%".format(r_squared2 * 100)

        predictions2 = [round(float(a)) for a in predictions]

        timer2 += 1


    # I created this while loop to cater for deaths only. Here, the data is passed into the model and the result is displayed.
    #This while loop runs only once
    timer3 = 1
    while (timer3 <= 1):

        fetched_deaths_total = new_deaths_df.iloc[-1]
        
        number_to_start_iteration3 = "{0:.0f}".format(0.7 * fetched_deaths_total)

        index_iterator = 0
        zip_column_row = zip(final_deaths_df.columns, final_deaths_df.iloc[index_iterator, :])
        for c,d in enumerate(zip_column_row):
            if d[1] >= int(number_to_start_iteration3):
                index_iterator = c
                break



        # The process to define the predictor and target variables for each country's model
        y_axis = final_deaths_df.iloc[0, index_iterator:]
        sub_x_axis = final_deaths_df.columns.values.tolist()
        x_axis = sub_x_axis[index_iterator:]

        # This is to convert the predictor variables to the standard pandas datetime
        predictor_variables_to_series = pd.Series(x_axis)
        predictor_variables_to_datetime = pd.to_datetime(predictor_variables_to_series)

        # Finally defining the predictor and target variables
        X = predictor_variables_to_datetime
        Y = y_axis

        # Since the relationship is polynomial, we would convert the predictor variables to fit polynomial features
        poly = PolynomialFeatures(degree = 16)
        X_ = poly.fit_transform(X[:, np.newaxis])

        # Now, we split the predictor and target variables into training and testing data
        X_train3, x_test3, Y_train3, y_test3 = train_test_split(X_, Y, train_size = 0.9, random_state = 1)

        # We train the model by fitting the training data into the model
        lm = linear_model.LinearRegression()
        lm.fit(X_train3, Y_train3)

        # We would have to convert the date_input to the standard pandas datetime
        date_to_series = pd.Series(date_input)
        date_to_datetime = pd.to_datetime(date_to_series, errors = "coerce")

        # Now, we transorm it to fit the polynomial features requirement
        date_transformed = poly.fit_transform(date_to_datetime[:, np.newaxis])

        # The input_date can now be passed as a predictor
        predictions = lm.predict(date_transformed)
        
        #   The accuracy if the model is given as
        r_squared3 = lm.score(X_train3, Y_train3)
        r_squared3_display = "{0:.2f}%".format(r_squared3 * 100)

        predictions3 = [round(float(a)) for a in predictions]

        timer3 += 1

    # To display the result in a tabualar form for a better view
    df_predictions = pd.DataFrame({
        "Predicted number of Cases" : predictions1,
        "Predicted number of Recoveries" : predictions2,
        "Predicted number of Deaths" : predictions3}, index = date_input)

    # Setting the name of the index
    df_predictions.index.name = "Date(s) in (yy-mm-dd)"
    print(df_predictions)
    print("\n")
    
    # To display the accuracy of the model
    print("P.S.: The prediction for cases in {} has an accuracy of {} \n      The prediction for recoveries in {} has an accuracy of {} \n      The prediction for deaths in {} has an accuracy of {}".format(name_input, r_squared1_display, name_input, r_squared2_display, name_input, r_squared3_display))

    


def my_model_database():
    warning = str(input("This process takes a lot of time. Do you want to proceed? (Yes or No): ")).title()
    print("\n")

    if warning == "Yes":
        get_database = input("Enter name of database in your xampp admin: ")
        
        # THESE ARE THE FUNCTIONS
        #  Connect to the database
        connection = pymysql.connect(host='localhost',
                                    user='root',
                                    password='',
                                    db='{}'.format(get_database),
                                    charset='utf8mb4',
                                    cursorclass=pymysql.cursors.DictCursor)


        def create_tables():
            with connection.cursor() as Cursor:
                
                create_countries_table = "create table IF NOT EXISTS countries (id int(10) AUTO_INCREMENT PRIMARY KEY NOT NULL, name VARCHAR(100), lng float, lat float)"

                Cursor.execute(create_countries_table)

                create_cases_table = "CREATE table IF NOT EXISTS country_data (id int(10) AUTO_INCREMENT PRIMARY KEY NOT NULL , country_id INT(10), FOREIGN KEY (country_id) REFERENCES countries(id), number_of_cases INT(100), number_of_deaths INT(100), number_of_recoveries INT(100), `date` DATE)"

                Cursor.execute(create_cases_table)
                
                connection.commit()


        def write_country(name, lat, lng):

            with connection.cursor() as Cursor:
                

                add_country = r"INSERT INTO countries (name, lat, lng) values ('{}','{}','{}')".format(name, lat, lng)
                
                Cursor.execute(add_country)
                
                connection.commit()

        def write_country_data (country_id, number_of_cases, number_of_deaths, number_of_recoveries, date):

            with connection.cursor() as Cursor:
                
                
                add_case = f"INSERT INTO country_data (country_id, number_of_cases, number_of_deaths, number_of_recoveries, date) values('{country_id}','{number_of_cases}','{number_of_deaths}', '{number_of_recoveries}', '{date}')"

                Cursor.execute(add_case)
                
                connection.commit()

        def check_country(name):
            with connection.cursor() as Cursor:
                
                get_country = f"SELECT * FROM countries where name = '{name}'"

                Cursor.execute(get_country)
                
                return Cursor.fetchall()   

        
        def format_time(date):
            
            "1/22/20" # before split
            month, day, year = date.split("/") #["1","22", "20"] #after split
        
            fixed_date = "-".join([year.replace('\n','')+'20', month, day]) #20+20 ==== 2020
            "2020-1-22"
            return fixed_date


        create_tables()

    # To write the data into the database

        countries_of_choice = []
        for a in df1["Country/Region"]:
            if a in countries_of_choice:
                pass
            else:
                countries_of_choice.append(a)



        for country in countries_of_choice:

            df1_database = pd.read_csv("https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_confirmed_global.csv&filename=time_series_covid19_confirmed_global.csv")
            df2_database = pd.read_csv("https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_recovered_global.csv&filename=time_series_covid19_recovered_global.csv")
            df3_database = pd.read_csv("https://data.humdata.org/hxlproxy/api/data-preview.csv?url=https%3A%2F%2Fraw.githubusercontent.com%2FCSSEGISandData%2FCOVID-19%2Fmaster%2Fcsse_covid_19_data%2Fcsse_covid_19_time_series%2Ftime_series_covid19_deaths_global.csv&filename=time_series_covid19_deaths_global.csv")
            
            
            
            pre_heading = df1_database.iloc[0, 4:]
            heading = pre_heading.index



            # To group the cases dataset by countries and fetch the country pertaining to the user's input
            grouped_cases = df1_database.groupby("Country/Region")
            fetched_cases = grouped_cases.get_group(country)
            new1 = pd.DataFrame(fetched_cases)
            new_cases = pd.DataFrame(new1.iloc[:, 4:])
            #To sum up the daily values. This caters fot situations where the country has multiple provinces
            new_cases_df = new_cases.sum(axis = "rows")
            number_of_cases = new_cases_df.iloc[4:]


            # To group the recoveries dataset by countries and fetch the country pertaining to the user's input
            grouped_recoveries = df2_database.groupby("Country/Region")
            fetched_recoveries = grouped_recoveries.get_group(country)
            new2 = pd.DataFrame(fetched_recoveries)
            new_recoveries = pd.DataFrame(new2.iloc[:, 4:])
            #To sum up the daily values. This caters fot situations where the country has multiple provinces
            new_recoveries_df = new_recoveries.sum(axis = "rows")
            number_of_recoveries = new_recoveries_df.iloc[4:]


            # To group the deaths dataset by countries and fetch the country pertaining to the user's input
            grouped_deaths = df3_database.groupby("Country/Region")
            fetched_deaths = grouped_deaths.get_group(country)
            new3 = pd.DataFrame(fetched_deaths)
            new_deaths = pd.DataFrame(new3.iloc[:, 4:])
            #To sum up the daily values. This caters fot situations where the country has multiple provinces
            new_deaths_df = new_deaths.sum(axis = "rows")
            number_of_deaths = new_deaths_df.iloc[4:]


            country_name = country
            lat = new1.iloc[0, 2]
            lng = new1.iloc[0, 3]

            if country_name == "Cote d'Ivoire":
                country_name = "Cote d\'Ivoire"


            if country_name == country:
                country_exists = check_country(country_name)
                if country_exists:
                    for data in list(zip(number_of_cases, number_of_deaths, number_of_recoveries, heading)):
                        write_country_data(country_exists[0]['id'], data[0], data[1], data[2], format_time(data[3]))

                else:
                    write_country(country_name, lat, lng)


        
    elif warning == "No":
        my_model_menu()



def if1():
    my_model_current_values()
    print("\n")
    sub_question = str(input("Do you want to access the current data values for another Country? (Yes or No): ")).title()
    if sub_question == "Yes":
        if1()
    elif sub_question == "No":
        print("\n")
        my_model_menu()


def if2():
    my_model_line_chart()
    print("\n")
    sub_question = str(input("Do you want to access the line chart for another Country? (Yes or No): ")).title()
    if sub_question == "Yes":
        if2()
    elif sub_question == "No":
        print("\n")
        my_model_menu()


def if3():
    my_model_bar_chart()
    print("\n")
    sub_question = str(input("Do you want to access the bar chart for another Country? (Yes or No): ")).title()
    if sub_question == "Yes":
        if3()
    elif sub_question == "No":
        print("\n")
        my_model_menu()


def if4():
    my_model_predictions()
    print("\n")
    sub_question = str(input("Do you want to access the predictions for another Country? (Yes or No): ")).title()
    if sub_question == "Yes":
        if4()
    elif sub_question == "No":
        print("\n")
        my_model_menu()


def if5():
    my_model_database()
    print("\n")

    try:
        if warning == "Yes":
            sub_question = str(input("Do you want to write covid19 data to another database? (Yes or No): ")).title()
            if sub_question == "Yes":
                if5()
            elif sub_question == "No":
                print("\n")
                my_model_menu()
        elif warning == "No":
            my_model_menu()

    except NameError: 
        warning = None



def if6():
    print("Thank you for choosing Dami's covid-19 app.\nGoodbye {} and stay safe!".format(get_name))
        
    


def my_model_menu():
    print("DAMI'S COVID19 APP MAIN MENU!!!")
    print("Enter 1 to access CURRENT DATA FIGURES")
    print("Enter 2 to access LINE CHARTS")
    print("Enter 3 to access BAR CHARTS")
    print("Enter 4 to access PREDICTIONS")
    print("Enter 5 to write the covid19 data to a database")
    print("Enter 6 to end session")
    print("\n")


    second_question = int(input("Enter number here: "))
    
    if second_question == 1:
        if1()
    elif second_question == 2:
        if2()
    elif second_question == 3:
        if3()
    elif second_question == 4:
        if4()
    elif second_question == 5:
        if5()
    elif second_question == 6:
        if6()


print("Dami's covid-19 app!")
get_name = input("Please enter your name: ").title()
print("Welcome, {}".format(get_name))
print("\n")
my_model_menu()


    






    

