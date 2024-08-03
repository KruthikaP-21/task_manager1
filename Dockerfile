# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /task_manager1

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the working directory
COPY . .

# Expose the port that the Flask app runs on
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app1/app.py
ENV FLASK_ENV=production

# Run the application
CMD ["cd","app1"]
CMD ["python", "wait-for-it.py", "db", "3306", "&&", "python","-m","flask", "run", "--host=0.0.0.0"]
