

import streamlit_authenticator as stauth

input_password = input("Write a password ")
hashed_passwords = stauth.Hasher([input_password]).generate()

print(hashed_passwords[0])