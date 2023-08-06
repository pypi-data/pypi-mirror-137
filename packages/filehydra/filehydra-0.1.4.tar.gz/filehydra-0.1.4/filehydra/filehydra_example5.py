

import filehydra_pkg.filehydra.filehydra_core as fh


fq=fh.FileQueue("C:\\Users\\EUROCOM\\Documents\\Git\\DovaX\\forloop-projects\\iroda","iroda_queue")
template=fh.FileTemplate("", "xlsx")
#filename,df=fq.process_next_file(template)


def fc(data1,data2):
    print(len(data1),len(data2))

fq.compare_two_files_and_process_first(template,fc)