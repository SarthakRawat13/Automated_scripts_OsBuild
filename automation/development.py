import json
import os
import sys
import subprocess
try:
    import yaml
except ImportError:
    print("PyYAML is not installed. Installing it now...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml"])
    print("PyYAML has been installed successfully.")
import yaml
    

MAIN_DIR = "flexbuild_lsdk2108_github"
flex_zip = "flexbuild_lsdk2108_github.tgz"
json_file_path = 'file.json'
required_field = ['atf', 'rcw', 'dt_uboot','dt_linux','board','defconfig','lsconfig','sdk'] 
require_folder = "require_files"
bld_checks_file = []
flex_command_dir = ""

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
    bool = execute_command(command = f'. {MAIN_DIR}/setup.env')
    if bool:
        print("Successfully init flex builder")
    else:
        print("init flex builder unscuccessfull")
        sys.exit(1)
        
# Function to verify if file is present        
def is_file_present2(file):
    if os.path.exists(file):
        return True
    print(f"{file} not present. Please make it available")
    return False
    
def parent_loc():
    current_directory = os.getcwd()
    parent_directory="/".join(current_directory.rsplit('/')[:-1])
    return parent_directory


# Function for confirmation
def confirmation(note = "Press y/Y To proceed\n n/N To terminate"):
    while True:
        key_pressed = input(note)
        if key_pressed == 'y' or key_pressed == 'Y':
            return True
        if key_pressed == 'n' or key_pressed == 'N':
            sys.exit(1)
        
        print("****** Please either enter y or n")
        

# Function to verify if file is present        
def is_file_present(file):
    if os.path.exists(file):
        return True
    print(f"{file} not present. Please make it available")
    sys.exit(1)
        
# Function to read a JSON file
def read_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return "File not found."
    except json.JSONDecodeError:
        return "Error decoding JSON."


# Function to check required parameters in the JSON data
def check_required_params(data, required_params):
    if isinstance(data, dict):
        missing_params = [param for param in required_params if param not in data or data[param] == ""]
        if missing_params:
            print(f"Missing params: {required_params[missing_params]}")
            sys.exit(1)
        else:
            return "All required parameters are present."
    else:
        return "Invalid JSON data."


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

        # Check if the process has errors
        if process.returncode != 0:
            error_output = process.stderr.read()
            print(f"\nCommand failed with error:\n{error_output}")
            sys.exit(1)
            return False
        else:
            print("\nCommand executed successfully.")
            return True
        return True
    
    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)


def scratch_build(board = "ls1046ardb"):
    print(f"Board: {board} is seleted for the default/scratch build")
    
    command = f'flex-builder' 
    execute_command(command)
    
    command = f'flex-builder -c rcw -m {board}' 
    execute_command(command)
    
    command = f'flex-builder -c atf -m {board} -b qspi'
    execute_command(command)
    
    command = f'bld -m {board}'
    execute_command(command)
    

def optee(value, targetdirectory):
    with open(os.path.join(targetdirectory,'configs/sdk.yml'), 'r') as file:
        data = yaml.safe_load(file)
        
    data['CONFIG_APP']['OPTEE'] = value 

    with open(os.path.join(targetdirectory,'configs/sdk.yml'), 'w') as file:
        yaml.dump(data, file, default_flow_style=False)
    
    

def custom_build(board = "ls1046ardb", targetdirectory=MAIN_DIR, firmware=False):
    print(f"Board: {board} is seleted for the build")
    
    command = f'flex-builder -c rcw -m {board}' 
    execute_command(command)
    
    command = f'flex-builder -c atf -m {board} -b qspi'
    execute_command(command)
    
    if firmware:
        optee('n', targetdirectory)
        command = f'flex-builder -i mkfw -m {board} -b qspi'
        execute_command(command)
        optee('y', targetdirectory)
        return
    
    optee('y', targetdirectory)
    command = f'bld -m {board}'
    execute_command(command)



