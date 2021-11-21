import os
from PIL import Image
from tqdm import tqdm
import re
import shutil

file_locs = [os.path.join(os.getcwd(), folder_name) for folder_name in os.listdir(os.getcwd()) if folder_name != "Tachiyomier.py"]

def natural_key(string):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)',string)]

def rename_files(files):
    new_file_names = []

    # Get list of file name and sort them
    file_names = [name for name in os.listdir(files)]
    file_names = sorted(file_names,key=natural_key)

    # Rename files based on the page number
    for name in file_names:

        pic_path = os.path.join(files,name)
        new_pic_path = os.path.join(files,re.sub(r' -.*\.','.',name))

        os.rename(pic_path,new_pic_path)
        new_file_names.append(new_pic_path)

    return new_file_names

def convert_to_jpeg(pics,direc):

    # Loop through all images in the directory
    for idx,page in enumerate(pics):

        # Change the image filetype to jpg or gif
            if page.find('webp') != -1 or page.find('png') != -1:
                img = Image.open(page).convert("RGB")
                img.save(os.path.join(direc,f"{idx:03}.jpg"),"jpeg")
                os.remove(page)

            elif page.find('jpg') != -1 or page.find('jpeg') != -1:
                img = Image.open(page).convert("RGB")
                img.save(os.path.join(direc,f"{idx:03}.jpg"),"jpeg")
                os.remove(page)

            elif page.find('gif') != -1:
                os.rename(page,os.path.join(direc,f"{idx:03}.gif"))

def make_cover_file(cover_direc,chapter_direc):

    # Check if the cover page does not exist
    if not os.path.exists(cover_direc):

        # Copy the first image and rename it as cover.jpg
        page_names = os.listdir(chapter_direc)
        print(chapter_direc)
        shutil.copyfile(os.path.join(chapter_direc,page_names[1]),os.path.join(files,'cover.jpg'))

        # Create the cover page with a given size
        cover = Image.open(os.path.join(files,'cover.jpg'))
        cover.save(os.path.join(files,'cover.jpg'),dpi=(96,96))

for files in tqdm(file_locs):

    cover_path = os.path.join(files,'cover.jpg')
    chapter_path = os.path.join(files,'Chapter')
    outside_path = os.path.join(files,'.outside')
    nomedia_path = os.path.join(files,'.nomedia')
    chp_nomedia_path = os.path.join(chapter_path,'.nomedia')

    # Check if Chapter file exists in folder
    if not os.path.exists(chapter_path):

        # Create chapter folder
        os.mkdir(chapter_path)

        # Check if .nomedia file exists and if not, create it.

        if os.path.exists(outside_path):
            os.rename(outside_path,nomedia_path)

        elif not os.path.exists(nomedia_path):
            with open(chp_nomedia_path,'w') as f:
                pass
            f.close()
        
        elif os.path.exists(nomedia_path):
            os.rename(nomedia_path,chp_nomedia_path)

        # Based on file type, convert it into jpg or remain it as gif file if possible
        convert_to_jpeg(rename_files(files),chapter_path)
    
    else :
        convert_to_jpeg(rename_files(chapter_path),chapter_path)
    
    make_cover_file(cover_path, chapter_path)