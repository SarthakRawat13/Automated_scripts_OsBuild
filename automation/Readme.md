
# Building and Deployment Automation Instructions

## Introduction
This project aims to automate the build and production deployment process for custom hardware or software environments. It simplifies the workflow by using Python scripts to streamline both stages—building the project and deploying it. With clear instructions and easy setup, users can get their custom boards up and running efficiently.

## Requirements
- A **Python environment** is required to run the provided scripts.
- The **flexbuild_lsdk2108_github** package is necessary to initialize the build environment.

## Steps to Follow

### 1. Clone the Repository
First, clone the repository where the automation scripts are stored. Once the repository is cloned, you will find two folders inside:
   - **automation**: This folder contains four critical files:
     - `development.py`: A Python script responsible for the build process.
     - `production.py`: A Python script that handles the deployment.
     - `file.json`: Contains configuration details needed for the custom board.
     - `githubCred.json`: Holds user-specific information like GitHub username and SSH key.
     - `required_file`: Directory structure for custom build: custom board and custom device tree, and custom OS.
   - **flex.zip**: A zipped folder related to Flexbuild.

### 2. Prepare the Environment
There are two paths you can take, depending on your setup:
   - **Step 3**: If you have already downloaded and extracted Flexbuild, follow this step.
   - **Step 4**: If Flexbuild is not downloaded, proceed to the step 4 or step 5.

### 3. Directory Placement
If you have previously downloaded Flexbuild, ensure that the `automation` folder from the cloned repository is placed **at the same directory level** as your `flexbuild_lsdk2108_github` folder. This is crucial for ensuring that the build scripts can locate necessary resources.

### 4. Running the Build Process
Once the environment is set, follow these steps to run the build process:

1. **Open Terminal**: Open a terminal window and navigate to the repository's `automation` folder where the `development.py` script is located. You can do this using the `cd` command. For example:
   ```bash
   cd <parentDirectory>/automation
   ```

2. **Run the Build Script**: In the terminal, execute the build script by typing the following command:
   ```bash
   python3 development.py
   ```

3. **Follow On-Screen Instructions**: The script will guide you through the build process. Follow the instructions as they appear in the terminal.

4. **Custom Builds**:
   - For a **custom board build**, you need to modify the `file.json` file to include the board's name.
   - Additionally, place the required files for the build in the `required_file` folder. 
   - **Important**: Ensure that the folder structure inside `required_file` remains consistent with the project’s requirements, as incorrect placement could lead to build errors.

### 5. Running the production process
To execute the deployment process:
1. **Open Terminal**: Open a terminal window and navigate to the repository's `automation` folder where the `production.py` script is located. You can do this using the `cd` command. For example:
   ```bash
   cd <parentDirectory>/automation
   ```

2. **Run the Production Script**: In the terminal, execute the build script by typing the following command:
   ```bash
   python3 production.py
   ```

3. **Follow On-Screen Instructions**: The script will guide you through the build process. Follow the instructions as they appear in the terminal.
   - **Important**: While executing `production.py`, especially if you're using GitHub for version control, ensure that the **GitHub username** and **SSH key** are correctly filled out in 		`githubCred.json`. These credentials are necessary for secure access and proper functioning of the script.

### Additional Considerations
- Always verify that your Python environment is correctly set up, with any required dependencies installed.
- Double-check the JSON configuration files (`file.json` and `githubCred.json`) to ensure they contain accurate information, especially if you are working with custom hardware.

This process helps automate and standardize the build and deployment flow, reducing manual work and minimizing the chances of error.




