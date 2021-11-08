# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 19:33:00 2021

@author: janhofma
"""

import arduino_serial

if __name__ == '__main__':
    filename = 'plot_commands.txt'
    with open(filename) as f:
        commands = f.readlines()
    
    print(len(commands[0]))
    arduino_serial.send_commands(commands[0])