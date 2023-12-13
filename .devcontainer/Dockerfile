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
    sudo \
    zlib1g-dev

ARG USERNAME=dev
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# create a non-root user
RUN groupadd --gid $USER_GID $USERNAME \
  && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
  # [Optional] Add sudo support for the non-root user
  && apt-get update \
  && apt-get install -y sudo \
  && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
  && chmod 0440 /etc/sudoers.d/$USERNAME \
  # Cleanup
  && rm -rf /var/lib/apt/lists/* \
  && echo "source /usr/share/bash-completion/completions/git" >> /home/$USERNAME/.bashrc

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
