## creating files and folders
import os
import streamlit as st

def createFol(path,n,folname,yn,n1,infolname):
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
               
    else:
        print("Enter path first")

    
        