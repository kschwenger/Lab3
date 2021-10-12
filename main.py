#   To check address: sudo i2cdetect -y 1

import smbus
from time import sleep

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

class Joystick:

  def __init__(self,address):
    self.joystick = PCF8591(address)
  
  def getX(self):
    return str(self.joystick.read(0))

  def getY(self):
    return str(self.joystick.read(1))

theJoystick = Joystick(0x48)
if __name__ == "__main__":
  try:
    while True:
      print ("{: >s}, {: >s}".format(theJoystick.getX(),theJoystick.getY()))
      sleep(0.1)
  except KeyboardInterrupt: # if user hits ctrl-C
    print('\nExiting')
  except Exception as e: # catch all other errors
    print('\ne') 