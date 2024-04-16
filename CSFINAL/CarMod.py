import math
import matplotlib.pyplot as plot

class car(): 
	def __init__(self, CarFolder): 
		#These are self variables that are used throughout the program
		self.Make = ''
		self.Model = ''
		self.Year = 0
		self.Price = 0.0
		self.Mass = 0
		self.Wheels = []
		self.TQ = []
		self.G = []
		self.I = []
		self.Gearing = []
		self.FinalGearing = []
		self.FinalSpeeds = []
		self.Wheels = []
		self.SpeedRating = ""
		self.Accelerationgraph = []


		#Reading from the files, saving to self
		with open(CarFolder + '/CarInfo', 'r') as Info: 
			text = Info.read()
			self.I = text.split()
			print("Make: " + self.I[0])
			print("Model: " + self.I[1])
			print("Year: " + self.I[2])
			print("Price: $" + self.I[3])
			print("Mass: " + self.I[4] + " kg")
			print("Wheel Diameter: " + self.I[5] + " cm")
			print("Max traction : " + self.I[6] + " g's" + '\n')


		with open(CarFolder + '/Torque', 'r') as Torque:
			print("     RPM : Torque")
			text = Torque.read().split()
			for value in text:
				temp = value.split(',')
				self.TQ.append([int(temp[0]), int(temp[1])])
				print(temp[0]+ " RPM : " + temp[1] + " Nm")
			print()

		#Printing out the transmission gearing
		with open(CarFolder + '/Gearing', 'r') as Gearing:
			self.G = Gearing.read().split()
			print("Transmission Gearing")
			count = 0
			while(count < len(self.G) - 1):
				print(count + 1, ':', self.G[count])
				count += 1
			print("Differential Ratio: " + self.G[-1] + "\n")
		

		#Setting final gearing
		counter = 0
		print("Final Gearing:")
		while(counter < len(self.G)-1):
			calculation = float(self.G[counter]) * float(self.G[-1])
			self.FinalGearing.append(calculation)
			print(counter + 1, ":", calculation)
			counter += 1
		print()


		#Reading self.I and saving values appropriately
		self.Make = self.I[0]
		self.Model = self.I[1]
		self.Year = int(self.I[2])
		self.Price = int(self.I[3])
		self.Mass = int(self.I[4])
		self.Wheels = [int(self.I[5]),float(self.I[6])]
		

		#Calculating top speed in each gear
		print("Final Speeds Per Gear")
		itr = 1
		for gearratio in self.FinalGearing:
			calculation = int(self.TQ[-1][0] / gearratio * self.Wheels[0] * 3.141 * 60/100000)
			self.FinalSpeeds.append(calculation)
			print(itr, ":", calculation, "kph")
			itr +=1

		#Setting the SpeedRating
		if(self.FinalSpeeds[-1] >= 350):
			self.SpeedRating = "Hypercar"
		elif(self.FinalSpeeds[-1] >= 225 and self.FinalSpeeds[-1] < 350):
			self.SpeedRating = "Supercar"
		elif(self.FinalSpeeds[-1] >= 160 and self.FinalSpeeds[-1] < 225):
			self.SpeedRating = "Sports car"
		else:
			self.SpeedRating = "Daily car"
		print(self.SpeedRating, '\n')


		#Calculating the acceleration curve
		counter = 1
		print("Acceleration Curve")
		for gear in self.FinalGearing:
			print("Gear", counter)
			for tq in self.TQ: 
				calculation = [counter, int(tq[0]), round(10 * (int(tq[1])*gear)/(self.Mass * self.Wheels[0]/2), 2)]
				self.Accelerationgraph.append(calculation)
				print(calculation)
			counter += 1 
			print()

	def corneringefficiency(self, radius): #I don't think this works quite right
		print(f"Speed needed to achieve {self.Wheels[1]} g's in a {radius} meter radius turn:")
		print(round(math.sqrt(self.Wheels[1] * radius * 9.8), 2), 'kph', '\n')
		if(self.Wheels[1] <= 0.8):
			print("This car cannot go around turns very fast.", '\n')
		elif((self.Wheels[1] <= 1) and (self.Wheels[1] > 0.8)):
			print("This car can handle decently well!", '\n')
		else:
			print("This car can handle exceptionally well and is very controllable!", '\n')


#Actual program:
Car1 = car("Koenigsegg")
Car1.corneringefficiency(50)


# Graphing each gear differently
listx = []
listy = []
for ind in Car1.G:
	listx.append([])
	listy.append([])

gear = 0
for i in Car1.Accelerationgraph:
	if(i[0] == gear + 1):
		gear += 1 
		listx[gear].append(i[1])
		listy[gear].append(i[2])
		plot.plot(listx[gear],listy[gear], marker = '*', linestyle = '-') 
	elif(i[0] == gear):
		listx[gear].append(i[1])
		listy[gear].append(i[2])
		plot.plot(listx[gear],listy[gear], marker = '*', linestyle = '-') 



# Add labels and title
plot.xlabel('RPM')
plot.ylabel("Acceleration (g's)")
plot.title('Acceleration/RPM Per Gear')

# Show grid
plot.grid(True)

# Show the plot
plot.show()



