# -------------------------------
# Juniper Command System
# 'juniper_source.py'
# Author: Juan Carlos Juárez.
# Licensed under MPL 2.0.
# All rights reserved.
# -------------------------------

# Packages

import junipercs.ply.lex as lex
import junipercs.ply.yacc as yacc
import sys 
import os # delete

# Additional Resources

import junipercs.resources.commands_list as cmd_file
import junipercs.system_parser.tokens as tokens_file
# import junipercs.system_parser.tokens_definition

# Commands

import junipercs.modules.options as options
import junipercs.modules.create as create
import junipercs.modules.goto as goto
import junipercs.modules.list as list_cmd

#-------------------------------------------
# ___________GLOBAL VARIABLES_______________
#-------------------------------------------

# Variables Memory

varMemory = {}

# Auxiliary Checks

###############

cmdList = cmd_file.cmdList

tokens = tokens_file.tokens

checkString = False
checkId = False

# System Tokens Definition

def t_CREATE(t):
	r'\b(create)\b'
	t.type = 'CREATE'
	return t

def t_SET(t):
	r'\b(set)\b'
	t.type = 'SET'
	return t

def t_DELETE(t):
	r'\b(delete)\b'
	t.type = 'DELETE'
	return t

def t_READ(t):
	r'\b(read)\b'
	t.type = 'READ'
	return t

def t_START(t):
	r'\b(start)\b'
	t.type = 'start'
	return t

def t_NEW(t):
	r'\b(new)\b'
	t.type = 'NEW'
	return t

def t_WEBSERVER(t):
	r'\b(webServer)\b'
	t.type = 'WEBSERVER'
	return t

def t_AT(t):
	r'\b(at)\b'
	t.type = 'AT'
	return t

def t_INSTANCE(t):
	r'\b(instance)\b'
	t.type = 'INSTANCE'
	return t

def t_DIRECTORY(t):
	r'\b(dir)\b'
	t.type = 'DIRECTORY'
	return t

def t_PATH(t):
	r'\b(path)\b'
	t.type = 'PATH'
	return t

def t_EXIT(t):
	r'\b(exit)\b'
	t.type = 'EXIT'
	return t

def t_THIS(t):
	r'\b(this)\b'
	t.type = 'THIS'
	return t

def t_GOTO(t):
	r'\b(goto)\b'
	t.type = 'GOTO'
	return t

def t_LIST(t):
	r'\b(list)\b'
	t.type = 'LIST'
	return t

def t_FILE(t):
	r'\b(file)\b'
	t.type = 'FILE'
	return t

def t_UP(t):
	r'\b(up)\b'
	t.type = 'UP'
	return t

def t_DOWN(t):
	r'\b(down)\b'
	t.type = 'DOWN'
	return t

def t_WITH(t):
	r'\b(with)\b'
	t.type = 'WITH'
	return t

def t_FROM(t):
	r'\b(from)\b'
	t.type = 'FROM'
	return t

def t_VARIABLES(t):
	r'\b(variables)\b'
	t.type = 'VARIABLES'
	return t

def t_HELP(t):
	r'\b(help)\b'
	t.type = 'HELP'
	return t

def t_COMMANDS(t):
	r'\b(commands)\b'
	t.type = 'COMMANDS'
	return t

def t_VAR(t):
	r'\b(var)\b'
	t.type = 'VAR'
	return t

def t_FORGET(t):
	r'\b(forget)\b'
	t.type = 'FORGET'
	return t

def t_IS(t):
	r'\b(is)\b'
	t.type = 'IS'
	return t

# Defined One-Character-Tokens

t_LEFTPAR = r'\('
t_RIGHTPAR = r'\)'
t_QUOTES = r'\"'
t_SEMICOLON = r'\;'
t_DASH = r'\-'
t_DOUBLEDASH = r'\-\-'
t_ARROW = r'\-\>'

# Ignored Line Jumps

t_ignore = " \t"

# Variable Types Definitions

def t_NUMBER(t):
    r'(\-|)\d+((\.\d+)|)'
    try:
        t.value = float(t.value)
    except ValueError:
        print("\n<!> Juniper CS Command Error: Float value not supported %d", t.value)
        t.value = 0
    return t

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	t.type = 'ID'
	return t

def t_STRING(t):
	r'\".+?(")'
	curr = str(t.value)
	curr = curr[1:]
	curr = curr[:-1]
	t.value = curr
	return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("\n<!> Juniper CS Command Error: '%s' is not a defined Keyword." % t.value[0])
    t.lexer.skip(1)

# ----------------------------
# _____LEXER CONSTRUCTION_____
# ----------------------------

lexer = lex.lex()

# ----------------------------
# __________GRAMMAR___________
# ----------------------------

# Main Grammar Command Production

def p_juniper(t):
    'juniper                : juniper_command'

# Command Options

def p_juniper_command(t):
    '''juniper_command      : command_selection
                            | EXIT
                            | VARIABLES
                            | HELP
                            | COMMANDS'''
    global varMemory
    global cmdList
    selection = str(t[1])
    if(selection is None): return
    if options.default_options(selection,varMemory,cmdList) == 1: sys.exit()
    
# Command Selection
    
def p_command_selection(t):
    '''command_selection    : create 
                            | goto
                            | list
                            | up
                            | down
                            | read
                            | forget
                            | var'''

# Create Selection

def p_create(t):
    '''create               : create_directory
                            | create_file'''

# Goto Command

def p_goto(t):
    'goto               : GOTO STRING'
    path = repr(str(t[2]))[1:-1]
    goto.goto(path)

# List Command

def p_list(t):
    '''list               : list_string
                          | list_id  
                          | list_this '''

def p_list_string(t):
    'list_string          : LIST STRING'
    path = str(t[2])
    list_cmd.list_string(path)

