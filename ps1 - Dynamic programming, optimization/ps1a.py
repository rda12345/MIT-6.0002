###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    
    # Load and read the file
    print("Loading word list from file...")
    # inFile: file
    file = open(filename, 'r')   # The 'r' represents that the mode to use the file for is the "read" mode.
    # cowdict: dictionary containing cow:wieght pairs
    cow_dict = {}
    # Loads the cows and inserts them into the dictionary
    for line in file:
        name,weight = line.split(',')
        cow_dict[name] = int(weight)
    file.close()

    print("  ", len(cow_dict), "cows loaded.")
    return cow_dict
    

    
# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # Sort the dictionary in decreasing order of weights
    sorted_cows = dict(sorted(cows.items(), key=lambda item: item[1],reverse = True))
    # Create a list of wieghts in reversed order and the associated cows names
    weight_list = list(sorted_cows.values())
    name_list = list(sorted_cows.keys())
    
    # Try and insert the cows in the spaceship going from the largest to the smallest
    weight_left = limit
    # The list which will contaian the lists associated with the different trips
    total_list = []
    
    # While there are still cows left on earth
    while len(weight_list)> 0:
        trip_list = []
        # Go over the weights of the cows and try to add them to the spaceship from the most heavy to the list heavey    
        for i in range(len(weight_list)):
            # Get a list containing the keys
            weight = weight_list[i]
            name = name_list[i]
            # If there is weight left in the spaceship
            if weight_left >= weight:
                trip_list.append(name) 
                weight_left -= weight
        # Deleting the cows sent
        for cow in trip_list:
            name_list.remove(cow)
            weight_list.remove(cows[cow])
        # Append the trip list to the total list
        total_list.append(trip_list)
        # Reset the weight left to the limit for the new trip
        weight_left = limit
    return total_list
    



# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # Run over all partitions
 
    for partition in get_partitions(list(cows.keys())):
        check_bool = True
        for trip in partition:
            #sum over the weights of each trip 
            trip_sum = sum([cows[c] for c in trip])
            #  If the weight sum of the trip is overweight change the check boolian to False
            if trip_sum >= limit:
                check_bool = False
                break
        # If all the trips pass the weight test then return partition, if one of the trips fails
        # The for function will go to the next partition, which contains eather the same number of trips or lower.
        # There partition will include the smallest number of trips (sets).
        if check_bool:
            return partition
                
        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # Loading the cows data
    #cows = load_cows('ps1_cow_data.txt')  
    
    # Running greedy_cow_solution
    start = time.time()
    greedy_list = greedy_cow_transport(cows,limit=10)
    end = time.time()
    print('greedy_cow_transport:')
    print('number of trips: ',len(greedy_list))
    print('run time: ',end-start)
    print('-----------------------------\n')
    start = time.time()
    brute_list = brute_force_cow_transport(cows,limit=10)
    end = time.time()
    print('brute force cow transport:')
    print('number of trips: ',len(brute_list))
    print('run time: ',end-start)
    print('-----------------------------')
    

## Tests:
if __name__ =='__main__':
    cows = load_cows('ps1_cow_data.txt')  
    compare_cow_transport_algorithms()

#print(cows)
# greedy_cow_solution = greedy_cow_transport(cows,limit=10)
# print(greedy_cow_solution)
#brute_force_solution = brute_force_cow_transport(cows,limit=10)
#print(brute_force_solution)




# sorted_cows = dict(sorted(cow_dict.items(), key=lambda item: item[1],reverse = True))
# weight_list = sorted_cows.values()
# name_list = sorted_cows.keys()
# print(sorted_cows)
# print(weight_list)
# print(name_list)

