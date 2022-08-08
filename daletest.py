#!/usr/bin/python
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
from strand import *
import os

from neopixel import *
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)



# LED strip configuration:

TIMESHIFT = 0

UPDATERATE =10 #is mS
SONGLENGTH = 116

STRAND1START = 1
STRAND1SIZE = 48
STRAND1FILE = "/home/pi/rpi_ws281x/python/examples/strip1.csv"

STRAND2START = STRAND1SIZE
STRAND2SIZE = 42
STRAND2FILE = "/home/pi/rpi_ws281x/python/examples/strip2.csv"

STRAND3START = STRAND2START+STRAND2SIZE
STRAND3SIZE = 49
STRAND3FILE = "/home/pi/rpi_ws281x/python/examples/strip3.csv"

STRAND4START = STRAND3START+STRAND3SIZE
STRAND4SIZE = 49
STRAND4FILE = "/home/pi/rpi_ws281x/python/examples/strip4.csv"

STRAND5START = STRAND4START + STRAND4SIZE 
STRAND5SIZE = 43
STRAND5FILE = "/home/pi/rpi_ws281x/python/examples/strip5.csv"

LED_COUNT      = STRAND1SIZE + STRAND2SIZE + STRAND3SIZE +STRAND4SIZE + STRAND5SIZE      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 125     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

FRAMESSKIP = (TIMESHIFT*120)/3.13
#about 300 frames per 10 seconds

def loadDataFromStrands(strip, strand1,strand2, strand3, strand4,strand5):
	"""update data to strand from strip segments"""	
	for j in range(STRAND1START,strand1.numPixels() , 1):
		strip.setPixelColor(j,strand1.ledData[j])

	for j in range(STRAND2START,STRAND2START+strand2.numPixels() , 1):
		strip.setPixelColor(j,strand2.ledData[j-STRAND2START])	
	
	for j in range(STRAND3START,STRAND3START+strand3.numPixels() , 1):
		strip.setPixelColor(j,strand3.ledData[j-STRAND3START])
	
	for j in range(STRAND4START,STRAND4START+strand4.numPixels() , 1):
		strip.setPixelColor(j,strand4.ledData[j-STRAND4START])

	for j in range(STRAND5START,STRAND5START+strand5.numPixels() , 1):
		strip.setPixelColor(j,strand5.ledData[j-STRAND5START])
		
	#print('strip load')	
def resetStrands():
	strand1.resetTime(time.time(), TIMESHIFT)
	strand2.resetTime(time.time(), TIMESHIFT)
	strand3.resetTime(time.time(), TIMESHIFT)
	strand4.resetTime(time.time(), TIMESHIFT)
	strand5.resetTime(time.time(), TIMESHIFT)
	return 0
def updateStrands():
	strand1.update()
	strand2.update()
	strand3.update()
	strand4.update()
	strand5.update()
	#print(strand1.playData())
	loadDataFromStrands(strip,strand1,strand2,strand3,strand4,strand5)
	strip.show()
	return 0
	
# Main program logic follows:
if __name__ == '__main__':
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	# Intialize the library (must be called once before other functions).
	strip.begin()
	
	#MODIFY HERE WHEN OTHER STRAND CLASSES WRITTEN
	strand1=strand(STRAND1SIZE)
	strand2=strand(STRAND2SIZE)
	strand3=strand(STRAND3SIZE)
	strand4=strand(STRAND4SIZE)
	strand5=strand(STRAND5SIZE)	
	
#	os.system('mpg321 /home/pi/thrillerTrimed.mp3 --single0 --2to1 --skip ' + str(FRAMESSKIP) + '&')
#	time.sleep(1.5)
	
	strand1.begin(STRAND1FILE, time.time(), TIMESHIFT)
	strand2.begin(STRAND2FILE, time.time(), TIMESHIFT)
	strand3.begin(STRAND3FILE, time.time(), TIMESHIFT)
	strand4.begin(STRAND4FILE, time.time(), TIMESHIFT)
	strand5.begin(STRAND5FILE, time.time(), TIMESHIFT)
	
	resetStrands()
	timeReset = 0

	print ('Press Ctrl-C to quit.')
	while True:
		
		#| 
		if ((GPIO.input(23) == True) ) :
			if ((time.time() - timeReset) > SONGLENGTH):
				#print('restarting song')
				#time.sleep(.1)
				os.system('mpg321 /home/pi/thrillerTrimed.mp3 --single0 --2to1 --skip ' + str(FRAMESSKIP) + '&')
				time.sleep(.5)
				resetStrands()
				timeReset = time.time()
			else:
				#print('playing song')
				cats = 0
		else:
			os.system('killall mpg321 &')
			resetStrands()
			timeReset = 0
		updateStrands()
		time.sleep(UPDATERATE/1000)

