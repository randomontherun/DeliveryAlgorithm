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
        package = packages_table.find(package_id)  # Retrieve the package from the hash table

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
truck_1 = Truck([13, 14, 15, 16, 19, 20, 27, 29, 30, 31, 34, 35, 39, 40], 0.0,
                "4001 South 700 E", datetime.timedelta(hours=8))

truck_2 = Truck([1, 3, 6, 12, 18, 21, 22, 23, 24, 25, 26, 28, 36, 37, 38], 0.0,
                "4001 South 700 E", datetime.timedelta(hours=9, minutes=5))

truck_3 = Truck([2, 4, 5, 7, 8, 9, 10, 11, 17, 32, 33], 0.0,
                "4001 South 700 E", datetime.timedelta(hours=10, minutes=20))

print('Number of packages:')
print(len(truck_1.packages) + len(truck_2.packages) + len(truck_3.packages))
print('Packages in order:')
all_trucks = truck_1.packages + truck_2.packages + truck_3.packages
all_trucks.sort()
print(all_trucks)

# Send out the trucks
deliver_packages(truck_1)
deliver_packages(truck_2)
deliver_packages(truck_3)


print('Truck 1 mileage:')
print(truck_1.mileage)
print('Truck 2 mileage:')
print(truck_2.mileage)
print('Truck 3 mileage:')
print(truck_3.mileage)
print('Total mileage:')
print(truck_1.mileage + truck_2.mileage + truck_3.mileage)
print('Truck 1 finish time:')
print(truck_1.time)
print('Info for package ' + str(packages_table.find(1)))


