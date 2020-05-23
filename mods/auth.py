import pickle 


def load_user():
    with open('proj.pk', 'rb') as f:
        data = pickle.load(f)
    return data.split(',')

def save_user(up):
    with open('proj.pk', 'wb') as f:
        data = pickle.dump(up,f)


def auth(username,password):
    ou,op = load_user()
    if ou == username:
        if op == password:
            return True

def create_cred():
    u = input('enter new username: ')
    p = input('enter new password: ')
    if u and p:
        up=f'{u},{p}'
        save_user(up)


if __name__ == "__main__":
    # run this file first
    x  = input('enter name')
    y  = input('enter password')
    if x and y:
        out = auth(x,y)
        
