# Student Name: Jessica Short
# Student ID: 010500487
# Course: Data Structures and Algorithms II - C950
# Assignment: NHP3 Task 1: WGUPS Routing Program Planning
# Date: 11/25/2024

import csv
import datetime


# Read the CSV files and converts their contents into Python lists
with open("CSV/csvaddress.csv") as address_file:
    address_data = csv.reader(address_file)
    address_data = list(address_data)

with open("CSV/csvdistance.csv") as distance_file:
    distance_data = csv.reader(distance_file)
    distance_data = list(distance_data)



# Creating the hash table
# Source
# C950 - Webinar-1 - Let’s Go Hashing
# W-1_ChainingHashTable_zyBooks_Key-Value.py
# Ref: zyBooks: Figure 7.8.2: Hash table using chaining.
# Modified for Key:Value

# HashTable class using chaining.
class ChainingHashTable:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initialcapacity=40):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initialcapacity):
            self.table.append([])

    # Inserts a new item into the hash table and will update an item in the list already
    def insert(self, key, item): #  does both insert and update
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # update key if it is already in the bucket
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                kv[1] = item
                return True

       # if not, insert the item to the end of the bucket list.
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Searches for an item with matching key in the hash table.
    # Returns the item if found, or None if not found.
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        # print(bucket_list)
        # search key in bucket
        for kv in bucket_list:
            # print(key_value)
            if kv[0] == key:
                return kv[1]  # value
        return None

    # Removes an item with matching key from the hash table.
    def remove(self, key):
        # get the bucket list where this item will be removed from.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the item from the bucket list if it is present.
        for kv in bucket_list:
            # print (key_value)
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])



# Define Package class
class Package:
    def __init__(self, ID, address, city, state, zipcode, deadline, weight, notes, status, departureTime, deliveryTime):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.departureTime = None
        self.deliveryTime = None

    # Defines the __str__ method of the Package class for readable output
    def __str__(self):
        bold_status_label = f"\033[1mStatus:\033[0m"  # Bold the "Status:" label
        bold_status_value = f"\033[1m{self.status}\033[0m"  # Bold the status value
        return (
            f"ID: {self.ID}, Address: {self.address}, {self.city}, {self.state}, {self.zipcode}, "
            f"Weight: {self.weight} lbs, "
            f"Departure Time: {self.departureTime or 'Not set'}, "
            f"Deadline: {self.deadline}, "
            f"Delivery Time: {self.deliveryTime or 'Not set'}, | "
            f"{bold_status_label} {bold_status_value}"
        )

    # This method updates the status of a Package object based on a given time
    def updateStatus(self, userTime):
        if self.deliveryTime is None or userTime < self.departureTime:
            self.status = "At the hub"
        elif userTime < self.deliveryTime:
            self.status = "En route"
        else:
            self.status = "Delivered"

        # Handle address update for package 9 after it's received at 10:20AM
        if self.ID == 9:
            self._updatePackage9Address(userTime)

    def _updatePackage9Address(self, userTime):
        cutoff_time = datetime.timedelta(hours=10, minutes=20)
        if userTime > cutoff_time:
            self.address = "410 S State St"
            self.zipcode = "84111"
        else:
            self.address = "300 State St"
            self.zipcode = "84103"



#This function loads package data from a CSV file and inserts it into a hash table
def loadPackagesFromCSV(file_path):
    with open(file_path) as file:
        package_data = csv.reader(file, delimiter=',')
        for data in package_data:
            package_id = int(data[0])
            street_address = data[1]
            city = data[2]
            state = data[3]
            zip_code = data[4]
            deadline = data[5]
            weight = data[6]
            notes = data[7]
            status = "At the Hub"
            departure_time = None
            delivery_time = None

            # Create a new Package instance
            package = Package(package_id, street_address, city, state, zip_code, deadline, weight, notes, status,
                              departure_time, delivery_time)

            # Insert the Package object into the hash table
            packageMap.insert(package_id, package)


