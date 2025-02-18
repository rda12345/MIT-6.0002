# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re
import math
import numpy

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    # For every degree in degs generate a model
    models = []
    for deg in degs:
        models.append(pylab.polyfit(x,y,deg))
    return models


    
def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    mean_y = sum(y)/len(y)
    r_squared = 1 - sum((y-estimated)**2)/sum((y-mean_y)**2)
    return r_squared

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    fits = []
    r_squared_list = []
    for model in models:
        degree = len(model)-1
        estimated = pylab.zeros(len(x))
        for coeff in model:
            estimated += coeff*x**degree
            degree -= 1
        r_squared_list.append(r_squared(y, estimated))
        fits.append(estimated)
        
        if len(model) == 2:
            SE_over_sl = se_over_slope(x,y,estimated,model)
        
    for i in range(len(models)):
        pylab.figure(i+1)
        pylab.plot(x,y,'bo')
        pylab.plot(x,fits[i],'r')
        degree = len(models[i])-1
        if degree == 1:
            pylab.title('Model of degree: '+str(degree)+' , R^2  ='+ str(r_squared_list[i])\
                        +'\n'+'SE = '+ str(SE_over_sl))
        else:
            pylab.title('Model of degree: '+ str(degree)+' , R^2  ='+ str(r_squared_list[i]))
        pylab.xlabel('Years')
        pylab.ylabel('Degrees in Celcius')
        pylab.show()
 
# Test    
# x = pylab.array(range(10))
# y = pylab.array([x**2 for x in range(10)])      
# models = generate_models(x, y, [1,2])
# evaluate_models_on_training(x, y, models)   

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    national_temp_list = []
    for year in years:
        avrg_temp_city_list = []
        for city in multi_cities:
            # Evaluate the average annual temperature at city and add it to associated list
            year_temps_city = climate.get_yearly_temp(city,year) 
            avrg_temps_city = sum(year_temps_city)/len(year_temps_city)
            avrg_temp_city_list.append(avrg_temps_city)
        # Average over the cities to get the national annual average   
        avrg_national_temp = sum(avrg_temp_city_list)/len(multi_cities)
        national_temp_list.append(avrg_national_temp)
        
    return national_temp_list
        
def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    avrg_list = []
    for i in range(len(y)):
        if i-window_length+1 < 0:
            vec = y[0:(i+1)]
            avrg_list.append(sum(vec)/len(vec))
        else: 
            vec = y[i-window_length+1:i+1]
            avrg_list.append(sum(vec)/window_length)
    return avrg_list     



def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    rmse_val = math.sqrt(sum((y-estimated)**2)/len(y))
    return rmse_val


def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    std_year_temps = [] 
    for year in years:
        # evaluate the number of days in the year
        num_days = len(climate.get_yearly_temp(multi_cities[0],year))
        year_temps_city_list = pylab.zeros(num_days)
        for city in multi_cities:
            # Import the temperatures in city at year and add it to an array containing the sum of the temperatures
            # at different cities on a specific day of the year
            year_temps_city_list += climate.get_yearly_temp(city,year) 
        
        # Evaluate the average (deviding by the number of cities in multi_cities)        
        avrg_year_temps = year_temps_city_list/len(multi_cities)
        # Evaluate the standard deviation and append it to an appropriate list
        std_year_temps.append(numpy.std(avrg_year_temps))
        
    return pylab.array(std_year_temps)
    
def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    fits = []
    rmse_list = []
    for model in models:
        degree = len(model)-1
        estimated = pylab.zeros(len(x))
        for coeff in model:
            estimated += coeff*x**degree
            degree -= 1
        rmse_list.append(rmse(y, estimated))
        fits.append(estimated)
        
    for i in range(len(models)):
        pylab.figure(i+1)
        pylab.plot(x,y,'bo')
        pylab.plot(x,fits[i],'r')
        degree = len(models[i])-1
        pylab.title('Model of degree: '+ str(degree)+' , RMSE  ='+ str(rmse_list[i]))
        pylab.xlabel('Years')
        pylab.ylabel('Degrees in Celcius')
        pylab.show()

