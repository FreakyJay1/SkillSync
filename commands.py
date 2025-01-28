from auth import register_user, login_user, get_current_user_id, logout_user
from database import add_user_to_db, get_mentors, book_meeting_in_db, get_user_by_id,get_peers
from calendar_api import create_calendar_event
from models import Meeting
from utils import parse_datetime_string, is_valid_email, is_strong_password

def handle_command(args):
    """
        Handles various commands based on the provided arguments.
        Args:
            args: An object containing the command and associated parameters.
                Expected attributes:
                - command (str): The command to execute. Possible values are "register_mentor", "register_peer", "login", "logout", "book_meeting".
                - email (str): The email address of the user (required for "register_mentor", "register_peer", "login").
                - password (str): The password of the user (required for "register_mentor", "register_peer", "login").
                - name (str): The name of the user (required for "register_mentor", "register_peer").
        Commands:
            - "register_mentor": Registers a new mentor with expertise and availability.
            - "register_peer": Registers a new peer.
            - "login": Logs in a user.
            - "logout": Logs out the current user.
            - "book_meeting": Books a meeting with a mentor for the current logged-in peer.
        Returns:
            None
    """
    
    if args.command == "register_mentor":
        expertise = input("Enter your area of expertise: ")
        availability = input("Enter your availability (e.g., Mon-Wed 9-5, Fri 10-1): ")
        
        if not is_valid_email(args.email):
            print("Invalid email format.")
            return
        
        if not is_strong_password(args.password):
            print("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number.")
            return
        
        user = register_user(args.email, args.password, args.name, "mentor")
        if user:
            add_user_to_db(user.uid, args.name, args.email, "mentor", expertise, availability)
    
    elif args.command == "register_peer":
        if not is_valid_email(args.email):
            print("Invalid email format.")
            return
        
        if not is_strong_password(args.password):
            print("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one number.")
            return
        
        user = register_user(args.email, args.password, args.name, "peer")
        if user:
            add_user_to_db(user.uid, args.name, args.email, "peer")
    
    elif args.command == "login":
        login_user(args.email, args.password)
    
    elif args.command == "logout":
        logout_user()
    
    elif args.command == "book_meeting":
        # Role-Based Logic: Check if the user is logged in
        current_user_id = get_current_user_id()

        if not current_user_id:
            print("Please log in to book a meeting.")
            return

        current_user = get_user_by_id(current_user_id)  # Fetch user from Firestore

        # Check if the current user is a mentor or a peer
        if current_user.role == "peer":
            # Existing logic for peers booking meetings with mentors
            mentors = get_mentors()
            if not mentors:
                print("No mentors available.")
                return

            print("Available Mentors:")
            for i, mentor in enumerate(mentors):
                print(
                    f"{i + 1}. {mentor.name} (Expertise: {mentor.expertise}, Availability: {mentor.availability})"
                )

            # Get Mentor Selection
            while True:
                try:
                    mentor_index = int(input("Select a mentor by number: ")) - 1
                    selected_mentor = mentors[mentor_index]
                    break
                except (ValueError, IndexError):
                    print("Invalid mentor selection. Please enter a valid number.")

            # Parse Date and Time 
            # Use args.date and args.time directly
            try:
                start_time = parse_datetime_string(args.date, args.time)
                end_time = start_time.replace(hour=start_time.hour + 1)
            except ValueError as e:
                print(e)
                return

            # Book Meeting in Database
            meeting_id = book_meeting_in_db(
                selected_mentor.user_id, current_user_id, start_time, end_time, booked_by_role="peer"
            )

            # Create Google Calendar Event
            meeting = Meeting(
                meeting_id, selected_mentor.user_id, current_user_id, start_time, end_time
            )
            try:
                create_calendar_event(meeting)
            except ValueError as e:
                print(e)
                print(
                    "Error creating calendar event. The meeting has been booked in the database but not on the calendar."
                )

        elif current_user.role == "mentor":
            # New logic for mentors booking meetings with peers
            peers = get_peers()
            if not peers:
                print("No peers available.")
                return

            print("Available Peers:")
            for i, peer in enumerate(peers):
                print(f"{i + 1}. {peer.name} (Email: {peer.email})")

            # Get Peer Selection
            while True:
                try:
                    peer_index = int(input("Select a peer by number: ")) - 1
                    selected_peer = peers[peer_index]
                    break
                except (ValueError, IndexError):
                    print("Invalid peer selection. Please enter a valid number.")

            # Parse Date and Time (same as for peers booking with mentors)
            # Use args.date and args.time directly
            try:
                start_time = parse_datetime_string(args.date, args.time)
                end_time = start_time.replace(hour=start_time.hour + 1)
            except ValueError as e:
                print(e)
                return

            # Book Meeting in Database (switch mentor_id and peer_id)
            meeting_id = book_meeting_in_db(
                current_user_id, selected_peer.user_id, start_time, end_time, booked_by_role="mentor"
            )

            # Create Google Calendar Event
            meeting = Meeting(
                meeting_id, current_user_id, selected_peer.user_id, start_time, end_time
            )
            try:
                create_calendar_event(meeting)
            except ValueError as e:
                print(e)
                print(
                    "Error creating calendar event. The meeting has been booked in the database but not on the calendar."
                )

        else:
            print("Invalid user role.")
            return
    else:
        print("Invalid command")