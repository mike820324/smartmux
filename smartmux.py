#!/usr/bin/python

# TODO
# + support search range. [window | session | system wild]
#   -- lacking session only
# + support differnt open mode. [pane | window | session]
#   -- lacking open session
#
# - support customize the open pane size

# - check process uid and switch to window with the same uid.
#   Should check the uid of the process
#   tmux list-panes -a -F '#{pane_pid}' | xargs ptree -u
import argparse

from utils.tmuxWrap import listClient, sendKey, openClient, switchClient
from utils.transformers import defaultTransform, vimTransform, weechatTransform

def findClientByCommand(search_type, command_selector):
    clientInfos = listClient(search_type)
    targetId = [ clientInfo["clientId"] for clientInfo in clientInfos if clientInfo["command"] == command_selector ]
    
    if len(targetId) == 0:
        return None
    else:
        return targetId[0]

def commandSwitcher(search_type, open_options, command_selector, command_options):
    supportTransformers = {
            "vim": vimTransform,
            "weechat": weechatTransform
    }

    clientId = findClientByCommand(search_type, command_selector)

    try:
        transformer = supportTransformers[command_selector]
        
    except KeyError:
        print "Can not find transformer of given command, using default"
        transformer = defaultTransform

    if clientId == None:
        openClient(open_options, command_selector, " ".join(command_options))

    else:
        # if have options call the Transformer and send keys
        if len(command_options) != 0:
            for key in map(transformer, command_options):
                sendKey(clientId, key)

        switchClient(clientId)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="The tmux command switcher")
    parser.add_argument('-s', '--search-type', dest="search_type", choices=["system", "session", "window"], default="session")
    parser.add_argument('--open-type', dest="open_type", choices=["session", "window", "pane"], default="window")
    parser.add_argument('--open-direction', dest="open_direction", choices=["vertical", "horizontal"], default="vertical")
    parser.add_argument('--pane-size', dest="pane_size", type=int, default=50)
    parser.add_argument("command_selector", help="The command you want to execute")
    parser.add_argument("command_options", help="Arguments for the command", nargs="*")
    args = parser.parse_args()
    
    open_options = {
            "type": args.open_type,
            "direction": args.open_direction,
            "size": args.pane_size
    }
    commandSwitcher(args.search_type, open_options, args.command_selector, args.command_options)
