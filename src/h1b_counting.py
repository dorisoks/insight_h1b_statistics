"""
Methodology & Discussion:
    The task is to find out Top 10 states and occupations which have the most certified H1B application.
    The methodology is similar to find Top K frequent words: using dictionary and then sorting

    For sorting, there are three candidate methods can be used to find top K elements:
        1. Normal sort algorithm (quick sort, merge sort...): O(NlogN + K)
            time complexity O(NlogN) for sorting, and O(k) for selecting first K elements;
        2. Heap: O(N + KlogN)
            time complexity O(N) for heapify N size heap, and O(klogN) for pop first K elements;
        3. Bucket sort: O(N), worst O(NlogN):
            Not considered because the bucket list requires large space and only save data sparsely.

    Comparing sort and heap:
        sort has time complexity of O(NlogN + K)
        heap has time complexity of O(KlogN + N).
        So when K ~= N, they have similar time complexity;
        But when K << N, heap will have advanced benefit over sort.

        in this case, for request of top 10 state and occupation, the total number of unique SOC_NAME are ~1000 in 2016.
        So ratio K/N ~= 0.01, which is not large enough to show the benefit of heap obviously.

        The average run time of 10 loops of sort and heap are:
            sort: 3.98s
            heap: 3.95s

    So in this solution, I will use the method of dict and heap:
        create two dictionaries: for occupation and for state;
        read csv file row by row with data cleaning:
            for each fow, update the count for both dictionaries;
        after reading all input, find the top 10 counts in dictionaries:
            save dictionary into heap, then pop 10 times; Time O(N + klogN)

"""



import csv
import collections
import heapq
import sys
import timeit


def get_header_index(list_input_header, list_target_header):
    """
    To check if any header in list_target_header are found in header line of input file
    :param list_input_header: line of header in input file
    :param list_target_header: list of target headers
    :return: index of target header or -1 (means not existed)
    """
    curr_index = -1     # initial value for index
    for i in range(len(list_input_header)):
        if list_input_header[i] in list_target_header:
            # if any header in target header list is found, update index
            curr_index = i
    return curr_index   # if found, return true index, otherwise return -1


def convert_dict_to_heap(input_dict):
    """
    To convert dictionary to heap by adding dict pairs into heap then heapifying
    Note: in order to sort count descending and key ascending, use (-value, key) as element in heap
    :param input_dict: dictionary after counting
    :return: heap after heapify
    """
    input_heap = [(-count, key) for key, count in input_dict.items()]   #initiate heap and add dict pairs into it
    heapq.heapify(input_heap)   # heapify heap, time complexity O(N)
    return input_heap


def format_heap_tuple_as_output(input_data, total_count):
    """
    For each tuple (-value, key), to format it as "key;value;percentage"
    :param input_data: Tuple (-value, key)
    :param total_count: total amount of certified case
    :return:
    """
    return ';'.join([input_data[1], str(-input_data[0]), str("{:.1%}".format((-1.0 * input_data[0] / total_count)))])


def save_top_n_tuple_to_txt(input_heap,total_count_certified, output_file_name, list_header_to_txt, k):
    with open(output_file_name, 'w') as op:
        op.write(list_header_to_txt)
        for _ in range(k):
            if len(input_heap) != 0:
                current_item = heapq.heappop(input_heap)
                op.write('\n' + format_heap_tuple_as_output(current_item, total_count_certified))


def format_sort_output_line(input_data, total_count):
    """
    For method of sort and comparison purpose only
    :param input_data:
    :param total_count:
    :return:
    """
    return ';'.join([input_data[0], str(input_data[1]), str("{:.1%}".format((1.0 * input_data[1] / total_count)))])


def save_sorted_top_n_to_txt(input_sorted_list,total_count_certified, output_file_name, list_header_to_txt):
    """
    For method of sort and comparison purpose only:
    :param input_sorted_list: list with sorted elements
    :param total_count_certified: total amount of certified cases
    :param output_file_name: output txt file name
    :param list_header_to_txt: header line in output txt file
    :return:
    """
    with open(output_file_name, 'w') as op:
        op.write(list_header_to_txt)
        for current_item in input_sorted_list:
          op.write('\n' + format_sort_output_line(current_item, total_count_certified))


