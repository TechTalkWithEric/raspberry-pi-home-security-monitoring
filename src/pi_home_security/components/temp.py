from smbus2 import SMBus


with SMBus(13) as bus:
    print("smbus2 13 is working!")

with SMBus(14) as bus:
    print("smbus2 14 is working!")
