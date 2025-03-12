import os
import shutil

# Define paths
base_path = r"C:\Users\welcome\Downloads\People Detection"
train_path = os.path.join(base_path, 'train')
valid_path = os.path.join(base_path, 'valid')
test_path = os.path.join(base_path, 'test')

# Function to move files
def move_files(src, dest_images, dest_labels):
    for file_name in os.listdir(src):
        if file_name.endswith('.jpg'):
            shutil.move(os.path.join(src, file_name), os.path.join(dest_images, file_name))
        elif file_name.endswith('.txt'):
            shutil.move(os.path.join(src, file_name), os.path.join(dest_labels, file_name))

# Move files to respective directories
move_files(train_path, os.path.join(train_path, 'images'), os.path.join(train_path, 'labels'))
move_files(valid_path, os.path.join(valid_path, 'images'), os.path.join(valid_path, 'labels'))
move_files(test_path, os.path.join(test_path, 'images'), os.path.join(test_path, 'labels'))

print("Files organized successfully!")
