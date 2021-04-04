# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 13:30:22 2021

@author: oixc
"""

import serial

def cmd(ser, cmd):
    if cmd[-1] != '\n':
        cmd += '\n'
    ser.write(cmd.encode())
    ser.flush()

with serial.Serial() as ser:
    ser.baudrate = 9600
    ser.port = 'COM4'
    ser.timeout = None
    ser.open()
    print(ser.readline())
    
    cmd(ser, 'LL')
    cmd(ser, 'LR')
    cmd(ser, 'RR')
    cmd(ser, 'RL')