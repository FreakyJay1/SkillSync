from datetime import datetime

class User:
    def __init__(self, user_id, name, email, role, expertise=None, availability=None):
        
        """
            Initialize a new user with the given attributes.
            Args:
                user_id (int): The unique identifier for the user.
                name (str): The name of the user.
                email (str): The email address of the user.
                role (str): The role of the user within the system.
                expertise (str, optional): The area of expertise of the user. Defaults to None.
                availability (str, optional): The availability status of the user. Defaults to None.
        """
        
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role
        self.expertise = expertise
        self.availability = availability

    @classmethod
    def from_dict(cls, user_id, data):
        
        """
            Create an instance of the class from a dictionary.
            Args:
                cls (type): The class to instantiate.
                user_id (int): The ID of the user.
                data (dict): A dictionary containing user data with keys "name", "email", "role", "expertise", and "availability".
            Returns:
                object: An instance of the class.
        """
        
        return cls(user_id, data.get("name"), data.get("email"), data.get("role"), data.get("expertise"), data.get("availability"))

    def to_dict(self):
        
        """
            Converts the object attributes to a dictionary.
            Returns:
                dict: A dictionary containing the object's user_id, name, email, role, expertise, and availability.
        """
        
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "expertise": self.expertise,
            "availability": self.availability
        }

class Meeting:
    def __init__(self, meeting_id, mentor_id, peer_id, start_time, end_time, status="pending"):
        
        """
            Initialize a new meeting instance.
            Args:
                meeting_id (str): The unique identifier for the meeting.
                mentor_id (str): The unique identifier for the mentor.
                peer_id (str): The unique identifier for the peer.
                start_time (datetime): The start time of the meeting.
                end_time (datetime): The end time of the meeting.
                status (str, optional): The status of the meeting. Defaults to "pending".
        """
        
        self.meeting_id = meeting_id
        self.mentor_id = mentor_id
        self.peer_id = peer_id
        self.start_time = start_time
        self.end_time = end_time
        self.status = status

    @classmethod
    def from_dict(cls, meeting_id, data):
        
        """
            Create an instance of the class from a dictionary of attributes.
            Args:
                cls (type): The class to instantiate.
                meeting_id (int): The ID of the meeting.
                data (dict): A dictionary containing the attributes of the meeting.
            Returns:
                An instance of the class with attributes populated from the dictionary.
            The dictionary `data` should have the following keys:
                - "mentor_id" (int): The ID of the mentor.
                - "peer_id" (int): The ID of the peer.
                - "start_time" (datetime, optional): The start time of the meeting.
                - "end_time" (datetime, optional): The end time of the meeting.
                - "status" (str): The status of the meeting.
        """
        
        start_time = data.get("start_time").to_pydatetime() if data.get("start_time") else None
        end_time = data.get("end_time").to_pydatetime() if data.get("end_time") else None

        return cls(meeting_id, data.get("mentor_id"), data.get("peer_id"), start_time, end_time, data.get("status"))

    def to_dict(self):
        
        """
            Converts the meeting object to a dictionary representation.
            Returns:
                dict: A dictionary containing the meeting details with keys:
                    - "meeting_id" (int): The unique identifier for the meeting.
                    - "mentor_id" (int): The unique identifier for the mentor.
                    - "peer_id" (int): The unique identifier for the peer.
                    - "start_time" (datetime): The start time of the meeting.
                    - "end_time" (datetime): The end time of the meeting.
                    - "status" (str): The current status of the meeting.
        """
        
        return {
            "meeting_id": self.meeting_id,
            "mentor_id": self.mentor_id,
            "peer_id": self.peer_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "status": self.status
        }