# **Recommender System based on User Data**<br>
This project is a recommender system based on user data. It analyzes user behavior and preferences to provide personalized recommendations. The system is built using Flask, a Python web framework, and utilizes a SQLite database for data storage. The project also includes user authentication and session management functionalities.

# **Prerequisites**<br>
Python 3.x<br>
Flask<br>
SQLAlchemy<br>

# **Getting Started**<br>
Follow these steps to run the project after cloning it from GitHub:
<br><br>
## **Create a virtual environment**
To ensure a clean and isolated development environment, it is recommended to set up a virtual environment. Follow the steps below to create and activate a virtual environment:

Install virtualenv (if not already installed) by opening your command prompt or terminal and running the following command:

**pip install virtualenv**<br><br>
Choose a directory where you want to create the virtual environment. This could be your project directory or any other location.

Navigate to the chosen directory using the command prompt or terminal.

Create a new virtual environment by running the following command:

**virtualenv <environment_name>**<br><br>
Replace <environment_name> with the desired name for your virtual environment.

Activate the virtual environment. The process differs depending on your operating system:

For Windows:<br><br>
**<environment_name>\Scripts\activate**<br><br>
For macOS/Linux:<br><br>
**source <environment_name>/bin/activate**<br><br>
Once the virtual environment is activated, you will notice that the command prompt or terminal prompt changes to reflect the name of the virtual environment.

Now you have successfully created and activated the virtual environment. You can proceed with installing the project dependencies and running the code within this isolated environment.

## **Install the required dependencies:**
pip install flask
<br>pip install Flask SQLAlchemy

## **Start the Flask development server:**
python tut1.py

## **Usage**
Home: The homepage of the application, displaying a test message.<br>
View: Displays a list of registered users.<br>
Login: Allows users to log in or create a new account.<br>
User: Shows user details and allows users to update their email address.<br>
Logout: Logs out the current user and clears the session.<br>
IIT List: Displays a table of Colleges.<br>
Individual College: Shows details of a specific IIT based on the provided ID.<br>
Add College: Allows logged-in users to add a new college to the list.<br>