# Initialize the hash table and assigns it to the variable packageMap
packageMap = ChainingHashTable()



# Define Truck class
class Truck:
    def __init__(self, capacity, speed, mileage, current_location, depart_time, packages):
        self.capacity = capacity
        self.speed = speed
        self.mileage = mileage
        self.current_location = current_location
        self.time = depart_time
        self.depart_time = depart_time
        self.packages = packages

    # Defines the _str_ method of the Truck class
    def __str__(self):
        return (
            f"Truck Capacity: {self.capacity}, Speed: {self.speed} mph, "
            f"Mileage: {self.mileage} miles, Location: {self.current_location}, "
            f"Time: {self.time}, Departure Time: {self.depart_time}, "
            f"Packages: {', '.join(map(str, self.packages)) if self.packages else 'No packages'}"
        )


# This function searches through the address_data list to find the ID number
# of a given address. It returns the ID as an integer if the address is found.
# The ID number is also the row/column number in the distance matrix distance_data.
def find_address_id(target_address):
    for row in address_data:
        if target_address in row[2]:
           return int(row[0])


# The function looks up and returns the distance between two addresses
# based on the distance matrix distance_data.
def calculate_distance(location1, location2):
    dist = distance_data[location1][location2]
    if dist == '':
        dist = distance_data[location2][location1]
    return float(dist)


# pulls data from CSV into the function
loadPackagesFromCSV('CSV/csvpackage.csv')



# Load the trucks and assign them a departure time
# The special instructions that are listed in the package notes
# have been taken into consideration when assigning packages to a truck
# and choosing a departure time.
truck1 = Truck(16, 18, 0.0,"4001 South 700 East", datetime.timedelta(hours=8),
                [1, 4, 13, 14, 15, 16, 19, 20, 21, 29, 30, 34, 37, 39, 40])
truck2 = Truck(16, 18, 0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=21),
                [2, 5, 7, 8, 9, 10, 11, 12, 17, 22, 23, 24, 27, 33, 35])
truck3 = Truck(16, 18, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=6),
                [3, 6, 18, 25, 26, 28, 31, 32, 36, 38])

# Store the original package assignments for each truck.  For use on line 335 for printing to the user interface.
original_truck_packages = {
    "Truck 1": truck1.packages.copy(),
    "Truck 2": truck2.packages.copy(),
    "Truck 3": truck3.packages.copy()
}


# This function simulates the process of delivering packages assigned to a truck
# Uses the nearest neighbor algorithm
def deliverTruckPackages(truck, priority_packages=None):
    # Default priority packages if not provided
    # Packages 25 and 6 are delayed on their flight.  They will not arrive at the
    # depot until 9:05am yet they have a 10:30AM deadline.
    priority_packages = priority_packages or [25, 6]

    # Initialize an empty list to store packages to go out for delivery
    packages_in_transit = []

    # Loop through each package ID currently assigned to the truck
    for packageID in truck.packages:
        # Use the packageMap to find the detailed information for the package
        package = packageMap.search(packageID)

        # Add the retrieved package object to the packages_in_transit list
        packages_in_transit.append(package)

    # Clear the truck's package list after adding the packages to packages_in_transit
    truck.packages.clear()

    # Represents a large initial distance to ensure correct comparison
    # The current max distance between 2 locations is 14.2
    LARGE_INITIAL_DISTANCE = 30

    # Process deliveries
    # This while loop will continue to execute as long as the list packages_in_transit is not empty.
    while packages_in_transit:
        # Find the next package to deliver
        next_delivery, delivery_distance = find_next_package(truck, packages_in_transit, priority_packages,
                                                             LARGE_INITIAL_DISTANCE)

        if next_delivery:
            # Update truck's status after delivery
            update_truck_and_package_status(truck, next_delivery, delivery_distance)

            # Remove the package from the list of packages in transit
            packages_in_transit.remove(next_delivery)


