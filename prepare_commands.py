# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 16:16:44 2021

@author: oixc
"""

# import arduino_serial
import simulation
import numpy as np
from util import command_dict
import cairo
from plotter import create_plotter

if __name__ == '__main__':    
    p, send_commands, sim  = create_plotter()
    
    # sim.drawing_area = [(390 + 15 - 15, 300 + 25), (390 + 297 - 15 - 15, 300 + 420 - 35)]  # A3
    # sim.drawing_area = [(390 + 15 - 15, 300 + 25), (390 + 297 - 15 - 15, 300 + 210 - 35)]  # A4
    sim.drawing_area = [(390 + 10, 300 + 10), (390 + 100 - 10, 300 + 100 - 10)]  # 10x10
    p.drawing_area = sim.drawing_area

    place_to_drawing_area = False
    all_commands = []
    
    filename = 'vpype'
    p.translate = [396, 306]
    p.scale = [0.427, 0.427]
    
    with open(f'svg/{filename}.path', 'r') as f:
        path = f.read()
        
    xs = []
    ys = []
        
    path = iter(path.split())
    for action in path:
        x = float(next(path))
        y = float(next(path))
        
        xs.append(x)
        ys.append(y)
        
        if not place_to_drawing_area:
            if action == 'M':
                all_commands.extend(p.move_to(x, y))
            elif action == 'L':
                all_commands.extend(p.line_to(x, y))
            else:
                raise NotImplementedError()
                
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
    
    ## scale to drawing area        
    current_width = max(xs) - min(xs)
    target_width = p.drawing_area[1][0] - p.drawing_area[0][0]
    # target_width *= 0.9
    x_scale = target_width / current_width   
    
    current_height = max(ys) - min(ys)
    target_height = p.drawing_area[1][1] - p.drawing_area[0][1]
    # target_height *= 0.9
    y_scale = target_height / current_height            
    
    x_scale = y_scale = min(x_scale, y_scale)
    
    current_center = (max(xs) + min(xs)) / 2 * x_scale
    target_center = (p.drawing_area[1][0] + p.drawing_area[0][0]) / 2
    x_translate = target_center - current_center            
    
    # current_top = min(ys) * x_scale
    # target_top = p.drawing_area[0][1]
    # y_translate = target_top - current_top        
    
    current_center = (max(ys) + min(ys)) / 2 * y_scale
    target_center = (p.drawing_area[1][1] + p.drawing_area[0][1]) / 2
    y_translate = target_center - current_center     
    
    print('-- drawing area --')        
    print(f'p.translate = [{x_translate:.0f}, {y_translate:.0f}]')        
    print(f'p.scale = [{x_scale:.3f}, {y_scale:.3f}]')
    
    assert not place_to_drawing_area, 'if we only place to drawing area we do not need the rest'
    
    # return home
    all_commands.append(command_dict['PU'])
    all_commands.extend(p.move_to(*p.reverse_offset(*p.home)))
    # all_commands.extend(p.move_to(p.anchor_width / 2, 200))
    # all_commands.extend([command_dict['RL']] * 500)
    
    
    # write commands
    with open(f'plot_commands_{filename}.txt', 'w') as f:
        f.write(''.join(all_commands))  
            
    # generate simulation
    print(len(all_commands))
    sim.send_commands(all_commands)
    print('commands written')
                    
    # sim.draw_svg(draw_move_lines=False, draw_tension_lines=False, draw_anchor_lines=False)
    sim.draw_svg(draw_move_lines=True, draw_tension_lines=True, draw_anchor_lines=True)
