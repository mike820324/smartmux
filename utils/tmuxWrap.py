import subprocess
import shlex
import argparse
import pwd

def currentPathClient(sessionId = None):
    if sessionId == None:
        command = "tmux display-message -p '#{pane_current_path}'"
    else:
        command = "tmux display-message -p -t {0} '#{pane_current_path}'".format(sessionId)
    p = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    output = p.stdout.read()
    return output.strip()

def uidOfClient(pid):
    shellCommand = "pstree -u {0}".format(pid)
    p = subprocess.Popen(shlex.split(shellCommand), stdout=subprocess.PIPE)
    output = p.stdout.read()

    commandChain = [ command.strip() for command in output.split("---") if command.strip() != "" ]
    
    currentUser = ""
    for command in commandChain:
        if "(" in command:
            currentUser = command.split("(")[1][:-1]
    
    return pwd.getpwnam(currentUser).pw_uid

def listClient(search_type):
    if search_type == "session" or search_type == "system": # @fixme: how to search current session only
        command = "tmux list-panes -a -F '#{pane_id} #{pane_current_command} #{pane_pid}'"
    elif seach_type == "window":
        command = "tmux list-panes -F '#{pane_id} #{pane_current_command} #{pane_pid}'"
        
    p = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    output = p.stdout.read()

    return [ 
        {
            "clientId": paneStrList[0], 
            "command": paneStrList[1],
            "pid": paneStrList[2],
            "uid": uidOfClient(paneStrList[2])
        }
        for paneStrList in map(lambda x: x.split(" "), output.split("\n"))
        if len(paneStrList) == 3
    ]

def openClient(open_options,  command_selector, command_options):
    if open_options["type"] == "window":
        command = "tmux new-window {0} {1}".format(command_selector, command_options)
    elif open_options["type"] == "pane":
        command = "tmux split-window -v -p {0} {1} {2}".format(open_options["size"], command_selector, command_options)
    
    print command
    subprocess.call(shlex.split(command))

def switchClient(sessionId):
    command = "tmux switch-client -t {0}".format(sessionId)
    subprocess.call(shlex.split(command))

def sendKey(sessionId, value):
    command = "tmux send-keys -t {0} {1} Enter".format(sessionId, value)
    print command
    subprocess.call(shlex.split(command))

if __name__ == '__main__':
    print "Do not use this file directory"
    exit(1)
