# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 13:30:22 2021

@author: oixc
"""

import serial
import itertools

def cmd(ser, cmd):
    # if cmd[-1] != '\n':
    #     cmd += '\n'
    cmd = cmd.encode()
    ser.write(cmd)
    ser.flush()
    result = ser.read()
    print(cmd, result, cmd == result)
    # print(cmd[:-1])

knightrider = ['a', 'b', 'c', 'd']
# knightrider.extend(reversed(knightrider[1:-1]))
knightrider = itertools.cycle(knightrider)

with serial.Serial() as ser:
    ser.baudrate = 9600
    ser.port = 'COM4'
    ser.timeout = None
    ser.open()
    # ser.flush()
    print(ser.read())
    # cmd(ser, 'a')
    # cmd(ser, 'b')
    # cmd(ser, 'a')
    # cmd(ser, 'b')
    # cmd(ser, 'c')
    # cmd(ser, 'd')

    for c in knightrider:
        cmd(ser, c)
        # print('>>', ser.read())