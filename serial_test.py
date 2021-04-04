# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 13:30:22 2021

@author: oixc
"""

import serial
import itertools

def cmd(ser, cmd):
    if cmd[-1] != '\n':
        cmd += '\n'
    ser.write(cmd.encode())
    ser.flush()
    print(cmd[:-1])

knightrider = ['LL', 'LR', 'RL', 'RR', 'rr']
# knightrider.extend(reversed(knightrider[1:-1]))
# knightrider = itertools.cycle(knightrider)

with serial.Serial() as ser:
    ser.baudrate = 9600
    ser.port = 'COM4'
    ser.timeout = None
    ser.open()
    print(ser.readline())
    cmd(ser, 'lr')

    # for c in knightrider:
    #     cmd(ser, c)
