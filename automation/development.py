import json
import os
import sys
import subprocess
import shutils

# Function for confirmation
def confirmation(note = "Press y to proceed and n to terminate"):
    while True:
        key_pressed = input(note)
        if key_pressed == 'y' or key_pressed == 'Y':
            return True
        if key_pressed == 'n' or key_pressed == 'N':
            sys.exit(1)
        
        print("****** Please either enter y or n")
        

# Function to verify if file is present        
def is_file_present(file):
    if os.path.exits(file):
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
        missing_params = [param for param in required_params if param not in data]
        if missing_params:
            return f"Missing parameters: {', '.join(missing_params)}"
        else:
            return "All required parameters are present."
    else:
        return "Invalid JSON data."


# Function to execute Linux command and display output in real-time
def execute_command(command):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
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
    
    except Exception as e:
        print(f"Error occurred: {e}")
        sys.exit(1)

# Add error detection logic if some command fails then what
# also add optee False
def scratch_build(json_data):
    try:
        board = json_data['board']
    except:
        board = "armv8"
    
    if board == "":
        board = "armv8"
    
    print(f"You have selected {board} for the build")
    
    command = f'flex-builder -c rcw -m {board}' 
    execute_command(command)
    
    command = f'flex-builder -c atf -m {board} -b qspi'
    execute_command(command)
    
    command = 'rm -rf ../build/firmware/u-boot/ls1046afrwy/'
    execute_command(command)
    
    command = f'flex-builder -i mkfw -m {board} -b qspi'
    execute_command(command)
    
    command = f'bld -m {board}'
    execute_command(command)
    
    #run change optee
    pass
    

if __name__ == "__main__":
    json_file_path = './file.json'
    required_files = ['param1', 'param2', 'param3'] 
    require_folder = "./require_file"
    bld_checks_file = []
    
    #Description for the script
    print(f"This automated script is built for ls1046ARDB for kernel version 5.10 \n\n")
    confirmation(note = "Press y to proceed and n to terminate if you understood the message")
    print("")
    
    
    # Cross check if files are present or not
    print(f"Did you place each and every updated file in the {require_folder} folder")
    print(f"The files are:")
    for number, file in enumerate(required_files):
        print(f"  {number+1}.  {file}")
    confirmation(note = "Press y to proceed and n to terminate if you have placed the files in the required folder")
    print("")
    
    
    # Cross check if files are present or not
    print(f"Performing checks to see if files are present")
    count = 1
    is_file_present(json_file_path)
    
    # Read the JSON file
    json_data = read_json(json_file_path)
    if isinstance(json_data, dict):
        result = check_required_params(json_data, required_files)
        print(result)
    else:
        print(json_data)

    is_file_present(require_folder)
    for file in required_files:
        is_file_present(os.path.join(require_folder, file))
        count+=1
    if count!=len(required_files):
        print(f"Mismatch file counts: Count: {count}    file counts: {len(required_files)}")
        sys.exit(1)
    count = 1
    for file in required_files:
        if file not in json_data.keys():
            print(f"key: {file} not present please fill that")
            sys.exit(1)
    print(f"All files are present \n")
    

    # build check
    print(f"Is this your first build? Means is the a build fro scratch")
    confirm = confirmation(note = "Press y if this is the first build for the first time and n if this is not te first time")
    print("")  
    
    
    if confirm:
        scratch_build()
    
    # perform components checks if fails give option to rerun from scratch or exit
    for file in bld_checks_file:
        is_file_present(file)
        
        
    # Copy file to each location
#    shutil.copy(source, destination)
    
    
    
    
    

