

import filehydra_pkg.filehydra.filehydra_core as fh


fh1=fh.FileHydra()

fh1.create_folder("folder")

fh1.copy_file("filehydra_example.py", "folder")

fh1.rename_file("folder//filehydra_example.py", "folder//testtest.py")