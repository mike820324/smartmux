
def defaultTransform(command_option):
    return command_option

# transform functions
def vimTransform(command_option):
    import os
    # use absolute path instead of relative path
    currentDir = os.getcwd()
    
    # ensure that vim is in normal mode
    return "Escape ':e {0}'".format(os.path.join(currentDir, command_option))

def weechatTransform(command_option):
    return "/connect {0}".format(command_option)

if __name__ == '__main__':
    print "Do not use this file directory"
    exit(1)
