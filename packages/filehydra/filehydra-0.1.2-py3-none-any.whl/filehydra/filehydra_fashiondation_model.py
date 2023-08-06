
import filehydra

import os

cloth_type="dresses"

cloth_type="skirts"
#Example
hydra=filehydra.FileHydra("")
#hydra.move_file("",".pdf","C:\\Users\\EUROCOM\\Desktop\\Folder","C:\\Users\\EUROCOM\\Desktop",0)

directory="C:\\Users\\EUROCOM\\Documents\\Git\\DovaX\\fashiondation\\react-flask-mysql-login-reg\\src\\discover\\woman\\"+cloth_type
suffix="jpg"

files=list(os.walk(directory))
files=files[:-1]
#files=glob.glob(directory + '/*'+suffix, recursive=True)


#files=hydra.get_files_in_directory("C:\\Users\\EUROCOM\\Documents\\Git\\DovaX\\fashiondation\\react-flask-mysql-login-reg\\src\\discover\\woman\\skirts\\*.png",)
for i in range(len(files)):
    folder=files[i][0]
    
    hydra.move_file("",".jpg",folder,"C:\\Users\\EUROCOM\\Documents\\Git\\DovaX\\fashiondation\\react-flask-mysql-login-reg\\src\\discover\\woman\\"+cloth_type+"\\"+str(i)+".jpg",2)
#"C:\\Users\\EUROCOM\\Documents\\Git\\DovaX\\fashiondation\\react-flask-mysql-login-reg\\src\\discover\\woman\\skirts\\1693693-levi-s-sukne"

