# Table of Contents
1. [Project Summary](README.md#Project_Summary)
2. [Methodology](README.md#Methodology)
3. [Discussion](README.md#Discussion)
4. [Work Environment](README.md#Work_Environment)

# Project Summary

This repo is to solve the h1b statistic challenge for Insight Data Engineering Program. With input file contains yearly H1B(H-1B, H-1B1, E-3) visa application, this repo will output two txt files contains **Top 10 Occupations** and **Top 10 States** with most certified visa applications.

# Methodology

The methodology to find out Top 10 states and occupations which have the most certified H1B application can be summarized as below:

1. Create default dictionary to keep tracking accumulated count of desired fields for certified application
2. While reading input CSV file, with ';' as delimiter: Time complexity O(N)
   1. Locate the index of correspoding fields name in header line
   2. Validate data in target column of each row 
   3. For 'certified' case, update the count for correpsonding state and occupation 
3. Using `heap` to get top 10 states and occupations from updated dictionaies:
   1. Convert dictionary into heap: Time complexity O(M)
   2. Then heappop 10 times to output file: Time complexity O(10 * logM)
   3. Python internal method `sorted()` is also tested and compared to `heap` (see [Discussion](README.md#Discussion) for details)

The theoretical time complexity should be O(N + M + 10 * logM), where N is number of row in input file and M is size of dictionary.

# Discussion

1. Two candidate methods to find top K elements:`Sorted()` vs. `Heap`

   1. Time complexity difference:

      1. Normal sort algorithm (quick sort, merge sort...): O(NlogN + K) time complexity O(NlogN) for sorting, and O(k) for selecting first K elements; 
      2. Heap: O(N + KlogN) time complexity O(N) for heapify N size heap, and O(klogN) for pop first K elements; 

   2. Comparing sort and heap: 

      ​	sort has time complexity of O(NlogN + K) 

      ​	heap has time complexity of O(KlogN + N). 

      ​	So when K ~= N, they have similar time complexity; 

      ​	But when K << N, heap will have advanced benefit over sort. 

      in this case, for request of top 10 state and occupation, the total number of unique SOC_NAME are ~1000 in 2016. So ratio K/N ~= 0.01, which is not large enough to show the benefit of heap obviously. 

      The average run time of 10 loops of sort and heap are: sort: 3.98s heap: 3.95s dictionary vs. default dictionary

   3. `bucket sort` :

      As we known, `bucket sort` can also be used to find top K elements. However, in this case, it is not recommended to use it because the size of bucket list has to be N (number of row in input file), not M (size of dictionary). The dictionary pair will be only saved into bucket list sparsely and a lot of space are wasted.

2. Input data validation: 

   1. directly used the converted CSV in Google drive [folder](https://drive.google.com/drive/folders/1Nti6ClUfibsXSQw5PUIWfVGSIrpuwyxf?usp=sharing).
   2. checked the number of column in each row
   3. checked if the target name existed or mis-spelled
   4. Also checked the number of system files 

3. 

4. For case of less than 10 records in dictionary

5. To sort value descending and name alphabetically

6. Each line of the `top_10_occupations.txt` file should contain these fields in this order:

   1. __`TOP_OCCUPATIONS`__: Use the occupation name associated with an application's Standard Occupational Classification (SOC) code
   2. __`NUMBER_CERTIFIED_APPLICATIONS`__: Number of applications that have been certified for that occupation. An application is considered certified if it has a case status of `Certified`
   3. __`PERCENTAGE`__: % of applications that have been certified for that occupation compared to total number of certified applications regardless of occupation. 

   The records in the file must be sorted by __`NUMBER_CERTIFIED_APPLICATIONS`__, and in case of a tie, alphabetically by __`TOP_OCCUPATIONS`__.

   

# Output 

Your program must create 2 output files:
* `top_10_occupations.txt`: Top 10 occupations for certified visa applications
* `top_10_states.txt`: Top 10 states for certified visa applications

Each line holds one record and each field on each line is separated by a semicolon (;).

Each line of the `top_10_occupations.txt` file should contain these fields in this order:
1. __`TOP_OCCUPATIONS`__: Use the occupation name associated with an application's Standard Occupational Classification (SOC) code
2. __`NUMBER_CERTIFIED_APPLICATIONS`__: Number of applications that have been certified for that occupation. An application is considered certified if it has a case status of `Certified`
3. __`PERCENTAGE`__: % of applications that have been certified for that occupation compared to total number of certified applications regardless of occupation. 

The records in the file must be sorted by __`NUMBER_CERTIFIED_APPLICATIONS`__, and in case of a tie, alphabetically by __`TOP_OCCUPATIONS`__.

Each line of the `top_10_states.txt` file should contain these fields in this order:
1. __`TOP_STATES`__: State where the work will take place
2. __`NUMBER_CERTIFIED_APPLICATIONS`__: Number of applications that have been certified for work in that state. An application is considered certified if it has a case status of `Certified`
3. __`PERCENTAGE`__: % of applications that have been certified in that state compared to total number of certified applications regardless of state.

The records in this file must be sorted by __`NUMBER_CERTIFIED_APPLICATIONS`__ field, and in case of a tie, alphabetically by __`TOP_STATES`__. 

Depending on the input (e.g., see the example below), there may be fewer than 10 lines in each file. There, however, should not be more than 10 lines in each file. In case of ties, only list the top 10 based on the sorting instructions given above.

Percentages also should be rounded off to 1 decimal place. For instance, 1.05% should be rounded to 1.1% and 1.04% should be rounded to 1.0%. Also, 1% should be represented by 1.0%

## Python Version
Python 2.7.13


