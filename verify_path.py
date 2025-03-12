import os

# Corrected path to the extracted directory
dataset_path = r"C:\Users\welcome\Downloads\People Detection"

subdirs = ['train', 'valid', 'test']
subsubdirs = ['images', 'labels']

# Function to verify directory structure
def verify_structure(path):
    for subdir in subdirs:
        for subsubdir in subsubdirs:
            dir_path = os.path.join(path, subdir, subsubdir)
            if os.path.exists(dir_path) and os.path.isdir(dir_path):
                print(f"Directory {dir_path} exists and is correctly structured.")
            else:
                print(f"Directory {dir_path} is missing or incorrectly structured.")

# Verify the dataset structure
verify_structure(dataset_path)


