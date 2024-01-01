# Student ID: 011770050
# Student name: Richard Bueno

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

# Returns the package nearest to the truck's current location
def min_distance_from(truck):
    # Initialize variables to track the minimum distance and corresponding package
    min_distance = float('inf')
    closest_package = None

    for package_id in truck.packages:
        package = packages_table.lookup(package_id)  # Retrieve the package from the hash table

        # Calculate the distance between the truck and the package's destination address
        distance = distance_between(truck.address, package.address)

        # Update minimum distance and corresponding package if a shorter distance is found
        if distance < min_distance:
            min_distance = distance
            closest_package = package

    return closest_package

# Function for delivering all the packages on the truck
def deliver_packages(truck):

    while len(truck.packages) > 0:
        # Find the closest undelivered package
        closest_package = min_distance_from(truck)

        # Specify the truck the package is on
        closest_package.on_truck = truck.name

        # Set departure time of package
        closest_package.depart_time = truck.depart_time

        # Update total mileage
        distance = distance_between(truck.address, closest_package.address)
        truck.mileage += distance

        # Update current address
        truck.address = closest_package.address

        # Update time for truck at delivery
        truck.time += datetime.timedelta(hours=distance / 18)

        # Update time delivered
        closest_package.time_delivered = truck.time

        # Remove package from truck
        truck.packages.remove(closest_package.ID)

    # Return the truck to the hub
    distance = distance_between(truck.address, '4001 South 700 E')
    # Update final mileage and time for the truck
    truck.mileage += distance
    truck.time += datetime.timedelta(hours=distance / 18)

# Instantiate truck objects with packages manually loaded according to restraints
truck_1 = Truck('Truck 1', [1, 13, 14, 15, 16, 19, 20, 27, 29, 30, 31, 34, 35, 37, 39, 40], 0.0,
                "4001 South 700 E", datetime.timedelta(hours=8))

truck_2 = Truck('Truck 2', [3, 6, 12, 18, 21, 22, 23, 24, 25, 26, 28, 36, 38], 0.0,
                "4001 South 700 E", datetime.timedelta(hours=9, minutes=5))

truck_3 = Truck('Truck 3', [2, 4, 5, 7, 8, 9, 10, 11, 17, 32, 33], 0.0,
                "4001 South 700 E", datetime.timedelta(hours=10, minutes=20))

# Send out the trucks
deliver_packages(truck_1)
deliver_packages(truck_2)
deliver_packages(truck_3)

class Main:
    # User interface
    print('WGUPS Package Status Interface\n')

    # Mileage report
    print('The first driver departed with the first truck at ' + str(truck_1.depart_time) +
          ' and returned at ' + str(truck_1.time))
    print('The second driver departed with the second truck at ' + str(truck_2.depart_time) +
          ' and returned at ' + str(truck_2.time))
    print('The first driver departed with the third truck at ' + str(truck_3.depart_time) +
          ' and returned at ' + str(truck_3.time) + '\n')

    print('Total mileage: ' + str(truck_1.mileage + truck_2.mileage + truck_3.mileage) + '\n')

    # Get the time for use in delivery status
    time_input = input('Please enter the time at which you wish to view the packages. Use the HH:MM format: ')
    (hour, minute) = time_input.split(':')
    time_lookup = datetime.timedelta(hours=int(hour), minutes=int(minute))

    # Determine whether the user wants to view one or all delivery statuses
    user_input = input("\nPlease enter 'one' to view a single package or 'all' to view all the packages: ")

    if user_input == 'one':
        user_package = input('\nPlease enter the Package ID number: ')

        package = packages_table.lookup(int(user_package))
        package.status_at_time(time_lookup)
        print('Package ' + str(package.ID) + ' status: ' + str(package.status))

    elif user_input == 'all':
        for package_id in range(1, 41):
            package = packages_table.lookup(package_id)
            package.status_at_time(time_lookup)
            print('Package ' + str(package.ID) + ' status: ' + str(package.status))

    # Demonstration of the lookup funtion for part B of the assignment
    user_input2 = input("\nTo demonstrate the lookup function, please enter 'lookup': ")
    if user_input2 == 'lookup':
        lookup_input = input('Please enter the ID number of the package you would like to look up: ')
        package = packages_table.lookup(int(lookup_input))
        print(package)