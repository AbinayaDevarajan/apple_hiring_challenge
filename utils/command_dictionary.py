"""
Command Interpretation
This has the command interpretation and the dictionary of possible commands

"""

command_description_dict ={
    'DEPEND':' item1 item2[item3 ...] item1 depends on item2(and item3 ...)' ,
    'INSTALL':' item1 install item1 and those on which it depends',
    'REMOVE':' item1 remove item1, and those on which it depends, if possible.',
    'LIST':'list the names of all currently installed components',
    'END':'End of the program'
}

command_dictionary={

    'dependency_build':'DEPEND',
    'installation':'INSTALL',
    'uninstallation':'REMOVE',
    'terminate_program':'END',
    'list_installed_components': 'LIST'
}
