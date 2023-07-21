import os
import subprocess
import shutil

top_level_files_to_copy = ["config.json", "User Instructions.md", "run.bat"]
dist_folder = "dist"

subprocess.run(["PyInstaller", "main.spec", "--noconfirm"])

for file_to_copy in top_level_files_to_copy:
    shutil.copyfile(file_to_copy, os.path.join(dist_folder, file_to_copy))
