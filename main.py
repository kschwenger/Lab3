#   To check address: sudo i2cdetect -y 1

# import smbus and sleep function
import smbus
from time import sleep

# PCF8591 composite class (given)
class PCF8591:

  def __init__(self,address):
    self.bus = smbus.SMBus(1)
    self.address = address

  def read(self,chn): #channel
      try:
          self.bus.write_byte(self.address, 0x40 | chn)  # 01000000
          self.bus.read_byte(self.address) # dummy read to start conversion
      except Exception as e:
          print ("Address: %s \n%s" % (self.address,e))
      return self.bus.read_byte(self.address)

  def write(self,val):
      try:
          self.bus.write_byte_data(self.address, 0x40, int(val))
      except Exception as e:
          print ("Error: Device address: 0x%2X \n%s" % (self.address,e))

# new Joystick component class 
class Joystick:

  def __init__(self,address):         # extend via composition
    self.joystick = PCF8591(address)  # create object from composite class
  
  def getX(self):                     # method using composite class 'read' method to read channel 0 of PCF
    return (self.joystick.read(0))

  def getY(self):
    return (self.joystick.read(1))    # method using composite class 'read' method to read channel 1 of PCF



theJoystick = Joystick(0x48)       # new object theJoystick from component Joystick class on specified channel

try:                # exception handling
  while True:       # continually print the getX and getY values every 100ms
    print('%3.f,  %3.f' % (theJoystick.getX(),theJoystick.getY()))
    sleep(0.1)

except KeyboardInterrupt: # if user hits ctrl-C
  print('\nExiting')
except Exception as e: # catch all other errors
  print('\ne') 