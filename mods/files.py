## creating files and folders
import os
import streamlit as st
import shutil as s

def createFol(path,n,folname,yn,n1,infolname):
    current  = os.getcwd()
    if path is not None:
        for i in range(0,n):
            st.write("task started")
            os.chdir(path)
            NewFoldr=folname +str(i)
            os.makedirs(NewFoldr)
            ## to make foldre inside othe foldr
            # ans=input(f"You want folder inside folder {folname} y/n")
            if yn is 'y':
                st.write("subfolders started")
                path2=path+'\\'+NewFoldr
                os.chdir(path2)
            #     n1=int(input("Enter how many folder u want imside this folder"))
                for j in range(0,n1):
                    NewFoldr2=infolname+str(j)
                    os.makedirs(NewFoldr2)
                
            else:
                st.write("task completed")
        os.chdir(current)
    else:
        print("Enter path first")

    
def secretStore(from_dir,fname,pas):
    todir='C:\\Users\\Akansha Singh\\Desktop\\secretfiles'
    todir=os.path.join(todir,fname)
    st.write("directory made")
    os.mkdir(todir)
    st.write("directory made")
    for i in pas:
        st.write("et pass")
        for j in range(1,11):
            path=os.path.join(todir,str(j))
            try:
                os.mkdir(path)
            except:
                print("error")
            for k in range(1,11):
                path2=os.path.join(path,str(k))
                try:
                    os.mkdir(path2)
                except:
                    print('error2')
        todir=todir+'\\'+i
        print(todir)
        print(from_dir)
    try:
        s.move(from_dir,todir)
        
    except:
        print()
            
