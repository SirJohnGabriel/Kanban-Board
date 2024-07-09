# Kanban Board Application

## Overview
This Python application implements a simple Kanban board using Tkinter for the GUI and SQLite for the database backend. It allows users to manage tasks through a visual interface with columns representing different stages of task completion.

## Features
- **Task Management:** Add, edit, delete tasks categorized into To-Do, Doing, and Done.
- **GUI Interface:** Utilizes Tkinter and Customtkinter for a simple yet effective graphical interface.
- **SQLite Database:** Stores tasks locally using SQLite for lightweight data management.

## Installation
1. Clone the repository:

  ```
  git clone https://github.com/SirJohnGabriel/Kanban-Board.git
  cd Kanban-Board
  ```

2. Install dependencies:
- Ensure Python 3.11 is installed.
- Install required packages using pip:

  ```
  pip install -r requirements.txt
  ```
  
3. Run the application:

  ```
  python index.py
  ```

## Usage
- Upon launching the application, you'll see columns labeled "To-Do," "Doing," and "Done."
- Click "Add Task" to create a new task.
- Tasks can be edited, deleted, and moved between columns by clicking respective buttons.

## Contributing
Contributions are welcome! If you find any issues or have suggestions, please open an issue or create a pull request.

## License
This project is licensed under the [MIT License](LICENSE).
