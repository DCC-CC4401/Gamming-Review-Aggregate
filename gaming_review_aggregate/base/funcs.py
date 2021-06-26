#!/usr/bin/env python3

import hashlib

def AddFoto(img, total_images):
    fileobj = img
    fileb = fileobj.value  
    filename = fileobj.filename

    # creación nuevo nombre archvio 
    hash_archivo = str(total_images) + hashlib.sha256(
            filename.encode()).hexdigest()[0:30]

    file_path = 'media/' + hash_archivo
    with open(file_path, 'wb') as image: 
        image.write(fileb)
    return (filename, file_path)

