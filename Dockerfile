FROM python:3.11-slim

# Create a user with the same UID/GID as the host user
ARG USER_ID=1000
ARG GROUP_ID=1000
RUN groupadd -g ${GROUP_ID} appuser && \
    useradd -u ${USER_ID} -g appuser -m -s /bin/bash appuser

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Change ownership of the working directory
RUN chown -R appuser:appuser /code

# Switch to the non-root user
USER appuser

# Keep container running
CMD ["tail", "-f", "/dev/null"]