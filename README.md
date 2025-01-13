# SkillSync

SkillSync is a Python-based Command-Line Interface (CLI) application designed to manage workshop bookings and one-on-one meetings efficiently. The system leverages Firebase for authentication and database management and integrates the Google Calendar API for scheduling.

## Features

- Request meetings with mentors from a database.
- Schedule one-on-one sessions with peers.
- Ensure all bookings occur strictly during weekdays (Monday to Friday) between 07:00 and 17:00.

## Technology Stack

- **Python**: Core programming language.
- **Firebase**: Used for authentication and database management.
- **Google Calendar API**: Integrated for scheduling meetings.
- **PyInstaller**: Used for packaging the application for distribution.

## Installation

To install SkillSync, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/skillsync.git
    ```
2. Navigate to the project directory:
    ```bash
    cd skillsync
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Package the application using PyInstaller:
    ```bash
    pyinstaller --onefile skillsync.py
    ```

## Usage

Run the application from the terminal:
```bash
./dist/skillsync
```

Follow the on-screen instructions to manage your workshop bookings and one-on-one meetings.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.