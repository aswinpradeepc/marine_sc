FROM python:3

# Set environment variables for Python optimizations
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set the working directory in the container
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/

# Copy the project code into the container
COPY . /code/

# Install GDAL dependencies
RUN apt-get update

RUN pip install --upgrade pip

# Install dependencies
RUN pip install setuptools
RUN pip install --no-cache-dir -r requirements.txt



# Expose the port on which Gunicorn will run
EXPOSE 8000
