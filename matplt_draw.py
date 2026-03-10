import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import json, os
import numpy as np

# filenames = [f"samples/results/skeleton_0000{i}.json" for i in range(1, 9)]
filenames = ["samples/Fall/sample_00027/skeleton.json"]

points = [
    "pelvis", "spine1", "spine2", "spine3", "neck",
    "left_collar", "right_collar", "left_shoulder", "right_shoulder",
    "left_elbow", "right_elbow", "left_wrist", "right_wrist",
    "left_hand_thumb4", "right_hand_thumb4",
    "left_hip", "right_hip", "left_knee", "right_knee",
    "left_ankle", "right_ankle", "left_foot", "right_foot",
    "head", "head_nose"
]


connections = [
    ("pelvis", "spine1"), ("spine1", "spine2"), ("spine2", "spine3"), ("spine3", "neck"),
    ("neck", "head"),
    ("neck", "left_shoulder"), ("neck", "right_shoulder"),
    ("left_shoulder", "left_elbow"), ("left_elbow", "left_wrist"), ("left_wrist", "left_hand_thumb4"),
    ("right_shoulder", "right_elbow"), ("right_elbow", "right_wrist"), ("right_wrist", "right_hand_thumb4"),
    ("pelvis", "left_hip"), ("pelvis", "right_hip"),
    ("left_hip", "left_knee"), ("left_knee", "left_ankle"), ("left_ankle", "left_foot"),
    ("right_hip", "right_knee"), ("right_knee", "right_ankle"), ("right_ankle", "right_foot")
]


views = [
    (0, 0), (0, 45), (0, 90), (0, 135), (0,180), (0, 225), (0, 270), (0, 315), (0, 360), 

    (45, 0), (45, 45), (45, 90), (45, 135), (45, 180), (45, 225), (45, 270), (45, 315), (45, 360),
    (-45, 0), (-45, 45), (-45, 90), (-45, 135), (-45, 180), (-45, 225), (-45, 270), (-45, 315), (-45, 360),

    (90, 0), (-90, 0)    
]


for filename in filenames:

    with open(filename) as f:
	    data = json.load(f)

    x = np.array([data[p][0] for p in points])
    y = np.array([data[p][1] for p in points])
    z = np.array([data[p][2] for p in points])

    base_name = os.path.splitext(os.path.basename(filename))[0]
    output_dir = os.path.join(".", base_name)
    os.makedirs(output_dir, exist_ok=True)

    for i, (elev, azim) in enumerate(views):

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(x[y<=0], y[y<=0], z[y<=0], c='r', s=5)               
        ax.scatter(x[y>0],  y[y>0],  z[y>0],  c='gray', s=5, alpha=0.2)  

        for start, end in connections:
            ax.plot([data[start][0], data[end][0]],
                [data[start][1], data[end][1]],
                [data[start][2], data[end][2]], 'b')

        L = 1
        ax.plot([-L, L], [0, 0], [0, 0], color='k', linewidth=1) # X
        ax.plot([0, 0], [-L, L], [0, 0], color='k', linewidth=1) # Y
        ax.plot([0, 0], [0, 0], [-L, L], color='k', linewidth=1) # Z

        # transparent XZ plane (Y = 0) — use numpy arrays
        X, Z = np.meshgrid([-L, L], [-L, L])
        Y = np.zeros_like(X, dtype=float)
        ax.plot_surface(X, Y, Z, color='cyan', alpha=0.2, shade=False)
        
        ax.text(0.52, 0, 0, 'X', color='k', size=12)
        ax.text(0, 0.52, 0, 'Y', color='k', size=12)
        ax.text(0, 0, 0.52, 'Z', color='k', size=12)

        ax.set_xlim([-L, L])
        ax.set_ylim([-L, L])
        ax.set_zlim([-L, L])

        ax.view_init(elev=elev, azim=azim)

        plt.savefig(os.path.join(output_dir, f"view_{i+1}.png"))
        plt.close()
