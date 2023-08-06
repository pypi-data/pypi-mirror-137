#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Library to convert OSM and CSV Objects to Plotable Items'''

import json
from unidecode import unidecode
from math import sin, cos, sqrt, atan2, radians

def distance(lon1,lat1,lon2,lat2):
    ''' Calulate distance between 2 Points on Earth's surface '''
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
    length = 0.0

    if type(long) == float:
        length = 0
    else:
        for i in (range(len(long)-1)):
            length = length + distance(long[i], lat[i], long[i + 1], lat[i + 1])
    return "{0:.3f}".format(length)




def add_lengths(elements):
    ''' Caculates length of Line Element and attach it as parameter
    \n.. comments:
    Sample:
           length(SciGrid.Pipelines) '''
    for element in elements:
        element.param['length_km'] = routelength(element.long, element.lat)
    pass




def sum_length(elements):
    sumlength=0.0
    for element in elements:
        sumlength+=float(element.param['length_km'])
    return sumlength




def avg_lonlat(lonlat_array):
    long=0
    lat=0
    for entry in lonlat_array:
        long+=entry[0]
        lat+=entry[1]
    return float("{0:.6f}".format(long/(len(lonlat_array)))) ,float("{0:.6f}".format(lat/(len(lonlat_array))))




def Nodes2Points(elements, tagstyle = 2,parameter='',dictionary='param'):
    long    = []
    lat     = []
    taglist = []
    parameterlist=[]

    #if parameter!='':
    for element in elements:
        parameterlist.append(element.__dict__
                             [dictionary].get(parameter,""))

    # in case that long is a list
    if type(elements[0].long) == list:
        for idf, element in enumerate(elements):

                long.append(element.long[0])
                lat.append(element.lat[0])


                tag = 'id:'+ str(element.get('id'))+'\n'
                if tagstyle >1:
                    tag+='name:'+str(element.get('name'))+'\n'
                    tag+='lat:' +str(element.lat[0])+'\n'
                    tag+='lon:' +str(element.long[0])
                    
                tag_parameter='\n'+str(element.get('param').get(parameter,''))
            
                if tag_parameter!="\n":
                    tag+=parameter +':' + tag_parameter                 
                    
                if tagstyle >2:
                    tag+=(json.dumps(element.__dict__[dictionary],
                          ensure_ascii=False,indent=2)).replace('{','').replace('}','').replace('\\"','')
                taglist.append(tag)

    # in case that long is a float
    else:
        for element in elements:

            long.append(element.long)
            lat.append(element.lat)
            tag = 'id:'+ str(element.get('id'))+'\n'
            #tag = '(' + str(element.id) + ') ' + str(element.name) + '\n'
            if tagstyle >1:
                tag+='name:'+str(element.get('name'))+'\n'
                tag+='lat:' +str(element.lat)+'\n'
                tag+='lon:' +str(element.long)
            tag_parameter=str(element.__dict__['param'].get(parameter,''))
            
            if tag_parameter!='':
                tag+='\n'
                tag+=parameter +':' + tag_parameter             
           
            if tagstyle >2:
                tag+=(json.dumps(element.__dict__[dictionary],ensure_ascii=False,indent=2)).replace('{','').replace('}','').replace('\\"','')
            taglist.append(tag)

    
#    if parameter!='':
    return long,lat,taglist,parameterlist
#    else:
#        return long,lat,taglist




def Ways2Lines(elements, min_length = 0, tagstyle = 1,parameter='diameter_mm',
               pipelinethickness=False,orig_path=False,dictionary='param'):
    ''' convert Ways2Lines to plotable lines '''
    lines   = []
    long    = []
    lat     = []
    if len(elements)>0:
        for element in elements:
            if orig_path==True and ("path_lat" in element.param.keys()):
                lat =([element.lat[0]]+
                     element.param["path_lat"]+
                     [element.lat[-1]])
                     
                long =([element.long[0]]+
                      element.param["path_long"]+
                      [element.long[-1]])
                             
            else:
                lat         = element.lat
                long        = element.long
                                
            
            #if parameter!='':
            para=element.__dict__[dictionary].get(parameter,"")
                
            if pipelinethickness==True:
                thickness=element.__dict__[dictionary].get(parameter,"")

            if type(lat) != type(None):
                tag         = ('id:'+str(element.get('id')) + '\n'+
                               'name:'+str(element.get('name')) + '\n'+
                              'dia:' +str(element.get('param').get('diameter_mm')) + '\n'+
                              'press:'+str(element.get('param').get('max_pressure_bar')) + '\n'+
                              'cap:'+str(element.get('param').get('max_cap_M_m3_per_d')) + '\n' )
                              
            #if parameter=='':
            #    line        = [long,lat,tag]
            #else:
            line        = [long,lat,tag,para]
                
            if pipelinethickness==True:
                line.append(thickness)
            linelength  = float(routelength(long,lat))
            if linelength>=min_length:
                lines.append(line)
            else:
                print('M_PlotObjects.Ways2Lines: Too short')
    return lines




