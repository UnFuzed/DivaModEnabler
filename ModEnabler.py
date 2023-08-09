#Version 1.1
#DivaModEnabler
#UnFuzed

import os
import sys
import platform
import PySimpleGUI as psg
import textwrap as tw
import ast


mod_folders = []


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



#writes to viewer heo new contents of the config.toml
def update_mod_enable(select):
    with open(os.getcwd() + "/mods/" + select + "/" + "config.toml", "r") as file:
            contents = file.read()
            
    window["--Viewer--"].update(contents)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#checks priority line to see what mods should be loaded in what order 
def load_mods():
    global mod_folders
    try:

        mod_folders = os.listdir(os.getcwd() + '/mods')

    except Exception as error:
        psg.PopupError("Error! \nPlease have a 'mods' folder in the same location as DivaModEnabler", title = "DivaModEnabler")
        sys.exit()

    else:
        #exits if no mods are in mods folder
        if len(mod_folders) == 0:
            sys.exit()

            
    try:

        file = open("config.toml", "r+")
        contents = file.read()
   
    except:
        psg.PopupError("Error! \nPlease have DivaModLoader's config.toml in the same location as DivaModEnabler", title = "DivaModEnabler")
        sys.exit()

    else:

        #if there is no priority line then add it
        if contents.find("priority = [") == -1:
            file.write("\npriority = " + str(mod_folders))

            file.close()
            
        #if there is a priority line then make mod_folder's list out of it
        else:
            mod_folders_name = []
            mod_remove_name = []

            #loads priority 
            mod_folders_name = ast.literal_eval(contents[contents.find("["):])

            #addings new mods
            for mod in mod_folders:
                if mod not in mod_folders_name:
                    mod_folders_name.insert(0, mod)
            
            #get mod names to be removed
            for mod in mod_folders_name:
                
                #adds each mod to be removed to a list
                if mod not in mod_folders:
                    mod_remove_name.append(mod)

            #removes each mod in the remove mod list from the priority list
            for mod in mod_remove_name:
                    mod_folders_name.remove(mod)

            #sets the list from priority line to the main variable for listbox
            mod_folders = mod_folders_name
            file.close()

            #overwrites the config.toml with new priority line
            with open("config.toml", "r+") as file:
                contents = file.read()
                file.write("")

            with open("config.toml", "w") as file:
                    file.write(contents[:contents.find("priority")] + "priority = " + str(mod_folders))

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 


#function to check if a mod is disabled/enabled or not a real mod
def check_mod(select, write):
    
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
        
        if write == True:
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
            
            window["--Text--"].update("Log: Missing enabled =")
            
        
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
        
        #checks for a DLL file in the mod and include = line
        for files in os.listdir(os.getcwd() + "/mods/" + select):
            
             #if there is a DLL file and there is no line for it in the config.toml.
            if ".dll" in files and files.count(".") < 2:
                
                if contents.find(f'dll = [') == -1:
                      
                    #user error messaging  
                    window["--Text--"].update("Log: Missing the dll =")
                    
                        
            #if there is a rom folder and there is no line for it in the config.toml
            if "rom" in files:
                
                if contents.find('include = [') == -1:
                    
                    #user error messaging 
                    window["--Text--"].update("Log: Missing the include =")



#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



#Icon image
base64 = b'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'

psg.set_global_icon(base64)
psg.theme("DarkBlue14")

#loads mod order
load_mods()


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



#window layout
column_one = [
             [psg.Button("🡅", font = 10, key = "Move Up", size = (4, 1)), psg.Button("🡇", font = 10, key = "Move Down", size = (4, 1)), psg.Push(), psg.Button("Enable All", size = (10, 1)), psg.Button("Disable All", size = (10, 1))],
             [psg.Listbox(mod_folders, default_values = [mod_folders[0]], size = (50, 27), key = "--List--", enable_events = True, pad = 2)],
             [psg.Button("Refresh", size = (10, 1)), psg.Text("Log: ", key = "--Text--", size = 32)],
             ]
              
