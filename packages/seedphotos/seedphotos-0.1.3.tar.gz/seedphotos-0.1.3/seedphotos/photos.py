from os import path
import requests

class Photos:
    def __init__(self, width: int, height: int, filename: str, seed: str, folder: str, format: str):
        self.width = width; self.height = height; self.filename = filename; self.seed = seed; self.folder = folder; self.format = format
    
    def getPhotos(self):
        URL = f'https://picsum.photos/seed/{self.seed}/{self.width}/{self.height}.{self.format}'
        file = requests.get(URL, allow_redirects=True)
        filepath = f'{self.folder}/{self.filename}.{self.format}'

        if file.status_code == requests.codes.OK:
            with open(f'{filepath}','wb') as photo:
                photo.write(file.content)

            size = path.getsize(f'{filepath}')
            print(f'image: .{self.format} size: {float(size) / 1024:.3}KB resolution: {self.width}x{self.height} \n')
            
            OK = 'OK'
            return OK
        else:
            file.raise_for_status()
