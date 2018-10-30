# Table of Contents
1. [Project Summary](README.md#Project_Summary)
2. [Methodology](README.md#Methodology)
3. [Discussion](README.md#Discussion)
4. [Python Version](README.md#Python_Version)

# Project Summary

This repo is to solve the h1b statistic challenge for Insight Data Engineering Program. With input file contains yearly H1B(H-1B, H-1B1, E-3) visa application, this repo will output two txt files contains **Top 10 Occupations** and **Top 10 States** with most certified visa applications.

# Methodology

The methodology to find out Top 10 states and occupations which have the most certified H1B application can be summarized as below:

1. Create default dictionary to keep tracking accumulated count of desired fields for certified application
2. While reading input CSV file, with ';' as delimiter: Time complexity O(N)
   1. Locate the index of correspoding fields name in header line
   2. Validate data in target column of each row 
   3. For 'certified' case, update the count for correpsonding state and occupation 
3. Using **`heap`** to get top 10 states and occupations from updated dictionaies:
   1. Since we don't care abot sorting ALL of the data in dictionary, but do care about constantly maintainng the largest elements, A heap (priority queue) is a good fit here.
   2. Convert dictionary into heap: Time complexity O(M)
   3. Then heappop 10 times to output file: Time complexity O(10 * logM)
   4. Python internal method **`sorted()`** is also tested and compared to `heap` (see [Discussion](README.md#Discussion) for details)

The theoretical time complexity should be O(N + M + 10 * logM), where N is number of row in input file and M is size of dictionary.

# Discussion

1. Two candidate methods to find top K in dictionary:**`sorted()`** vs. **`heap`**

   1. Time complexity difference:

      1. Python internal **`sorted()`** algorithm are similar to merge sort, so it has O(MlogM) for sorting, and O(K) for selecting first K elements, in total of **O(MlogM + K)**.
      2. **`heap`**: To heapify a heap with size of M will have time complexity of O(M), and O(klogM) for call pop() K times, in total of **O(M + KlogM)** 
      3. So when **K ~= M**, they have similar time complexity: O(MlogM); However, when **K << N**, heap will have advanced benefit over sort. 

      In this project, the total number of unique SOC_NAME of occupation is ~1000 for year 2016. So the corresponding ratio K/N ~= 0.01, which is not large enough to obviously display the benefit of heap obviously.

      Thus, codes with **`sorted()`** and **`heap`** are ran for 10 times respectively and the average run time are: 

      ​	**`sorted()`**: 3.98s 

      ​	**`heap`**: 3.95s 

   2. **`bucket sort`** :

      As we known, **`bucket sort`** can also be used to find top K elements. However, in this case, it is not recommended because the size of bucket list has to be N (number of row in input file), not M (size of dictionary). The dictionary pair will be only saved very sparsely into bucket list and a lot of space are wasted, for occupation dictionary with N ~= 600,000 and M ~= 1000 in year 2016.

2. Input data validation on converted CSV in Google drive [folder](https://drive.google.com/drive/folders/1Nti6ClUfibsXSQw5PUIWfVGSIrpuwyxf?usp=sharing):

   1. checked the number of column in each row to see if it is consistent with number of column in header line;
   2. Throw warning if the target header name is not existed in input file (due to different file structure)
   3. Also checked the number of system files 

3. To sort value ascending and name alphabetically:

   When building heap from dictionary, use tuple of (-value, key) as the element in heap. for different value, heap will put the smallest of (-value) on top, which has largest absolute value; if two values are identical, then key will be sorted alphabetically.

## Python Version
Python 2.7.13


