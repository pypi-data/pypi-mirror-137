# -*- coding: utf-8 -*-
"""
Net class
*********
"""

from __future__ import print_function
from . import K_Component as K_Component


import copy
import ast






class NetComp(object):
    """Main class **NetComp**. Class containing components such as **BorderPoints** or
    **Compressors**, used for the non-OSM data set.
    """
    
    
    def __init__(self):
        Comps=['BorderPoints','Compressors', 'Consumers', 'LNGs','Nodes','PowerPlants','Productions','PipePoints','PipeSegments', 'PipeLines','Storages'] 
        self.SourceName             = ['']
        for comp in Comps:
            setattr(self,comp,[])
        self.Processes              = []



    def copy2(self):
        """Method of creating a true independent copy of a class instance.
        """
        RetNetz      = NetComp()

        RetNetz      = copy.deepcopy(self)

        return RetNetz

    def AttribLables(self):
        return ['id', 'name', 'source_id', 'node_id', 'lat', 'long', 'country_code', 'comment']

    def CompLabelsSpot(self):
        return ['Compressors', 'Consumers',
                'BorderPoints', 'LNGs', 'Storages', 'PowerPlants','Productions' ]

    def CompLabelsPipes(self):
        return ['PipeSegments', 'PipeLines']

    def CompLabelsNoNodes(self):
        return [*self.CompLabelsSpot(), *self.CompLabelsPipes(),
                'PipePoints']

    def CompLabels(self):
        return ['Nodes', *self.CompLabelsNoNodes()]





    def copy(self):
        """Method to create copy of instance.
        """

         # BookKeeping
        self.Processes.append(K_Component.Processes('K_Netze.Netz..copy: Creation of copy of  Netze instance'))

        # Initialization
        self2 = NetComp()
        try:
            for key in sorted(self.__dict__.keys()):
                if self.__dict__[key] is not None:
                    for dd  in self.__dict__[key]:
                        self2.__dict__[key].append(dd)
        except:
            pass
        return self2


    def getcountry4pipelines(self):
        """Method of getting pipeline CountryCode from Nodes-list exists
        """

        for i in range(len(self.PipeLines)):
            countrycodelist=[]
            for id in self.PipeLines[i].node_id:
                countrycode=self.Nodes[ast.literal_eval(repr(self.Nodes)).index(id)].country_code
                countrycodelist.append(countrycode)
            self.PipeLines[i].country_code=countrycodelist
        print('Got countrycodes for pipelines from nodes list')
        pass




    def para(self, element,parameter):
        """ Returns valuelist of a p from an element type
        """
        liste=[]
        print(element,'-',parameter,':')
        for single_element in self.__dict__[element]:
            liste.append(single_element.param.get(parameter))
        return liste


    def get_elevations(self):
        """Method uses bing api to get elevation of Nodes and write them to param dictionary elevation_m
        """
        from Code.M_Elevation import get_elevation
        nodelist=[]
        for node in self.Nodes:
            nodelist.append([node.lat,node.long])
        elevationlist=get_elevation(nodelist)
        for elevationVal, node in zip(elevationlist,self.Nodes):
            node.param.update({'elevation_m':elevationVal})
            node.method.update({'elevation_m':'bing API'})
            node.uncertainty.update({'elevation_m': 0})
        pass



    def rename_nodes(self,prestring='LKD_'):
        """Renaming of Node ids in Network
        """
        newnodelist=[]
        complist=self.CompLabels()
        for component in complist:
            for element in self.__dict__[component]:
                newnodelist=[]
                for node in element.node_id:
                    newnodelist.append(prestring+node)
                element.node_id=newnodelist

        complist=self.CompLabelsSpot()+['Nodes',]
        for component in complist:
            for element in self.__dict__[component]:
                element.id=(prestring+element.id)
        pass


    def all(self,component='',param='',verbose=True):
        """Method of displaying of all attributes from the NetComp class instance.
        """

        # checking how many components have more than zero element
        for key in self.__dict__.keys():
            # print(key)
            # if len(self.__dict__[key]) > 0:
            CompCount =  len(self.__dict__[key])
        if verbose==True:
            print("--------------------------------------")
            print("{0:30s} {1:>6s}".format('Source ', str(self.SourceName[0])))
            print("{0:30s} {1:>6s}".format('total component type count',str(CompCount)))
            print("--------------------------------------")
            for key in sorted(self.__dict__.keys()):
                if key == 'SourceName':
                    pass
                else:
                    print("{0:30s} {1:>6s}".format(key, str(len(self.__dict__[key]))))

            print("--------------------------------------")
            print("{0:30s} {1:>6s}".format('Length of PipeLines    [km]', str(round(self.sumLength('PipeLines')))))
            print("{0:30s} {1:>6s}".format('Length of PipeSegments [km]', str(round(self.sumLength('PipeSegments')))))
        if (component and param) !='':
            tagliste=[]
            for element in self.__dict__[component]:
                if verbose==True:
                    print(element.__dict__[param])
                tagliste.append(element.__dict__[param])
            return tagliste
        
            
        


    def sumLength(self, compName = 'PipeLines'):
        """Method returning total sum length of all pipeline/pipeSegment in units of [km]."""

        RetSum = 0

        for pipe in self.__dict__[compName]:
            if 'length_km' in pipe.param:
                if pipe.param['length_km'] != None:
                    RetSum = RetSum + float(pipe.param['length_km'])
        return RetSum


    def select2(self,CompName,AttribName,AttribVal):
        liste=[]
        for item in self.__dict__[CompName]:
            if AttribVal in item.__dict__[AttribName]:
                liste.append(item)
                #self2.__dict__[CompName].append(item.__dict__[AttribName])
        return liste


    def select_with_exception(self,CompName,AttribName,AttribVal,exceptionlist):
        liste=[]
        for item in self.__dict__[CompName]:
            if AttribVal in item.__dict__[AttribName] or item.id in exceptionlist:
                liste.append(item)
                #self2.__dict__[CompName].append(item.__dict__[AttribName])
        return liste

    def select(self,CompName,AttribName,AttribVal):
        
        for item in self.__dict__[CompName]:
            if AttribVal == item.__dict__[AttribName]:
                return item
                #self2.__dict__[CompName].append(item.__dict__[AttribName])
                #yield item

    def reduce(self, AttribVal, AttribName = 'country_code'):
        '''Method of reducing data to a country specified by AttribVal=country_code  
        \n.. comments:
            Input:
				AttribVal: 		Attribute value
				AttribName: 	String of attribute name
								(default = 'country_code')'''
		
        self2 = self.copy()
        #reduce all PipeLines and PipeSegments

        if AttribVal=='EU' and AttribName=='country_code':
            return self2
        else:
            CompNames=self.CompLabelsPipes()
            
            nodes_to_keep=[]
            for compname in CompNames:
                self2.__dict__[compname]=self.select2(CompName=compname,
                                                      AttribName = AttribName,
                                                      AttribVal = AttribVal)
                                                      

                for comp in self2.__dict__[compname]:
                    nodes_to_keep+=comp.node_id

            # create ID List of points to keep

            PointCompNames = self.CompLabels()
            for compname in PointCompNames:  
                self2.__dict__[compname]=self.select_with_exception(CompName=compname,
                                                      AttribName = AttribName,
                                                      AttribVal = AttribVal,
                                                      exceptionlist=nodes_to_keep)       
      
                    
                                                      
            print('Reduce data to Country:', AttribVal)
            return self2


    def select_from_param(self,CompName,AttribName,AttribVal):
        for item in self.__dict__[CompName]:
            if AttribVal == item.param[AttribName]:
                return item

        return False

    def path2coords(self,CompName):
        for pipe in self.__dict__[CompName]:
            pipe.lat=pipe.param['path_lat']
            pipe.long=pipe.param['path_long']
        pass

    def Emap_path2coords(self,CompName):
        for pipe in self.__dict__[CompName]:
            pipe.lat=pipe.lat[0],*pipe.param['path_lat'],pipe.lat[-1]
            pipe.long=pipe.long[0],*pipe.param['path_long'],pipe.long[-1]
        pass


    def select_from_Pipelines(self,CompName,AttribName,AttribVal):
        for item in self.__dict__[CompName]:
            if AttribVal in item.__dict__[AttribName]:
                pos=item.__dict__[AttribName].index(AttribVal)
                point={}
                point.update({'id':AttribVal})
                point.update({'lat':item.__dict__['lat'][pos]})
                point.update({'long':item.__dict__['long'][pos]})
                point.update({'country_code':item.__dict__['country_code'][pos]})
                return point
        return False

    def search(self,CompName,AttribName,AttribVal):
        for item in self.__dict__[CompName]:
            if AttribVal in item.__dict__[AttribName]:
                return item


    def getElem(self,CompName,AttribName,AttribVal):
        """Returns the element for which a requested attribute value could be found
        """
        for item in self.__dict__[CompName]:
            if AttribVal in item.__dict__[AttribName]:
                return item
        return None


    def Lines2Nodes(self,Line='PipeLines',Node="Nodes"):
        """ Creating Point from Line Element
        """
        def non_existing_nodes(Nodelist,Newnodes):
            non_existing_nodes=[]
            for newnode in Newnodes:
                flag=False
                for node in Nodelist:
                    if node.id==newnode.id:
                        flag=True
                if flag==False:
                    non_existing_nodes.append(newnode)
            return non_existing_nodes

        nodes=[]
        # Checking for the first two PipePoints
        for pipe in self.__dict__[Line]:
            for i,node in enumerate(zip(pipe.lat,pipe.long)):
                print(i,pipe.id,sep=' ')
                nodes.append(K_Component.__dict__['Nodes'](
                          id        = pipe.node_id[i],
                          name      = pipe.node_id[i],
                          source_id = [pipe.id],
                          node_id   = pipe.node_id[i],
                          country_code = pipe.country_code[i],
                          lat       = node[0],
                          long      = node[1]))
        #Only add non existing nodes
        for node in non_existing_nodes(self.__dict__[Node],nodes):
            self.__dict__[Node].append(node)
        pass



    def PipeLines2PipeSegments(self):
        """Method of converting PipeLines to PipeSegments.
        And changing length value of PipeSegments
        """

        RetPipeSegments = []

        # Checking for the first two PipePoints
        for pipe in self.PipeLines:
            if len(pipe.node_id) == 2:
                RetPipeSegments.append(K_Component.PipeSegments(id = pipe.id,
                                name        = pipe.name,
                                source_id   = pipe.source_id,
                                node_id     = pipe.node_id,
                                lat         = pipe.lat,
                                long        = pipe.long,
                                country_code = pipe.country_code,
                                param       = pipe.param.copy()))
            else:
                for ii in range(len(pipe.node_id) - 1):
                    if pipe.lat == None:
                        RetPipeSegments.append(K_Component.PipeSegments(id = pipe.id + "_EE_" + str(ii),
                                name        = pipe.name+str(ii),
                                source_id   = pipe.source_id,
                                lat         = None,
                                long        = None,
                                node_id     = pipe.node_id[ii : ii+2],
                                country_code = pipe.country_code,
                                param       = pipe.param.copy()))
                    else:
                        print('ERROR: K_Netze.PipeLines2PipeSegments: code not written yet, as lat long missing.')
                        RetPipeSegments.append(K_Component.PipeSegments(id = pipe.id + "_EE_" + str(ii),
                                name        = pipe.name+str(ii),
                                source_id   = pipe.source_id,
                                node_id     = pipe.node_id[ii : ii+2],
                                country_code = pipe.country_code,
                                param       = pipe.param.copy()))


        self.PipeSegments = RetPipeSegments
        self.replace_length(compName = 'PipeSegments')

        #return []


    def PipeSegments2PipePoints(self):
        """ Method of converting PipeSegments to PipePoints
            Not working probably, lat, long!!!
        """

        RetPipePunkte = []
        count = 0
        # Checking for the first two PipePoints
        for pipe in self.PipeSegments:
            RetPipePunkte.append(K_Component.PipePoints(id = pipe.id,
                          name      = pipe.name,
                          source_id = pipe.source_id,
                          node_id   = [pipe.node_id[0]],
                          country_code = pipe.country_code,
                          lat       = None,
                          long      = None))
            RetPipePunkte.append(K_Component.PipePoints(id = pipe.id,
                          name      = pipe.name,
                          source_id = pipe.source_id,
                          node_id   = [pipe.node_id[1]],
                          country_code = pipe.country_code,
                          lat = None,
                          long = None))
            count = count + 1
        self.PipePoints = RetPipePunkte





class NetComp_OSM(NetComp):
    """
    same as NetComp but more elements, [outdated]
    """    
    
    
    def __init__(self):
        Comps=['BorderPoints','Compressors', 'Consumers', 'LNGs','Nodes','PowerPlants', 'Productions','PipePoints','PipeSegments', 'PipeLines','Storages'] 
       
        self.SourceName             = ['']
        for comp in Comps: 
           setattr(self,comp,[])
        self.Processes              = []
    pass






