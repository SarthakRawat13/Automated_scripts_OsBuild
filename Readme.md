
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
   - **flex.zip**: A zipped folder related to Flexbuild.

### 2. Prepare the Environment
There are two paths you can take, depending on your setup:
   - **Step 3**: If you have already downloaded and extracted Flexbuild, follow this step.
   - **Step 4**: If Flexbuild is not downloaded, proceed to the next step.

### 3. Directory Placement
If you have previously downloaded Flexbuild, ensure that the `automation` folder from the cloned repository is placed **at the same directory level** as your `flexbuild_lsdk2108_github` folder. This is crucial for ensuring that the build scripts can locate necessary resources.

### 4. Running the Script
To execute the deployment process:
1. Open a terminal window.
2. Navigate to the `automation` folder using the `cd` command. For example:
   ```bash
   cd ./automation
   ```
3. Run the deployment script by typing:
   ```bash
   python3 production.py
   ```
   Follow the on-screen instructions that will guide you through the deployment process.

## Special Note
While executing `production.py`, especially if you're using GitHub for version control, ensure that the **GitHub username** and **SSH key** are correctly filled out in `githubCred.json`. These credentials are necessary for secure access and proper functioning of the script.

### Additional Considerations
- Always verify that your Python environment is correctly set up, with any required dependencies installed.
- Double-check the JSON configuration files (`file.json` and `githubCred.json`) to ensure they contain accurate information, especially if you are working with custom hardware.

This process helps automate and standardize the build and deployment flow, reducing manual work and minimizing the chances of error.