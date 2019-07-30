# -*- coding: utf-8 -*-
'''
Created on 30.07.2019

@author: yu03
'''
import numpy as np

file_name = 'test.txt'
f = open(file_name,'r')
lines = np.loadtxt(file_name, dtype=str, delimiter=' ')
# f = open(file_name,'rb')
# lines = np.load(f)
print(lines[:5])
print(len(lines))
