#spliting the data into the approprite structure for the terminal 
import os
import shutil
import random

# Define paths
coco_path = 'C:\\COCO'
images_path = os.path.join(coco_path, 'images')
train_images_path = os.path.join(coco_path, 'train', 'images')
val_images_path = os.path.join(coco_path, 'val', 'images')

# Create directories if they don't exist
os.makedirs(train_images_path, exist_ok=True)
os.makedirs(val_images_path, exist_ok=True)

# Get list of downloaded images
image_files = [f for f in os.listdir(images_path) if f.endswith('.jpg')]

# Shuffle and split data (80% train, 20% val)
random.shuffle(image_files)
split_index = int(0.8 * len(image_files))

train_files = image_files[:split_index]
val_files = image_files[split_index:]

# Move files to respective directories
for file in train_files:
    shutil.move(os.path.join(images_path, file), os.path.join(train_images_path, file))

for file in val_files:
    shutil.move(os.path.join(images_path, file), os.path.join(val_images_path, file))

print('Data split complete!')