def flex_checks(MAIN_DIR):
    bool_check = False
    path = os.join.path(MAIN_DIR, 'components','linux', 'linux')
    if not os.path.exists(path):
        print(f'PAth doen not exists {path}')
        bool_check = True
        
    path = os.join.path(MAIN_DIR, 'components','firmware','uboot')
    if not os.path.exists(path):
        print(f'PAth doen not exists {path}')
        bool_check = True

    path = os.join.path(MAIN_DIR, 'components','firmware','rcw')
    if not os.path.exists(path):
        print(f'PAth doen not exists {path}')
        bool_check = True
        
    path = os.join.path(MAIN_DIR, 'components','firmware','atf')
    if not os.path.exists(path):
        print(f'PAth doen not exists {path}')
        bool_check = True
        
    path = os.join.path(MAIN_DIR, 'configs','linux')
    if not os.path.exists(path):
        print(f'PAth doen not exists {path}')
        bool_check = True
        
    path = os.join.path(MAIN_DIR, 'configs','sdk.cfg')
    if not os.path.exists(path):
        print(f'PAth doen not exists {path}')
        bool_check = True
        
    if bool_check:
        print("Please rerun the flexbuilder from scratch")
        sys.exit(1)

if __name__ == "__main__":
    MAIN_DIR = os.path.join(parent_loc(), MAIN_DIR)
    sys.path.append(os.getcwd())
    sys.path.append(MAIN_DIR)
    os.chdir(MAIN_DIR)

    os.system(f". {os.path.join(os.getcwd(),'setup.env')}")
    print(f". {os.path.join(os.getcwd(),'setup.env')}")
    os.system(f"flex-builder")
    
    #Description for the script
    print(f"This automated script is built for AICRAFT pulsar\n")
    confirmation(note = "Press\n y/Y to proceed\n n/N to terminate\n")
    print()

    print(f"Checking {MAIN_DIR}")
    bool_check = is_file_present2(MAIN_DIR)
    if not bool_check:
        extract_flex()
    print(f"{MAIN_DIR} present\n\n")
    
    
    print("Initializing flex installer")
    init_flex()
    print("\n")
    

    # build check
    print(f"Is this your first build? Means is the a build from scratch")
    confirm = confirmation(note = "Press\n y/Y For first/default build\n n/N Custom build\n")
    parent_dir = parent_loc()
    print()  
    
    if confirm:
        print("This is a default/scratch build")
        scratch_build()
        print("Build process is completed")    
        sys.exit(1)


    print("This is a custom build")
    print(f"Make sure you have placed all the files in {require_folder} folder")
    confirmation(note = "Press\n y/Y to proceed\n n/N to terminate\n")
    
    # Cross check if files are present or not
    print(f"Performing checks to see if files are present")
    is_file_present(json_file_path)
    print()
    
    # Read the JSON file
    # count = 0
    json_data = read_json(json_file_path)
    # if isinstance(json_data, dict):
    #     result = check_required_params(json_data, required_field)
    #     print(result)
    # else:
    #     print(f"file is not a json file")
    #     sys.exit(1)

    # # Verifing each and every files
    # is_file_present(require_folder)
    # for file_ in json_data:
    #     is_file_present(os.path.join(require_folder, file_))
    # print(f"All files are present \n")
    
    #Getting board from user file.json
    try:
        board = json_data['board']
        if board == "":
            board = "ls1046ardb"
    except:
        board = "ls1046ardb"
        

    print("Copying all the files")
    command = f"cp -r ./{require_folder} {MAIN_DIR}"
    execute_command(command)
    print("/n")

    #Perfrom checks first to flexbuilder folder
    flex_checks(MAIN_DIR)
    
    print(f"Build process")
    confirmation(note = "Press\n y/Y to proceed\n n/N to terminate\n")
    
    #board process for firmware
    bool_check = input("Do you want to Build firmware only\nPress\n y/Y to proceed\n Any other key to skip\n")
    if bool_check:
        custom_build(board = board, targetdirectory = MAIN_DIR, firmware=True)
    
    print(f"Whole build process which includes rootfs, bootfs and firmware")
    bool_check = input("Do you want to Build whole OS\nPress\n y/Y to proceed\n Any other key to skip\n")
    if bool_check:
        custom_build(board = board, targetdirectory = MAIN_DIR, firmware=False)
        
    print("Build process is completed")    
    
    
    

