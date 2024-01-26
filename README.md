# VMware vCenter Connection Script

This Python script connects to a VMware vCenter server, retrieves information about virtual machines (VMs) in a specified cluster, prints this information in a structured format, and is compatible with both Windows and Linux environments.

## Requirements

- **Python**: The script is written in Python 3.12.0. Python 3.12.0 is recommended. Ensure you have Python installed on your system.
- **pyVmomi**: This is the Python SDK for the VMware vSphere API that allows you to manage ESXi and vCenter server.

## Installation Steps

### Windows

1. **Install Python**: Download and install Python from [python.org](https://www.python.org). During installation, ensure to select the option to Add Python to PATH.
2. **Verify Installation**: Open Command Prompt and run `python --version` and `pip --version` to verify the installation.

### Linux

1. **Install Python**: Most Linux distributions come with Python pre-installed. If not, install it using your distribution's package manager. For Ubuntu, use `sudo apt install python3`.
2. **Verify Installation**: Open a terminal and run `python3 --version` and `pip3 --version` to verify the installation.

## Install Required Libraries

Run the following command to install the required Python library pyVmomi:

- **Windows**: `pip install pyvmomi`
- **Linux**: `pip3 install pyvmomi`

Note: We are installing pyVmomi, the Python SDK for VMware vSphere. This installation is necessary because it includes pyVim, which we are using for this script. Additionally, pyVmomi is a useful and essential tool in many areas.

## Create required Config.ini

Create a configuration file `config.ini` with the following structure:

### Example

```ini
[vCenter]
host = 192.168.1.########
user = ########@########.####
password = ########

[Cluster]
name = ########
```

## Running the Script

1. Save the script as `vcenter_info.py`.
2. Open a terminal or Command Prompt.
3. Navigate to the directory containing `vcenter_info.py`.
4. Run the script with the following command:
   - **Windows**: `python vcenter_info.py path_to_your_config_file`
   - **Linux**: `python3 vcenter_info.py path_to_your_config_file`

   Replace `path_to_your_config_file` with the path to your `config.ini` file.

### Example Output (Prints to terminal)

```json
[
    {
        "name": "vm1",
        "creator": "unknown",
        "creation_date": "2021-01-01T00:00:00",
        "resource_allocation": {
            "cpu": 4,
            "memory": 8192
        }
    },
    {
        "name": "vm2",
        "creator": "unknown",
        "creation_date": "2021-01-02T00:00:00",
        "resource_allocation": {
            "cpu": 2,
            "memory": 4096
        }
    }
]
```
### Understanding Output

Currently, the `creator` information for VMs is set as "unknown" in the output. This is due to the complexity involved in retrieving creator data through our existing methods. 
Acquiring this information requires additional scripting and more intricate interaction with the vCenter APIs, which is beyond the scope of our current time constraints. 
However, enhancing the script to include VM creator details is a goal for future updates. We aim to improve the script's capabilities as we continue to develop and refine our approach.

## Troubleshooting

- **Module Not Found Errors**:
  - Make sure all required Python modules are installed (pyVmomi, ConfigParser, etc.). If a module is missing, install it using pip (e.g., `pip install pyvmomi`).

- **Connection Errors**:
  - Verify that the vCenter details in the configuration file are correct.
  - Ensure that your machine can reach the vCenter server (no network issues).

- **Configuration File Errors**:
  - Ensure the configuration file is correctly formatted and all necessary keys are provided.

- **Script Errors**:
  - Review any error messages in the output. They should give clues about what's gone wrong.

## Future Goals

As this project evolves, there are several enhancements we aim to implement, should time and resources permit. These goals are focused on increasing the functionality and efficiency of the script:

1. **Retrieve Creator Information**: A primary objective is to enhance the script to capture the creator information of VMs. This task involves more complex scripting and deeper interaction with the vCenter APIs. Achieving this will provide more comprehensive data about each VM.

2. **Designate Output File for JSON**: Implementing a feature to allow users to specify an output file for the JSON data. This would make the script more user-friendly by providing flexibility in how and where users want to save their data.

3. **Multithreading/Parallel Processing**: To improve the efficiency of data retrieval, especially in environments with numerous hosts and VMs, I plan to explore multithreading or parallel processing techniques. This would significantly speed up the process of gathering VM information from each cluster, making the tool more efficient for large-scale deployments.

4. **Metadata Tags via Config File**: Another enhancement on the horizon is to allow the application of metadata tags to VMs through a configuration file. This would enable users to categorize and organize VMs more efficiently based on their specific requirements and use cases.

Each of these goals is aimed at enhancing the script's capabilities, making it more robust, user-friendly, and suitable for diverse environments and use cases.
