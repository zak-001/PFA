FROM debian:bookworm

# Install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        nftables \
        iproute2 \
        iputils-ping \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy your nftables rule set into the container
COPY nftables.conf /etc/nftables.conf

# Run nftables rules at container start
CMD ["nft", "-f", "/etc/nftables.conf"]

