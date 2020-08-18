#by Bhuris Mun
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time, json, math
from pymodbus.register_read_message import *

client = ModbusClient(method='rtu', port='/dev/ttyUSB0', timeout=0.3, baudrate=9600, stopbit=1, bytesize=8, parity='N')
client.connect()
#print(client.connect())

def main():
    value = client.read_input_registers(0, 10, unit=0x01) #read from unit 0x01
    #print(value.registers) #for prove test
    volt = value.registers[0]*0.1
    amp = value.registers[1]*0.001
    power = value.registers[3]*0.1
    energy = value.registers[5]*0.001
    freq = value.registers[7]*0.1
    pwfac = value.registers[8]*0.01
    alarm = value.registers[9]
    if alarm == 0x0000:
        alarmtran = 'NORMAL JA'
    elif alarm == 0xFFFF:
        alarmtran = 'ALARM'
    else:
        alarmtran = 'N/A'
    pwangle=math.acos(pwfac)
    apparent = power/math.cos(pwangle)
    reactive = apparent*math.sin(pwangle)
    impedance= apparent/(amp*amp)
    rinline = impedance*math.cos(pwangle)
    xinline = impedance*math.sin(pwangle)
    data={}
    data={
        "volt":volt,
        "amp":amp,
        "realpower":power,
        "energy":energy,
        "freq":freq,
        "pwfac":pwfac,
        "reactive":reactive,
        "apparent":apparent,
        "powerangle":pwangle,
        "impedance":impedance,
        "rinline":rinline,
        "xinline":xinline,
        "status":alarmtran
        }
    dataff=json.dumps(data) # format data to json
    print(dataff) # for stdout nodered
