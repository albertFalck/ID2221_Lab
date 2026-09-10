# Python program to read CSV file without header
# Code taken from: https://www.geeksforgeeks.org/computer-science-fundamentals/reading-rows-from-a-csv-file-in-python/

# Import necessary packages
import csv

# Just outputs the first "num_rows" rows of the csv file into the console.
def read_csv(path, num_rows):
    with open(path) as file_obj:

        i = 0
        # Skips the heading
        # Using next() method
        heading = next(file_obj)
        
        # Create reader object by passing the file 
        # object to reader method
        reader_obj = csv.reader(file_obj)
        
        # Iterate over each row in the csv file 
        # using reader object
        for row in reader_obj:
            i = i + 1
            print(row)
            if (i > num_rows):
                break


# I extracted the zip file and renamed the .csv file contained inside to "air_quality.csv".
Path = 'ID2221_Lab/LabWeek1/Datasets/air_quality.csv'

# Currently just outputs the first 10 rows in the "air_quality.csv" file.
read_csv(Path, 10)

