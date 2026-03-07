import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def load_kitti_poses(filepath):
    poses = []
    with open(filepath) as f:
        for line in f:
            values = list(map(float, line.strip().split()))
            pose = np.array(values).reshape(3, 4)
            poses.append(pose)
    return np.array(poses)

def extract_positions(poses):
    return poses[:, :3, 3]

# Results data
sequences = ['00', '05', '08']
ate = [7.606532, 5.744033, 13.166984]
rpe = [0.028937, 0.028068, 0.038882]
results_dir = '/home/jinesh/visual-slam-pipeline/results'

fig = plt.figure(figsize=(20, 14))
fig.patch.set_facecolor('#0d1117')
gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.4, wspace=0.3)

# Trajectory plots
for idx, seq in enumerate(sequences):
    est_poses = load_kitti_poses(f'{results_dir}/seq{seq}_trajectory.txt')
    gt_poses = load_kitti_poses(f'{results_dir}/gt_seq{seq}.txt')
    est_pos = extract_positions(est_poses)
    gt_pos = extract_positions(gt_poses)

    ax = fig.add_subplot(gs[0, idx])
    ax.set_facecolor('#161b22')
    ax.plot(gt_pos[:, 0], gt_pos[:, 2], color='#2ea043', linewidth=1.5, label='Ground Truth')
    ax.plot(est_pos[:, 0], est_pos[:, 2], color='#58a6ff', linewidth=1, label='ORB-SLAM3')
    ax.scatter(est_pos[0, 0], est_pos[0, 2], c='#2ea043', s=80, zorder=5)
    ax.scatter(est_pos[-1, 0], est_pos[-1, 2], c='#f85149', s=80, zorder=5)
    ax.set_title(f'Sequence {seq}', color='white', fontsize=12, fontweight='bold')
    ax.set_xlabel('X (m)', color='#8b949e')
    ax.set_ylabel('Z (m)', color='#8b949e')
    ax.tick_params(colors='#8b949e')
    ax.legend(facecolor='#161b22', labelcolor='white', fontsize=8)
    ax.grid(True, color='#21262d', linewidth=0.5)
    for spine in ax.spines.values():
        spine.set_edgecolor('#21262d')

# ATE bar chart
ax2 = fig.add_subplot(gs[1, :2])
ax2.set_facecolor('#161b22')
bars = ax2.bar(['Seq 00', 'Seq 05', 'Seq 08'], ate,
               color=['#58a6ff', '#2ea043', '#f85149'], width=0.4)
ax2.set_title('ATE (Absolute Trajectory Error)', color='white', fontsize=12, fontweight='bold')
ax2.set_ylabel('RMSE (m)', color='#8b949e')
ax2.tick_params(colors='#8b949e')
ax2.grid(True, axis='y', color='#21262d')
ax2.set_facecolor('#161b22')
for spine in ax2.spines.values():
    spine.set_edgecolor('#21262d')
for bar, val in zip(bars, ate):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
             f'{val:.2f}m', ha='center', color='white', fontsize=10)

# RPE bar chart
ax3 = fig.add_subplot(gs[1, 2])
ax3.set_facecolor('#161b22')
bars2 = ax3.bar(['Seq 00', 'Seq 05', 'Seq 08'], rpe,
                color=['#58a6ff', '#2ea043', '#f85149'], width=0.4)
ax3.set_title('RPE (Relative Pose Error)', color='white', fontsize=12, fontweight='bold')
ax3.set_ylabel('RMSE (m/frame)', color='#8b949e')
ax3.tick_params(colors='#8b949e')
ax3.grid(True, axis='y', color='#21262d')
for spine in ax3.spines.values():
    spine.set_edgecolor('#21262d')
for bar, val in zip(bars2, rpe):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.0005,
             f'{val:.4f}', ha='center', color='white', fontsize=10)

# Comparison table
ax4 = fig.add_subplot(gs[2, :])
ax4.set_facecolor('#0d1117')
ax4.axis('off')
table_data = [
    ['Sequence', 'Frames', 'ATE RMSE (m)', 'RPE RMSE (m/frame)', 'Status'],
    ['KITTI 00', '4541', '7.606', '0.029', '✅ Good'],
    ['KITTI 05', '2761', '5.744', '0.028', '✅ Best'],
    ['KITTI 08', '4071', '13.167', '0.039', '⚠️ Long seq'],
]
table = ax4.table(cellText=table_data[1:], colLabels=table_data[0],
                  loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1, 2)
for (row, col), cell in table.get_celld().items():
    cell.set_facecolor('#161b22')
    cell.set_text_props(color='white')
    cell.set_edgecolor('#21262d')
    if row == 0:
        cell.set_facecolor('#21262d')
        cell.set_text_props(color='white', fontweight='bold')

# Title
fig.suptitle('ORB-SLAM3 Performance on KITTI Odometry Dataset\nWeek 2 Evaluation Dashboard',
             color='white', fontsize=16, fontweight='bold', y=0.98)

plt.savefig(f'{results_dir}/week2_dashboard.png', dpi=150, bbox_inches='tight',
            facecolor='#0d1117')
print("Saved to results/week2_dashboard.png")
