import helper

class HashMap:
    def __init__ (self,size):
       self.size = size
       self.map = [None] * self.size
       self.trucks = []

    def add (self,id,destinationAddress, city, state,zip, deadline, weight, notes): # add new packages to the hashmap
       package = Package(id,destinationAddress, city, state,zip, deadline, weight, notes)
       self.map[package.id-1] = package

    def importTrucks (self, truck1, truck2, truck3): # method to give hashMap access to all trucks
       self.trucks.append(truck1)
       self.trucks.append(truck2)
       self.trucks.append(truck3)

    def delete (self, id):
      self.storage[id-1] = None

    def get (self,id):
       return self.map[id-1]
    
    def lookUp (self,id):

      package = self.get(id)
      miles = self.trucks[0].milesTravelled + self.trucks[1].milesTravelled + self.trucks[2].milesTravelled

      if(package.id == 6 or package.id == 25 or package.id == 28 or package.id == 32): #modify default timestamp of late arrivals for 9:05 AM
         package.timestamp[0][1] = helper.convertTimeStampToSeconds("9:05 AM")


      if(package.id == 9): # handle address change of package 9
         package.destinationAddress = "410 S State St"
         package.zip = 84111


      print("\n-----------------------------------------------------------------------------------------")
      print("PACKAGE DETAILS ->")
      print("ID:", package.id)
      print("DELIVERY ADDRESS:", package.destinationAddress)
      print("DELIVERY DEADLINE:", package.deadline)
      print("DELIVERY CITY:",package.city)
      print("DELIVERY ZIP CODE:", package.zip)
      print("PACKAGE WEIGHT:", package.weight, "KILOS")
      print("DELIVERY STATUS:", package.status + "(" + helper.convertSecondsToTime(package.seconds) + ")")
      print("TOTAL MILEAGE OF ALL TRUCKS:",miles)
      print("\nPACKAGE TIMESTAMPS ->")

      target = "10:20 AM" # time when package 9 dest change takes place
      targetSeconds = helper.convertTimeStampToSeconds(target)

      if(package.id == 9):
         for item in package.timestamp:
            status = item[0]
            time = helper.convertSecondsToTime(item[1])
            curr = item[2]
            dest = item[3]
            if(package.id == 9 and item[1] <= targetSeconds): # Handle package 9 destination change
                item[3] = "300 State St"
            else:
                item[3] = "410 S State St"
            print(time,"| STATUS:",status,"| CURRENT:",curr,"| DESTINATION:",item[3])
      else:
         for item in package.timestamp:
            time = helper.convertSecondsToTime(item[1])
            status = item[0]
            curr = item[2]
            dest = item[3]
            print(time,"| STATUS:",status,"| CURRENT:",curr,"| DESTINATION:",dest)
      
      return ("-----------------------------------------------------------------------------------------")
    
    def printAllPackagesStatusByTimeRange (self, start, end, truck1, truck2, truck3):
       print("\n-----------------------------------------------------------------------------------------")
       print("PACKAGE STATUSES FROM", start,"to",end,"->")
       for package in self.map:
          print(package.getPackageStatusByTimeRange(start,end)[0], package.getPackageStatusByTimeRange(start,end)[1])

       miles1 = truck1.getMileageByTime(end)
       miles2 = truck2.getMileageByTime(end)
       miles3 = truck3.getMileageByTime(end)

       total = miles1 + miles2 + miles3

       print("\nTRUCK 1 MILES BY",end + ":","{:.1f}".format(miles1))
       print("TRUCK 2 MILES BY",end + ":","{:.1f}".format(miles2))
       print("TRUCK 3 MILES BY",end + ":","{:.1f}".format(miles3))
         
       print("\nTOTAL MILES OF ALL TRUCKS BY", end + ":","{:.1f}".format(total))
       print("-----------------------------------------------------------------------------------------")

    def print(self):
       for package in self.storage:
          print(package.id, package.timestamp)

