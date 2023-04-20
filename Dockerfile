###
FROM python:3-alpine
COPY requirements.txt .

# Set the working directory to /web
WORKDIR /web

# Copy the current directory contents into the container at /web
ADD . /web
# RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN apk update && \
 apk add python3 postgresql-libs && \
 apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 pip install --trusted-host pypi.python.org -r requirements.txt && \
 apk --purge del .build-deps

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "run.py"]