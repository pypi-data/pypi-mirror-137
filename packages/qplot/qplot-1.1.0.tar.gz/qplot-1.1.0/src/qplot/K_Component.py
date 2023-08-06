# -*- coding: utf-8 -*-
"""
Component Class
***************
"""

from . import M_DataAnalysis
import copy


def typcheck(x):
    if x == 'None':
        x = None

    if x is None:
        return x
    else:
        return float(x)
    pass



class Component(object):
    """Class **Component** with the following fixed attributes **id**, **name**, **source_id**, **node_id**,** country_code**,
	**lat**, **long**, and **comment**, and the following dicts, **tags**, **uncertainty**, **method**, **param**."""

    def __init__(self, id, name, source_id, node_id, country_code = None, lat = None, long = None, comment = None, tags = None, uncertainty = None, method = None, param = None):


        if lat is None:
            lat = None
        if long is None:
            long = None
        if tags is None:
            tags = {}
        if param is None:
            param = {}
        if uncertainty is None:
            uncertainty = {}
        if method is None:
            method = {}


        self.id             = id
        self.name           = name
        self.source_id      = source_id
        self.node_id        = node_id
        self.lat            = lat
        self.long           = long
        self.country_code   = country_code
        self.comment        = comment

        self.param          = param
        self.uncertainty    = uncertainty
        self.method         = method
        self.tags           = tags





    def copy2(self):
        """Method of creating a true independent copy of a class instance.
        """
        id          = self.id
        name        = self.name
        source_id   = self.source_id
        node_id     = self.node_id 
        
        RetElem      = Component(id = id, name = name, source_id = source_id, node_id = node_id)

        RetElem      = copy.deepcopy(self)

        return RetElem








    def get(self,value):
        return self.__dict__[value]

    def all(self,path=False):
        """Method to get info on component of Netz instancde"""
        for key in self.__dict__.keys():
            param=self.__dict__[key]
            if type(param)!=dict:
                print(key + ': ' + str(self.__dict__[key]))    
            if type(param)==dict:
                print(key + ': ')
                dict_list=list(param.items())
                for item in dict_list:         
                    if not (item[0] in ['path_lat','path_long']) or key!="param":
                        print('     '+ str(item))    
                    else:    
                        if len(item[1])<4:
                             print('     '+ str(item[0])+':',str(item[1]))
                            
                        else:
                            #print('     '+ str(item[0]))
                            print('     '+ str(item[0])+':[',str(item[1][0]),'+ {'+str(len(item[1])-2),'values} +'+str(item[1][-1])+']')
                        


    def __repr__(self):
        return str(self.name)


    def AttribLables(self):
        """Method that returns list of string, that are the attribute labels for the component."""
        return ['id', 'name', 'source_id', 'node_id', 'lat', 'long', 'country_code', 'comment']




    def getPipeLength(self):
        length = 0
        if self.lat == None:
            length = None
        else:
            for idx in range(len(self.lat)-1):
                length = length + M_DataAnalysis.distance(self.long[idx], self.lat[idx], self.long[idx+1], self.lat[idx+1])

        return round(length*1000)/1000




    def get_Attrib(self, attribName, removeNone = False):
        """Method to get attribute values from all elements of this component.
        **attribName** are the inputs, and a list of values will
        be returned. None values can be removed, but can be suppressed with
        **removeNone**.

        \n.. comments:
        Input:
            attribName:         string of attribute name/label
            removeNone:         Boolean of None shall be removed or not
                                [Default = False]
        Return:
            attribList:         list of values
        """
        attribList = []

        for elem in self:

            if attribName in elem.__dict__['param'].keys():
                if isinstance(elem.param[attribName], list):
                    for tt in elem.param[attribName]:
                        attribList.append(tt)
                else:
                    attribList.append(elem.param[attribName])
            elif attribName in elem.__dict__.keys():
                if isinstance(elem.__dict__[attribName], list):
                    for tt in elem.__dict__[attribName]:
                        attribList.append(tt)
                else:
                    attribList.append(elem.__dict__[attribName])
            else:
                return []

        # leave data as is and return
        if removeNone == False:
            return attribList

        # removes Nones, and then return
        else:
            attribList2 = []
            for val in attribList:
                if val != None:
                    attribList2.append(val)
            return attribList2



class BorderPoints(Component):
    """ Component Class BorderPoints"""


class Compressors(Component):
    """ Component Class Compressors"""


class ConnectionPoints(Component):
    """ Component Class ConnectionPoints"""


class Consumers(Component):
    """ Component Class Consumers"""


class EntryPoints(Component):
    """ Component Class EntryPoints"""


class InterConnectionPoints(Component):
    """ Component Class InterConnectionPoints"""


class LNGs(Component):
    """ Component Class LNGs"""


class Nodes(Component):
    """ Component Class Nodes"""


class Operators(Component):
    """ Component Class Operators"""


class PipeLines(Component):
    """ Component Class PipeLines"""


class PipePoints(Component):
    """ Component Class PipePoints"""


class PipeSegments(Component):
    """ Component Class PipeSegments"""

class PowerPlants(Component):
    """ Component Class PowerPlants"""


class Productions(Component):
    """ Component Class Productions"""


class Storages(Component):
    """ Component Class Storages"""


class Processes():
    def __init__(self, Commments):
        self.Commments  = Commments


class PolyLine():
    def __init__(self, long, lat):
        self.long = long
        self.lat  = lat



class MetaData(object):
    def __init__(self):
        self.BorderPoints           = []
        self.Compressors            = []
        self.EntryPoints            = []
        self.InterConnectionPoints  = []
        self.LNGs                   = []
        self.PipePoints             = []
        self.Storages               = []










# #class Component(object):
# def makeLine(X = [], Y = []):

#     polyLine        = PolyLine(lat = [], long = [])
#     polyLine.long   = X
#     polyLine.lat    = Y


#    return polyLine

class OSMComponent(Component):
    def __init__(self, id, name, source_id, node_id, lat, long, country_code, tags,param,uncertainty,method):
        self.id             = id
        self.name           = name
        self.source_id      = source_id
        self.node_id        = node_id
        self.lat            = lat
        self.long           = long
        self.country_code   = country_code
        self.tags           = tags
        self.param = param
        self.uncertainty = uncertainty
        self.method = method
        self.comments = None
 
 

        # for key in param:
        #     if key!= 'uncertainty' and key != 'method' and key != 'source' and key != 'license':
        #         self.uncertainty[key]  = None
        #         self.method[key] = None










