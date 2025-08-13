#get random user data for test
from randomuser import RandomUser
import pandas as pd

r = RandomUser()
user_list = r.generate_users(10)

def get_user():
    users = []

    for user in user_list:
        users.append({"Name ":user.get_full_name(),"Gender":user.get_gender(),"City":user.get_city(),"State":user.get_state(),"Email":user.get_email(),"DOB":user.get_dob(),"Picture":user.get_picture()})

    return pd.DataFrame(users)


usersDF = get_user()
print(usersDF)

