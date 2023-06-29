# set the home path in each script
import os
# get current working directory as home path
cwd = os.getcwd()

def main() :
    # all the script need to replace the variable of home_path
    all_scripts = ["query.py", "deployWordpress.py", "call_prom.py", "monitor/podCreate.py", "monitor/weirdPod.py"]
    # rewrite all script
    rewriteAllScripts(all_scripts)

# rewrite all script
def rewriteAllScripts(all_scripts) :
    for script in all_scripts :
        # open script
        f = open(script, "r+")
        file_content = f.readlines()

        # find the variable of home_path in each line in the script
        home_path_line = findHomePath(file_content)

        # no vairable of home_path in the script
        if home_path_line == -1 :
            print(f"the home_path variable is not found in the {script}")
            f.close()
        else :
            # set the new script content with home path
            file_content[home_path_line] = f"home_path = '{cwd}'\n"

            # clear the script content at first
            f.truncate(0)
            # no seek will add weird \x00 at the start
            f.seek(0)
            # write the home path into script
            f.writelines(file_content)
            f.close()

# find line index of home_path in the script
def findHomePath(file_content) :
    index = 0
    for line in file_content :
        if "home_path" in line :
            return index
        index += 1 
    return -1

main()
