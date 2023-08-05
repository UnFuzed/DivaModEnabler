#DivaModEnabler
#UnFuzed


import os
import subprocess
import platform
import PySimpleGUI as psg
import textwrap as tw

psg.theme("DarkBlue14")


#get mod folder names

try:
    mod_folders = os.listdir(os.getcwd() + '/mods')
    
except: 
    psg.PopupError("No mods folder located")
    exit()
    
#window layout
column_one = [[psg.Listbox(mod_folders, default_values = mod_folders[0], size = (50, 20), key = "--List--", enable_events = True),],
              [psg.Text("Log: "), psg.Text("", key = "--Text--", size = 30, pad = 10)],
              [psg.Button("Enable All", size = (20, 2), border_width = 5), psg.Button("Disable All", size = (20, 2), border_width= 5)],
              ]
              
column_two = [[psg.Push(), psg.Text("Mod Name", key = "--Name--", font = ("Arial", 15, "bold"), size = 30, justification = "center"), psg.Push()],
              [psg.Checkbox("Enabled",True, enable_events = True, key = "--Check--"), psg.Button("Open", size = (10, 1), border_width = 5)],
               [psg.Multiline("", key = "--Viewer--", size = (50, 17), enable_events = True, border_width = 5)],
               [psg.Text("", size = 30, pad = 10)],
               [psg.Push(), psg.Button("Reset Folders", size = (20, 2), border_width= 5)]]

layout = [[psg.Column(column_one),
           psg.VSeparator(),
           psg.Column(column_two)]]

window = psg.Window("DivaModEnabler", layout, grab_anywhere = True, enable_close_attempted_event=True, titlebar_icon = "", finalize = True)


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 


def update_mod_enable(select):
    with open(os.getcwd() + "/mods/" + select + "/" + "config.toml", "r") as file:
            contents = file.read()
            
    window["--Viewer--"].update(contents)


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 


#function to check if a mod is disabled/enabled or not a real mod
def check_mod(select):
    
    window["--Name--"].update(tw.fill(select, 30))
    
    try:
        #tries to open the config.toml of the mod
        with open(os.getcwd() + "/mods/" + select + "/" + "config.toml", "r") as file:
            contents = file.read()
            
    except:
        #disables checkbox and makes it false for any mod without a config.toml
        window["--Check--"].update(False)
        window["--Check--"].update(disabled = True)
        
        
    else:
        
        window["--Viewer--"].update(contents)
        
        
        #if found true update checkbox to be checked
        if contents.find("enabled = true") != -1:
            window["--Check--"].update(True)
            window["--Check--"].update(disabled = False)
            
        #if found false update checkbox to be unchecked
        elif contents.find("enabled = false") != -1:
            window["--Check--"].update(False)
            window["--Check--"].update(disabled = False)
            
        
        else: 
            
            window["--Text--"].update("Missing enabled config.toml line")
            
        
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
        
        #checks for a DLL file in the mod and include = line
        for files in os.listdir(os.getcwd() + "/mods/" + select):
            
             #if there is a DLL file and there is no line for it in the config.toml.
            if ".dll" in files and files.count(".") < 2:
                
                if contents.find(f'dll = [') == -1:
                      
                    #user error messaging  
                    window["--Text--"].update(select + " is missing the dll config.toml line")
                    
                        
            #if there is a rom folder and there is no line for it in the config.toml
            if "rom" in files:
                
                if contents.find('include = [') == -1:
                    
                    #user error messaging 
                    window["--Text--"].update(select + " is missing the include config.toml line")
                    
          
        
 #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------          
          
                
                
#checks first mod on start up
check_mod(mod_folders[0])          
                    
