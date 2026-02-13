import os
import getpass
from dotenv import load_dotenv

# This file is used to both load secret.env file if user is lazy to input username/password.
class LoginHandler:
    @staticmethod
    def login(apiHandler, storeIdHandler):
        env_path = "secret.env"
        message = ""
        SESSION_ID = "ASP.NET_SessionId"
        sessionId = ""
        isLoggedIn = False
        isUpdateSessionId = False
        if os.path.exists(env_path):
            load_dotenv(env_path)
            sessionId = os.getenv(SESSION_ID)
            if sessionId:
                apiHandler.set_session_id(sessionId)
                print("Trying old session ID to see if it is expired or not.")
                isLoggedIn = storeIdHandler.getAllStoresId(apiHandler)
                # Check if can get all stores id. If cannot then isLoggedIn == false
                if isLoggedIn == True:
                    print("Old session ID can be used. No action necessary.")
                else:
                    print("Token expired, please try again!")
            if isLoggedIn == False:
                username = os.getenv("username")
                password = os.getenv("password")
                if username and password:
                    message = ""
                    isLoggedIn = apiHandler.login(username, password)
                    isUpdateSessionId = True
                else:
                    message = "Username or password field not found in secret.env. Please input manually for login."
        while isLoggedIn == False:
            if (message):
                print(message)
            username = input("Username: ")
            password = getpass.getpass("Password: ")
            isLoggedIn = apiHandler.login(username, password)
            isUpdateSessionId = True
        if os.path.exists(env_path) and isUpdateSessionId:
            lines = []
            updated = False
            with open(env_path, 'r') as f:
                lines = f.readlines()
            # Update the line if it exists
            for i, line in enumerate(lines):
                if line.startswith(SESSION_ID):
                    lines[i] = f"{SESSION_ID}={apiHandler.get_session_id()}\n"  # Update the existing line
                    updated = True
                    break
            # If not updated, append the new key-value pair
            if not updated:
                lines.append(f"{SESSION_ID}={apiHandler.get_session_id()}\n")
            # Write back to the file
            with open(env_path, 'w') as f:
                f.writelines(lines)
            storeIdHandler.getAllStoresId(apiHandler)
        return apiHandler.get_session_id()
        