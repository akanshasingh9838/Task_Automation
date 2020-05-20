import streamlit as st
from PIL import Image
import matplotlib
import os
import sys 
import datetime
import shutil
import urllib.request
import PyPDF2 as p2
from pdf import *
from files import *
from typing import Dict
matplotlib.use('Agg')




html_temp="""
    <div style="background-color:crimson;padding:15px;">
    <h1>Task Automation</h1>
    </div>
    """
html_temp1="""
    <div style="background-color:crimson;padding:5px;">
    <h1>Choose->TOOLS</h1>
    </div>
    """

st.markdown(html_temp,unsafe_allow_html=True)
#img=Image.open("images/task1.jpg")
#st.image(img,width=500)


st.sidebar.markdown(html_temp1,unsafe_allow_html=True)
#img2=Image.open("images/task1.jpg")
#st.sidebar.image(img2,width=305)
def get_static_store():
    return {}

def save_img(img,path):
    with open(path,'wb') as f:
        f.write(img.read())

def main():
    activities=['FILE PROCESS','PDF TOOLS','INFO ABOUT FILES/FOLDERS/DIRECTORIES','DOWNLOAD IMAGE','BATCH FILE CREATION','CONVERT PHOTOS TO PDF']
    choice=st.sidebar.selectbox("Select Activity",activities)
    if choice=='FILE PROCESS':
        st.header("PROCESSING OF FILE RELATED DATA")
        st.subheader("Choose the option")
        fileactivity=['Find all files which are older than x days','Sorting files in the Folder','Copy the content of one file into another','find all files of required extension']
        filechoice=st.selectbox("Select Activity to perform",fileactivity)
        if filechoice=='Find all files which are older than x days':
            req_path=st.text_input("Enter your path","Type here...")
            st.write(os.listdir(req_path))
            days=st.slider("Slide how many days u want",1,100)
            if not os.path.exists(req_path):
                st.write("not exist")

            if os.path.isfile(req_path):
                st.write("please provide directory path")
                
            today_date=datetime.datetime.now()
            for each_file in os.listdir(req_path):
                each_file_path=os.path.join(req_path,each_file)
                if os.path.isfile(each_file_path):
                    file_creat_date=datetime.datetime.fromtimestamp(os.path.getctime(each_file_path))
                    difference_in_days=(today_date-file_creat_date).days
                    if difference_in_days>days:
                        st.write(each_file_path,difference_in_days)
        

        if filechoice == 'Sorting files in the Folder':
            path=st.text_input("Enter path to the folder whose files u want to sort ","Type here...")
            files=os.listdir(path)
            st.write(files)
            folder=st.multiselect("Folders name u want to make, in which u want to kept files?",("pdf","txt","image","python"))
            st.write("You selected ",len(folder),folder)
            
            for x in range(0,len(folder)):
                if not os.path.exists(path+folder[x]):
                    os.makedirs(path+folder[x])

            for f in files:
                if "png" or "jpg" or "PNG" in f and not os.path.exists(path+'image/'+f):
                    shutil.move(path+'\\'+f,path+'image/'+f)
                if "pdf" in f and not os.path.exists(path+'pdfs/'+f):
                    shutil.move(path+'\\'+f,path+'pdf/'+f)
                if "txt" in f and not os.path.exists(path+'text/'+f):
                    shutil.move(path+'\\'+f,path+'text/'+f)
        
        if filechoice =='Copy the content of one file into another':
            st.write("Enter following details ")
            sfile=st.text_input("Enter your source file location","Type here...")
            dfile=st.text_input("Enter your destination file location")
            sfo=open(sfile,'r')
            content=sfo.read()
            sfo.close()
            dfo=open(dfile,'w')
            dfo.write(content)
            if st.checkbox("Show Copied Content"):
                st.write(content)
            dfo.close()

        if filechoice == 'find all files of required extension':
            st.write("Enter following details ")
            rpath=st.text_input("Enter your directory path","Type here...")
            if os.path.isfile(rpath):
                st.write(f"The given path {rpath} is a file. Please! pass only directory path")
            else:
                st.write("logic starts")
                st.write(rpath)
                #all_files=os.listdir(rpath)
               
                # if len(all_files)==0:
                #     st.write(f"The given path {rpath} is an empty")
                # else:
                #     req_ex=st.text_input("Enter the required files extension such as .py/.txt/.log/.sh/.zip")
                #     req_files=[]
                #     for eachfile in all_files:
                #         if eachfile.endswith(req_ex):
                #             req_files.append(eachfile)
                #     if len(req_files)==0:
                #         st.write("There are no {req_ex} files in the location of {rpath}")
                #     else:
                #         st.write(f"There are {len(req_files)} files in the location of {rpath} with an extension of {req_ex}")
                #         st.write(f"So, The files are : {req_files}")
    if choice=='PDF TOOLS':
        st.header("PROCESSING OF PDF RELATED STUFF")
        st.subheader("Choose the option")
        pdfact=['Extract data of pdf','Merge pages of pdf','Get document info','Convert Photos to pdf']
        pdfchoice=st.selectbox("Select Activity to perform",pdfact)
        data=st.file_uploader("Upload a file",type=['pdf'])
        if data:
            pdf_path = 'uploads/file.pdf'
            save_pdf(data,pdf_path)
            if pdfchoice == 'Extract data of pdf':
                result = extract_text_from_pdf(pdf_path)
                if result:
                    st.subheader("extracted data from PDF file")
                    if st.button('save'):
                        name = st.text_input('file name (no extensions)')
                        if name:
                            try:
                                savepath = f'extracted/{name}.txt'
                                with open(savepath,'w') as f:
                                    f.write(result)
                                    st.success(f"saved file to {savepath}")
                            except:
                                st.error('error occured during saving the file')
                    st.write(result)
                else:
                    st.error("could not extract data from file")
           

            elif pdfchoice == 'Merge pages of pdf':
                PDFfile=open(pdf_path,"rb")
                pdfread=p2.PdfFileReader(PDFfile)
                st.info(f'Uploaded file has {pdfread.numPages} pages')
                pageno=st.slider("Which page you want to merge to another pdf")
                st.write("Upload file to be merge")
                mergedata=st.file_uploader("Upload another file",type=['pdf'])
                save_pdf(mergedata,pdf_path)
                PDFfile2=open(pdf_path,"rb")
                pdfread2=p2.PdfFileReader(PDFfile)
                st.info(f'Uploaded file has {pdfread2.numPages} pages')

                page_one=pdfread.getPage(pageno)
                output_file=open('new_pdf1.pdf','wb')
                pdfwriter=p2.PdfFileWriter()
                pdfwriter.addPage(page_one)
                pdfwriter.write(output_file)
                st.write("page is added successfully to another pdf")

            

            elif pdfchoice =='Get document info' :
                st.write(getinfo(pdf_path))

            
            else:
                st.error("select an option")
        else:
            st.error("upload a file to conitnue")

    if choice == 'INFO ABOUT FILES/FOLDERS/DIRECTORIES':
        
        path=st.text_input("Enter path to which you want information ","Type here...")
        if path:
            st.write(list(os.walk(path)))

            st.subheader("All Directories")
            for r,d,f in os.walk(path,topdown=False):
                if len(d)!=0:
                    for each_dir in d:
                        st.write(each_dir)

            st.subheader("All Files")
            for r,d,f in os.walk(path,topdown=False):
                if len(f)!=0:
                    for each_file in f:
                        st.write(each_file)
                    

            # for r,d,f in os.walk(path,topdown=False):
            #     if len(f)!=0:
            #         st.write(r)
            #         for each_file in f:
            #             st.write(each_file)
                
            st.success("Only this much u have")

        else:
            st.info("Enter the path")
                

    if choice == 'DOWNLOAD IMAGE':
        st.write("Enter following details to download image from web")
        url=st.text_input("Enter img url to download from web","Type here...")
        file_name=st.text_input("Enter filename to save as:","Type here...")
        def dl_jpg(url,file_path,file_name):
            full_path=file_path+file_name+'.jpg'
            urllib.request.urlretrieve(url,full_path)
        dl_jpg(url,'images/',file_name)


    if choice == 'BATCH FILE CREATION':
        path=st.text_input("Write path where u want to create folder ","Type_here")
        n=st.slider("Enter how many folders you want inside given path",1,100)
        folname=st.text_input("Write the name u want to give to the folder")
        yn=st.text_input("Writeif u want subfolders inside each folder y/n ","Type_here")
        if yn is 'y':
            n1=st.slider("Enter how many sub folders you want inside each folder",1,100)
            infolname=st.text_input("Write the name u want to give to the subfolders")
        else:
            n1=0
            infolname=None
        createFol(path,n,folname,yn,n1,infolname)

    if choice =='CONVERT PHOTOS TO PDF':
        # static_store=get_static_store()
        # st.info(__doc__)
        # result=st.file_uploader("Upload",type=['png','jpeg','jpg'])
        # if result:
        #     value=result.getvalue()
        #     if not value in static_store.values():
        #         static_store[result]=value
        # else:
        #     static_store.clear()
        #     st.info("Upload one more photo")                
        
        # if st.button("Clear file list"):
        #     static_store.clear()
        
        # if st.checkbox("Show file list?"):
        #     st.write(list(static_store.keys()))
        
        n=st.slider("Enter how many photos you want to upload")
        result=st.text_input("Write each photo path separated by comma").split(",")
        st.write(result)
        #photo_to_pdf(images)
        img1=Image.open("task.jpg")
        for i in result:
            st.write(i)
            img=Image.open(i)
            img1.save("aka.pdf",'PDF',resolution=100,save_all=True,append_images=[img])

        st.success("Done")

if __name__ == "__main__":
    main()
        



