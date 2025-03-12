import os
import requests
from pycocotools.coco import COCO
import time

# Define the paths
coco_path = 'C:\\COCO'
images_path = os.path.join(coco_path, 'images')
annotations_path = os.path.join(coco_path, 'annotations')
os.makedirs(images_path, exist_ok=True)
os.makedirs(annotations_path, exist_ok=True)

# Download the annotations file
annotations_url = 'http://images.cocodataset.org/annotations/annotations_trainval2017.zip'
annotations_zip_path = os.path.join(annotations_path, 'annotations_trainval2017.zip')
annotations_extract_path = os.path.join(annotations_path, 'annotations_trainval2017')

if not os.path.exists(annotations_zip_path):
    print('Downloading annotations...')
    response = requests.get(annotations_url)
    with open(annotations_zip_path, 'wb') as f:
        f.write(response.content)

# Extract the annotations
if not os.path.exists(annotations_extract_path):
    print('Extracting annotations...')
    import zipfile
    with zipfile.ZipFile(annotations_zip_path, 'r') as zip_ref:
        zip_ref.extractall(annotations_extract_path)

# Ensure the JSON file exists
annotation_file_path = os.path.join(annotations_extract_path, 'annotations', 'instances_train2017.json')
if not os.path.exists(annotation_file_path):
    print(f'File not found: {annotation_file_path}')
else:
    print('Loading annotations into memory...')
    coco = COCO(annotation_file_path)

    # Get all image IDs for the 'person' category
    cat_ids = coco.getCatIds(catNms=['person'])
    img_ids = coco.getImgIds(catIds=cat_ids)
    images = coco.loadImgs(img_ids)

    # Function to download images with retry logic
    def download_image(img):
        img_url = img['coco_url']
        img_path = os.path.join(images_path, img['file_name'])
        if not os.path.exists(img_path):
            for attempt in range(5):  # Retry up to 5 times
                try:
                    print(f'Downloading {img["file_name"]}...')
                    img_data = requests.get(img_url).content
                    with open(img_path, 'wb') as f:
                        f.write(img_data)
                    break  # Exit the retry loop if download is successful
                except requests.exceptions.RequestException as e:
                    print(f'Error downloading {img["file_name"]}: {e}')
                    time.sleep(5)  # Wait for 5 seconds before retrying
            else:
                print(f'Failed to download {img["file_name"]} after multiple attempts.')

    # Use threading to download images in parallel
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(download_image, images)

    print('Download complete!')