class Truck:
   def __init__ (self, number, addresses, hashmap):
      self.number = number
      self.addresses = addresses
      self.driver = None
      self.milesTravelled = 0
      self.packages = []
      self.currentAddress = '4001 South 700 East'
      self.seconds = 28800 # 8hrs * 60 minutes * 60 seconds
      self.timestamp = []
      self.trucks = []
      self.hashmap = hashmap
      self.lastPackageDelivered = None

   def incrementPackagesSeconds (self, seconds): # increment package seconds on each package timestamp
      for package in self.packages:
         if(package.status != "DELIVERED"):
            package.seconds += seconds

   def updatePackagesAddress (self, address): # update address of packages when truck moves to new location
      for package in self.packages:
            package.setCurrentAddress(address)

   def addDriver (self,name):
      self.driver = name

   def removeDriver (self):
      self.driver = None

   def returnToHub (self): # first truck back must return to hub and increment miles/seconds
      mileageToAdd = self.determineCost(self.currentAddress, '4001 South 700 East')
      self.incrementMilesTravelledByTruck(mileageToAdd)
      seconds = helper.convertDistanceToSeconds(mileageToAdd)
      self.incrementTruckSeconds(seconds)
      self.updateTruckAddress('4001 South 700 East')
      self.createTruckTimeStamp()

   def getMileageByTime(self,input): # get mileage by time so trucks have an accurate time
      last = 0
      target = helper.convertTimeStampToSeconds(input)
      for timestamp in self.timestamp:
         currSeconds = timestamp[1]
         mileage = timestamp[2]
         if(currSeconds <= target):
            last = mileage

      return last

   def importTrucks (self, x, y, z): # method to allow trucks to have access to each other
      self.trucks.append(x)
      self.trucks.append(y)
      self.trucks.append(z)

      for i in range(0,len(self.trucks)):
         for j in range(0,len(self.trucks[i].timestamp)):
            print(self.trucks[i].timestamp[j])

   def createTruckTimeStamp(self): # create timestamp in an array to track truck number, seconds, and miles travelled
      myStamp = [self.number,self.seconds,self.milesTravelled]
      hasStamp = False

      for item in self.timestamp:
         if(item == myStamp): # prevent duplicate truck timestamps from being made
            hasStamp = True

      if(hasStamp == False):
         self.timestamp.append(myStamp)

   def setPackagesSeconds (self, seconds): # used to update truck 3's packages seconds
      for package in self.packages:
         if(package.status != "DELIVERED"):
            package.seconds = seconds

   def incrementTruckSeconds (self,seconds): # update truck seconds attribute when truck changes locations
      self.seconds += seconds

   def updatePackagesTimeStamps (self): #update all packages time stamps
      for package in self.packages:
         package.createPackageTimeStamp()

   def determineNextDestination (self, packages):

      currentAddress = self.currentAddress
      lowestCost = 100000
      nextDestination = packages[0].destinationAddress

      for package in packages:
         destination = package.destinationAddress
         cost = self.determineCost(currentAddress,destination)
         
         if(cost < lowestCost and package.status != "DELIVERED"):
            lowestCost = cost
            nextDestination = package.destinationAddress

      return nextDestination
   
   def deliverPackages (self):

      while(len(self.packages) and self.driver != None): # trucks without drivers cannot deliver packages
          destinationAddress = self.determineNextDestination(self.packages)
            
          mileageToAdd = self.determineCost(self.currentAddress,destinationAddress)

          # update miles, seconds, destination, and timestamps of truck and packages
          self.handleUpdates(mileageToAdd, destinationAddress)
    
          # Remove package once delievered
          self.removePackagesFromTruck()

          if(len(self.packages) == 0 and self.number == 1):
            self.handleLastTruckRide()

   def updateTruckAddress (self, address):
      self.currentAddress = address

   def handleLastTruckRide (self): # method to handle truck 3
      self.returnToHub()
      truck3 = self.trucks[2]
      truck3.seconds = self.seconds #update final trucks seconds
      truck3.createTruckTimeStamp()
      truck3.addDriver(self.driver) # add driver to truck3
      self.removeDriver() # remove truck1 driver
      truck3.setPackagesSeconds(self.seconds)
      truck3.updatePackagesTimeStamps()
      truck3.deliverPackages()
      
      
   def handleUpdates (self,mileageToAdd,destinationAddress):

      seconds = helper.convertDistanceToSeconds(mileageToAdd)

      #increment miles travelled by Truck
      self.incrementMilesTravelledByTruck(mileageToAdd)

      #update time in seconds of Truck and Packages
      self.incrementPackagesSeconds(seconds)
      self.incrementTruckSeconds(seconds)

      #update new destination of packages and truck
      self.updatePackagesAddress(destinationAddress)
      self.updateTruckAddress(destinationAddress)

      #create timestamps for truck and packages
      self.createTruckTimeStamp()
      self.updatePackagesTimeStamps()

   def removePackagesFromTruck (self): # find the index of the delivered packages and remove
      i = 0

      while(i < len(self.packages)):
         if(self.packages[i].currentAddress == self.packages[i].destinationAddress):
            self.lastPackageDelivered = self.packages[i]
            self.packages.pop(i)
            i = 0  
         i+= 1

   def incrementMilesTravelledByTruck (self, miles): # increment miles of each truck when reaching a new location
      self.milesTravelled += miles

   def add (self, package):
      self.packages.append(package)

   def determineCost (self, oldAddress, newAddress): # determine the mileage cost between two locations

      addressOld = self.addresses.get(oldAddress)
      addressNew = self.addresses.get(newAddress)
      idx = 0
      mileageToAdd = 0

      if(len(addressOld.neighbors) > len(addressNew.neighbors)):
         idx = self.addresses.getAddressIndex(addressNew.address)
         mileageToAdd = addressOld.neighbors[idx]
      else:
         idx = self.addresses.getAddressIndex(addressOld.address)
         mileageToAdd = addressNew.neighbors[idx]

      return mileageToAdd

