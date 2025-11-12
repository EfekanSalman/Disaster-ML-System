# Dockerfile
# This is the list of instructions explaining how to package our "System" (API)
# into a portable "Box" (Container).

# Step 1: Base Image
# We know which Python version we are using (from your logs)
FROM python:3.12-slim

# Step 2: Working Directory
# Put our code inside a folder named /app within the "Box"
WORKDIR /app

# Step 3: Installing Dependencies
# First, copy our "instruction list" (requirements.txt) into the box
COPY requirements.txt .

# Now install ALL packages (fastapi, prophet, sklearn...) from that list
# This will download from the internet during 'docker build'
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copying the "System" Code
# After dependencies are installed, copy the entire "System"
# (src/, models/, the csv file...) into the box (the /app folder)
COPY . .

# Step 5: Exposing the Port
# Our FastAPI (uvicorn) was running on port 8000.
# Expose port 8000 of the "Box" to the outside world
EXPOSE 8000

# Step 6: Command to Run
# The default command to run when this "Box" (Container) is started:
# "Start the API (uvicorn) in production mode"
# Note: There is no '--reload' (development mode) anymore.
# '--host 0.0.0.0' -> Accept connections coming from outside the "Box"
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
