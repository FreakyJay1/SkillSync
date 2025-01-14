from datetime import datetime, time
import re

def is_weekday(dt: datetime):
    
    """
        Check if a given date is a weekday.
        Args:
            dt (datetime): The date to check.
        Returns:
            bool: True if the date is a weekday (Monday to Friday), False otherwise.
    """
    
    return dt.weekday() < 5 

def is_valid_time_range(start_dt: datetime, end_dt: datetime):
    
    """
        Check if the given start and end datetime objects fall within the valid time range of 7:00 AM to 5:00 PM.
        Args:
            start_dt (datetime): The start datetime object.
            end_dt (datetime): The end datetime object.
        Returns:
            bool: True if both start and end times are within the range of 7:00 AM to 5:00 PM, False otherwise.
    """
    
    start_time = start_dt.time()
    end_time = end_dt.time()
    
    return time(7, 0) <= start_time <= time(17, 0) and time(7, 0) <= end_time <= time(17, 0)

def parse_datetime_string(date_str, time_str):
    
    """
        Parses a date and time string and returns a datetime object.
        Args:
            date_str (str): The date string in the format 'YYYY-MM-DD'.
            time_str (str): The time string in the format 'HH:MM'.
        Returns:
            datetime: A datetime object representing the parsed date and time.
        Raises:
            ValueError: If the date or time string is not in the correct format.
    """
    
    try:
        return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    
    except ValueError:
        raise ValueError("Invalid date or time format. Use YYYY-MM-DD HH:MM.")

def is_valid_email(email):
    
    """
        Check if the given email address is valid.
        Args:
            email (str): The email address to check.
        Returns:
            bool: True if the email address is valid, False otherwise.
    """
    
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    
    return re.match(regex, email) is not None

def is_strong_password(password):
    
    """
        Checks if the given password is strong.
        A strong password is defined as one that:
        - Is at least 8 characters long
        - Contains at least one lowercase letter
        - Contains at least one uppercase letter
        - Contains at least one digit
        Args:
            password (str): The password to check.
        Returns:
            bool: True if the password is strong, False otherwise.
    """
    
    if len(password) < 8:
        return False
    
    if not re.search("[a-z]", password):
        return False
    
    if not re.search("[A-Z]", password):
        return False
    
    if not re.search("[0-9]", password):
        return False
    
    return True
