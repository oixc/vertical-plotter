# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 13:30:22 2021

@author: oixc
"""

import serial
import itertools
import sys
import time

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def cmd(ser, cmd):
    cmd = cmd.encode()
    ser.write(cmd)
    ser.flush()
    result = ser.read()
    assert (cmd == result), 'cmd and result need to match'
    print(cmd, result, cmd == result)

def send_commands(commands):
    with serial.Serial() as ser:
        ser.baudrate = 9600
        ser.port = 'COM4'  # usb
        # ser.port = 'COM5'  # bluetooth
        ser.timeout = None
        ser.open()
        # ser.flush()
        # result = ser.read_until()
        # if not result == b'Ready\r\n':
        #     print('incorrect handshake')
        #     print(result)
        #     sys.exit()
        # else:
        #     print('ready to go')
        
        start = time.time()
        establish_contact(ser)
        print(f'contact {time.time() - start:.3f}')
        
        for chunk in chunks(commands, 20):
            for c in chunk:
                ser.write(c.encode())
                # ser.flush()
                # cmd(ser, c)
            # print(ser.readlines())
            # print(ser.read_until())
            
            while ser.in_waiting <= 0:
                pass
            result = ser.read(ser.in_waiting)
            print(f'{time.time() - start:.3f}', result)            
                
        # print(ser.read())
        # ser.flush()
        # result = ser.read()
        # print(result)
                               
def establish_contact(ser):
    while ser.in_waiting <= 0:
        pass
    ser.write(b'A')
    result = ser.read(ser.in_waiting)
    time.sleep(0.3)
    return result
    
        
if __name__ == '__main__':
    knightrider = ['a', 'b', 'c', 'd']
    knightrider.extend(reversed(knightrider[1:-1]))
    # knightrider = itertools.cycle(knightrider)
    
    send_commands(['d'] * 2500 + ['x'])
    # send_commands(['c', 'a'] * 100)
    # send_commands(knightrider)
    
    # send_commands(['e', 'f'] * 10)
    
    # ser = serial.Serial()
    # ser.baudrate = 9600
    # ser.port = 'COM4'  # usb
    # # ser.port = 'COM5'  # bluetooth
    # ser.timeout = None
    # ser.open()
    # result = establish_contact(ser)
    
    # # for c in knightrider * 10: # ['a', 'c'] * 25:
    # #     ser.write(c.encode())
    # ser.close()
# 