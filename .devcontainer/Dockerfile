# Use the official Ubuntu image as the base image
FROM ubuntu:latest

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    python3 \
    build-essential \
    tar \
    python3-pip \
    wget \
    gcc \
    make \
    zlib1g-dev

    # Download and install the SPICE Toolkit
RUN wget https://naif.jpl.nasa.gov/pub/naif/toolkit/C/PC_Linux_GCC_64bit/packages/cspice.tar.Z && \
    tar -xvf cspice.tar.Z && \
    wget https://naif.jpl.nasa.gov/pub/naif/toolkit/C/PC_Linux_GCC_64bit/packages/importCSpice.csh && \
    chmod u+x importCSpice.csh && \
    sed -i "s|.csh|/bash|g" importCSpice.csh && \
    ./importCSpice.csh && \
    /bin/bash -f importCSpice.csh

    # Install SpiceyPy using pip
RUN pip3 install spiceypy

# install git 
RUN apt-get -y update
RUN apt-get -y install git

# Print cd cSpiceyPy version for verification
RUN python3 -c "import spiceypy as spice; print('SpiceyPy version:', spice.tkvrsn('TOOLKIT'))"
