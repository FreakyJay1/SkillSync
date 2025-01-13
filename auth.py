import firebase_admin
from firebase_admin import credentials, auth
import json
import os

cred = credentials.Certificate("firebase-admin.json")
firebase_admin.initialize_app(cred)

def register_user(email, password, name, role):
    
    """
        Registers a new user with the given email, password, name, and role.
        Args:
            email (str): The email address of the user.
            password (str): The password for the user account.
            name (str): The display name of the user.
            role (str): The role of the user (e.g., admin, user).
        Returns:
            UserRecord: The created user record if registration is successful.
            None: If an error occurs during registration.
        Raises:
            auth.EmailAlreadyExistsError: If the email address is already in use.
            Exception: For any other errors that occur during registration.
    """
    
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=name
        )

        print(f"Successfully registered {role}: {user.uid}")
        return user
    
    except auth.EmailAlreadyExistsError:
        print("Error: Email already exists.")
        return None
    
    except Exception as e:
        print(f"An error occurred during registration: {e}")
        return None

def login_user(email, password):
    
    """
        Authenticates a user with the provided email and password, saves the authentication token
        to a file, and returns the token.
        Args:
            email (str): The email address of the user.
            password (str): The password of the user.
        Returns:
            str: The authentication token for the user.
        Raises:
            Exception: If authentication fails or if there is an issue writing the token to the file.
        Side Effects:
            Writes the authentication token to a file located at ~/.skillsync_token.json with
            permissions set to 600.
    """
    
    user = auth.sign_in_with_email_and_password(email, password)
    id_token = user['idToken']
    
    token_file = os.path.expanduser("~/.skillsync_token.json")
    with open(token_file, "w") as f:
        json.dump({"token": id_token}, f)
    
    os.chmod(token_file, 0o600)

    print("Login successful.")
    return id_token

def get_current_user_id():
    
    """
        Retrieves the current user's ID by reading and verifying an ID token from a local file.
        The function attempts to read a JSON file containing an ID token from the user's home directory.
        It then verifies the token and extracts the user ID (UID) from it.
        Returns:
            str: The user ID (UID) if the token is valid and successfully verified.
            None: If the token file is not found, the token is invalid, expired, or any other error occurs.
        Exceptions:
            FileNotFoundError: If the token file does not exist.
            auth.ExpiredIdTokenError: If the token has expired.
            Exception: For any other errors that occur during reading or verifying the token.
    """
    
    token_file = os.path.expanduser("~/.skillsync_token.json")
    try:
        with open(token_file, "r") as f:
            data = json.load(f)
            id_token = data.get("token")
        if id_token:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token['uid']
        else:
            print("No valid token found. Please log in.")
            return None
    
    except FileNotFoundError:
        print("Token file not found. Please log in.")
        return None
    
    except auth.ExpiredIdTokenError:
        print("Token has expired. Please log in again.")
        return None
    
    except Exception as e:
        print(f"Error reading or verifying token: {e}")
        return None

def logout_user():
    """
        Logs out the user by removing the token file.
        This function attempts to remove the token file located at 
        ~/.skillsync_token.json. If the file is successfully removed, 
        it prints a success message. If the file does not exist, it 
        prints a message indicating that the user is not logged in. 
        If any other exception occurs during the removal process, it 
        prints an error message with the exception details.
    """
    
    token_file = os.path.expanduser("~/.skillsync_token.json")
    
    try:
        os.remove(token_file)
        print("Logged out successfully.")
        
    except FileNotFoundError:
        print("Not logged in.")
        
    except Exception as e:
        print(f"Error during logout: {e}")