def find_top_n_state_and_occupation(input_file, output_occupation, output_state):
    """
    Main function to get top K elements:
        Initialize default dictionary to track counts and list of target headers
        After reading input CSV file, separate each row by ';' with data validation
        Locating index of corresponding fields
        For 'certified' case, update the count for correpsonding state and occupation
        Call other functions to find top 10 states and occupations with most certified cases
    :param input_file: Input CSV file name
    :param output_occupation: Output file name for occupation
    :param output_state: Output file name for state
    :return:
    """

    # Initialize two default dictionaries to count numbers of state and occupation
    # parameter of int in defaultdict will automatically assign 0 to a new key
    dict_occupation = collections.defaultdict(int)
    dict_state = collections.defaultdict(int)

    # Create list of target headers for required fields
    list_state_header = ['WORKSITE_STATE', 'LCA_CASE_WORKLOC1_STATE']
    list_occupation_header = ['LCA_CASE_SOC_NAME', 'SOC_NAME']
    list_status_header = ['CASE_STATUS', 'STATUS']

    # Create list of headers for output files
    list_header_to_txt_state = 'TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE'
    list_header_to_txt_occupation = 'TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE'


    with open(input_file) as csvfile:
        # note: There are some lines have special content for single column:
        #       use semicolon inside quote marks, i.e. ...;"PRESIDENT &AMP; CHIEF EXECUTIVE OFFICER";...
        #       To avoid separating column based on this inner semicolon, here I used csv.reader with delimiter
        #       This method will ignore the case of semicolon used inside quote mark for single column
        readCSV = csv.reader(csvfile, delimiter=';')

        # Here use 'next' to save header line and avoid dictionary count
        header = next(readCSV, None)

        # Call function to find corresponding index of 'state' and 'occupation'
        index_state = get_header_index(header, list_state_header)
        index_occu = get_header_index(header, list_occupation_header)
        index_status = get_header_index(header, list_status_header)

        # Check if the target header is found or not:
        #   if not found, the program will provide warning and stop program
        if index_status == -1 or index_state == -1 or index_occu == -1:
            print """\
                !!!Program stopped!!!
                Couldn't find target header name in current file
                Please check the spelling of header name for desired fields
            """
            return

        # Get length of header line to verify if all of rows have the same length or not
        length_header_list = len(header)

        # Initiate count to store total number of certified cases for percentage calculation
        count_certified = 0


        """
        Updating dictionary and total count:
            iterate all records line by line
            only work when case status is 'certified'
        """
        for row in readCSV:
            # Data validation:
            #   check if the length of input row is consistent with header line
            #   if not, it will be ignored for now, and later may be checked manually
            if len(row) != length_header_list:
                continue

            # Only update dictionary if case is certified
            if (row[index_status] == 'CERTIFIED'):
                # update dictionary
                dict_state[row[index_state]] += 1
                dict_occupation[row[index_occu]] += 1

                # update total count of certified cases
                count_certified += 1

        """
        method: heap
            Time complexity: O(N + K*logN)
            Space complexity: O(N)
        """
        # call function to covert dictionary to heap and heapify
        heap_state = convert_dict_to_heap(dict_state)
        heap_occupation = convert_dict_to_heap(dict_occupation)

        # find top 10 state and occupation with most certified cases:
        save_top_n_tuple_to_txt(heap_state, count_certified, output_state, list_header_to_txt_state, 10)
        save_top_n_tuple_to_txt(heap_occupation, count_certified, output_occupation, list_header_to_txt_occupation, 10)


        """
        # For comparison purpose:
        #       method: sort
        #           time complexity: O(NlogN)

            # sort dictionary based on value (descending) and key (alphabetically) 
            # and only keep the first 10 elements
            sorted_state = sorted(dict_state.items(), key=lambda (k, v): (-v, k))[:10]
            sorted_occupation = sorted(dict_occupation.items(), key=lambda (k, v): (-v, k))[:10]
            
            # write to txt files
            save_sorted_top_n_to_txt(sorted_state, count_certified, output_state, list_header_to_txt_state)
            save_sorted_top_n_to_txt(sorted_occupation, count_certified, output_occupation, list_header_to_txt_occupation)
        """



if __name__ == "__main__":
    """
        call function to read data from input csv file and then write top 10 into corresponding output files:
            sys.argv[1]: input csv file
            sys.argv[2]: output txt file of top 10 occupations
            sys.argv[3]: output txt file of top 10 states
    """

    # I/O validation: Check the number of arguments in use
    if len(sys.argv) != 4:
        print """\
            Please enter correct numbers of files following the usage below:
            USAGE: python h1b_counting.py input_file output_file_occupation output_file_state
        """
        sys.exit(1)

    find_top_n_state_and_occupation(sys.argv[1], sys.argv[2], sys.argv[3])

