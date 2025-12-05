Project Overview


This project guides you through creating a complete Dockerized Python application that connects to a PostgreSQL database. You'll learn:

•	Docker fundamentals: Images, containers, Dockerfiles

•	Container networking: Creating custom networks

•	Multi-container applications: Python + PostgreSQL setup

•	Database operations: CRUD operations with PostgreSQL

•	Docker commands: Build, run, manage containers

2. Prerequisites
   
Software Requirements:

1.	Operating System:
   
	Windows 10/11 (64-bit) with WSL2 enabled

	macOS (Catalina 10.15 or newer)

 Linux (Ubuntu 18.04+, Fedora, CentOS)
 
3.	Required Software:
   
	->Docker Desktop (for Windows/macOS) or Docker Engine (for Linux)
  	
	->VS Code or any text editor
  	
	->Terminal/Command Prompt
  	
5.	Basic Knowledge:
   
->	Basic Python programming 

->	Basic command line/terminal usage  

->Fundamental database concept.

->  Before starting, verify your system is ready:

 docker –version 
 
 docker info
 
 docker run hello-world
 
Project Structure:

We'll create two projects:

Project A: Simple Python App in Docker

simple-app/
├── app.py
└── Dockerfile


Project B: Python + PostgreSQL App


docker-postgres-app/
├── app.py
├── Dockerfile



                                        Project A: Simple Python App in Docker

                                        
Create app.py

•	Create a tiny Python file that prints a message.

File app.py:

print("Hello from inside a Docker container!")

•	This is the program the container will run. It helps verify the container works.

3) Create the Dockerfile
   
•	Add a text file named Dockerfile (no extension) that tells Docker how to build the image.

File Dockerfile:

# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy app file
COPY app.py .
# Command to run the app
CMD ["python", "app.py"]

Step-by-step explanation of each line:

•	FROM python:3.10-slim — base image: small official Python 3.10 environment. All images start FROM another image (or scratch).

•	WORKDIR /app — sets the working directory inside the image. Later commands (and the running process) will use /app as the current directory.

•	COPY app.py . — copies app.py from your project folder into /app inside the image. The . means “into the current WORKDIR”.

•	CMD ["python", "app.py"] — default command for the container. When the container starts, it will run python app.py. CMD is the runtime command (can be overridden by docker run <image> <cmd>).


4) Build the Docker image
   
Command:

docker build -t my-python-app .

•	docker build reads the Dockerfile in the current directory (.).

•	-t my-python-app tags the new image with the name my-python-app. The tag makes it easier to refer to the image later.

Important details:

•	The build will run each Dockerfile step and produce layered filesystem image. You’ll see output describing each step.

•	If Docker cannot find Dockerfile or app.py, you’ll get an error — make sure you’re in the folder containing those files.

6) Run a container from the image
   
Command:

docker run my-python-app

•	Docker run creates a new container from the my-python-app image and executes the CMD (python app.py).

•	The container runs, prints the message, then exits (because the script ends).

Expected output in your terminal:

<img width="1450" height="931" alt="Screenshot 2025-12-05 135652" src="https://github.com/user-attachments/assets/c9574919-5b26-4f6b-b27c-7c97c9564e5d" />

 


Stop a running container:

Command:

docker stop <container_id>

Example:

docker stop my-running-app

•	Gracefully asks the container to stop (sends SIGTERM then SIGKILL after a timeout)

<img width="557" height="59" alt="Screenshot 2025-12-05 135808" src="https://github.com/user-attachments/assets/13cb434c-43be-48a5-bcd8-bc320f2b013e" />


 
.
If container already exited:

•	Stopping a stopped container yields an error; you can remove it instead.

8) Remove a container.
   
Command:

docker rm <container_id_or_name>

Example:

docker rm <container_id_or_name>

•	Removing a container frees up the container record. You need to remove containers to clean up disk usage if many stopped containers exist.

<img width="1727" height="987" alt="Screenshot 2025-12-05 135918" src="https://github.com/user-attachments/assets/982ababf-8284-4f6b-94f9-1f545360f0b6" />

 





                                       Project B: Python + PostgreSQL App

									   
Create a Dockerized Python app that:

•	Connects to a PostgreSQL container on a user-defined Docker network