class Addresses:
   def __init__(self):
      self.storage = []

   def add (self,address):
      self.storage.append(address)

   def get (self,address):
      for item in self.storage:
         if(address == item.address):
            return item
   
   def getAddressIndex (self,address):
      for i in range(len(self.storage)):
         if(self.storage[i].address == address):
            return i
         
   def hasAddress (self, address):
      for item in self.storage:
         if(item == address):
            return True
      return False
              
   def printNames (self):
      for item in self.storage:
         print(item.address)

   def printNeighbors (self):
      for item in self.storage:
         print(item.neighbors)

class Address:
   def __init__ (self, address):
      self.address = address
      self.neighbors = []

class Package:
    def __init__(self, id, destinationAddress, city, state, zip, deadline, weight, notes):
      self.id = id
      self.destinationAddress = destinationAddress
      self.city = city
      self.state = state
      self.zip = zip
      self.deadline = deadline
      self.weight = weight
      self.notes = notes
      self.currentAddress =  '6351 South 900 East'
      self.status = "AT THE HUB"
      self.seconds = 28800 # 8hrs * 60 minutes * 60 seconds
      self.timestamp = [["AT THE HUB", 28800, '6351 South 900 East', self.destinationAddress]]
      self.packagesAssignedToTruck1 = []
      self.packagesAssignedToTruck2 = []
      self.packagesAssignedToTruck3 = []
   
    def getTruckNumberOfPackage(self):
       truck1 = self.packagesAssignedToTruck1
       truck2 = self.packagesAssignedToTruck2
       truck3 = self.packagesAssignedToTruck3

       if(self.id in truck1):
          return "TRUCK 1"
       if(self.id in truck2):
          return "TRUCK 2"
       if(self.id in truck3):
          return "TRUCK 3"

    def getDeliveryStatusByTime (self,time):
       target = helper.convertTimeStampToSeconds(time)
       lastStatus = None
       deliveryTime = None

       if(self.id == 6 or self.id == 25 or self.id == 28 or self.id == 32):
          self.timestamp[0][1] = 32700

       if(len(self.timestamp) > 0):
         for item in self.timestamp:
            if(item[1] <= target):
             lastStatus = item[0]
             deliveryTime = helper.convertSecondsToTime(item[1])
       
       if(lastStatus == None):
          return "HASN'T BEEN LOADED ONTO TRUCK"
       elif(lastStatus == "DELIVERED"):
          return lastStatus + "(" + deliveryTime + ")"
       elif (lastStatus == "EN ROUTE"):
          truck = self.getTruckNumberOfPackage()
          return lastStatus + "("+ str(truck) + ")"
          


    def printPackageByTime(self, time, truck1, truck2, truck3):

      if(self.id == 9): # Handle package 9 destination change
         self.destinationAddress = "410 S State St"
         self.city = "Salt Lake City"
         self.state = "UT"
         self.zip = 84111

      target = helper.convertTimeStampToSeconds(time)
      isDelivered = False

      miles1 = truck1.getMileageByTime(time)
      miles2 = truck2.getMileageByTime(time)
      miles3 = truck3.getMileageByTime(time)

      total = miles1 + miles2 + miles3

      lastStatus = None
      lastTime = None

      historyOfPackage = []

      if(self.id == 6 or self.id == 25 or self.id == 28 or self.id == 32): #modify default timestamp of late arrivals for 9:05 AM
         self.timestamp[0][1] = helper.convertTimeStampToSeconds("9:05 AM")

      for timestamp in self.timestamp:
         if(timestamp[1] <= target):
            lastStatus = timestamp[0]
            lastTime = helper.convertSecondsToTime(timestamp[1])

      print("\n-----------------------------------------------------------------------------------------")
      print("PACKAGE DETAILS ->")
      print("ID:", self.id)
      print("DELIVERY ADDRESS:", self.destinationAddress)
      print("DELIVERY DEADLINE:", self.deadline)
      print("DELIVERY CITY:",self.city)
      print("DELIVERY ZIP CODE:", self.zip)
      print("PACKAGE WEIGHT:", self.weight, "KILOS")
      if(lastStatus != None):
         print("DELIVERY STATUS:", lastStatus +"(" + lastTime + ")")
      else:
         print("DELIVERY STATUS:", "HASN'T BEEN LOADED ONTO TRUCK")
      print("TOTAL MILEAGE OF ALL TRUCKS AT", time + ":",  "{0:.1f}".format(total), "MILES")
      print("\nPACKAGE TIMESTAMPS ->")

      for timestamp in self.timestamp:
         if(timestamp[1] <= target and isDelivered == False):
            historyOfPackage.append([timestamp[1], timestamp[0], timestamp[2], timestamp[3]])
            if(timestamp[0] == "DELIVERED"):
               isDelivered = True

      target = "10:20 AM" # time when package 9 dest change takes place
      targetSeconds = helper.convertTimeStampToSeconds(target)

      for item in historyOfPackage:
         if(self.id == 9 and item[0] <= targetSeconds): # Handle package 9 destination change
            item[3] = "300 State St"
         else:
            item[3] = "410 S State St"
         time = helper.convertSecondsToTime(item[0])
         status = item[1]
         if(item[1] == "DELIVERED" and self.id == 9): # Handle package 9 change
            item[2] = "410 S State St"
         print(time,"| STATUS:",status,"| CURRENT:",item[2],"| DESTINATION:",item[3])
      print("-----------------------------------------------------------------------------------------")

    def getPackageStatusByTimeRange(self, start, end):
       
       if(self.id == 6 or self.id == 25 or self.id == 28 or self.id == 32): #modify late arrivals timestamp
           self.timestamp[0][1] = 32700
       
       lastStatus = self.getDeliveryStatusByTime(end)
       if(lastStatus == None):
          lastStatus = "AT THE HUB"

       return ["PACKAGE "+str(self.id) + ":", lastStatus]

    def setCurrentAddress (self, address): # change the package current address when a package reaches a new location
      oldAddress = self.currentAddress
      newAddress = address

      if(oldAddress == self.destinationAddress or newAddress == self.destinationAddress):
         self.status = "DELIVERED"
      elif (self.status != "DELIVERED"):
         self.status = "EN ROUTE"

      self.currentAddress = newAddress

    def createPackageTimeStamp (self): # timestamp is an array that stores status, seconds, curr, dest for each package
      newTimeStamp = [self.status, self.seconds, self.currentAddress, self.destinationAddress]
      duplicate = False

      for timestamp in self.timestamp:
         if(timestamp[1] == newTimeStamp[1]):
            duplicate = True

      if(duplicate == False):
         self.timestamp.append(newTimeStamp)