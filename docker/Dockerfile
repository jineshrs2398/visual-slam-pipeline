# Base image: ROS2 Humble on Ubuntu 22.04 (current LTS)
FROM ros:humble-ros-base-jammy

# Avoid interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential cmake git python3-pip \
    libopencv-dev libgl1-mesa-glx \
    libeigen3-dev \
    libgl1-mesa-dev libwayland-dev libxkbcommon-dev wayland-protocols \
    libepoxy-dev \
    libboost-all-dev \
    ros-humble-cv-bridge \
    && rm -rf /var/lib/apt/lists/*

# Build Pangolin from source
RUN git clone https://github.com/stevenlovegrove/Pangolin.git /opt/Pangolin && \
    mkdir /opt/Pangolin/build && cd /opt/Pangolin/build && \
    cmake .. && make -j4 && make install

# Install Python packages
RUN pip3 install numpy matplotlib evo

# Clone and build ORB-SLAM3
WORKDIR /opt
RUN git clone https://github.com/UZ-SLAMLab/ORB_SLAM3.git
WORKDIR /opt/ORB_SLAM3
RUN chmod +x build.sh && \
    sed -i 's/-Werror//g' CMakeLists.txt && \
    sed -i 's/++11/++14/g' CMakeLists.txt && \
    sed -i 's/++11/++14/g' Thirdparty/DBoW2/CMakeLists.txt && \
    sed -i 's/++11/++14/g' Thirdparty/g2o/CMakeLists.txt && \
    ./build.sh

# Set working directory for our project
WORKDIR /workspace
CMD ["bash"]