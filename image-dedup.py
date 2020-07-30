import os
import shutil
import sys
import json
from pathlib import Path

image_dupes_path = 'dupes.txt'
dupe_list = []
url_translate = {}
dedup_dir = 'images_dedup'
working_dir = os.getcwd()

if len(sys.argv) > 1 and sys.argv[1] == '--clear':
    try:
        os.remove('fingerprints')
    except FileNotFoundError:
        pass


image_folder = input(f'image folder path (absolute or relative to {working_dir})[./images] ') or 'images'

os.system(f'findimagedupes -f fingerprints --prune {image_folder} > dupes.txt')



# relative_path = input('relative path (from the bucket root)? ') or 'banner'
# relative_path = relative_path.strip(os.sep)

with open(image_dupes_path) as file:
    for line in file:
        image_list = line.split(' ')
        image_list = [(i.strip('\n'), Path(i.strip('\n')).stat().st_size) for i in image_list]
        image_list.sort(key=lambda tup: tup[1], reverse=True)
        dupe_list += [i[0] for i in image_list[1:]]
        dedup_image = os.path.basename(image_list[0][0])

        for image in image_list:
            image_name = os.path.basename(image[0])
            url_translate[image_name] = dedup_image

if len(sys.argv) > 1 and sys.argv[1] == '--clear':
    try:
        os.remove('fingerprints')
    except FileNotFoundError:
        pass

if os.path.exists(dedup_dir):
    shutil.rmtree(dedup_dir)

os.makedirs(dedup_dir)

with os.scandir(os.path.abspath(image_folder)) as directory:
    for file in directory:
        if file.is_file() and file.path not in dupe_list:            
            shutil.copy2(file.path, os.path.join(dedup_dir, file.name))

with open('url_translate.json', 'w') as file:
    file.write(json.dumps(url_translate))
