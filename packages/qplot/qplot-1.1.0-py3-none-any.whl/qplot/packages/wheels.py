#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 12:40:43 2021

@author: apluta
"""
import matplotlib

def linewidthwheel(parameters,parametername):
    """
    Thickness of Lineelements by diameter_mm, pressure_bar or capacity
    """
    
    no_value    = ['',None,0,'0','None']
    minmax_array= parameters
    for element in no_value:
         minmax_array=list(filter(lambda a: a != element, minmax_array))

    if len(minmax_array)==0:
        print('No None values for', parametername)
        minmax_array.append(0)
        minmax_array.append(1)

    if len(set(minmax_array))==1:
            mid=float(minmax_array[0])
            minmax_array=[]
            minmax_array.append(mid*0.9)
            minmax_array.append(mid*1.1)
    
        
    if parametername=='diameter_mm':
        vmin=min(min(minmax_array),0)
    else:
        if len(minmax_array)>1:
            #print(minmax_array)
            vmin=min(min(minmax_array),0)
        else:
            vmin=minmax_array[0]
    if len(minmax_array)>1:            
        vmax=max(minmax_array)
    else:
        vmax=minmax_array[0]
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    widths=[]
    for parameter in parameters:
        if parameter in no_value:
            width=0.3
            widths.append(width)
        else:
            width=0.3+5*norm(parameter)
            widths.append(width)
    return widths


def parawheel(parameters):
    """
    Maps color to html color
    if color = colorwheel, it rotates through colors for each call
    """
    no_value= ['',None,0,'0','None']
    minmax_array=parameters
    for element in no_value:
         minmax_array=list(filter(lambda a: a != element, minmax_array))

    if len(set(minmax_array))==1:
       minmax_array=[minmax_array[0]*0.9,minmax_array[0]*1.1]

    if len(minmax_array)!=0:
        vmin=min(minmax_array,)
        #print(vmin)
        vmax=max(minmax_array)
        #print(vmax)
        norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
        color=[]
        cmap = matplotlib.cm.get_cmap('cool')#'YlOrRd')
        for parameter in parameters:
            if parameter in no_value:
                color.append('k')
            else:
                rgb=cmap(norm(parameter))
                color.append(rgb)
        return color,cmap,norm
#    else:
#        minmax_array.append(0)
#        vmin=min(minmax_array)
#        vmax=max(minmax_array)
#        norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
#        color=[]
#        cmap = matplotlib.cm.get_cmap('cool')#)'binary')
#        for parameter in parameters:
#            if parameter in no_value:
#                color.append('k')
#            else:
#                rgb=cmap(norm(parameter))
#                color.append(rgb)
#      
#        return color,cmap,norm

def colorwheel(color,colors):
    """
    Maps color to html color
    if color = colorwheel, it rotates through colors for each call
    """
    

    colordict={"t":'#597DFF',"o":'#C76730',"v":'#728C00',"r":"#FF0000",
               "g":"#00CD00","mustard":'#FFDB58',"lime":'#E3FF00',
               "b":'#1022ff', 'y':'#ffed10', 'k':'000000'}
    if color =="colorwheel":
        #print(next(colors))
        return next(colors)
    if color in colordict:
        return colordict[color]
    else:
        return color
