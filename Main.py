import csv
from Package import Package

# Read distances and addresses from CSV files
with open("CSV/Distance.csv") as distance:
    Distance = csv.reader(distance)
    Distance = list(Distance)

with open("CSV/Addresses.csv") as address:
    Addresses = csv.reader(address)
    Addresses = list(Addresses)


# Function for loading package data into hash table. Used code from official WGU webinars
# as guidance (W-3_ChainingHashTable_zyBooks_Key-Value_CSV_Greedy_Dijkstra.py)
def load_package_data(fileName, hash_table):
    with open(fileName) as packages:
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

            # Create package object for use in hash table
            p = Package(ID, address, city, state, zip_code, departure_time, weight, status)

            # Insert package data in hash table with ID as the key
            hash_table.add(ID, p)


