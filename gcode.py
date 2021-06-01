# -*- coding: utf-8 -*-
"""
Created on Sun Apr  18 16:16:44 2021

@author: oixc

https://howtomechatronics.com/tutorials/g-code-explained-list-of-most-important-g-code-commands/
"""

import numpy as np
from util import command_dict
import plotter

if __name__ == '__main__':        
    p, send_commands, sim = plotter.create_plotter(simulate=True)
    
    sim.step_unit = p.step_unit = 1
    p.translate = [470, 350]
    p.scale = [1/2, 1/2]
    all_commands = []
    xs = []
    ys = []
    
    with open('gcode/output_0011.ngc', 'r') as f:
        for line in f.readlines():
            line = line.strip().upper()
            if line.startswith('G'):
                command = line[:3]
                print(command, line)
                
                if command == 'G21':
                    # metric, we are good
                    pass
                elif command == 'G20':
                    raise NotImplementedError('use G21 for metric!')
                elif command in ['G00', 'G01']:
                    # linear movement
                    x = None
                    y = None
                    z = None
                    line = line.replace('X ', 'X')
                    line = line.replace('Y ', 'Y')
                    line = line.replace('Z ', 'Z')                    
                    for part in line.split():
                        if part.startswith('X'):
                            x = float(part[1:])
                        elif part.startswith('Y'):
                            y = float(part[1:])
                        elif part.startswith('Z'):
                            z = float(part[1:])
                    
                    if z is not None:
                        if z > 0:
                            all_commands.extend(command_dict['PU'])
                        else:
                            all_commands.extend(command_dict['PD'])
                            
                    if (x is not None) and (y is not None):            
                        xs.append(x)
                        ys.append(y)            
                        all_commands.extend(p.find_step_squence(*p.offset(x, y), fast=False))
                else:
                    raise NotImplementedError(command)
      

    print('top left canvas: ', p.offset(min(xs), min(ys)))
    print('bottom right canvas: ', p.offset(max(xs), max(ys)))
            
    current_width = max(xs) - min(xs)
    target_width = p.anchor_width * 0.5
    x_scale = target_width / current_width            
    x_scale = p.scale[0] 
    
    current_center = (max(xs) + min(xs)) / 2 * x_scale
    target_center = p.anchor_width / 2 
    x_translate = target_center - current_center            
    
    current_top = min(ys) * x_scale
    target_top = (p.home[1] + p.upper_tension_border) / 2
    target_top = p.home[1]
    y_translate = target_top - current_top        
    
    print('translate', x_translate, y_translate)
    print('scale', x_scale, x_scale)        
      
    print(len(all_commands))
    send_commands(all_commands)
    
    # sim.draw_svg(draw_move_lines=False, draw_tension_lines=False, draw_anchor_lines=False)
    sim.draw_svg(draw_move_lines=True, draw_tension_lines=True, draw_anchor_lines=True)
