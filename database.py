import firebase_admin
from firebase_admin import firestore
from models import User, Meeting

db = firestore.client()

def add_user_to_db(user_id, name, email, role, expertise=None, availability=None):
    
    """
        Adds a user to the database with the provided details.
        Args:
            user_id (str): The unique identifier for the user.
            name (str): The name of the user.
            email (str): The email address of the user.
            role (str): The role of the user (e.g., 'admin', 'member').
            expertise (str, optional): The expertise of the user. Defaults to None.
            availability (str, optional): The availability status of the user. Defaults to None.
        Returns:
            None
    """
    
    user_data = {
        "name": name,
        "email": email,
        "role": role,
        "expertise": expertise,
        "availability": availability
    }
    
    db.collection("users").document(user_id).set(user_data)
    
def get_user_by_id(user_id):
    
    """
        Retrieve a user from the database by their user ID.
        Args:
            user_id (str): The unique identifier of the user.
        Returns:
            User: An instance of the User class if the user exists.
            None: If the user does not exist in the database.
    """
    
    doc = db.collection("users").document(user_id).get()
    
    if doc.exists:
        return User.from_dict(doc.id, doc.to_dict())
    
    else:
        return None

def get_mentors():
    
    """
        Retrieves a list of mentors from the database.
        This function queries the "users" collection in the database for documents
        where the "role" field is equal to "mentor". It then converts each document
        into a User object and appends it to a list.
        Returns:
            list: A list of User objects representing mentors.
    """
    
    mentors = []
    
    docs = db.collection("users").where("role", "==", "mentor").stream()
    
    for doc in docs:
        mentors.append(User.from_dict(doc.id, doc.to_dict()))
    return mentors

def book_meeting_in_db(mentor_id, peer_id, start_time, end_time):
    
    """
        Books a meeting in the database with the given details.
        Args:
            mentor_id (str): The ID of the mentor.
            peer_id (str): The ID of the peer.
            start_time (datetime): The start time of the meeting.
            end_time (datetime): The end time of the meeting.
        Returns:
            str: The ID of the newly created meeting document in the database.
    """
    
    meeting_data = {
        "mentor_id": mentor_id,
        "peer_id": peer_id,
        "start_time": start_time,
        "end_time": end_time,
        "status": "pending"
    }
    
    meeting_ref = db.collection("meetings").add(meeting_data)
    return meeting_ref[1].id