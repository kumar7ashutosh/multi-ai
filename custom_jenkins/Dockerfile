# Use the Jenkins LTS image as base
FROM jenkins/jenkins:lts

# Switch to root user
USER root

# Install Docker + Python inside Jenkins container
RUN apt-get update && \
    apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    python3 \
    python3-pip && \
    install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | \
    gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    chmod a+r /etc/apt/keyrings/docker.gpg && \
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
    https://download.docker.com/linux/debian bookworm stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && \
    apt-get install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    apt-get clean

# Add Jenkins user to Docker group
RUN groupadd -f docker && \
    usermod -aG docker jenkins

# Docker storage directory
RUN mkdir -p /var/lib/docker

# Optional Docker volume
VOLUME /var/lib/docker

# Switch back to Jenkins user
USER jenkins