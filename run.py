import subprocess

# Define the file names for insert_meals.py and server.py
insert_meals_script = 'insert_meals.py'
server_script = 'server.py'

# Run the insert_meals.py script
subprocess.run(['python', insert_meals_script], check=True)

# Run the server.py script
subprocess.run(['python', server_script], check=True)