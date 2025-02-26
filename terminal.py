import helper

def beginPrompt (hashMap, truck1, truck2, truck3):
  
  while(True):
   val = input("\nSelect your next action (press 'q' to quit)\n1. Look up package by ID \n2. Look up package by ID and filter by time \n3. View status of all packages by time range \n4. Calculate total truck mileage after delivering all packages ")

   if(val == '1'):
      id = input("What is the ID of the package? ")

      print(hashMap.lookUp(int(id)))

      if(id == 'q'):
         break

   if(val == '2'):
      id = input("What is the ID of the package? ")

      if(id == 'q'):
         break

      timestamp = input("Please enter the time (example: 8:00 AM or 5:00 PM) ")
      hashMap.get(int(id)).printPackageByTime(timestamp, truck1, truck2, truck3)

   if(val == '3'):
      start = input("What is the start time? (example: 8:00 AM or 5:00 PM) ")

      if(start =='q'):
         break
      
      end = input("What is the end time? (example: 8:00 AM or 5:00 PM) ")

      if(end == 'q'):
         break

      hashMap.printAllPackagesStatusByTimeRange(start,end, truck1, truck2, truck3)

   if(val == '4'):
       miles1 = truck1.getMileageByTime("11:59 PM")
       miles2 = truck2.getMileageByTime("11:59 PM")
       miles3 = truck3.getMileageByTime("11:59 PM")

       total = miles1 + miles2 + miles3
       print("\n-----------------------------------------------------------------------------------------")
       print("TRUCK 3 DELIVERED PACKAGE", str(truck3.lastPackageDelivered.id) + "(THE LAST PACKAGE) AT", helper.convertSecondsToTime(truck3.seconds))

       print("\nTRUCK 1 MILES:","{:.1f}".format(miles1))
       print("TRUCK 2 MILES:","{:.1f}".format(miles2))
       print("TRUCK 3 MILES:","{:.1f}".format(miles3))
         
       print("\nTOTAL MILES OF ALL TRUCKS:","{:.1f}".format(total))
       print("-----------------------------------------------------------------------------------------")

   if(val == 'q'):
      break

