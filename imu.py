#!/usr/bin/python

import smbus
import math

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
    return bus.read_byte_data(mpu_address, adr)

def read_word(adr):
    high = bus.read_byte_data(mpu_address, adr)
    low = bus.read_byte_data(mpu_address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def read_regs(sens_adr, adr, len):
    buf = []
    for i in range(0, len):
        buf[i] = bus.read_byte_data(sens_adr, adr + len)
    return buf

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
mpu_address = 0x68   # This is the address value read via the i2cdetect command
hmc_address = 0x1e

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(mpu_address, power_mgmt_1, 0)

# configure the MPU6050 (gyro/accelerometer)
bus.write_byte_data(mpu_address, 0x6B, 0x00);                # exit sleep
bus.write_byte_data(mpu_address, 0x19, 109);                 # sample rate = 8kHz / 110 = 72.7Hz
bus.write_byte_data(mpu_address, 0x1B, 0x18);                # gyro full scale = +/- 2000dps
bus.write_byte_data(mpu_address, 0x1C, 0x08);                # accelerometer full scale = +/- 4g
bus.write_byte_data(mpu_address, 0x38, 0x01);                # enable INTA interrupt

# configure the HMC5883L (magnetometer)
bus.write_byte_data(mpu_address, 0x6A, 0x00);                # disable i2c master mode
bus.write_byte_data(mpu_address, 0x37, 0x02);                # enable i2c master bypass mode
bus.write_byte_data(hmc_address, 0x00, 0x18);                # sample rate = 75Hz
bus.write_byte_data(hmc_address, 0x01, 0x60);                # full scale = +/- 2.5 Gauss
bus.write_byte_data(hmc_address, 0x02, 0x00);                # continuous measurement mode
bus.write_byte_data(mpu_address, 0x37, 0x00);                # disable i2c master bypass mode
bus.write_byte_data(mpu_address, 0x6A, 0x20);                # enable i2c master mode
HMC5883L_ADDRESS = 0x1e
# configure the MPU6050 to automatically read the magnetometer
bus.write_byte_data(mpu_address, 0x25, HMC5883L_ADDRESS | 0x80); # slave 0 i2c address, read mode
bus.write_byte_data(mpu_address, 0x26, 0x03);                # slave 0 register = 0x03 (x axis)
bus.write_byte_data(mpu_address, 0x27, 6 | 0x80);            # slave 0 transfer size = 6, enabled
bus.write_byte_data(mpu_address, 0x67, 1);                   # enable slave 0 delay



if 1:
    print "gyro data"
    print "---------"

    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)

    print "gyro_xout: ", gyro_xout, " scaled: ", (gyro_xout / 131)
    print "gyro_yout: ", gyro_yout, " scaled: ", (gyro_yout / 131)
    print "gyro_zout: ", gyro_zout, " scaled: ", (gyro_zout / 131)

    print
    print "accelerometer data"
    print "------------------"

    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)

    accel_xout_scaled = accel_xout / 16384.0
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0

    print "accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled
    print "accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled
    print "accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled

    print "x rotation: " , get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
    print "y rotation: " , get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
    rx_buffer = read_regs(mpu_address, 0x3b, 20)
    accel_x  = rx_buffer[0]  << 8 | rx_buffer[1];
    accel_y  = rx_buffer[2]  << 8 | rx_buffer[3];
    accel_z  = rx_buffer[4]  << 8 | rx_buffer[5];
    mpu_temp = rx_buffer[6]  << 8 | rx_buffer[7];
    gyro_x   = rx_buffer[8]  << 8 | rx_buffer[9];
    gyro_y   = rx_buffer[10] << 8 | rx_buffer[11];
    gyro_z   = rx_buffer[12] << 8 | rx_buffer[13];
    magn_x   = rx_buffer[14] << 8 | rx_buffer[15];
    magn_y   = rx_buffer[16] << 8 | rx_buffer[17];
    magn_z   = rx_buffer[18] << 8 | rx_buffer[19];

# convert accelerometer readings into G'
    accel_x_g = accel_x / 8192.0;
    accel_y_g = accel_y / 8192.0;
    accel_z_g = accel_z / 8192.0;

# convert temperature reading into degrees Celsius
    mpu_temp_c = mpu_temp / 340.0 + 36.53;

# convert gyro readings into Radians per second
    gyro_x_rad = gyro_x / 939.650784;
    gyro_y_rad = gyro_y / 939.650784;
    gyro_z_rad = gyro_z / 939.650784;

# convert magnetometer readings into Gauss's
    magn_x_gs = magn_x / 660.0;
    magn_y_gs = magn_y / 660.0;
    magn_z_gs = magn_z / 660.0;
    print "X Acceleration   ", accel_x_g, "G";
    print "Y Acceleration   ", accel_y_g, "G";
    print "Z Acceleration   ", accel_z_g, "G";
    print "MPU6050 Temp     ", mpu_temp_c, "C";
    print "X Rotation       ", gyro_x_rad, "Rad/s";
    print "Y Rotation       ", gyro_y_rad, "Rad/s";
    print "Z Rotation       ", gyro_z_rad, "Rad/s";
    print "X Magnetic Field ", magn_x_gs, "Gs";
    print "Y Magnetic Field ", magn_y_gs, "Gs";
    print "Z Magnetic Field ", magn_z_gs, "Gs";
    time.sleep(0.5);

