# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 13:30:22 2021

@author: oixc
"""

import serial
import itertools
import sys

def cmd(ser, cmd):
    cmd = cmd.encode()
    ser.write(cmd)
    ser.flush()
    result = ser.read()
    assert (cmd == result), 'cmd and result need to match'
    # print(cmd, result, cmd == result)

def send_commands(commands):
    with serial.Serial() as ser:
        ser.baudrate = 9600
        ser.port = 'COM4'  # usb
        # ser.port = 'COM5'  # bluetooth
        ser.timeout = None
        ser.open()
        if not ser.read() == b'A':
            print('incorrect handshake')
            sys.exit()
        else:
            print('ready to go')
    
        for c in commands:
            cmd(ser, c)
                                
if __name__ == '__main__':
    # knightrider = ['a', 'b', 'c', 'd']
    # knightrider.extend(reversed(knightrider[1:-1]))
    # knightrider = itertools.cycle(knightrider)
    
    send_commands(['b'] * 4 * 200)
    # send_commands(['c'] * 50)
    # send_commands(knightrider)
    
    # send_commands(['e', 'f'] * 10)