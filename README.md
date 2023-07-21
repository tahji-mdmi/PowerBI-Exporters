# MDMi Script Template

## Description

This script will look for all recently modified records and export the data to Excel. "Recently modified records" are records that have been modified after the date listed in the config file. After the script finishes running, the date in the config is updated to the current day. For more information on this, see `User Instructions.md`.

This script also acts as a template for other scripts to built off of! To get started writing your own script, see the rest of this document for instructions!

## Installation and Running

### Clone Template Repository

1. On GitHub.com, navigate to the main page of this repository.
2. Above the file list, click "Use this template" then select "Create a new repository".
3. Fill out the name and description of the new repository.
4. Change the repository visibility to "Private".
5. Click "Create repository from template".

Download your new repository to your machine, then open it in VS Code.

### Install Requirements

1. Open VS Code integrated terminal (`` Ctrl-Shift-` ``).
2. Create a new virtual environment for this project with the commands `python -m pip install virtualenv` and `python -m virtualenv env`.
3. Activate the virtual environement with the command `env\scripts\activate`.
4. Install the required Python modules found in the file `requirements.txt` with the command `python -m pip install -r requirements.txt`.

 > Note, this installs some libraries directly from Git. You must have access to these repositories for `pip` to install these dependencies.

This virtual environment keeps your installed Python modules separate from your other projects, allowing you to have multiple different version installed wihtout clashing.

To run the script (either as-is or after modifications), run the command `python proj\main.py`.

## Folder Structure and Files

This project has a folder structure designed to keep "meta" files and "code" files separate.

"Meta" files are either files not directly related to the script executing, or files that the end user will interact with. This includes...

- Documentation (`README.md` and `User Instructions.md`)
- Configuration files (`config.json`)
- The Python virtual environment (`env` folder)
- `.gitignore`
- `requirements.txt`
- `logs` folder
- `reports` folder

"Code" files are files that contain code or are used by the code, and should never be touched by the end user. These are all included inside the `proj` folder. This includes...

- Python files
- Report templates
- Developer config files

Inside the `proj` folder, the file that Python executes should always be named `main.py` for consistency and clarity. `main.py` will contain a majority of the code for the script and is where most of the processing happens. The `main` function inside this file should be at the top of the file, and as much as possible should read as English. The `main` function should also wrap most of the code in a `try/except` block to catch and log any unexpected errors. At the end of the `main` function, make the script sleep for a few seconds so users can read any messages before the script closes.

The file `projectFunctions.py` (commonly imported as `pf`) contains some of the side functions that `main.py` uses, but that aren't directly related to the script goal and would clutter the file. For example, most scripts will require a Granta MI Session, logging, and a config file, but setting those up is best done in `projectFunctions.py` to keep the rest of the project clean. The first thing the `main` function does is to call `pf.start()` to set up these tools.

The Python working directory is usually set wherever the script is executed. However, if the script was not executed within the `proj` folder then certain files would not be found in the working directory and the script could fail. The function `pf.start` also sets the working directory into the `proj` folder so that all files are consistently found. Whenever the script references files inside the `proj` folder use the `pf.curdir` property, and whenever the script creates user-visible files like logs and reports use the `pf.parentdir` property.

## Modifying the Template

As this template is also an example, you are free to delete any portions of this project that will not be relevent. However, please pay heed to the existing structure and format.

When we deliver code to customers we would like the documentation, config files, reports, and logs to feel familiar. Please do not change their formats too much.

Even if your script does not require reporting, consider adding it anyways to go above and beyond. It may also prove useful when debugging.

## Packaging

To package this script into an executable, run the following command:

``` cmd
python package.py
```

This creates a new `dist` folder that contains everything needed to run this in an environment without Python installed. The file `User Instructions.md` details how to set up and run the project. The executable itself is located inside the `dist\proj` folder, but because there are so many other files inside of that location it is best to run the file `run.bat` on the parent directory.