def p_list_id(t):
    'list_id              : LIST ID'
    global varMemory
    varId = str(t[2])
    list_cmd.list_id(varMemory,varId)

def p_list_this(t):
    'list_this            : LIST THIS'
    path = str(os.getcwd())
    list_cmd.list_this(path)

def p_up(t):
    'up                     : UP STRING'
    currentDirectory = str(os.getcwd())
    path = repr(str(currentDirectory))[1:-1]
    upDir = str(t[2])
    newPath = os.path.join(path, upDir)
    if(os.path.isdir(newPath)):
        os.chdir(newPath)
    else:
        print("\n<!> Juniper CS Command Error: Directory does not exist.")

def p_down(t):
    'down                     : DOWN'
    os.chdir("..")

def p_read(t):
    '''read                     : READ STRING is_string
                                | READ ID'''
    global varMemory
    global checkString
    try:
        path = ""
        if(checkString):
            path = repr(str(t[2]))[1:-1]
        else:
            varId = str(t[2])
            if(varId in varMemory):
                path = varMemory[varId][1]
            else:
                print("\n<!> Juniper CS Command Error: Variable does not exist.")
                return
        f = open(path, "r")
        print("\n<$> File Content: \n")
        for x in f:
            print(x)
    except:
        print("\n<!> Juniper CS Command Error: File could not be read or does not exist.")


def p_forget(t):
    'forget                     : FORGET ID'
    global varMemory
    variableId = str(t[2])
    try:
        del varMemory[variableId]
    except KeyError:
        print("\n<!> Juniper CS Command Error: Variable does not exist.") 

def p_create_directory(t):
    '''create_directory     : CREATE DIRECTORY STRING AT STRING ARROW ID
                            | CREATE DIRECTORY STRING AT THIS ARROW ID     
                            | CREATE DIRECTORY STRING AT STRING 
                            | CREATE DIRECTORY STRING AT THIS'''
    global varMemory
    if(t[len(t)-2] == "->" and (t[len(t)-1] in varMemory)):
        print("\n<!> Juniper CS Command Error: Variable with that name already exists.")
        return
    currentDirectory = str(os.getcwd())
    directoryName = str(t[3])
    path = ""
    if(str(t[5]) == "this"):
        path = repr(str(currentDirectory))[1:-1]
    else:
        path = repr(str(t[5]))[1:-1]
    newPath = os.path.join(path, directoryName)
    if(os.path.isdir(newPath)):
        print("\n<!> Juniper CS Command Error: Directory already exists.")
    else:
        try:
            os.mkdir(newPath)
            if(t[len(t)-2] == "->"): 
                varMemory[t[len(t)-1]] = ["Directory",newPath]
        except:
            print("\n<!> Juniper CS Command Error: Directory cannot be created.")

def p_create_file(t):
    '''create_file          : CREATE FILE STRING AT STRING ARROW ID
                            | CREATE FILE STRING AT THIS ARROW ID     
                            | CREATE FILE STRING AT STRING 
                            | CREATE FILE STRING AT THIS
                            | CREATE FILE STRING AT STRING WITH STRING ARROW ID
                            | CREATE FILE STRING AT THIS WITH STRING ARROW ID
                            | CREATE FILE STRING AT STRING WITH STRING
                            | CREATE FILE STRING AT THIS WITH STRING'''
    global varMemory
    if(t[len(t)-2] == "->" and (t[len(t)-1] in varMemory)):
        print("\n<!> Juniper CS Command Error: Variable with that name already exists.")
        return
    currentDirectory = str(os.getcwd())
    fileName = str(t[3])
    path = ""
    if(str(t[5]) == "this"):
        path = repr(str(currentDirectory))[1:-1]
    else:
        path = repr(str(t[5]))[1:-1]
    newPath = os.path.join(path, fileName)
    if(os.path.isfile(newPath)):
        print("\n<!> Juniper CS Command Error: File already exists.")
    else:
        try:
            with open(newPath, 'w') as fp:
                if(len(t) >= 8 and str(t[6] == "with")):
                    fp.write(str(t[7]))
            if(t[len(t)-2] == "->"): 
                varMemory[t[len(t)-1]] = ["File",newPath]        
            #print("\n<" + str(globalCounter) + "$> File '% s' has been created." % fileName)
        except:
            print("\n<!> Juniper CS Command Error: File cannot be created.")

def p_var(t):
    '''var                 : VAR FILE IS STRING ARROW ID
                           | VAR DIRECTORY IS STRING ARROW ID'''
    global varMemory
    objectType = str(t[2])
    varId = str(t[6])
    if(varId in varMemory):
        print("\n<!> Juniper CS Command Error: Variable with that name already exists.")
        return
    path = str(t[4])
    newPath = repr(str(path))[1:-1]
    if(objectType == "file"):
        if(os.path.isfile(newPath)):
            varMemory[varId] = ["File",newPath]
        else:
            print("\n<!> Juniper CS Command Error: Variable Type does not match.")
    else:
        if(os.path.isdir(newPath)):
            varMemory[varId] = ["Directory",newPath]
        else:
            print("\n<!> Juniper CS Command Error: Variable Type does not match.")


def p_is_string(t):
    'is_string             : empty'
    global checkString
    checkString = True

# Syntax Error

def p_error(t):
    if(t is not None):
        print("\n<!> Juniper CS Command Error: Syntax Error at '%s'." % t.value)
    else:
        print("\n<!> Juniper CS Command Error: Syntax Error.")

# Empty Rule

def p_empty(t):
	'''
	empty : 
	'''
	t[0] = None

parser = yacc.yacc()

def resetChecks():
    global checkString
    global checkId
    checkString = checkId = False

def exec(command):
    resetChecks()
    if(command != ""): parser.parse(command)
