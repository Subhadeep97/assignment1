import re

def check_password_strength(password):

    if len(password) < 8:
        return False

    if not re.search("[a-z]", password):
        return False

    if not re.search("[A-Z]", password):
        return False

    if not re.search("[0-9]", password):
        return False

    if not re.search("[!@#\$%^&*_()+-]", password):
        return False

    return True

if __name__ == "__main__":
    password = input("Enter your password: ")
    if check_password_strength(password):
        print("Password is strong.")
    else:
        print("Password is weak. Please choose a stronger password.")
