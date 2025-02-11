###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    # Reverse the order of egg weights
    sorted_egg_weights = tuple(sorted(egg_weights,reverse = True))
    # Check if the answer is in the memo
    if (len(egg_weights),target_weight) in memo:
        return memo[(len(egg_weights),target_weight)]
    # Check if there is any weight left in the ship
    elif target_weight == 0: 
        return 0
    elif len(sorted_egg_weights) == 1:
        with_egg = dp_make_weight(sorted_egg_weights, target_weight-1,memo)
        result = with_egg + 1
    # Check if there is enough weight left for the specific egg checked
    elif target_weight < egg_weights[0]:
       result = dp_make_weight(sorted_egg_weights[1:], target_weight,memo)
    else:
        weight = sorted_egg_weights[0]
        # Explore branch with this egg
        weight_left = target_weight - weight
        #print('weight_left: ', weight_left)
        #print('sorted_egg_weights ', sorted_egg_weights)

        with_egg = dp_make_weight(sorted_egg_weights, weight_left,memo)
        # Explore branch without this egg
        without_egg = dp_make_weight(sorted_egg_weights[1:], target_weight,memo)
        if with_egg <= without_egg:
            result = with_egg+1
        else:
            result = without_egg
    # Add the 
    memo[(len(egg_weights),target_weight)] = result    
    return result
    
    # if (len(toConsider), avail) in memo:
    #     result = memo[(len(toConsider), avail)]
    # elif toConsider == [] or avail == 0:
    #     result = (0, ())
    # elif toConsider[0].getCost() > avail:
    #     #Explore right branch only
    #     result = fastMaxVal(toConsider[1:], avail, memo)
    # else:
    #     nextItem = toConsider[0]
    #     #Explore left branch
    #     withVal, withToTake =\
    #              fastMaxVal(toConsider[1:],
    #                         avail - nextItem.getCost(), memo)
    #     withVal += nextItem.getValue()
    #     #Explore right branch
    #     withoutVal, withoutToTake = fastMaxVal(toConsider[1:],
    #                                             avail, memo)
    #     #Choose better branch
    #     if withVal > withoutVal:
    #         result = (withVal, withToTake + (nextItem,))
    #     else:
    #         result = (withoutVal, withoutToTake)
    # memo[(len(toConsider), avail)] = result
    # return result
    
        
    
    

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()