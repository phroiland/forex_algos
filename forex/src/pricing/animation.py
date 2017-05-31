#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 14:44:45 2017

@author: johnfroiland
"""
import matplotlib
matplotlib.use('Qt5Agg')

print matplotlib.rcParams['backend']
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    pullData = open('sampleText.txt','r').read()
    dataArray = pullData.split('\n')
    times=[]
    price=[]
    for eachLine in dataArray:
        if len(eachLine) > 1:
            x,y = eachLine.split(',')
            times.append(int(x))
            price.append(int(y))
    ax1.clear()
    ax1.plot(times,price)
    
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
