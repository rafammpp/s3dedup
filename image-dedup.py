import os
import shutil
import json
from pathlib import Path

abs_path = os.path.dirname(os.path.abspath(__file__))
os.system('findimagedupes -f fingerprints images > dupes.txt')

image_dupes_path = os.path.join(abs_path, 'dupes.txt')
print('dupes.txt path: ', image_dupes_path)
dupe_list = []
url_translate = {}
dedup_dir = './images_dedup/'


with open(image_dupes_path) as file:
    for line in file:
        image_list = line.split(' ')
        image_list = [(i.strip('\n'), Path(i.strip('\n')).stat().st_size) for i in image_list]
        image_list.sort(key=lambda tup: tup[1], reverse=True)
        print(image_list)
        dupe_list += [i[0] for i in image_list[1:]]
        for image in image_list:
            url_translate[image[0]] = image_list[0][0]

with os.scandir(os.path.join(abs_path, 'images/')) as directory:
    for file in directory:
        if file.is_file() and file.path not in dupe_list:
            if not os.path.exists(dedup_dir):
                os.makedirs(dedup_dir)
            shutil.copy(file.path, dedup_dir+file.name)


with open('url_translate.json', 'w') as file:
    file.write(json.dumps(url_translate))
