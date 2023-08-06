# -*- coding: utf-8 -*-
"""
M_DataAnalysis
---------
"""

from math import sin, cos, sqrt, atan2, radians


def Pipelength(Pipelines):
    total=0
    for pipe in Pipelines:
        length      = routelength(pipe.long,pipe.lat)
        pipe.length = length
        total       = total+float(length)

    return total




def distance(lon1,lat1,lon2,lat2):
    ''' Calculate distance between 2 Points on Earth's surface.

    \n.. comments:
    Input:
        lon1: 		float of long pos 1
		lat1: 		float of lat pos 1
		lon2: 		float of long pos 2
		lat2: 		float of lat pos 2
    Output:
		distance 	float
		'''
    R = 6373.0 # radius earth
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance




def routelength(long, lat):
    """Returns total length of a pipeline (polyline, multi point pipeline)

    \n.. comments:
    Input:
        lon1: 		list of floats of long values
		lat1: 		lit of float of lat values
    Output:
		distance 	float

	"""

    length=0.0
    for i in (range(len(long)-1)):
        length = length + distance(long[i],lat[i],long[i+1],lat[i+1])

    return "{0:.3f}".format(length)




def set_lengths(elements):
    ''' Calculates length of Line Element and attach it with dict param

    \n.. comments:
    Sample:
           length(SciGrid.Pipelines) '''
    for element in elements:
        element.param['length_km']   = float(routelength(element.long, element.lat))
    pass




def sum_length(elements):
    """Sums values over all elements of the attribute length in dict param.

    \n.. comments:
    Input:
		elements: 	List of elements
    Output:
		sumlength:
	"""

    sumlength=0.0

    for element in elements:
        sumlength += float(element.param['length_km'])

    return sumlength




