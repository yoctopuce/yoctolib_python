#!/usr/bin/env python

#
# Run this script to install yocto_api as a package
#

import os
import site
import shutil

src = "Sources/yocto_api"
site_packages = site.getsitepackages()[0]
dest = os.path.join(site_packages, "yocto_api")

print("Install in:", dest)

try:
    shutil.copytree(src, dest)
# Directories are the same
except shutil.Error as e:
    print('Directory not copied. Error: %s' % e)
# Any error saying that the directory doesn't exist
except OSError as e:
    print('Directory not copied. Error: %s' % e)
