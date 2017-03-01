import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axes as axes


def load_camera_pose(file_name='camera_pose.txt'):
    with open(file_name) as input_file:
        raw_data = input_file.read()
        numbers = [float(x) for x in raw_data.strip().split()]
        return list(zip(*[iter(numbers)] * 6))


class camera:
    camera_depth = 0.07
    camera_width = 0.05
    camera_height = 0.05
    axis_length = 0.1

    def __init__(self, pos, direction=None, target=None):
        self.pos = pos
        if direction is not None:
            self.direction = direction
            temp_len = sum((d * d for d in self.direction)) ** 0.5
            self.direction = tuple(d / temp_len for d in self.direction)
        elif target is not None:
            self.direction = tuple(t - p for p, t in zip(pos, target))
            temp_len = sum((d * d for d in self.direction)) ** 0.5
            self.direction = tuple(d / temp_len for d in self.direction)
        else:
            raise Exception('error')

    def draw(self, ax):
        centre = np.array(tuple((p + d * self.camera_depth) for p, d in zip(self.pos, self.direction)))
        y = np.array((0, 1, 0))
        horizontal_direction = np.cross(self.direction, y)
        horizontal_direction /= np.linalg.norm(horizontal_direction)
        
        vertical_direction = np.cross(self.direction, horizontal_direction)
        vertical_direction /= np.linalg.norm(vertical_direction)

        another_direction = np.cross(vertical_direction, horizontal_direction)
        another_direction /= np.linalg.norm(another_direction)
        axis_points = [self.pos, self.pos - horizontal_direction * self.axis_length / 2]
        ax.plot(*zip(*axis_points), color = 'r')
        axis_points = [self.pos, self.pos - vertical_direction * self.axis_length / 2]
        ax.plot(*zip(*axis_points), color = 'g')
        axis_points = [self.pos, self.pos - another_direction * self.axis_length * 1.5]
        ax.plot(*zip(*axis_points), color = 'b')


        vertical_direction *= self.camera_height / 2
        horizontal_direction *= self.camera_width / 2
        p1 = centre + horizontal_direction + vertical_direction
        p2 = centre + horizontal_direction - vertical_direction
        p3 = centre - horizontal_direction - vertical_direction
        p4 = centre - horizontal_direction + vertical_direction

        bottom_points = [p1, p2, p3, p4]

        # draw bottom
        temp = bottom_points + bottom_points[0:1]
        ax.plot(*zip(*temp), color = (1,1,1,1), linewidth=3)

        # draw edge
        for p in bottom_points:
            temp = [self.pos, p]
            ax.plot(*zip(*temp), color =  (1,1,1,1), linewidth=3)




raw_camera = load_camera_pose()
camera_number = len(raw_camera)
camera_positions = [r[:3] for r in raw_camera]
camera_direct = [r[3:] for r in raw_camera]

# cameras = [camera(r[:3], direction=r[3:]) for r in raw_camera]
centre = tuple(sum(xyz) / camera_number for xyz in zip(*camera_positions))
print(centre)
cameras = [camera(r[:3], target=centre) for r in raw_camera]

fig = plt.figure()
#fig = plt.figure(figsize=(20, 20))  # set figure size

ax = fig.gca(projection='3d')  # Type:axes

for c in cameras:
    c.draw(ax)

p = [(0.25, 0, 0), (0, 0.25, 0), (0, 0, 0.25)]
colors = ['r', 'g', 'b']
ori = (-1.5, 0, -2)                 #need to be adjusted
for pp, c in zip(p,colors):
    temp = [tuple(ppp + o for ppp, o in zip(pp, ori)), ori]
    ax.plot(*zip(*temp), color = c )
#ax.axis('off')
# ax.set_axis_bgcolor((0.5, 0.5, 0.5))
ax.set_axis_bgcolor((0.5, 0.5, 0.5))
show_range = tuple([xyz - 1, xyz + 1] for xyz in centre)
ax.set_xlim(show_range[0])
ax.set_ylim(show_range[1])
ax.set_zlim(show_range[2])
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

plt.show()
