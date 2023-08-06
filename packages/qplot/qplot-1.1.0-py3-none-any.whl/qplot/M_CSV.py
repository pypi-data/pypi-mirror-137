

import numpy as np
import pandas as pd
import os

def CSV_Write(file, subkeys, subvalues):
    """Description:
    -------------
        Schreibt die Eigenschaften(subkeys) eines Netzattribute in ein File
        zusammen mit seinen werten (subvalues)
        file = filepath+name.csv (des Netzattributes)
    Input:
    ------
        file        String containing absolute path and name to file
        subkeys
        subvalues
    Called by:
    ----------
        WriteCSVfiles()

    Needs:
    ------
        Panda, Numpy
    """

    tsubvalues  = np.matrix(subvalues,dtype=object)
    tsubvalues  = np.transpose(tsubvalues)
    df          = pd.DataFrame(tsubvalues, subkeys,dtype=object)
    df.T.to_csv(file,sep=';', index = False, na_rep = 'None')


def write(Grid,NameStart,filepath):
    """Writes Instance of Netz-Class (**Grid**) into CSV tables, located in relative folder **RelDirName**.

..comments:
    Input:
        CSV_Path_write:  Output Directory
        Grid:          Instance of Netz Class
    Return:
        []
    """
    # dir name
    RelDirName=filepath
    dataFolder = os.getcwd()
    DirName = os.path.join(dataFolder, RelDirName)

    FileList = Grid.CompLabels()
    
    if not os.path.exists(os.path.dirname(RelDirName)):
        os.makedirs(os.path.dirname(RelDirName))

    
#    list(map(os.unlink, (os.path.join( DirName,f) for f in os.listdir(DirName)) ) )

    for key in FileList:
        # Resetting values
        subkeys             = []
        dictSubKeysParam    = []
        dictSubKeysMethod   = []
        subvalues           = []
        tempsubvalues       = []
        i                   = 0
        dictSubKeysUncertainty = []
        # groing through each component, as long as length larger than 0
        if len(Grid.__dict__[key]) > 0:
            for subkey in Grid.__dict__[key][0].__dict__.keys():
                if 'param' in subkey:
                    for subKey2 in Grid.__dict__[key][0].param.keys():
                        subkeys.append(subKey2)
                        dictSubKeysParam.append(subKey2)
                elif 'uncertainty' in subkey:
                    for subKey2 in Grid.__dict__[key][0].uncertainty.keys():
                        subkeys.append(subKey2)
                        dictSubKeysUncertainty.append(subKey2)
                elif 'method' in subkey:
                    for subKey2 in Grid.__dict__[key][0].method.keys():
                        subkeys.append(subKey2)
                        dictSubKeysMethod.append(subKey2)
                elif 'tags' in subkey:
                    for subKey2 in Grid.__dict__[key][0].tags.keys():
                        subkeys.append(subKey2)
                        dictSubKeysMethod.append(subKey2)
                elif 'license' in subkey:
                    for subKey2 in Grid.__dict__[key][0].tags.keys():
                        subkeys.append(subKey2)
                        dictSubKeysMethod.append(subKey2)
                else:
                    subkeys.append(subkey)

            # Loop for number of Components
            fileSubKeys = []
            if len(Grid.__dict__[key]) > 0:
                subkeys         = Grid.__dict__[key][i].__dict__.keys()
                for ss in subkeys:
                    fileSubKeys.append(ss)

            for i in range(len(Grid.__dict__[key])):
                subvalue        = Grid.__dict__[key][i].__dict__.values()
                tempsubvalues   = []
                for val, subkey in zip(subvalue, subkeys):
                    tempsubvalues.append(val)

                subvalues.append(tempsubvalues)
            if 'Meta_' in key:
                # Writing the compopnent meta data
                CSV_Write(os.path.join((DirName), key + '.csv'), fileSubKeys, subvalues)
            else:
                # Writing the component position data
                CSV_Write(os.path.join((DirName), NameStart + '_' + key + '.csv'), fileSubKeys, subvalues)
        else:
            pass

