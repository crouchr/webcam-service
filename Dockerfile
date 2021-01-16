# https://linuxize.com/post/how-to-install-opencv-on-debian-10/
# based on Debian Buster
FROM python:3.8.5-buster
LABEL author="Richard Crouch"
LABEL description="Webcam Service"

# generate logs in unbuffered mode
ENV PYTHONUNBUFFERED=1

# install opencv
RUN apt -y update
RUN apt -y install python3-opencv joe

# Install Python dependencies
RUN pip3 install pipenv
COPY Pipfile* ./
RUN pipenv install --system --deploy

# Copy application and files
RUN mkdir /app
COPY app/*.py /app/
WORKDIR /app

EXPOSE 9503

# run Python unbuffered so the logs are flushed
CMD ["python3", "-u", "webcam_service.py"]
#CMD ["tail", "-f", "/dev/null"]