column_two = [
             [psg.Push(), psg.Text("Mod Name", key = "--Name--", font = ("Arial", 15, "bold"), size = 30, justification = "center", pad = ((0, 0), (0, 14))), psg.Push()],
             [psg.Checkbox("Enabled",True, enable_events = True, key = "--Check--"), psg.Push(), psg.Button("Open", size = (10, 1))],
             [psg.Multiline("", key = "--Viewer--", size = (50, 26), enable_events = True)],
             [psg.Push(), psg.Text("Diva Mod Enabler V1.1", size = 20), psg.Text("Mods: " + str(len(mod_folders)), size = 8, key = "--Mod Count--")]
             ]

layout = [
         [psg.Column(column_one), psg.VSeparator(), psg.Column(column_two)],
         ]

window = psg.Window("DivaModEnabler", layout, grab_anywhere = True, enable_close_attempted_event=True, finalize = True)


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
                
                
#checks first mod on start up
check_mod(mod_folders[0], True)          
                    
#main loop
while True:
        
    event, values = window.read()
    window["--Text--"].update("Log: ")
        
    #close window
    if event == psg.WINDOW_CLOSE_ATTEMPTED_EVENT:
        break
    
    
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
    
    #resets the listbox with updated folders
    if event == "Refresh":
        load_mods()
        window["--Mod Count--"].update("Mods: " + str(len(mod_folders)))
        window["--List--"].update(mod_folders)
        window["--List--"].update(set_to_index = 0)
        
        window["--Text--"].update("Log: Refreshed")
        
        #checks the first mod in the list to see if its enabled or not
        check_mod(mod_folders[0], True)
   
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
      
    #if clicking on new mod name
    if event == "--List--":
        check_mod(values["--List--"][0], True)


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ 
               
    if event == "--Check--":
        
        #opens the config.toml to check if its enabled or disabled  
        with open(os.getcwd() + "/mods/" + values["--List--"][0] + "/" + "config.toml", "r") as file:
            contents = file.read()
            
        #checks if they should disable or enable the mod
        match values["--Check--"]:
            
            case True:
            
                new_entry = contents.replace("enabled = false", "enabled = true")
                window["--Text--"].update("Log: Enabled " + values["--List--"][0])

            case False:
            
                new_entry = contents.replace("enabled = true", "enabled = false")
                window["--Text--"].update("Log: Disabled " + values["--List--"][0])

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
        
     
        check_mod(values["--List--"][0], False)
       
       
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
                window["--Text--"].update("Log: Enabled all mods")
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
                window["--Text--"].update("Log: Disabled all mods")
                window["--Check--"].update(False)
                    
            
                with open(os.getcwd() + "/mods/" + mod + "/" + "config.toml", "w") as file:
                    file.write(new_entry)
                    
                    
                update_mod_enable(values["--List--"][0])


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                 
    if event == "Move Up" or event == "Move Down":

        index = mod_folders.index(values["--List--"][0])
      
        match event:

            case "Move Up": 

                if not mod_folders.index(values["--List--"][0]) == 0:
                    mod_folders.pop(index)
                    mod_folders.insert(index - 1, values["--List--"][0])
                    window["--List--"].update(mod_folders)
                    window["--List--"].update(set_to_index = index - 1)
                    window["--List--"].update(scroll_to_index = index -1)
                
                else:
                        window["--List--"].update(set_to_index = index)


            case "Move Down": 
                if not mod_folders.index((values["--List--"][0])) == len(mod_folders) + -1:
                    mod_folders.pop(index)
                    mod_folders.insert(index + 1, values["--List--"][0])
                    window["--List--"].update(mod_folders)
                    window["--List--"].update(set_to_index = index + 1)
                    window["--List--"].update(scroll_to_index = index + 1)

                else:
                        window["--List--"].update(set_to_index = index)
                
        
        with open("config.toml", "r+") as file:
            contents = file.read()
            file.write("")

        with open("config.toml", "w") as file:
                file.write(contents[:contents.find("priority")] + "priority = " + str(mod_folders))



#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                 
      
#When opening the mod folder      
    if event == "Open":
        
        match platform.system():
        
            case "Windows": os.startfile(os.getcwd() + "/mods/" + values["--List--"][0])
            case "Linux": os.system('xdg-open "%s"' % os.getcwd() + "/mods/" + values["--List--"][0])
            

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      
        
        
        
    
        
        
    
    
    
    
    
    