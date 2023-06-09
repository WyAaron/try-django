import os
import modules.sqlite3.serverDButil as serverDButil


def get_start_of_file(fileSize):
    pass

def filter_node_list():
    pass


#---------------GET MAXIMUM FILE TO STOR IN THE NODE------------------
def getMaxFile(mdList, storSize):
    fragments = fragmentCheck(mdList, storSize)
    largest = 0
    
    #print(fragments)
    for i in fragments:
        if i[1] - i[0] > largest:
            largest = i[1] - i[0]
    return largest



#-----------------Fragmented Check-----------------------
def fragmentCheck(mdList, storSize):
    #sort json list based on start point to sort the files
    if mdList:
        jsonList = sorted(mdList, key=lambda k: k["start"])
    else:
        jsonList = mdList
    
    
    prev_end = 0
    spaceBetweenFiles  = []
    
    for file in jsonList:
        # Calculate the end byte of the current file
        endByte = file["start"] + file["actualSize"]
        
        #calculate if there is a gap between the previous file and the current file
        if file["start"] != 0:
            space_start = prev_end
            space_end = file["start"]
            
            #if there is a gap append the gap to the list of gaps
            if (space_end - space_start) != 0:
                spaceBetweenFiles.append((space_start,space_end))
        
        prev_end = endByte
    
    #get the size between the last file and the storage location
    space_start = prev_end
    space_end = storSize
    spaceBetweenFiles.append((space_start,space_end))
    
    return spaceBetweenFiles




def get_storage_nodes(partNames,cwd):
    
    allNodes = serverDButil.getAllStorageNodes()
    
    
    
    #REMOVE ARCHIVE NODE FROM THE LIST OF ALL NODES
    allNodes = [item for item in allNodes if item["SID"] != "ARCHIVE"]
        
    
    
    print(len(allNodes))
    
    
    
    file_and_node_tuple_list = []
    file_and_node_tuple_list = []
    for partName in partNames:

        file_size = os.path.getsize(os.path.join(cwd, partName))
        
        to_up_storage_node = None
        
        for storage_node in allNodes:
            files_in_node = serverDButil.get_all_files_by_sid(storage_node["SID"])
            
            
            #SKIP THE NODE IF THE NODE IS OFFLINE OR IF THE NODE HAS A SMALLER MAXIMUM SIZE THAT CAN BE STORED
            if storage_node["status"] == False:
                continue
            
            elif getMaxFile(files_in_node, storage_node["allocSize"]) < file_size:
                continue
            
            
            node_allocated_size = storage_node["allocSize"]
            gap_list = fragmentCheck(files_in_node, node_allocated_size)
            
            
            #FIND THE SMALLES SPACE IN THE NODE
            newSmallestSpace = None
            for space in gap_list:
                
                if (space[1]- space[0]) >= file_size:
                    #CHECK IF THE NEW FOUND SPACE IS SMALLER THAN THE PREVIOUS SPACE
                    if newSmallestSpace is None or space[1]-space[0] < smallestSpaceBetween:
                        newSmallestSpace = space
                        smallestSpaceBetween = space[1]-space[0]
                        #print(f"SID: {storage_node['SID']} Smallest Space:{smallestSpaceBetween}")
            
            #CHECK IF NEW FOUND SPACE IN THE NEW NODE IS SMALLER THAN PREVIOUSLY FOUND SPACE
            
            if to_up_storage_node is None:
                to_up_storage_node = {"storageNode": storage_node , "Gap": newSmallestSpace}
                
            else:
                
                
                
            
                to_up_SID = to_up_storage_node['storageNode']['SID']
                to_up_total_size = to_up_storage_node['storageNode']['allocSize']
                to_up_file_list = serverDButil.get_all_files_by_sid(to_up_SID)
                
                totalUsed = 0
                
                for i in to_up_file_list:
                    totalUsed += i['actualSize']
                
                to_up_total_remaining_size = to_up_total_size - totalUsed
                
                totalUsed = 0
                for i in files_in_node:
                    totalUsed += i['actualSize']
                
                current_node_remaining_size = storage_node['allocSize'] - totalUsed
                
                
                if (current_node_remaining_size > to_up_total_remaining_size):
                    to_up_storage_node = {"storageNode": storage_node , "Gap": newSmallestSpace} 
                
        
                
            
                
                #print(f"newSmallestSpace: {newSmallestSpace[1] - newSmallestSpace[0]} current: {to_up_storage_node['Gap'][1] - to_up_storage_node['Gap'][0]}")  
        
        #IF THERE WAS NO NODE FOUND END FUNCTION AND RETURN NONE
        if to_up_storage_node == None:
            return None
        
        file_and_node_tuple_list.append({"fName": partName, 
                                         "storage_info":to_up_storage_node})

        #REMOVE SELECTED NODE FROM THE LIST OF POSSIBLE NODES
        allNodes = [item for item in allNodes if item["SID"] != to_up_storage_node["storageNode"]["SID"]]

    
    return file_and_node_tuple_list
            

    

            



    
    
    
  