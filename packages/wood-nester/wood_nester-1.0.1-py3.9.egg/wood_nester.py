""" print_lol receive list and show all elements
"""
def print_lol(the_list):
    """ we use loop for list
"""
#U can use single line comment also
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item)
        else:
            print(each_item)
        

        