•	Creates a table if it doesn't exist

•	Inserts one row

•	Reads and prints the row

You’ll run Postgres and the app in separate containers on the same network.

1) app.py — robust connecting + create/insert/read
   
Create app.py with the code below. 

This uses a small retry loop (better than a single sleep) so the app waits until Postgres is ready

import time

import psycopg2

time.sleep(5)  # wait for DB container

try:

    conn = psycopg2.connect(
	
        host="my-postgres",
		
        database="mydb",
		
        user="user",
		
        password="pass"
		
    )
	
    cursor = conn.cursor()
	
    print("Connected to PostgreSQL!")
	
    # Create table if it doesn't exist
	
    cursor.execute("""
	
        CREATE TABLE IF NOT EXISTS people (
		
            id SERIAL PRIMARY KEY,
			
            name VARCHAR(100)
			
        );
		
    """)
	
    conn.commit()
	
    print("Table created!")
	
    # Insert multiple values
	
    names = ["Vamsi", "Ris", "Kalyan", "Teja"]
	
    print("Inserting rows...")
	
    for name in names:
	
        cursor.execute("INSERT INTO people (name) VALUES (%s) RETURNING id;", (name,))
		
        inserted_id = cursor.fetchone()[0]
		
        print(f"Inserted row -> ID: {inserted_id}, Name: {name}")
		
    conn.commit()
	
    # Fetch all rows
	
    print("\nFetching all rows from table:")
	
    cursor.execute("SELECT * FROM people;")
	
    rows = cursor.fetchall()
	
    for row in rows:
	
        print(f"ID: {row[0]} | Name: {row[1]}")
		
    cursor.close()
	
    conn.close()
	
except Exception as e:

    print("Error:", e)
	
->Uses env vars to allow easy configuration.

-> Retries connection (so Postgres has time to initialize).

-> Uses psycopg2-binary convenience package in the container.

->Creates table if missing, inserts a row, and prints all rows.

Dockerfile

Create Dockerfile in the same folder:

FROM python:3.10-slim

WORKDIR /app

# Install required OS-level packages for psycopg2

RUN apt-get update && apt-get install -y \

    gcc \
	
    libpq-dev \
	
    && rm -rf /var/lib/apt/lists/*
	
COPY app.py .

RUN pip install --no-cache-dir psycopg2-binary

CMD ["python", "app.py"]

 Build the app image:
 
From the project folder:

docker build -t my-python-app .

Explanation:

•	docker build runs the Dockerfile and creates an image tagged my-python-app.

•	You should see steps execute and finish successfully.

 Create a Docker network
 
Create a user-defined bridge network so containers can address each other by name:

docker network create mynetwork


•	Containers on the same user network can resolve hostnames (my-postgres) to the container IP.


6) Run PostgreSQL container on the network
   
Run Postgres with environment vars matching what the app expects:

docker run -d \

  --name my-postgres \
  
  --network mynetwork \
  
  -e POSTGRES_USER=user \
  
  -e POSTGRES_PASSWORD=pass \
  
  -e POSTGRES_DB=mydb \
  
  -v pgdata:/var/lib/postgresql/data \
  
  postgres:15
  
Explanation of options:

•	-d run detached.

•	--name my-postgres gives container a name; app will use that as hostname.

•	--network mynetwork connects it to the network created earlier.

•	-e sets Postgres env vars (user/pass/db).

•	-v pgdata:... attaches a named Docker volume so data persists between container restarts.

•	postgres:15 pins the image version (preferable to using bare postgres).

Check it’s running:

docker ps

 <img width="666" height="186" alt="Screenshot 2025-12-05 140332" src="https://github.com/user-attachments/assets/0b636911-6ffe-4c30-a657-1f00b5737de9" />


 Run the app container on the same network
 
Now run your app image and connect it to the same network:

docker run --rm --network mynetwork my-python-app

Explanation:

•	--rm removes the container after it exits (keeps things tidy).

•	--network mynetwork lets the app resolve my-postgres

 <img width="1126" height="555" alt="Screenshot 2025-12-05 142727" src="https://github.com/user-attachments/assets/87e3f35e-9018-433a-a239-55fad62c9081" />








