import numpy as np
import matplotlib.pyplot as plt
import os

def load_kitti_poses(filepath):
    """Load KITTI format poses (3x4 matrix per line)"""
    poses = []
    with open(filepath) as f:
        for line in f:
            values = list(map(float, line.strip().split()))
            pose = np.array(values).reshape(3, 4)
            poses.append(pose)
    return np.array(poses)

def extract_positions(poses):
    """Extract XYZ positions from pose matrices"""
    positions = poses[:, :3, 3]
    return positions

def compute_ate(est_positions, gt_positions):
    """Compute Absolute Trajectory Error"""
    # Align lengths
    n = min(len(est_positions), len(gt_positions))
    est = est_positions[:n]
    gt = gt_positions[:n]
    errors = np.linalg.norm(est - gt, axis=1)
    return errors

sequences = ['00', '05', '08']
results_dir = os.path.expanduser('~/visual-slam-pipeline/results')

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for idx, seq in enumerate(sequences):
    est_file = f'{results_dir}/seq{seq}_trajectory.txt'
    gt_file = f'{results_dir}/gt_seq{seq}.txt'
    
    est_poses = load_kitti_poses(est_file)
    gt_poses = load_kitti_poses(gt_file)
    
    est_pos = extract_positions(est_poses)
    gt_pos = extract_positions(gt_poses)
    
    errors = compute_ate(est_pos, gt_pos)
    ate = np.sqrt(np.mean(errors**2))
    
    ax = axes[idx]
    ax.plot(gt_pos[:, 0], gt_pos[:, 2], 'g-', linewidth=1.5, label='Ground Truth')
    ax.plot(est_pos[:, 0], est_pos[:, 2], 'b-', linewidth=1, label='ORB-SLAM3')
    ax.set_title(f'Sequence {seq}\nATE: {ate:.2f}m')
    ax.legend()
    ax.grid(True)
    ax.axis('equal')
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Z (m)')
    
    print(f'Sequence {seq}: ATE = {ate:.4f}m')

plt.tight_layout()
plt.savefig(f'{results_dir}/week2_evaluation.png', dpi=150, bbox_inches='tight')
print(f'\nSaved to results/week2_evaluation.png')
