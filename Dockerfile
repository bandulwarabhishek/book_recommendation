FROM python:3.10-slim
# Use a specific SHA256 digest for consistency and security
WORKDIR /app
# Copy the requirements file into the container  
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy only necessary files (ignoring venv)
COPY . . 

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]


# FROM cmd-it is taking as the base image 
#     Why Use a SHA256 Digest?
#     -Ensures consistency → Docker will pull the exact image version, avoiding updates that may break your build.
#     -Enhances security → Prevents unexpected changes or tampering in public images.
#     -Useful in production → Keeps builds reliable and repeatable.

# COPY cmd - this will copy all the files from the current repository to the base image on dockerhub
# WORKDIR cmd - this is the working directory
# RUN cmd - it will install all the dependency which is required by the app
# EXPOSE cmd - to expose the application inside the dockerimage we require some port
# CMD cmd - to run the entire application
# 0.0.0.0:$PORT - this line means,we are binding the PORT we got from the dockerimage and assigning to the local address on the heroku cloud 



