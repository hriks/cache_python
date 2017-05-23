# cache_python
==============================

Implemented a cache that on start-up would load data from a file into the cache. The cache would have an initial size of 20 elements and upon reaching its limit, to add any new element it would remove the least recently accessed element. On shutdown it should store the cached data back to the file. The data should be stored in the cache according to a caching strategy. Provide options for cache CRUD.

## Setting up development environment

The development environment can be setup like a pythonista
with the usual python module setup.

### The pythonista way

Ensure that you have an updated version of pip

```
pip --version
```
Should atleast be 8.0

If pip version is less than 8.0 upgrade it
```
pip install -U pip
```

This will install latest pip

Ensure that you are in virtualenv
if not install virtual env
```
sudo pip install virtualenv
```
This will make install all dependencies to the virtualenv pip
not on your root pip

From the module folder install the dependencies. This also installs
the module itself in a very pythonic way.

```
pip install -r requirements.txt
```

## HOW TO RUN APPLICATION

Run app by 
```
python app.py filename(Currently supported only for CSV*)
```
Example
```
python app.py test.csv
```

## NOTE

Open app in Browser, App is running at localhost:5000

### 

## * BETA Application may able to read all other formats like txt, doc but formatting may be different