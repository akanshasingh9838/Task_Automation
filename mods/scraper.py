import requests
from bs4 import BeautifulSoup


def link_extractor(url="https://wikipedia.org"):
    linklist = []
    try:
        page = requests.get(url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, 'lxml')
            links = soup.findAll('a')
            for tag in links:
                if tag.attrs.get('href'):
                    if tag.attrs.get('href') != "#":
                        linklist.append(tag.attrs.get('href')+"\n")
                    else:
                        print("empty links")
                else:
                    print("empty a tag")
            else:
                print("done")
        else:
            print("path not found, check address")
    except Exception as e:
        print(e)
    return list(set(linklist))

def data_extractor(url ='http://wikipedia.org'):
    try:
        page = requests.get(url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.text,'lxml')
            return soup.body.text
        else:
            return ""
    except:
        return ""


if __name__ == "__main__":
    links =  link_extractor("https://in.ign.com")
    print(links)