# SeedPhotos

<p>A lib that create image through words</p>

## Install:

<p>Use poetry or pip for installation: </p>

    pip install seedphotos

or

    poetry add seedphotos



## How to use:

```python
from seedphotos.photos import *

    photos = Photos(width=300, height=300, filename='image name', seed='word seed', folder='file folder', format='webp or jpg') # Mandatory parameters to generate the image
    photos.getPhotos() # Download image
```

<p>With all parameters satisfied it looks like this: </p>

```python
from seedphotos.photos import *

photos = Photos(width=300, height=300, filename='image', seed='Brazil', folder='/home/barbosa/test/test', format='jpg')
photos.getPhotos()
```