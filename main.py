#NAME: CHARLES BRIXEY
#STUDENT ID: 004546211

import csv
import classes
import helper
import terminal

allAddresses = classes.Addresses()

# ***************************** add unique WGU Address for Hub **************************************

WGUAddress = classes.Address('4001 South 700 East')
WGUAddress.neighbors = [0]
allAddresses.add(WGUAddress)

# ***************************** add unique addresses **************************************

with open('WGUPS Distance Table.csv') as csvfile:
   distanceCSV = csv.reader(csvfile, delimiter=',')

   currentRow = 0
   for row in distanceCSV:
      currentRow += 1
      if(row[1] and row[1] != " HUB" and row[1] != "WGUPS Distance Table"):
          address = "".join(row[1]).split()
          address = " ".join(address[0:len(address)-1])

          if(address == "5383 S 900 East #104"): 
                address = "5383 South 900 East #104" # Adjust naming to be correct
          
          if(allAddresses.hasAddress(address) == False):
             newAddress = classes.Address(address)
             allAddresses.storage.append(newAddress)

# ***************************** parse number of packages ********************************
numPackages = 0
with open('WGUPS Package File.csv') as csvfile:
   packageCSV = csv.reader(csvfile, delimiter=',')
   currentRow = 0

   for row in packageCSV:
      currentRow += 1
      if(currentRow >= 9):
         numPackages = int(row[0])

hashMap = classes.HashMap(numPackages)

# ***************************** add packages ********************************

with open('WGUPS Package File.csv') as csvfile:
   packageCSV = csv.reader(csvfile, delimiter=',')
   currentRow = 0

   for row in packageCSV:
      currentRow += 1
      if(currentRow >= 9):
          
         id = int(row[0])
         destinationAddress = row[1]
         city = row[2]
         state = row[3]
         zip = int(row[4])
         deadline = row[5]
         weight = int(row[6])
         notes = row[7]

         hashMap.add(id,destinationAddress, city, state,zip, deadline, weight, notes)

# ***************************** add neighbor distances to each address ********************************

with open('WGUPS Distance Table.csv') as csvfile:
   distanceCSV = csv.reader(csvfile, delimiter=',')
   currentRow = 0
   distIdx = 1
   for row in distanceCSV:
      currentRow += 1
      if(currentRow >= 10):
         block = " ".join(row)
         idx = None
         
         for i in range(len(block)):
            if(block[i] == ")"):
               idx = i + 1
         
         block = block[idx:].split()

         # convert distances to floats
         for j in range(len(block)):
            block[j] = float(block[j])

         # assign each address its neighbor distances
         allAddresses.storage[distIdx].neighbors = block
         if(distIdx < len(allAddresses.storage)-1):
            distIdx += 1

# ***************************** add trucks and drivers ********************************

truck1 = classes.Truck(1, allAddresses, hashMap)
truck2 = classes.Truck(2, allAddresses, hashMap)
truck3 = classes.Truck(3, allAddresses, hashMap)

truck1.addDriver("John Lennon")
truck2.addDriver("Kurt Cobain")

truck1.importTrucks(truck1,truck2,truck3)
truck2.importTrucks(truck1,truck2,truck3)
truck3.importTrucks(truck1,truck2,truck3)

hashMap.importTrucks(truck1, truck2, truck3)

# ***************************** load packages on Trucks ********************************

packagesAssignedToTruck1 = [1,4,8,29,30,31,33,37]
packagesAssignedToTruck2 = [3,13,14,15,16,18,19,20,21,22,24,34,35,36,38,40]
packagesAssignedToTruck3 = [2,5,6,7,9,10,11,12,17,23,26,27,28,32,39]

for package in hashMap.map:
   package.packagesAssignedToTruck1 = packagesAssignedToTruck1
   package.packagesAssignedToTruck2 = packagesAssignedToTruck2
   package.packagesAssignedToTruck3 = packagesAssignedToTruck3

# Truck 1 has 8 Packages:
truck1.add(hashMap.map[1-1])
truck1.add(hashMap.map[4-1])
truck1.add(hashMap.map[8-1])
truck1.add(hashMap.map[29-1])
truck1.add(hashMap.map[30-1])
truck1.add(hashMap.map[31-1])
truck1.add(hashMap.map[33-1])
truck1.add(hashMap.map[37-1])

# Truck 2 has 16 Packages:
truck2.add(hashMap.map[3-1])
truck2.add(hashMap.map[13-1])
truck2.add(hashMap.map[14-1])
truck2.add(hashMap.map[15-1])
truck2.add(hashMap.map[16-1])
truck2.add(hashMap.map[18-1])
truck2.add(hashMap.map[19-1])
truck2.add(hashMap.map[20-1])
truck2.add(hashMap.map[21-1])
truck2.add(hashMap.map[22-1])
truck2.add(hashMap.map[24-1])
truck2.add(hashMap.map[34-1])
truck2.add(hashMap.map[35-1])
truck2.add(hashMap.map[36-1])
truck2.add(hashMap.map[38-1])
truck2.add(hashMap.map[40-1])

# Truck 3 has 16 Packages: 
truck3.add(hashMap.map[2-1])
truck3.add(hashMap.map[5-1])
truck3.add(hashMap.map[6-1])
truck3.add(hashMap.map[7-1])
truck3.add(hashMap.map[9-1])
truck3.add(hashMap.map[10-1])
truck3.add(hashMap.map[11-1])
truck3.add(hashMap.map[12-1])
truck3.add(hashMap.map[17-1])
truck3.add(hashMap.map[23-1])
truck3.add(hashMap.map[25-1])
truck3.add(hashMap.map[26-1])
truck3.add(hashMap.map[27-1])
truck3.add(hashMap.map[28-1])
truck3.add(hashMap.map[32-1])
truck3.add(hashMap.map[39-1])

# stategy: truck 1 has fewer packages so it can return to the hub first

# ***************************** deliver packages ********************************

truck1.deliverPackages()
truck2.deliverPackages()

# ***************************** calculate total miles ********************************

totalMiles = helper.sum(truck1,truck2,truck3)

# ***************************** Get input from user ********************************

terminal.beginPrompt(hashMap, truck1, truck2, truck3);
