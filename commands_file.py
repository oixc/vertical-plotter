# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 19:33:00 2021

@author: janhofma
"""

import arduino_serial
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', 
                        default='plot_commands.txt',
                        help='file to read commands from')
    args = parser.parse_args()

    with open(args.file) as f:
        commands = f.readlines()
    
    print(len(commands[0]) + 1)
    arduino_serial.send_commands('e' + commands[0])
    