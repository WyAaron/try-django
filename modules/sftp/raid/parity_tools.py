import os
import threading
import shutil

import modules.sftp.sftp_tools as sftp_tools
import modules.nodeTools.getTools as NodeGetTools
import modules.RAIDmod as raid_module
import modules.sqlite3.serverDButil as serverDButil

from CVSMS.models import  Files,storageNodeInfo



class thread_get(threading.Thread):
    def __init__(self, obj):
        # execute the base constructor
        threading.Thread.__init__(self)
        self.obj = obj

    def run(self):
        file_list = serverDButil.getFileMD(self.obj.FID)
        #SORT FILE LIST BY NAME
        file_list = sorted(file_list, key=lambda x: x['fName'])

       
        #GET THE CWD OF THE FILE
        cwd = os.path.dirname(self.obj.file.path)
        
        
        
        fileMD_nodeList_tuple = []
        
        #GET THE STORAGE NODE 

        for fileMD in file_list:
            if fileMD["RAIDid"] != -1:
                node = serverDButil.getStorageNode(fileMD["SID"])
                if node["status"]:
                    fileMD_nodeList_tuple.append({"fileMD":fileMD, "node":node}) 
               
                    
        if len(fileMD_nodeList_tuple) < 2:
            shutil.rmtree(cwd)
            print("Not enough storage nodes are up, Cannot download all the files in this RAID")
        elif len(fileMD_nodeList_tuple) < 3:
            print("Some nodes are missing attempting to download and repair the files...")
            
            for i in fileMD_nodeList_tuple:
                
                fileMD = i["fileMD"]
                storageNode = i["node"]
                
                
                
                message = {
                    "fName": fileMD["fName"],
                    "FID" : fileMD["FID"],
                    "command" : "download",
                    "cwd" : cwd
                    }
                
                #CONDITION CHECKER FOR SFTP IF SUCCESSFUL
                success = True
                
                try:
                    #CHECK IF FILE IS IN CACHE
                    if not os.path.isfile(os.path.join(cwd, fileMD["fName"])): #condition for file DNE in server
                        print(f'file is not in cache downloading...')
                        #GET THE FILES
                        sftp_tools.get(message, storageNode)
                    else:
                        print("Part Exists")
                        
                except Exception as e:
                    print(e)
                    print("ERROR DOWNLOADING FILES TO BE RAIDED")
                    success = False
                    shutil.rmtree(cwd)
                    break
                
                
            if not success:
            #SORT THE FILES BY RAID ID
                print("ERROR IN SFTP")
            else:
                fileList = [fileMD_nodeList_tuple[0]["fileMD"]["fName"], fileMD_nodeList_tuple[1]["fileMD"]["fName"]]
                print(fileList)
                raid_module.pRAID.repair(self.obj.fName, fileList[0][-1], fileList[1][-1], cwd)
                fileList = [f"{self.obj.fName}-0",f"{self.obj.fName}-1"]
                raid_module.pRAID.merge(self.obj.fName, fileList, cwd)
                
                pass
            
            
        else:
            
            
            for i in fileMD_nodeList_tuple:
                
                fileMD = i["fileMD"]
                storageNode = i["node"]
                
                print(fileMD["fName"][-2:])
                pass
            
            print("Downloading..")
            
        
        
        
        
        
        
        
        # for fileMD in file_list:
        #     # print(fileMD["RAIDid"])
        #     if fileMD["RAIDid"] != -1:
        #         storageNode = serverDButil.getStorageNode(fileMD["SID"])

          
            
        pass