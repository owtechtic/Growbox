import busio
import board
import digitalio
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import Adafruit_DHT
import time 
from datetime import datetime
import adafruit_character_lcd.character_lcd as characterlcd
import RPi.GPIO as GPIO
import I2C_LCD_driver

mylcd = I2C_LCD_driver.lcd()

#Setup Relay
GPIO.setmode(GPIO.BCM)
relay1 = 17
relay2 = 27
relay3 = 22
GPIO.setup(relay1, GPIO.OUT)#Lights relay
GPIO.setup(relay2, GPIO.OUT)#Pump relay 
GPIO.setup(relay3, GPIO.OUT)#system relay

#RGB LED Setup
Red = 14
Green = 15 #Blue isnt needed since we only want red, green and yellow
GPIO.setup(Red, GPIO.OUT)
GPIO.setup(Green, GPIO.OUT)

#Setup MCP3008 output pins
spi = busio.SPI(clock=board.SCK,MISO=board.MISO, MOSI=board.MOSI)
cs=digitalio.DigitalInOut(board.D8)
mcp=MCP.MCP3008(spi,cs)

#define anolog sensors being used 
chan0 = AnalogIn(mcp, MCP.P0)
#define digital sensor being used
sensor=Adafruit_DHT.DHT11

time.sleep(5)
GPIO.output(relay3, GPIO.LOW)
while True:
    try:
        now = datetime.now()
        current_time = int(now.strftime('%H%M'))
        minute = (int(now.strftime('%M')))
        #define window for light on/off
        start_time = 900
        end_time = 2130
        #turn light on or off
        if current_time > start_time and current_time<end_time:
            GPIO.output(relay1, GPIO.LOW)
        else:
            GPIO.output(relay1, GPIO.HIGH)
        #Pump Running
        if minute == 30 or minute ==0: #if the time is not on the half hour dont run the pump
            GPIO.output(relay2, GPIO.LOW)
        else:#otherwise run it
            GPIO.output(relay2, GPIO.HIGH)

        current_time = now.strftime("%H:%M:%S")
        humidity, temperature = Adafruit_DHT.read_retry(sensor, 4)
        temperature=round((temperature*(9/5)+32),1)
        R=chan0.value
    #react to changes in water level
        if R<2000:
            Level = 'LOW   '
            GPIO.output(Red, GPIO.HIGH)
            GPIO.output(Green, GPIO.LOW)
        #add refill pump here
        if R>50000:
            Level = 'HIGH  '
            GPIO.output(Red, GPIO.LOW)
            GPIO.output(Green, GPIO.HIGH)
        if R>2000 and R<50000:
            Level = 'MEDIUM'
            GPIO.output(Red, GPIO.HIGH)
            GPIO.output(Green, GPIO.HIGH)
    #Display Sensor Data    
        lcd_line_1 = 'Temp='+str(int(temperature))+' Humid='+ str(int(humidity))
        lcd_line_2 = 'Water Lvl:'+Level

        mylcd.lcd_display_string(lcd_line_1,1)
        mylcd.lcd_display_string(lcd_line_2,2)

    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2)
        continue
    
    except Exception as error:
        dhtDevice.exit()
        raise error 
    time.sleep(5)


