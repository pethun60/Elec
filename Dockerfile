
FROM python:alpine3.18
# Or any preferred Python version.
#Labels as key value pair
LABEL Maintainer="peterT"
COPY requirements.txt /app/src/requirements.txt
WORKDIR /app/src
RUN pip install -r requirements.txt
#to COPY the remote file at working directory in container
COPY hanport_v11.py .
# Now the structure looks like this '/app/src/test.py'
CMD ["python","./test.py"]

