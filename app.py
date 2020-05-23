import streamlit as st
from PIL import Image
import matplotlib
import os
import sys 
import datetime
import shutil
import urllib.request
import PyPDF2 as p2
from mods.pdf import *
from mods.files import *
from typing import Dict
from mods.wakeup import *
from mods.scraper import *
from mods.alarms import activate_alarm
from mods.topics_extractor import extract_topic
from mods.apps_finder import foo
import winreg
from mods.scheduler import schedule
from mods.cleaner import *
from mods.excel import convertpdf
from docx2pdf import convert
from mods.auth import auth

html_temp="""
    <div style="color:crimson;padding:15px;">
    <h1>Task Automation</h1>
    </div>
    """
html_temp1="""
    <div style="color:crimson;padding:5px;">
    <h1>Project Module</h1>
    </div>
    """

#img=Image.open("images/task1.jpg")
#st.image(img,width=500)


st.sidebar.image("images/task3.png",use_column_width=True)
st.sidebar.markdown(html_temp1,unsafe_allow_html=True)

def get_static_store():
    return {}

def save_img(img,path):
    with open(path,'wb') as f:
        f.write(img.read())

def main():
        
    activities=[
        'HOME',
        'FILE PROCESS',
        'PDF TOOLS',
        'INFO ABOUT FILES/FOLDERS/DIRECTORIES',
        'DOWNLOAD IMAGE',
        'BATCH FILE CREATION',
        'CONVERT PHOTOS TO PDF',
        'SECURE FILES (STORE SECRETLY)',
        'SET AN EMAIL REMINDER ALARM',
        'URL LINK EXTRACTOR',
        'WEB PAGE DATA EXTRACTOR',
        'Topics identifier in text'.upper(),
        'Schedule application'.upper(),
        'Clean temporary files'.upper(),
        'Excel to PDF'.upper(),
        'Word to PDF'.upper(),

    ]
    choice=st.sidebar.selectbox("Select Activity",activities)
    if choice =='HOME':
        st.image('task.jpg',use_column_width=True)
        st.info("This project use diffrent python script to do task,")
        st.warning('''
        select an option from the sidebar to use a particular module
        ''')
    if choice=='FILE PROCESS':
        st.header("PROCESSING OF FILE RELATED DATA")
        st.subheader("Choose the option")
        fileactivity=['Find all files which are older than x days','Sorting files in the Folder','Copy the content of one file into another','find all files of required extension']
        filechoice=st.selectbox("Select Activity to perform",fileactivity)
        if filechoice=='Find all files which are older than x days':
            req_path=st.text_input("Enter your path")
            if req_path:
                st.write(os.listdir(req_path))
                days=st.slider("Slide how much old data you wanna see, slide to hide newer files",1,500)
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
            else:
                st.warning("Enter your path first")

        if filechoice == 'Sorting files in the Folder':
            path=st.text_input("Enter path to the folder whose files u want to sort ")
            if path:
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
            else:
                st.warning("Write the path first")

        if filechoice =='Copy the content of one file into another':
            st.write("Enter following details ")
            sfile=st.text_input("Enter your source file location")
            dfile=st.text_input("Enter your destination file location")
            if sfile and dfile:
                sfo=open(sfile,'r')
                content=sfo.read()
                sfo.close()
                dfo=open(dfile,'w')
                dfo.write(content)
                if st.checkbox("Show Copied Content"):
                    st.write(content)
                dfo.close()
            else:
                st.warning("First enter the above details")

        if filechoice == 'find all files of required extension':
                st.write("Enter following details ")
                rpath=st.text_input("Enter your directory path")
                if rpath:
                    if os.path.isfile(rpath):
                        st.write(f"The given path {rpath} is a file. Please! pass only directory path")
                    else:
                        st.write("logic starts")
                        all_files=os.listdir(rpath)
                
                        if len(all_files)==0:
                            st.write(f"The given path {rpath} is an empty")
                        else:
                            req_ex=st.text_input("Enter the required files extension such as .py/.txt/.log/.sh/.zip")
                            req_files=[]
                            for eachfile in all_files:
                                if eachfile.endswith(req_ex):
                                    req_files.append(eachfile)
                            if len(req_files)==0:
                                st.write("There are no {req_ex} files in the location of {rpath}")
                            else:
                                st.info(f"There are {len(req_files)} files in the location of {rpath} with an extension of {req_ex}")
                                for i in req_files:
                                    #st.success(f"So, The files are : {req_files}")
                                    st.success(i)
                else:
                    st.warning("Enter the above details first")
    
    
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
                if mergedata:
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
                else:
                    st.warning("upload another file")

            

            elif pdfchoice =='Get document info' :
                st.write(getinfo(pdf_path))

            
            else:
                st.error("select an option")
        else:
            st.error("upload a file to continue.....")

    if choice == 'INFO ABOUT FILES/FOLDERS/DIRECTORIES':
        path=st.text_input("Enter path to which you want information ")
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

                
            st.success("Only this much u have")

        else:
            st.info("Enter the path first")
                

    if choice == 'DOWNLOAD IMAGE USING URL':
        st.header("Enter following details to download image from web")
        url=st.text_input("Enter img url to download from web")
        if url:
            file_name=st.text_input("Enter filename to save as:")
            def dl_jpg(url,file_path,file_name):
                full_path=file_path+file_name+'.jpg'
                urllib.request.urlretrieve(url,full_path)
                return full_path
            with st.spinner('wait...'): 
                path = dl_jpg(url,'images/',file_name)
                st.image(path,use_column_width=True)
        else:
            st.warning("Enter the url first")


    if choice == 'BATCH FILE CREATION':
        st.header("CREATE MULTIPLE FOLDERS AT ANY LOCATION")
        path=st.text_input("Write path where u want to create folder ")
        if path:
            n=st.slider("Enter how many folders you want inside given path",1,100)
            folname=st.text_input("Write the name u want to give to the folder")
            yn=st.text_input("if u want subfolders inside each folder y/n ")
            if yn is 'y':
                n1=st.slider("Enter how many sub folders you want inside each folder",1,100)
                infolname=st.text_input("Write the name u want to give to the subfolders")
            else:
                n1=0
                infolname=None
            if n and folname and yn:
                createFol(path,n,folname,yn,n1,infolname)
        else:
            st.warning("First write the path")

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
        st.header("Image to pdf converter")
        n=st.slider("Enter how many photos you want to upload")
        result=st.text_input("Write each photo path separated by comma").split(",")
        if n and result:
            st.write(result)
            #photo_to_pdf(images)
            img1=Image.open("task.jpg")
            for i in result:
                st.write(i)
                img=Image.open(i)
                img.save(f"{i.split('.')[0]}.pdf",'PDF',resolution=100,save_all=True)
            st.write(f"store as {i.split('.')[0]}.pdf")
            st.success("Done")
        else:
            st.warning("Fill the above details")

    ## not moving any problem in s.move
    if choice == 'SECURE FILES (STORE SECRETLY)':
        st.header('SECURE FILES (STORE SECRETLY)')
        from_dir=st.text_input("Enter the dir of folder to protect")
        fname=st.text_input("Enter folder name to create")
        pas=st.text_input("Enter the password")
        if from_dir and fname and pas:
            secretStore(from_dir,fname,pas)
        else:
            st.warning("Fill the above details")

    if choice == 'SET AN EMAIL REMINDER ALARM':
        st.warning('slow on windows, works well on linux')
        st.header('SET AN ALARM FOR SENDING EMAIL')
        subject = st.text_input("enter the subject for reminder")
        alarmH=st.number_input("At what hour do you want alarm to ring",value=1)
        alarmM=st.slider("At what min do you want alarm to ring")
        time=['am','pm']
        ap=st.selectbox("Select am/pm",time)
        st.info(alarmH)
        st.info(ap)
        if st.button('start'):
            if alarmH and alarmM and ap:
                if ap is 'pm':
                    alarmH=alarmM+12
                    st.write(alarmH)
                st.info(f" At {alarmH} : {alarmM} {ap} alarm will ring")
                activate_alarm(alarmH,alarmM)

            
        else:
            st.warning("Fill the above details")

    if choice ==  'URL LINK EXTRACTOR':
        st.header("EXTRACT & SAVE LINKS FROM A URL")
        st.info("enter a url below and a file name if you want to save links")
        url = st.text_input("enter a valid a URL")
        save_path = st.text_input("enter the path where you want to save links as txt file")
        if st.button('start'):
            with st.spinner('please wait...'):
                if url:
                    links = link_extractor(url)
                    st.write(links)
                    if save_path:
                        if '.txt' not in save_path:
                            save_path+='.txt'
                        with open(save_path,'a') as f:
                            f.writelines(links)
                        st.success('saved to '+save_path)

    if choice == 'WEB PAGE DATA EXTRACTOR':
        st.header("EXTRACT & SAVE DATA FROM A URL")
        st.info("enter a url below and a file name if you want to save data")
        url = st.text_input("enter a valid a URL")
        save_path = st.text_input("enter the path where you want to save data as txt file")
        
        if st.button('extract'):
            with st.spinner('please wait...'):
                if url:
                    links = data_extractor(url)
                    st.write(links)
                    if save_path:
                        if '.txt' not in save_path:
                            save_path+='.txt'
                        with open(save_path,'a',errors='ignore') as f:
                            f.write(links)
                        st.success('saved to '+save_path)

    if choice == 'Topics identifier in text'.upper():
        st.header("Topics identifier in multisentenced data")
        st.info("enter/ copy paste some text paragraph")
        data = st.text_area('enter sentences with 1 sentence on 1 line')
        topics = st.slider('number of topics ',2,4)
        if st.button("extract topics"):
            if data:
                result = extract_topic(data,num_topics=topics)
                st.write(result)

    if choice == 'Schedule application'.upper():
        st.header('Schedule application'.upper())
        with st.spinner('loading softwares'):
            softwares =  foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY) + foo(winreg.HKEY_CURRENT_USER, 0)
            names = [(k,v.get('name')) for k,v in enumerate(softwares)]
            software = st.selectbox("select a software",names)
            if software:
                sw_path = softwares[software[0]].get('path')
                st.write(sw_path)
                if sw_path is not 'undefined' and os.path.exists(sw_path):
                    st.write('found software location')
                    files = os.listdir(sw_path)
                    exefiles = [f for f in files if '.exe' in f]
                    exename = st.selectbox('select an executable',exefiles)
                    exepath = os.path.join(sw_path,exename)
                    st.write(exepath)

                    date= st.date_input("select a date to schedule")
                    time = st.time_input("select a time")
                    st.subheader('selected date time schedule')
                    st.write(datetime.datetime.combine(date,time))
                    if st.button('confirm'):
                        with st.spinner("scheduling, please wait"):
                            schedule(exepath,datetime.datetime.combine(date,time))
                            st.success("schedule task")
                else:
                    st.error("could not find exe file, try another")

    if choice=='Clean temporary files'.upper():
        st.error("Warning delete files permanently")
        st.warning('be careful')
        st.header('Clean temporary files'.upper())
        dir = st.text_input('enter a directory path')
        if os.path.exists(dir):
            o = st.radio('select an option',('delete file by search','delete by extension','delete temporary'))
            if o =='delete file by name':
                name = st.text_inut('filename(fullname with extension)')
                if name and st.button('confirm'):
                    with st.spinner("deleting"):
                        delete_file(dir,name)
                        st.success("done")
            if o == 'delete by extension':
                ext = st.text_inut('enter extension like *.pyc')
                if name and st.button('confirm'):
                    with st.spinner("deleting"):
                        delete_file_by_extension(dir,ext)
                        st.success("done")
            if o =='delete temporary':
                if st.button('confirm'):
                    with st.spinner("deleting"):
                        temp_file_removal(dir)
                        st.success("done")
        else:
            st.error("path invalid")


    if choice == 'Excel to PDF'.upper():
        st.header('Convert Excel file to pdf file'.upper())
        excelpath = st.text_input('enter path of excel file')
        pdfpath = st.text_input('enter path for new pdf file')
        if excelpath and pdfpath and st.button('convert'):
            with st.spinner('converting'):
                convertpdf(excelpath,pdfpath)
                st.success('done')
        else:
            st.error('invalid details')

    if choice == 'Word to PDF'.upper():
        st.header('Convert Word file to pdf file'.upper())
        wordpath = st.text_input('enter path of excel file')
        pdfpath = st.text_input('enter path for new pdf file')
        if wordpath and pdfpath and st.button('convert'):
            with st.spinner('converting'):
                convert(wordpath,pdfpath)
                st.success('done')




def is_authenticated(password):
    return password == "admin"


def generate_login_block():
    block1 = st.empty()
    block2 = st.empty()

    return block1, block2


def clean_blocks(blocks):
    for block in blocks:
        block.empty()


def login(blocks):
    blocks[0].markdown("""
            <style>
                input {
                    -webkit-text-security: disc;
                }
            </style>
        """, unsafe_allow_html=True)

    return blocks[1].text_input('Password')







if __name__ == "__main__":
    login_blocks = generate_login_block()
    password = login(login_blocks)

    if is_authenticated(password):
        clean_blocks(login_blocks)
        st.balloons()
        main()
    elif password:
        st.info("Please enter a valid password")
        