#main loop
while True:
        
    event, values = window.read()
    window["--Text--"].update("")
        
    #close window
    if event == psg.WINDOW_CLOSE_ATTEMPTED_EVENT:
        break
    
    
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    
    #resets the listbox with updated folders
    if event == "Reset Folders":
        mod_folders = os.listdir(os.getcwd() + '/mods')
        window["--List--"].update(mod_folders)
        window["--List--"].update(set_to_index = 0)
        
        window["--Text--"].update("Reset mod folder")
        
        #checks the first mod in the list to see if its enabled or not
        check_mod(mod_folders[0])
   
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
      
    #if clicking on new mod name
    if event == "--List--":
        check_mod(values["--List--"][0])


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
               
    if event == "--Check--":
        
        #opens the config.toml to check if its enabled or disabled  
        with open(os.getcwd() + "/mods/" + values["--List--"][0] + "/" + "config.toml", "r") as file:
            contents = file.read()
            
        #checks if they should disable or enable the mod
        match values["--Check--"]:
            
            case True:
            
                new_entry = contents.replace("enabled = false", "enabled = true")
                window["--Text--"].update("Enabled " + values["--List--"][0])

            case False:
            
                new_entry = contents.replace("enabled = true", "enabled = false")
                window["--Text--"].update("Disabled " + values["--List--"][0])

        #writes the new config.toml text
        with open(os.getcwd() + "/mods/" + values["--List--"][0] + "/" + "config.toml", "w") as file:
            file.write(new_entry)
            
        update_mod_enable(values["--List--"][0])
    
    
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
    
        
    if event == "--Viewer--":
        
        #writes new entry into config.toml
        with open(os.getcwd() + "/mods/" + values["--List--"][0] + "/" + "config.toml", "w") as file:
            file.write(values["--Viewer--"])
        
        #makes sure the file gets saved
        file.close()
        
     
        
        #checks to see if the new entry is enabled/disabled or missing 
        with open(os.getcwd() + "/mods/" + values["--List--"][0] + "/" + "config.toml", "r") as file:
            contents = file.read()
        
        
        #if found true update checkbox to be checked
        if contents.find("enabled = true") != -1:
            window["--Check--"].update(True)
            
        #if found false update checkbox to be unchecked
        elif contents.find("enabled = false") != -1:
            window["--Check--"].update(False)        
        
        else: 
            window["--Check--"].update(False)    
            window["--Text--"].update("Missing enabled config.toml line")
       
       
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  
       
          
    #enabling all mods  
    if event == "Enable All":
        for mod in os.listdir(os.getcwd() + "/mods"):
        
            try:
                with open(os.getcwd() + "/mods/" + mod + "/" + "config.toml", "r") as file:
                    contents = file.read()
            except:
                pass
                
            else:
                
                new_entry = contents.replace("enabled = false", "enabled = true")
                window["--Text--"].update("Enabled all mods")
                window["--Check--"].update(True)
                    
            
                with open(os.getcwd() + "/mods/" + mod + "/" + "config.toml", "w") as file:
                    file.write(new_entry)
                    
                update_mod_enable(values["--List--"][0])
                    
    
   #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
   
       
    #disabling all mods      
    if event == "Disable All":
        for mod in os.listdir(os.getcwd() + "/mods"):
            
            try:
                with open(os.getcwd() + "/mods/" + mod + "/" + "config.toml", "r") as file:
                    contents = file.read()
            except:
                pass
                
            else:
                new_entry = contents.replace("enabled = true", "enabled = false")
                window["--Text--"].update("Disabled all mods")
                window["--Check--"].update(False)
                    
            
                with open(os.getcwd() + "/mods/" + mod + "/" + "config.toml", "w") as file:
                    file.write(new_entry)
                    
                    
                update_mod_enable(values["--List--"][0])
              

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                 
      
#When opening the mod folder      
    if event == "Open":
        
        match platform.system():
        
            case "Windows":  os.system('explorer "%s"' % os.getcwd() + "/mods/" + values["--List--"][0])
            
            case "Linux": os.system('xdg-open "%s"' % os.getcwd() + "/mods/" + values["--List--"][0])
            
        
        
        
        
    
        
        
    
    
    
    
    
    