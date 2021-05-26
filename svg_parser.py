# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 21:20:39 2021

@author: oixc
"""

from svgpathtools import svg2paths

filename = 'test_pattern'
paths, attributes = svg2paths(f'svg/{filename}.svg')

with open(f'svg/{filename}.path', 'w') as f:
    for k, v in enumerate(attributes):
        
        try:
            print(v['d'])  # print d-string of k-th path in SVG
        except KeyError:
            continue
        f.write(v['d'])  # print d-string of k-th path in SVG
        

clean_up = True
if clean_up:
    with open(f'svg/{filename}.path', 'r') as f:
        path = f.read()
    
    clean_path = []
    xs = []
    ys = []
        
    path = path.replace(',', ' ')
    path = path.replace('M', ' M ')
    path = path.replace('L', ' L ')
    path = path.replace('H', ' H ')
    path = path.replace('V', ' V ')
    path = iter(path.split())
    for action in path:
        if action in ['M', 'L']:
            x = float(next(path))
            y = float(next(path))
        elif action == 'H':
            x = float(next(path))
            action = 'L'
        elif action == 'V':
            y = float(next(path))
            action = 'L'
        else:
            raise NotImplementedError(action)
            
        clean_path.append(action)
        clean_path.append(str(x))
        clean_path.append(str(y))
    
        xs.append(x)
        ys.append(y)
        
    clean_path = ' '.join(clean_path)
    
    with open(f'svg/{filename}.path', 'w') as f:
        f.write(clean_path)
        