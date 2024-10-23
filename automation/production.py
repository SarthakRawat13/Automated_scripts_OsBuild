import subprocess
import os
import sys
import json

MAIN_DIR = "flexbuild_lsdk2108_github"
MAIN_GITHUB = "github_dir"
bootfile = "boot_LS_arm64_lts_5.10.tgz"
rootfile = "rootfs_lsdk2108_ubuntu_main_arm64.tgz"
firmware = "firmware_ls1046ardb_sdboot.img"
out_device = "sdb"
flex_zip = "flexbuild_lsdk2108_github.tgz"
json_user_file = 'githubCred.json'

def parent_loc():
    current_directory = os.getcwd()
    parent_directory="/".join(current_directory.rsplit('/')[:-1])
    return parent_directory

def extract_flex():
    if not is_file_present2(f"{MAIN_DIR}/setup.env"):
        if is_file_present(os.path.join(parent_loc(),flex_zip)):
            print("Extracting zip file")
            command = f"tar -xvzf {os.path.join(parent_loc(),flex_zip)} -C {parent_loc()}"
            execute_command(command = command)
            print("Extracted zip file")
        else:
            print("flexbuild_lsdk2108_github.tgz file not present please download it")
            sys.exit(1)

def init_flex():
    bool = execute_command(command = f'source {MAIN_DIR}/setup.env')
    if bool:
        print("Successfully init flex builder")
    else:
        print("init flex builder unscuccessfull")
        sys.exit(1)
        
def json_user_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data['userName'], data['sshKey']
    except FileNotFoundError:
        return "File not found."
    except json.JSONDecodeError:
        return "Error decoding JSON."

# Function for confirmation
def confirmation(note = "Press\n y/Y to proceed\n n/N to terminate: "):
    print()
    while True:
        key_pressed = input(note)
        if key_pressed == 'y' or key_pressed == 'Y':
            return True
        if key_pressed == 'n' or key_pressed == 'N':
            sys.exit(1)
        
        print("****** Please either enter y or n")
        
        
def return_code(note = "Enter 1 or 2: ", number=2):
    while True:
        key_pressed = input(note)
        for numb in range(number):
            if str(numb+1) == str(key_pressed):
                return int(numb+1)
        print(f"****** Please provide a valid input: {note}")
    
      
      
# Function to verify if file is present        
def is_file_present2(file):
    if os.path.exists(file):
        return True
    print(f"{file} not present. Please make it available")
    return False
    
# Function to verify if file is present        
def is_file_present(file):
    if os.path.exists(file):
        return True
    print(f"{file} not present. Please make it available")
    sys.exit(1)
      

# Function to execute Linux command and display output in real-time
def execute_command(command):
    print(f"\nExectuting command: {command}")
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("process: ",process)
        # Iterate over the output line by line. Print the output in real-time
        for line in process.stdout:
            print(line, end='')  
        # Wait for the process to finish and capture any remaining output or errors
        process.wait()

        # # Check if the process has errors
        # if process.returncode != 0:
        #     error_output = process.stderr.read()
        #     print(f"\nCommand failed with error:\n{error_output}")
        #     sys.exit(1)
        #     return False
        # else:
        #     print("\nCommand executed successfully.")
        #     return True
        return True
    
    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)
        
        
def clone_repository():
    repo_url = input("Enter the GitHub repository URL: ").strip()

    if not repo_url:
        print("Invalid URL. Please provide a valid GitHub repository URL.")
        return

    message = "Press:\n 1 To manually type username and ssh key\n 2 Automatically uploading from json file\n "
    code = int(return_code(note = message, number=2))
    
    if code == 1:
        username = input("Enter your GitHub username (leave blank if not needed): ").strip()
        ssh_key = input("Enter your SSH key path (leave blank if not needed): ").strip()
        
    elif code == 2:
        if os.path.exists(json_user_file):
            username, ssh_key = json_user_data(json_user_file)
        else:
            print("******* JSON file not present")
            sys.exit(1)
    
    else:
        print("Invalid username and password")
        sys.exit(1)

    if username and ssh_key:
        os.environ['GIT_SSH_COMMAND'] = f'ssh -i {ssh_key} -o IdentitiesOnly=yes'
    
    try:
        location_github = os.path.join(parent_loc(), MAIN_GITHUB)
        if not os.path.exists(location_github):
            os.mkdir(location_github)
            
        subprocess.run(['git', 'clone', repo_url, location_github], check=True)
        print(f"Successfully cloned {repo_url}")
        return location_github

    except subprocess.CalledProcessError as e:
        print(f"An error occurred in the clone process: {e}")
        
 
def build_from_folder():
    folder_path = input("Enter full location of the folder: ")
    print(f"You entered: {folder_path}")

    if not os.path.exists(folder_path):
        print("************* Invalid path provided! please provide exact path")
        sys.exit(1)
    
    return folder_path
 
        
def flex_repo():
    bool_check = is_file_present(os.path.join(MAIN_DIR,"build","images"))
    if not bool_check:
        print("No prebuild folder present")
        sys.exit(1)
    
    print("Prebuild folder is present")
    
    return os.path.join(MAIN_DIR,"build","images")
    
    
def build(files_folder):
    command = f"lsblk"
    execute_command(command)
    
    print('\n')
    out_device = input("Enter output device eg. sdb,sdc, etc: ")
    print(f"Out device: {out_device}")
    if out_device[-1] == "a":
        print("Please verify device. Make sure it is not sda. Current entered device is sda")
        sys.exit(1)
    
    confirmation()
    print('\n')
    
    input("Press any key to continue")
    if (not is_file_present(os.path.join(files_folder,bootfile))) or (not is_file_present(os.path.join(files_folder,rootfile))) or (not is_file_present(os.path.join(files_folder,firmware))):
        print("One of the files missing from build image folder")
        sys.exit(1)
    print("All files present")
    
    print('\n')
    input("Press any key to continue")
    command = f"flex-installer -b {os.path.join(files_folder,bootfile)} -r {os.path.join(files_folder,rootfile)} -f {os.path.join(files_folder,firmware)} -d /dev/{out_device} -F"
    execute_command(command)
    

if __name__ == "__main__":
    print(f"This automated script is built production stage for the AICRAFT custom boards\n")
    print(f"*** Please make sure you have flex installer in the location\n")
    MAIN_DIR = os.path.join(parent_loc(), MAIN_DIR)
    print(f"Checking {MAIN_DIR}")
    bool_check = is_file_present2(MAIN_DIR)
    if not bool_check:
        extract_flex()
    print(f"{MAIN_DIR} present\n\n")
    
    
    print("Initializing flex installer")
    init_flex()
    print("\n")
    
    
    print("Do you want to build from github or the flex builder default library or userdefined folder?")
    print("\n")
    message = "Press:\n 1 Github\n 2 Flexbuilder default location\n 3 Custom folder name 'build'\n "
    code = int(return_code(note = message, number=3))
    print('\n')
    
    if code == 1:
        files_folder = clone_repository()
        
    elif code == 2:
        files_folder = flex_repo() 
        
    elif code == 3:
        files_folder = build_from_folder() 
        
        
    else:
        print("Wrong input")
        sys.exit(1)
    
    if files_folder:
        build(files_folder)
    else:
        print("******************* Build file folder is empty please check")
        
    print("Process completed")
    print("Byee")
