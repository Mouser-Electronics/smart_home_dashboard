#Version B
# Please refer to 114-13315 for connection diagram 

#I2C Pins 
#GPIO2 -> SDA
#GPIO3 -> SCL

#Import the Library Requreid 
import smbus
import time
import curses

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the I2C address of the AmbiMate module
address = 0x2A

elements = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
data = bytearray(elements)

# See application spec for more info regarding registers
fw_ver = bus.read_byte_data(address, 0x80)
fw_sub_ver = bus.read_byte_data(address, 0x81)
opt_sensors = bus.read_byte_data(address, 0x82)


out_str = "AmbiMate Sensor: 4 Core "
if (opt_sensors & 0x01):
        out_str += "+ CO2 "
if (opt_sensors & 0x04):
        out_str += "+ AUDIO "
print (out_str)

out_str = "AmbiMate Firmware version: %d.%d" %(fw_ver, fw_sub_ver)
print (out_str)
out_str = "Raspberry PI Demo version: A.2"
print (out_str)

    
#Loop starts here
def read_sensor_data():
    
    # All sensors except the CO2 sensor are scanned in response to this command   
    # The CO2 sensor scan rate is fixed internally at 10 seconds
    for _ in range(2):
        if (opt_sensors & 0x01):
                bus.write_byte_data(address, 0xC0, 0x7F)
        else:
                bus.write_byte_data(address, 0xC0, 0x3F)
        # Delay of 100ms to make sure all sensors are internally scanned      
        time.sleep(1)

	#bus.read_byte_data used, works most optimal
    #bus.read_block_data gave occasional incorrect values 
    #data = bus.read_i2c_block_data(address_2, 0x00, 15)

    for i in range(0, 15):
        data[i] = bus.read_byte_data(address, i)      
    

    read_sensor_data.temperatureC = (256* data[1] + data[2]) / 10.0
    read_sensor_data.Humidity = (256* data[3] + data[4]) / 10.0
    read_sensor_data.light = (256 * (data[5] & 0x7F) + data[6])
    read_sensor_data.audio = (256 * (data[7] & 0x7F) + (data[8] & 0x7F))
    read_sensor_data.motion = data[0]
    if (read_sensor_data.motion & 0x80) or (read_sensor_data.motion & 0x01):
        read_sensor_data.motion = True
        print('Motion DETECTED-not gui')
        time.sleep(2)
    else:
        read_sensor_data.motion = False


    return read_sensor_data.temperatureC, read_sensor_data.Humidity, read_sensor_data.light, read_sensor_data.audio, read_sensor_data.motion
