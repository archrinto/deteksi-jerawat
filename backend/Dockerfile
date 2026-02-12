FROM jhonatans01/python-dlib-opencv

# Set the working directory inside the container
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install libraries
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Open port 5050
EXPOSE 5050

# The command to start your Flask app
CMD ["python3", "app.py"]
