# Table of Contents
1. [Project Summary](README.md#Project Summary)
2. [Methodology](README.md#Methodology)
3. [Discussion](README.md#Discussion)
4. [Work Environment](README.md#Work Environment)

# Project Summary

This repo is to solve the h1b statistic challenge for Insight Data Engineering Program. With input file contains yearly H1B(H-1B, H-1B1, E-3) visa application, this repo will output two txt files contains **Top 10 Occupations** and **Top 10 States** with most certified visa applications.

# Methodology

The methodology to find out Top 10 states and occupations which have the most certified H1B application can be summarized as below:

1. Create default dictionary to track accumulated count of desired fields
2. After reading input CSV file, separate each row by ';' with data validation 
3. Locating index of corresponding fields 
4. For 'certified' case, update the count for correpsonding state and occupation 
5. Using Heap to get top 10 states and occupations with most certified cases from updated dictionaies

So in this solution, I will use the method of dict and heap: create two dictionaries: for occupation and for state; read csv file row by row with data cleaning: for each fow, update the count for both dictionaries; after reading all input, find the top 10 counts in dictionaries: save dictionary into heap, then pop 10 times; Time O(N + klogN)

Raw data could be found [here](https://www.foreignlaborcert.doleta.gov/performancedata.cfm) under the __Disclosure Data__ tab (i.e., files listed in the __Disclosure File__ column with ".xlsx" extension). 
For your convenience we converted the Excel files into a semicolon separated (";") format and placed them into this Google drive [folder](https://drive.google.com/drive/folders/1Nti6ClUfibsXSQw5PUIWfVGSIrpuwyxf?usp=sharing). However, do not feel limited to test your code on only the files we've provided on the Google drive 

**Note:** Each year of data can have different columns. Check **File Structure** docs before development. 

# Discussion

1. dictionary vs. default dictionary

2. Input data validation: 

   1. directly used the converted CSV in Google drive [folder](https://drive.google.com/drive/folders/1Nti6ClUfibsXSQw5PUIWfVGSIrpuwyxf?usp=sharing).
   2. checked the number of column in each row
   3. checked if the target name existed or mis-spelled

3. Sort vs. Heap

   1. Time complexity

   2. Python default sort vs bucket sort

   3. For sorting. 

      There are three candidate methods can be used to find top K elements: 

      1. Normal sort algorithm (quick sort, merge sort...): O(NlogN + K) time complexity O(NlogN) for sorting, and O(k) for selecting first K elements; 
      2. Heap: O(N + KlogN) time complexity O(N) for heapify N size heap, and O(klogN) for pop first K elements; 
      3. Bucket sort: O(N), worst O(NlogN): Not considered because the bucket list requires large space and only save data sparsely. 

4. Comparing sort and heap: 

   ​	sort has time complexity of O(NlogN + K) 

   ​	heap has time complexity of O(KlogN + N). 

   ​	So when K ~= N, they have similar time complexity; 

   ​	But when K << N, heap will have advanced benefit over sort. 

   in this case, for request of top 10 state and occupation, the total number of unique SOC_NAME are ~1000 in 2016. So ratio K/N ~= 0.01, which is not large enough to show the benefit of heap obviously. 

   The average run time of 10 loops of sort and heap are: sort: 3.98s heap: 3.95s 

5. Each line of the `top_10_occupations.txt` file should contain these fields in this order:

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


