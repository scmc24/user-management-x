# Base image
FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Set working directory



# Copy requirements first to leverage Docker cache
COPY requirements.txt /requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /requirements.txt


RUN mkdir /app
WORKDIR /app
# Copy application code
COPY ./src /app
COPY .env /app

RUN sed -i 's/\r$//g' /app/start.sh
RUN chmod +x /app/start.sh

# Expose port
EXPOSE 8079

# Command to run the application
ENTRYPOINT [ "/app/start.sh" ]