from . import K_Netze, K_Component 
from . PosFind import find_pos_StringInList
import os
import pandas as pd
import numpy as np
from pathlib import Path
import math

def read(RelDirName = 'Eingabe/CSV/', NumDataSets = 1e+100, 
          skiprows = [], NetzName = None, NameStart = 'Gas'):
    """Description:
    ------------
        Reads Data from folder CSV_Path into Grid
        Grid = Instance of Netz Class

    Input Parameter:
    ----------------
        RelDirName    string containing path name of data location [default: 'Eingabe/CSV/']
        NumDataSets   Number of elements to be read for each component [default: 1e+100]
        skiprows      number of rows to skip [default: []]
        NetzName      String containing the nme of the network
                      [Default = None]
        NameStart     String, containing the file name start of the files
                      [Default = 'Gas']

        SourceName
    Return Parameters:
    ------------------
        Grid            instance of class K_Netze.Netz, populated with
                         data from CSV files  """
    # Dir name stuff
    DirName     = Path.cwd() /  RelDirName
    if not os.path.isdir(DirName):
        print("RelDirName does not exist")

    Grid        = K_Netze.NetComp()
    FileList    = K_Netze.NetComp().CompLabels()
    for key in FileList:
        count       = 0
        filename    = NameStart + '_' + key + '.csv'
        CSV_File    = str(DirName / filename)

        # Z set to zero if file does not exist
        Z           = CSV_2_list(CSV_File, skiprows = skiprows)
        if len(Z) > 0:
            for entry in Z:
                Keys    = list(entry.keys())
                Vals    = list(entry.values())
                for ii in range(len(Vals)):
                    if Vals[ii] == 'None':
                        Vals[ii] = None
                    elif type(Vals[ii]) is float:
                        if math.isnan(Vals[ii]):
                            Vals[ii] = None
                    else:
                        try:
                            Vals[ii] = float(Vals[ii])
                        except:
                            pass

                pos_Id   = find_pos_StringInList('id', Keys)
                pos_Name = find_pos_StringInList('name', Keys)
                pos_SId  = find_pos_StringInList('source_id', Keys)
                pos_Node = find_pos_StringInList('node_id', Keys)
                pos_CC   = find_pos_StringInList('country_code', Keys)
                pos_lat  = find_pos_StringInList('lat', Keys)
                pos_long = find_pos_StringInList('long', Keys)
                pos_comm = find_pos_StringInList('comment', Keys)
                pos_para = find_pos_StringInList('param', Keys)
                pos_meth = find_pos_StringInList('method', Keys)
                pos_unce = find_pos_StringInList('uncertainty', Keys)
                pos_tags = find_pos_StringInList('tags', Keys)

                # in case that license information is in file
                pos_license = find_pos_StringInList('license', Keys)

                del entry['id']
                try:
                    del entry['name']
                
                    del entry['source_id']
                    del entry['node_id']
                    del entry['country_code']

                    del entry['lat']
                    del entry['long']
                except: 
                    #print('warning no value to delete')
                    pass
                try:
                    del entry['comment']
                    del entry['param']
                    del entry['method']
                except:
                    #print('warning no  comment to delete')
                    pass
                try:
                    del entry['uncertainty']
                    del entry['tags']

                except:
                    #print('warning no  uncertainty to delete')
                    pass
                # in case that license information is in file
                try:
                    del entry['license']
                except:
                    pass


                name        = Vals[pos_Name[0]]
                source_id   = makeList(Vals[pos_SId[0]])
                node_id     = makeList(Vals[pos_Node[0]])
                country_code = makeList(Vals[pos_CC[0]])
                
                try:
                    id          = Vals[pos_Id[0]]

                except:
                    id = id

                lat         = Vals[pos_lat[0]]
                if isinstance(lat, str):
                    lat         = eval(lat)

                long        = Vals[pos_long[0]]
                if isinstance(long, str):
                    long        = eval(long)

                try:
                    comment     = Vals[pos_comm[0]]
                except:
                    #print('warning no  comment to read')
                    comment={}
                    pass
                try:
                    param       = eval(Vals[pos_para[0]].replace(': nan,', ': float(\'nan\'),'))
                    method      = eval(Vals[pos_meth[0]].replace(': nan,', ': float(\'nan\'),'))
                except:
                    #print('warning no  value to delete')
                    pass
                try:
                    uncertainty = eval(Vals[pos_unce[0]].replace(': nan,', ': float(\'nan\'),'))
                    tags        = eval(Vals[pos_tags[0]].replace(': nan,', ': float(\'nan\'),'))

                except:
                    #print('warning no  uncertainty to delete')
                    uncertainty={}
                    pass
                # in case that license information is in file
                if len(pos_license) > 0:
                    license_val = eval(Vals[pos_license[0]].replace(': nan,', ': float(\'nan\'),'))
                else:
                    license_val = {}

                Grid.__dict__[key].append(K_Component.__dict__[key](id = id,
                             name       = name,
                             source_id  = source_id,
                             node_id    = node_id,
                             country_code = country_code,
                             param      = param,
                             lat        = lat,
                             long       = long,
                             method     = method,
                             uncertainty = uncertainty,
                             tags       = tags,
                             comment    = comment))
                # In case that license information is given
                if license_val != {}:
                    Grid.__dict__[key][count].license = license_val
                count = count + 1
                if count >= NumDataSets:
                    break
        else:
            Grid.__dict__[key]      = []
    Grid.SourceName = [NetzName]
    return Grid

def CSV_2_list(file, skiprows = []):
    """Description:
    ------------
        Liest ein Netzattribute aus einer CSV-datei (file) als Dataframe ein
        und liefert eine Liste zurück
    Parameter:
    -----------
        file = filepath+name.csv (des Netzattributes)
    Needs:
    -------
        Panda Library
    called by:
    -----------
        read_CSV()
    """
    if os.path.isfile(file):
        with open(file,'rt', encoding = 'iso-8859-15', errors = 'ignore') as csvfile:
            df = pd.read_csv(csvfile, sep =';', skiprows = skiprows)
            liste = []
            liste = df.T.to_dict().values()

            return liste
    else:
        return []

def makeList(stringVal):
    """Function to convert a string values into a list"""

    listVal = []
    if stringVal != None:
        if isinstance(stringVal, str):
            if '[\'' in stringVal and '\']' in stringVal:
                stringVal = stringVal[1:-2]
                stringVal   = stringVal
                stringVal   = stringVal.replace('\', \'', '\',\'')
                for val in stringVal.split(','):
                    if val[0] == '\'':
                        val = val[1:]
                    if val[-1] == '\'':
                        val = val[:-1]
                    listVal.append(val)
            else:
                listVal = stringVal
        else:
            listVal = stringVal

    else:
        listVal = stringVal

    return listVal
