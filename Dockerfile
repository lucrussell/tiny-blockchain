FROM python:3.4

# Copy all project files and chdir
COPY . /opt/server
WORKDIR /opt/server

# Install requirements
RUN pip install -r requirements.txt

RUN pip install -e .
