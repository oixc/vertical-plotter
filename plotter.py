# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 16:16:44 2021

@author: oixc
"""

import arduino_serial
import simulation
import numpy as np

class Plotter(simulation.Simulation):
    def __init__(self):
        super().__init__()
        
    def find_line_length(self, x, y):
        # pythagoras to the rescue: a**2 + b**2 = c**2
        line_length = []
        for anchor in [0, 1]:
            a = x - self.anchor_points[anchor][0]
            b = y - self.anchor_points[anchor][1]
            line_length.append(np.sqrt(a**2 + b**2))
            
        return line_length
    
    def find_step_squence(self, x, y):
        target_line_length = np.array(self.find_line_length(x, y))
        current_line_lenght = np.array(self.line_length)
        delta_line_lenght = target_line_length - current_line_lenght
        line_steps = delta_line_lenght / self.step_unit
        
        if any(abs(line_steps) <= 0.1):
            raise NotImplementedError('only one motor needs to turn')
            
        steps_ratio = line_steps[0] / line_steps[1]
        
        step_sequence = []
        for anchor in [0, 1]:
            direction = np.sign(line_steps[anchor])
            number_of_steps = int(abs(np.round(line_steps[anchor], 0)))
            step_sequence.extend(number_of_steps * [self._step_command(anchor, direction)])
        
        return step_sequence


if __name__ == '__main__':    
    send_commands = arduino_serial.send_commands
    
    sim = simulation.Simulation()
    send_commands = sim.send_commands
    
    # def send_commands(commands):
    #     sim.send_commands(commands)
    #     arduino_serial.send_commands(commands)


    p = Plotter()
    x, y = 150, 100
    x, y = p.pen_position
    x = 100
    step_sequence = p.find_step_squence(x, y)
    send_commands(['f'] + step_sequence + ['e']) 
    
    
    # send_commands(['f'] + ['c', 'c', 'a'] * 30 + ['e'] + ['a', 'a', 'd'] * 20 + ['f'] + ['a', 'c'] * 30 + ['e']) 
    
    sim.draw_svg()
