import argparse
from commands import handle_command

def main():
    """
        SkillSync - Workshop and Meeting Management CLI

        This script serves as the entry point for the SkillSync command-line interface (CLI) application.
        It allows users to manage workshop bookings and one-on-one meetings by providing functionalities for:

        - Registering as a mentor or a peer
        - Logging in
        - Booking meetings with mentors (for peers)

        Usage:
            To register as a mentor:
            python main.py register_mentor <email> <password> <name>

            To register as a peer:
            python main.py register_peer <email> <password> <name>

            To login:
            python main.py login <email> <password>

            To book a meeting:
            python main.py book_meeting <mentor_id> <date> <time>

            For help on a specific command:
            python main.py <command> -h

        Functions:
            main(): Parses the command-line arguments and invokes the appropriate command handler.
    """

    parser = argparse.ArgumentParser(description="SkillSync - Workshop and Meeting Management CLI", add_help=False)
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit')

    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Register Mentor commands
    
    register_mentor_parser = subparsers.add_parser("register_mentor", help="Register as a mentor")
    register_mentor_parser.add_argument("email", help="Email address")
    register_mentor_parser.add_argument("password", help="Password")
    register_mentor_parser.add_argument("name", help="Full name")
    
    # Register Peer commands
    
    register_peer_parser = subparsers.add_parser("register_peer", help="Register as a peer")
    register_peer_parser.add_argument("email", help="Email address")
    register_peer_parser.add_argument("password", help="Password")
    register_peer_parser.add_argument("name", help="Full name")
    
    # Login commands
    
    login_parser = subparsers.add_parser("login", help="Login to SkillSync")
    login_parser.add_argument("email", help="Email address")
    login_parser.add_argument("password", help="Password")
    
    # Logout commands
    logout_parser = subparsers.add_parser("logout", help="Logout from SkillSync")
    
    # Book Meeting commands
    
    book_meeting_parser = subparsers.add_parser("book_meeting", help="Book a meeting")
    book_meeting_parser.add_argument("mentor_id", help="ID of the mentor (use list_mentors to find IDs)")
    book_meeting_parser.add_argument("date", help="Date of the meeting (YYYY-MM-DD format)")
    book_meeting_parser.add_argument("time", help="Time of the meeting (HH:MM format, 24-hour clock)")
    
    args = parser.parse_args()

    if args.command:
        handle_command(args)
    else:
        print(main.__doc__)

if __name__ == "__main__":
    main()
    
    