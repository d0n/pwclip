Installation
------------

On Windows you need to install Python3 from http://python.org/ first. On most
Linux distributions python will be part of the system. With Python installed,
you can install the pwclip package from the Python-Package-Index (pyPI) by
running:

``pip3 install pwclip``

and installing the dependencies (not managed by pip) manually.

Installing from source
----------------------

To install this package from a source distribution archive, do the following:

1. Extract all the files in the distribution archive to some directory on your
   system.

2. In that directory, run:

``python setup.py install``

Installing via apt
------------------

curl deb.janeiskla.de/ubuntu/project/d0ndeb-pub.key | apt-key add -
apt-get update
apt-get install python3-pwclip
