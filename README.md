# Table of Contents
1. [Project Summary](README.md#Project_Summary)
2. [Methodology](README.md#Methodology)
3. [Discussion](README.md#Discussion)
4. [Python Version](README.md#Python Version)

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
   1. Since we don't care abot sorting ALL of the data in dictionary, but do care about constantly maintainng the largest elements, A heap (priority queue) is a good fit here.
   2. Convert dictionary into heap: Time complexity O(M)
   3. Then heappop 10 times to output file: Time complexity O(10 * logM)
   4. Python internal method `sorted()` is also tested and compared to `heap` (see [Discussion](README.md#Discussion) for details)

The theoretical time complexity should be O(N + M + 10 * logM), where N is number of row in input file and M is size of dictionary.

# Discussion

1. Two candidate methods to find top K in dictionary:`Sorted()` vs. `Heap`

   1. Time complexity difference:

      1. Python internal `sorted()` algorithm are similar to merge sort, so it has O(MlogM) for sorting, and O(K) for selecting first K elements, in total of **O(MlogM + K)**.
      2. `Heap`: To heapify a heap with size of M will have time complexity of O(M), and O(klogM) for call pop() K times, in total of **O(M + KlogM)** 
      3. So when **K ~= M**, they have similar time complexity: O(MlogM); However, when **K << N**, heap will have advanced benefit over sort. 

      In this project, the total number of unique SOC_NAME of occupation is ~1000 for year 2016. So the corresponding ratio K/N ~= 0.01, which is not large enough to obviously display the benefit of heap obviously.

      Thus, codes with `sorted()` and `heap` are ran for 10 times respectively and the average run time are: 

      ​	`sorted()`: 3.98s 

      ​	`heap`: 3.95s 

   2. `bucket sort` :

      As we known, `bucket sort` can also be used to find top K elements. However, in this case, it is not recommended to use it because the size of bucket list has to be N (number of row in input file), not M (size of dictionary). The dictionary pair will be only saved into bucket list sparsely and a lot of space are wasted.

2. Input data validation on converted CSV in Google drive [folder](https://drive.google.com/drive/folders/1Nti6ClUfibsXSQw5PUIWfVGSIrpuwyxf?usp=sharing):

   1. checked the number of column in each row to see if it is consistent with number of column in header line;
   2. Throw warning if the target header name is not existed in input file (due to different file structure)
   3. Also checked the number of system files 

3. For case of less than 10 records in dictionary

4. To sort value descending and name alphabetically

5. Each line of the `top_10_occupations.txt` file should contain these fields in this order:

   1. __`TOP_OCCUPATIONS`__: Use the occupation name associated with an application's Standard Occupational Classification (SOC) code
   2. __`NUMBER_CERTIFIED_APPLICATIONS`__: Number of applications that have been certified for that occupation. An application is considered certified if it has a case status of `Certified`
   3. __`PERCENTAGE`__: % of applications that have been certified for that occupation compared to total number of certified applications regardless of occupation. 

   The records in the file must be sorted by __`NUMBER_CERTIFIED_APPLICATIONS`__, and in case of a tie, alphabetically by __`TOP_OCCUPATIONS`__.

## Python Version
Python 2.7.13


