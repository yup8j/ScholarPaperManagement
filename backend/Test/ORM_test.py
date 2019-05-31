from views import *

database.connect()

def test_select():
    username = User.select(User.username)
    print("Length of username list:", len(username))
    print("list as follows:")
    for uname in username:
        print(uname)


if __name__ == '__main__':
    test_select()