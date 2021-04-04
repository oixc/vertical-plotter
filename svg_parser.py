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
        print(v['d'])  # print d-string of k-th path in SVG
        f.write(v['d'])  # print d-string of k-th path in SVG
        