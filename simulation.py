# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 16:52:37 2021

@author: oixc
"""

class Simulation():
    def __init__(self):
        self.line_length = {0: 100, 1:100}
        self.step_unit = 1

    def apply_command(self, command):
        if command == 'a':
            self.line_length[0] -= self.step_unit
        elif command == 'b':
            self.line_length[0] += self.step_unit
        elif command == 'c':
            self.line_length[1] += self.step_unit
        elif command == 'd':
            self.line_length[1] -= self.step_unit
        else:
            print(f'unknown command {command}')
        
    def send_commands(self, commands):
        for command in commands:
            self.apply_command(command)
        