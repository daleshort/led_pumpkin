
import csv
from collections import OrderedDict as dict
from neopixel import *
from strandtest import wheel
import time
import math
import random

class strand(object):

	def __init__(self, numPixels):
		self.ledData = [0]*numPixels
	
	def resetTime(self, startTime, timeShift):
		self.startTime = startTime
		self.timeShift = timeShift
		return 0 
	
	def begin(self, file, startTime, timeShift):
		
		self.startTime = startTime
		self.timeShift = timeShift
		
		#Load CSV
		
		csv.dict = dict
		csv.register_dialect("No whitespace", skipinitialspace=True)
		with open(file, "r") as fp:
		# create a reader and pass in the dialect we created
			csvreader = csv.DictReader(fp, dialect="No whitespace")

		# add each entry to a list as an ordereddict
			self.data = [row for row in csvreader]
		
		# long version if you don"t like list comprehension
		# data = list()
		# for row in csvreader:
		#    data.append(row)
			
		print("### This is the final data structure ###")
		print(self.data)
		print("\n")

		# accessing the contents 
		print("Access data by index")
		print("data[index in list][field]")
		#time,visual,color_r,color_g,color_b,param1,param2,param3,param4,param5,param6,param7,param8,param9,param10

		for entry in range(len(self.data)):
			self.data[entry]["paramList"] = [self.data[entry]["param1"],self.data[entry]["param2"],self.data[entry]["param3"],self.data[entry]["param4"],
			self.data[entry]["param5"],self.data[entry]["param6"],self.data[entry]["param7"],self.data[entry]["param8"],self.data[entry]["param9"],self.data[entry]["param10"]]
			
			#I think the color order may be messed up?
			self.data[entry]["color"] = Color(int(self.data[entry]["color_r"]),int(self.data[entry]["color_g"]),int(self.data[entry]["color_b"]))
			
			
			print("time:", self.data[entry]["time"])
			print("visual", self.data[entry]["visual"])
			print("color_r", self.data[entry]["color_r"])
			print("color_g:", self.data[entry]["color_g"])
			print("color_b:", self.data[entry]["color_b"])
			print("param1:", self.data[entry]["param1"])
			print("param2:", self.data[entry]["param2"])
			print("param3:", self.data[entry]["param3"])
			print("param4:", self.data[entry]["param4"])
			print("param5:", self.data[entry]["param5"])
			print("param6:", self.data[entry]["param6"])
			print("param7:", self.data[entry]["param7"])
			print("param8:", self.data[entry]["param8"])
			print("param9:", self.data[entry]["param9"])
			print("param10:", self.data[entry]["param10"])
			print("paramlist", self.data[entry]["paramList"])
			print("color", self.data[entry]["color"])
			print("\n")
			print("length of data")
			print(len(self.data))
			
		self.randData = [0]*self.numPixels()
		for entry in range(self.numPixels()):
			self.randData[entry] = random.random()

	def playTime(self):

		#returns seconds into the track current time is
		#print("playtime:",time.time() - self.startTime + self.timeShift)
		return time.time() - self.startTime + self.timeShift
	
	def update(self):
		dataPicked = self.playData()
		
		if dataPicked["visual"] == "oneColor": 
			self.oneColor(dataPicked["color"])
		elif dataPicked["visual"] == "fadeUp":
			self.fadeUp(dataPicked["paramList"])
		elif dataPicked["visual"] == "fadeFromToNext":
			self.fadeFromToNext(dataPicked["paramList"])
		elif dataPicked["visual"] == "beatFade":
			self.beatFade(dataPicked["paramList"])
		elif dataPicked["visual"] == "lengthUp":
			self.lengthUp(dataPicked["paramList"])
		elif dataPicked["visual"] == "lengthBeat":
			self.lengthBeat(dataPicked["paramList"])
		elif dataPicked["visual"] == "theaterChase":
			self.theaterChase(dataPicked["paramList"])
		elif dataPicked["visual"] == "cyclo":
			self.cyclo(dataPicked["paramList"])
		elif dataPicked["visual"] == "morphRainbow":
			self.morphRainbow(dataPicked["paramList"])
		elif dataPicked["visual"] == "twinkle":
			self.twinkle(dataPicked["paramList"])
		else:
			print('no match')

	
			
	def playData(self):
		i=0
		dataPicked = self.data[0]
		while (i < (len(self.data))):
			
			if(float(self.data[i]["time"]) < self.playTime()):
				dataPicked = self.data[i]
			i = i+1
		return dataPicked
		
	def playDataNext(self):
		i=0
		dataPicked = self.data[i]
		nextData = self.data[i+1]
		while (i < (len(self.data))):
			
			if(float(self.data[i]["time"]) < self.playTime()):
				dataPicked = self.data[i]
				if i+1 < len(self.data):
					nextData = self.data[i+1]
			i = i+1
		return nextData
	
	def test(self):
		print('testing of strand')
	
	def numPixels(self):
		return len(self.ledData)
	
	def pctIntoVis(self):
		y = float(self.playDataNext()["time"]) - float(self.playData()["time"])
		x = self.playTime() - float(self.playData()["time"])
		if y ==0:
			pct = 1
		else:
			pct = x/y
		
		#print("x:", x)
		
		#print("y:", y)
		
		return pct
		
	def pctIntoBeat(self,beat):
		beat = float(beat)
		
		if beat <= 0:
			beat =1
			
		beatsPlusFrac = (self.playTime() - float(self.playData()["time"]))/beat
		beatsNoFrac = math.floor((self.playTime() - float(self.playData()["time"]))/beat)
		
		return beatsPlusFrac -beatsNoFrac
	
	def pctIntoBeatWithRandShift(self,beat, rand):
		beat = float(beat)
		
		if beat <= 0:
			beat =1
			
		beatsPlusFrac = ((self.playTime() - (beat*rand)) - float(self.playData()["time"]))/beat
		beatsNoFrac = math.floor(((self.playTime() - (beat*rand)) - float(self.playData()["time"]))/beat)
		
		return beatsPlusFrac -beatsNoFrac
	
	def oneColor(self, color):
	#sets all leds to one color
		for pixel in range(self.numPixels()):
			self.ledData[pixel] = color
	
	def twinkle(self, params):
		
		playData = self.playData()
		red = int( playData["color_r"])
		green =int( playData["color_g"])
		blue = int(playData["color_b"])
		colorOn = Color(red,green,blue)
		
		
		baseRed = int(params[0])
		baseGreen = int(params[1])
		baseBlue = int(params[2])
		colorOff = Color(baseRed,baseGreen,baseBlue)
		
		beatMin = float(params[3])
		beatMax = float(params[4])
		percentTwinkle = float(params[5])

		for i in range(self.numPixels()):
			beatTime =  beatMin + ((beatMax-beatMin) * self.randData[i])
			beatPct =  self.pctIntoBeatWithRandShift(beatTime,self.randData[i])
			beatPct = self.beatPctSaw(beatPct)
			self.ledData[i] = self.fadeColorPct(red,green,blue,beatPct)
		
		
	def beatFade(self,params):
		
		#param 0 is beat, param2 if 1 gives a square wave fade
		playData = self.playData()
		red = int( playData["color_r"])
		green =int( playData["color_g"])
		blue = int(playData["color_b"])
		
		beat = float(params[0])
		
		beatPct = self.pctIntoBeat(beat)
		
		#1 is saw wave beat pct
		if float(params[1]) == 0:
			fadePct = beatPct
		else:
			fadePct = self.beatPctSaw(beatPct)
		
		color = self.fadeColorPct(red,green,blue,fadePct)

		self.oneColor(color)
		
		return 0
	def beatPctSaw(self,beatPct):
		if beatPct <.5:
			fadePct = 2*beatPct
		else:
			fadePct = 2-(2*beatPct)
		return fadePct
	
	def fadeColorPct(self,red,green,blue,pct):
		
		red = int(red*pct)
		blue = int( blue*pct)
		green = int(green*pct)
		color = Color(red,green,blue)		
		return color
	
	def fadeUp(self,params):
		playData = self.playData()
		red = int( playData["color_r"])
		green =int( playData["color_g"])
		blue = int(playData["color_b"])
		
		color = self.fadeColorPct(red,green,blue,self.pctIntoVis())

		self.oneColor(color)
		
		return 0
		
	def fadeFromToNext(self, params):
		playData = self.playData()
		playDataNext = self.playDataNext()
		
		red = int( playData["color_r"])
		green =int( playData["color_g"])
		blue = int(playData["color_b"])
		
		redNext = int( playDataNext["color_r"])
		greenNext =int( playDataNext["color_g"])
		blueNext = int(playDataNext["color_b"])
		
		pct = self.pctIntoVis()
		setRed = int( red + ((redNext - red) * pct))
		setGreen = int( green + ((greenNext - green) * pct))
		setBlue = int( blue + ((blueNext - blue) * pct))
		
		self.oneColor(Color(setRed,setGreen,setBlue))
		
		return 0
	
	def colorFromPlayData(self, playData):
		
		red = int( playData["color_r"])
		green =int( playData["color_g"])
		blue = int(playData["color_b"])
		
		return Color(red,green,blue)
	
	def lengthBeat(self,params):
		
		colorOn = self.colorFromPlayData(self.playData())
		
		if float(params[0]) >= 0:
			baseRed = int(params[0])
			baseGreen = int(params[1])
			baseBlue = int(params[2])
			colorOff = Color(baseRed,baseGreen,baseBlue)
		else:
			colorOff = -1
		
		
		#param 3 is start pct
		startPct = params[3]
		
		beat = float(params[5])
		
		beatPct = self.pctIntoBeat(beat)
		
		#param 4 is square wave (set to non 0 for square wave)
		if float(params[4]) == 0:
			cats = 0
		else:
			beatPct = self.beatPctSaw(beatPct)
		#print("beat pct: ", beatPct)
		
		self.lightPct(float(startPct),beatPct, colorOn, colorOff)
		
		return 0
	
	def lengthUp(self,params):
		
		colorOn = self.colorFromPlayData(self.playData())
		
		#if baseRed is negative leave the existing color alone
		if float(params[0]) >= 0:
		
			#params[0] to 2 are base colors
			baseRed = int(params[0])
			baseGreen = int(params[1])
			baseBlue = int(params[2])
			colorOff = Color(baseRed,baseGreen,baseBlue)
		else:
			colorOff = -1
		
		#param 3 is start pct
		startPct = params[3]
		
		pct= self.pctIntoVis()
		self.lightPct(float(startPct),pct, colorOn, colorOff)
		
		return 0
	
	def theaterChase(self,params):
		
		colorOn = self.colorFromPlayData(self.playData())
		
		if float(params[0]) >= 0:
		
			#params[0] to 2 are base colors
			baseRed = int(params[0])
			baseGreen = int(params[1])
			baseBlue = int(params[2])
			colorOff = Color(baseRed,baseGreen,baseBlue)
		else:
			colorOff = -1
		
		if colorOff < 0:
			cats = 0
		else:
			self.oneColor(colorOff)
		
		#scroll freq is param 3
		beat = float(params[3])
		pct = self.pctIntoBeat(beat)
		
		#scroll segments is param 4
		segments = int(params[4]) 
		skip = 1+math.floor(segments*pct)
		#print("float skip", skip)
		skip = int(skip)
		#print("int skip", skip)
		
		for pixel in range(skip-1,self.numPixels(),segments):
			self.ledData[pixel] = colorOn

		return 0
	
	def morphRainbow(self,params):
		#for param 0
		#0 is morphing rainbow according to visualization time
		#1 is morphing according to beat
		#other is fixed rainbow
		
		#param 1 is the beat if used
		
		if int(params[0]) == 1:
			iteration = 256 * self.pctIntoBeat(float(params[1]))
		elif int(params[0]) ==0:
			iteration = 256 * self.pctIntoVis()
		else:
			iteration = 1
		iteration = int(iteration)
		
		for i in range(self.numPixels()):
			self.ledData[i] = wheel(((i * 255 / self.numPixels()) + iteration) & 255)
		
		return 0
	
	def cyclo(self,params):

		colorOn = self.colorFromPlayData(self.playData())
		
		if float(params[0]) >= 0:		
			#params[0] to 2 are base colors
			baseRed = int(params[0])
			baseGreen = int(params[1])
			baseBlue = int(params[2])
			colorOff = Color(baseRed,baseGreen,baseBlue)
		else:
			colorOff = -1
		
		if colorOff < 0:
			cats = 0
		else:
			self.oneColor(colorOff)
		
		#scroll freq is param 3
		beat = float(params[3])
		pct = self.pctIntoBeat(beat)
		
		#cyclo segments is param 4
		segments = int(params[4]) 
		
		start = int(math.floor(self.numPixels()*pct))
		pixel = 0
		for i in range(0,segments,1):
			pixel = start + i
			if pixel<self.numPixels():
				self.ledData[pixel] = colorOn
			else:
				pixelSet = pixel-(self.numPixels()-1)
				if(pixelSet) > (self.numPixels() - 1):
					pixelSet = self.numPixels()-1
				if(pixelSet) <0:
					pixelSet = 0
				self.ledData[pixelSet] = colorOn
		return 0	
	
	def lightPct(self, startPct, pct, colorOn, colorOff):
		
		i = 0
		if colorOff < 0:
			cats = 0
		else:
			self.oneColor(colorOff)
		
		
		if startPct<=.5:	#sets all leds to one color
			start = int(self.numPixels()*startPct)
			stop = start + int((self.numPixels() - start)*pct)
			
			if stop<start:
				stop = start
				print('error corrected stop less than start')
			#print("start: ", start,"  stop: ", stop) 
			for pixel in range(start, stop,1):
				#print("pixel: ",pixel)
				self.ledData[pixel] = colorOn
				
				if (start - i)>0:
					self.ledData[start-i] = colorOn
				i+=1
		else:
			start = int(self.numPixels()*startPct)-1
			stop = start - int(start*pct)
			if stop > start:
				stop = start
				print('error corrected stop greater than start')
			#print("start: ", start,"  stop: ", stop) 
			for pixel in range(start, stop,-1):
				#print("pixel: ",pixel)
				self.ledData[pixel] = colorOn
				if (start + i)<self.numPixels():
					self.ledData[start+i] = colorOn
				i+=1
		return 0