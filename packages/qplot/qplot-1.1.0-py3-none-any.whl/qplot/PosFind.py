import array    		    as arr

def find_pos_StringInList(String, ListOfStrings, Str2Lower = False):
    """Find positions, where string is equal to a string in a list.  Input are **String**, and **ListOfStrings**
    and boolean **Str2Lower**.
	
    \n.. comments: 
    Input:
        String:          	String, 
        ListVonStrings:  	List of strings 
		Str2Lower: 			Boolean re converting strings to lower.
							(default = False)
    Return:
        pos:             	An array of type Integer, containing positions, where String were found in ListOfStrings."""

    # Initializierung von Variabeln
    pos = arr.array('i', [])
    
    if Str2Lower == False:
        if type(String) == str:
            count = 0
            
            for Name in ListOfStrings:
                if String == Name:
                    pos.append(count)
                count = count + 1
                
        elif type(String) == list:
            
            for Str in String:
                count = 0
                for Name in ListOfStrings:
                    if Str == Name:
                        pos.append(count)
                    count = count + 1
        else:
            print('ERROR: M_FindPos.find_pos_StringInList: Code noch NICHT geschrieben 1')
    else:
        if type(String) == str:
            count = 0
            String = String.lower()
            
            for Name in ListOfStrings:
                if Name is not None:
                    if String == Name.lower():
                        pos.append(count)
                count = count + 1
                
        elif type(String) == list:
            
            for Str in String:
                count = 0
                Str = Str.lower()
                for Name in ListOfStrings:
                    if Name is not None:
                        if Str == Name.lower():
                            pos.append(count)
                    count = count + 1
        else:
            print('ERROR: M_FindPos.find_pos_StringInList: Code noch NICHT geschrieben 2')
        
    return pos

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
