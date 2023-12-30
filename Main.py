import csv
import sys
from HashTable import HashTable
from Package import Package
from Truck import Truck
import datetime

# Read distances and addresses from CSV files
with open("CSV/Distance.csv") as distance:
    distance_data = csv.reader(distance)
    distance_data = list(distance_data)

with open("CSV/Addresses.csv") as address:
    address_data = csv.reader(address)
    address_data = list(address_data)


# Function for loading package data into hash table. Used code from official WGU webinars
# as guidance (W-3_ChainingHashTable_zyBooks_Key-Value_CSV_Greedy_Dijkstra.py)
def load_package_data(file_name, hash_table):
    with open(file_name) as packages:
        package_data = csv.reader(packages)
        for package in package_data:
            ID = int(package[0])
            address = package[1]
            city = package[2]
            state = package[3]
            zip_code = package[4]
            departure_time = package[5]
            weight = package[6]
            status = "At the hub"

            # Package object for use in hash table
            p = Package(ID, address, city, state, zip_code, departure_time, weight, status)

            # Insert package data in hash table with ID as the key
            hash_table.add(ID, p)


# Hash table to hold package data
packages_table = HashTable()

# Extract package data
load_package_data("CSV/Packages.csv", packages_table)

# Function to return distance between two addresses
def distance_between(address1, address2):
    for row in address_data:
        if address1 in row[2]:
            a1 = int(row[0])
        if address2 in row[2]:
            a2 = int(row[0])
    distance = distance_data[a1][a2]
    if distance == '':
        distance = distance_data[a2][a1]
    return float(distance)

# Instantiate truck objects with packages manually loaded according to restraints in part F
truck_1 = Truck([1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], 0.0,
                "4001 South 700 E", datetime.timedelta(hours=8))

# Truck 2 leaves at 10:20 to account for mislabeled package 9
truck_2 = Truck([2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33], 0.0,
                "4001 South 700 E", datetime.timedelta(hours=10, minutes=20))

truck_3 = Truck([3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], 0.0,
                "4001 South 700 E", datetime.timedelta(hours=9, minutes=5))

# Returns the address of the package nearest to the truck's current location
def min_distance_from(truck):
    # Initialize variables to track the minimum distance and corresponding package
    min_distance = float('inf')
    closest_package = None

    for package_id in truck.packages:
        package = packages_table.find(package_id)  # Retrieve the package from the hash table

        # Calculate the distance between the truck and the package's destination address
        distance = distance_between(truck.address, package.address)

        # Update minimum distance and corresponding package if a shorter distance is found
        if distance < min_distance:
            min_distance = distance
            closest_package = package.address

    return closest_package

