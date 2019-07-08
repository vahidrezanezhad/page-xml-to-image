all: build install

build:
       python3 setup.py build

install:
       python3 setup.py install --user
       cp pagexml2img/pagexml2img.py ~/bin/pagexml2img
       chmod +x ~/bin/pagexml2img