if __name__ == '__main__':
 
    
    # Part A.4
    ## Linear fit of the average temperature on January 10th in New York in the year range 1961-2009
    # temp_list = []
    # for year in TRAINING_INTERVAL: 
    #     climate = Climate('data.csv')
    #     temp_list.append(climate.get_daily_temp('NEW YORK', 1, 10, year))
    
    # temps = pylab.array(temp_list)
    # years = pylab.array(TRAINING_INTERVAL)
    # model = generate_models(years, temps, [1])
    # evaluate_models_on_training(years, temps, model)
    
    ## Linear fit of the average annual temperature New York in the year range 1961-2009 
    # temp_list = []
    # for year in TRAINING_INTERVAL: 
    #      climate = Climate('data.csv')
    #      year_temps = climate.get_yearly_temp('NEW YORK', year)
    #      avrg_year_temp = sum(year_temps)/len(year_temps)
    #      temp_list.append(avrg_year_temp)
    
    # temps = pylab.array(temp_list)
    # years = pylab.array(TRAINING_INTERVAL)
    # model = generate_models(years, temps, [1])
    # evaluate_models_on_training(years, temps, model)
    
    
    # Part B

    # climate = Climate('data.csv')
    # # A list of the national average temperature for every year between 1961-2009
    # national_avrg_temps = gen_cities_avg(climate, multi_cities = CITIES, years =TRAINING_INTERVAL)
    # years = pylab.array(TRAINING_INTERVAL)
    # model = generate_models(years, national_avrg_temps, [1])
    # evaluate_models_on_training(years, national_avrg_temps, model)
    

    # Part C - Moving avrage on the national annual average temperature
    
    # climate = Climate('data.csv')
    # # A list of the national average temperature for every year between 1961-2009
    # national_avrg_temps = gen_cities_avg(climate, multi_cities = CITIES, years =TRAINING_INTERVAL)
    # # Evaluate the moving average
    # mov_avrg =  moving_average(national_avrg_temps, window_length = 5)
    # years = pylab.array(TRAINING_INTERVAL)
    # model = generate_models(years, mov_avrg, [1])
    # evaluate_models_on_training(years,mov_avrg, model)

    # Part D.2I
    # climate = Climate('data.csv')
    # # A list of the national average temperature for every year between 1961-2009
    # national_avrg_temps = gen_cities_avg(climate, multi_cities = CITIES, years =TRAINING_INTERVAL)
    # # Evaluate the moving average
    # mov_avrg =  moving_average(national_avrg_temps, window_length = 5)
    # years = pylab.array(TRAINING_INTERVAL)
    # models = generate_models(years, mov_avrg, [1,2,4])
    # evaluate_models_on_training(years,mov_avrg, models)

    # Part D.2II
    # # A list of the national average temperature for every year between 2010-2015
    # testing_temps = gen_cities_avg(climate, multi_cities = CITIES, years =TESTING_INTERVAL)
    # # Evaluate the moving average
    # mov_avrg_testing =  moving_average(testing_temps, window_length = 5)
    # years = pylab.array(TESTING_INTERVAL)
    # evaluate_models_on_training(years,mov_avrg_testing, models)
    
    # Part E
    climate = Climate('data.csv')
    multi_cities = CITIES
    years = TRAINING_INTERVAL
    std_vec = gen_std_devs(climate, multi_cities, years)
    mov_avrg_std = moving_average(std_vec, window_length = 5)
    model = generate_models(years, mov_avrg_std, [1])
    years = pylab.array(TRAINING_INTERVAL)
    evaluate_models_on_training(years,mov_avrg_std, model)  # Note the the axis labels are wrong in the generated plot  
    