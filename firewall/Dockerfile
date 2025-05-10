FROM ubuntu:22.04

# Install required packages
RUN apt-get update && \
    apt-get install -y nftables iproute2 iputils-ping && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the nftables config into the container
COPY nftables.conf /etc/nftables.conf

# Run the nftables rules at container start
CMD ["nft", "-f", "/etc/nftables.conf"]
