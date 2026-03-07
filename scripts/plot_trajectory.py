import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('results/CameraTrajectory.txt')

x = data[:, 3]   # translation X
y = data[:, 7]   # translation Y  
z = data[:, 11]  # translation Z

plt.figure(figsize=(12, 8))
plt.plot(x, z, 'b-', linewidth=1, label='ORB-SLAM3 Trajectory')
plt.scatter(x[0], z[0], c='green', s=100, zorder=5, label='Start')
plt.scatter(x[-1], z[-1], c='red', s=100, zorder=5, label='End')
plt.xlabel('X (meters)')
plt.ylabel('Z (meters)')
plt.title('ORB-SLAM3 on KITTI Sequence 00')
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.savefig('results/trajectory_seq00.png', dpi=150, bbox_inches='tight')
print("Saved to results/trajectory_seq00.png")