def OSMnodes2points(elements):
    ''' convert OSMnodes to plotable Points '''
    long=[]
    lat=[]
    taglist=[]
    if "Node" in elements.keys():
        for entry in elements["Node"]:
            long.append(elements["Node"][entry]["lonlat"][0])
            lat.append(elements["Node"][entry]["lonlat"][1])
            tag=('ID:'+entry)
            tag+=('\n'+(unidecode(json.dumps(elements["Node"][entry]["tags"],ensure_ascii=False,indent=2))).replace('{','').replace('}','').replace('\\"',''))
            taglist.append(tag)
    return long,lat,taglist




def OSMways2points(elements,data,min_length=0):
    ''' convert OSMways  to Plotable Points '''
    long=[]
    lat=[]
    taglist=[]
    refs=[]
    long_avgs=[]
    lat_avgs=[]
    if "Way" in elements.keys():
        for entry in elements["Way"]:
            refs=elements["Way"][entry]['refs']
            lonlat_array=[]
            for ID in refs:
    #            for ID in reference:
                lonlat_array.append(data["Node"][str(ID)]['lonlat'])
            [long_avg,lat_avg]=avg_lonlat(lonlat_array)
            long=[]
            lat=[]

            #long
            linelength=0.0
            for coords in lonlat_array:
                long.append(coords[0])
                lat.append(coords[1])
            #lengths.append(routelength(long_way,lat_way))
            linelength=float(routelength(long,lat))
            if linelength>=min_length:
                long_avgs.append(long_avg)
                lat_avgs.append(lat_avg)
                tag='ID:'+entry
                tag+='\n'+'length:'+str(linelength)+' km \n'+unidecode(json.dumps(elements["Way"][entry]["tags"],ensure_ascii=False,indent=2)).replace('{','').replace('}','').replace('\\"','')
                taglist.append(tag)
    return long_avgs,lat_avgs,taglist




def OSMways2lines(elements,data,min_length=0):
    ''' Convert OSMways to plotable lines '''
    refs=[]
    lines=[]
    id=[]
    if "Way" in elements.keys():
        for entry in elements["Way"]:
            refs=elements["Way"][entry]['refs']
            lonlat_array=[]
            for ID in refs:
                lonlat_array.append(data["Node"][str(ID)]['lonlat'])
            long=[]
            lat=[]
            line=[]
            length=[]
            for coords in lonlat_array:
                long.append(coords[0])
                lat.append(coords[1])
            linelength=float(routelength(long,lat))
            id.append(entry)
            length.append(linelength)
            tag='ID:'+entry+'\n'+'length:'+(routelength(long,lat))+' km \n'+unidecode(json.dumps(elements["Way"][entry]["tags"],ensure_ascii=False,indent=2)).replace('{','').replace('}','').replace('\\"','')
            line=[long,lat,tag]
            if linelength>=min_length:
                lines.append(line)
    return lines




def OSMrelations2lines(elements,data):
    ''' Convert OSMrelation to plotable lines '''
    refs=[]
    lines=[]
    for entry in elements["Relation"]:
        refs=elements["Relation"][entry]['refs']
        lonlat_array=[]
        for ID in refs:
            lonlat_array.append(data["Node"][str(ID)]['lonlat'])
        long=[]
        lat=[]
        line=[]
        for coords in lonlat_array:
            long.append(coords[0])
            lat.append(coords[1])
        tag='ID:'+entry+'\n'+unidecode(json.dumps(elements["Way"][entry]["tags"],ensure_ascii=False,indent=2)).replace('{','').replace('}','').replace('\\"','')
        line=[long,lat,tag]
        lines.append(line)
    return lines




def create_CSVPlotPoints(elementlist,nodelist):
    ''' Convert CSV Objects to plotable points '''
    long=[]
    lat=[]
    tag=[]
    for element in elementlist:
        for node in nodelist:
            if element.id == node.id:
                long.append(node.long)
                lat.append(node.lat)
                tag.append(node.id)
    #plotobj=[long,lat,tag]
    return long,lat,tag




def create_CSVPlotLines(linelist,nodelist):
    '''Convert CSV Objects to plotable lines '''
    long=[]
    lat=[]
    tag=[]
    linename=''
    pipes=[]
    for line in linelist:
        if line.name != linename:
            pipe=[long,lat,linename]
            pipes.append(pipe)
            linename=line.name
            long=[];lat=[];tag=[]
        for node in nodelist:
            if line.node_id == node.id:
                long.append(node.long)
                lat.append(node.lat)
                tag.append(node.id)
    pipes.append(pipe)
    return pipes