def find_next_package(truck, packages_in_transit, priority_packages, max_distance):
    # Find the next package to deliver, prioritizing urgent ones and then selecting the nearest.
    # First, try to find the nearest priority package
    for package in packages_in_transit:
        if package.ID in priority_packages:
            distance = calculate_distance(find_address_id(truck.current_location), find_address_id(package.address))
            return package, distance

    # If no priority package found, find the nearest package
    shortest_distance = max_distance
    nearest_package = None
    for package in packages_in_transit:
        distance = calculate_distance(find_address_id(truck.current_location), find_address_id(package.address))
        if distance < shortest_distance:
            shortest_distance = distance
            nearest_package = package

    return nearest_package, shortest_distance


def update_truck_and_package_status(truck, package, distance):
    # Update truck's mileage, location, and time after delivering a package.
    # Update truck's mileage and location
    truck.mileage += distance
    truck.current_location = package.address

    # Update truck's time based on distance traveled (using truck's speed)
    truck.time += datetime.timedelta(hours=distance / truck.speed)

    # Set package's delivery and departure time
    package.deliveryTime = truck.time
    package.departureTime = truck.depart_time


# Example usage: Deliver packages for multiple trucks
deliverTruckPackages(truck1)
deliverTruckPackages(truck3)

# Truck 2 does not leave until either truck1 or truck3 are finished
truck2.depart_time = min(truck1.time, truck3.time)
deliverTruckPackages(truck2)



# Display the program title and calculate total mileage
print()
print("Welcome to Western Governors University Parcel Service")
total_miles = sum(truck.mileage for truck in [truck1, truck2, truck3])
print(f"The total mileage traveled on this route was {total_miles} miles.")


# Function to update and print package status based on the given time
def update_and_print_status(packageID, userTime):
    package = packageMap.search(packageID)
    if package:
        package.updateStatus(userTime)
        print(str(package))
    else:
        print(f"No package found with ID {packageID}.")


def display_package_status_by_truck(userTime):
    print(f"\nPackage status at {userTime}:")
    user_time = datetime.timedelta(hours=userTime.hour, minutes=userTime.minute)

    # Iterate over the trucks using the original package assignments
    for truck_name, package_ids in original_truck_packages.items():
        print(f"\n{truck_name}:\n")

        for package_id in package_ids:
            package = packageMap.search(package_id)
            if package:
                package.updateStatus(user_time)
                print(str(package))


# Main loop for user interaction
while True:
    print()
    # Display options for package status
    print("1. View the status of a single package at a specific time.")
    print("2. View the status of all packages at a specific time.")
    print("3. Exit.")
    print()
    user_option = input("Choose an option: ")
    print()

    # Option 1: View a specific package's status
    if user_option == "1":
        try:
            userTime = input("Enter a time to check package status. Format is HH:MM 24-Hour: ")
            (h, m) = userTime.split(":")
            userTime = datetime.timedelta(hours=int(h), minutes=int(m))

            packageID = int(input("Enter Package ID: "))
            if packageID <= 0 or packageID > 40:
                print("Invalid Package ID.")
                continue
            update_and_print_status(packageID, userTime)
        except (ValueError, IndexError):
            print("Invalid input. Please check the time or package ID format.")
            continue

    # Option 2: View the status of all packages at a specific time for all trucks
    elif user_option == "2":
        try:
            userTime = input("Enter a time to check package status. Format is HH:MM 24-Hour: ")
            (h, m) = userTime.split(":")
            userTime = datetime.time(hour=int(h), minute=int(m))
            display_package_status_by_truck(userTime)
        except (ValueError, IndexError):
            print("Invalid time format. Please use HH:MM.")
            continue

    # Option 3: Exit the program
    elif user_option == "3":
        print("Exiting the program.")
        break

    # Invalid option input
    else:
        print("Invalid input. Choose 1, 2, or 3.")
