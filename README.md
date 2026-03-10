# Visual SLAM Pipeline

A production-ready Visual SLAM pipeline built with ORB-SLAM3, evaluated on the KITTI Odometry Dataset.

## Results

| Sequence | Frames | ATE RMSE (m) | RPE RMSE (m/frame) |
|----------|--------|--------------|-------------------|
| KITTI 00 | 4541   | 7.606        | 0.029             |
| KITTI 05 | 2761   | 5.744        | 0.028             |
| KITTI 08 | 4071   | 13.167       | 0.039             |

![Week 2 Dashboard](results/week2_dashboard.png)

## Stack
- ORB-SLAM3 (Stereo mode)
- ROS2 Humble
- Docker
- KITTI Odometry Dataset
- evo toolbox for evaluation

## Setup
```bash
docker build -t visual-slam-pipeline:v1 -f docker/Dockerfile .
docker run -it --name slam-dev \
  -v /path/to/kitti:/data \
  -v $(pwd)/results:/workspace/results \
  -e LD_LIBRARY_PATH=/usr/local/lib \
  visual-slam-pipeline:v1
```
# Complete

## Week 3: Live Stereo-Inertial SLAM on Intel RealSense D435i

### Hardware Setup
- **Sensor:** Intel RealSense D435i (stereo IR cameras + IMU)
- **Mode:** Stereo-Inertial (IMU_STEREO) — fuses visual odometry with accelerometer/gyroscope
- **Environment:** Indoor room + outdoor vehicle dashboard test

### What Changed from KITTI
KITTI uses pre-recorded stereo sequences with ground truth GPS/IMU. The RealSense test runs **live** — frames are processed in real-time as the camera captures them, with no ground truth for comparison.

The ORB-SLAM3 source code (`stereo_inertial_realsense_D435i.cc`) had two bugs that required fixing:
1. **Missing trajectory save** — the example had no `SLAM.Shutdown()` or `SaveTrajectory()` call at exit
2. **Broken signal handler** — `Ctrl+C` set `b_continue_session = false` but the main loop checked `SLAM.isShutDown()` instead, so the process never exited cleanly

Both were fixed by patching the source and recompiling.

### Results

**Indoor room traversal:** 1443 poses captured over ~60 seconds

![RealSense Trajectory](results/realsense_trajectory.png)

### Failure Mode Analysis

| Failure | Cause | Why it matters |
|---|---|---|
| `not enough acceleration` | IMU needs sufficient motion to estimate gravity direction and bias | Static/slow motion prevents Visual-Inertial initialization |
| `Fail to track local map` | ORB features fail on textureless surfaces or with motion blur | Feature-based SLAM is sensitive to scene texture |
| `BAD LOOP` | Loop closure candidate rejected after Sim3 geometric verification | Visual similarity alone is insufficient — geometry must be consistent |
| IMU drift at scale | IMU integration accumulates error as O(t²) without GPS correction | Why production systems fuse SLAM with GPS and HD maps |

### Key Insight: Why the Trajectory Doesn't Close
Without GPS anchoring, IMU drift causes start and end points to diverge even when the camera physically returns to its origin. In production (Waymo, Cruise), this is addressed by fusing with GPS, HD prior maps, and tighter loop closure thresholds.
