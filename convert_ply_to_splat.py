import numpy as np
from plyfile import PlyData
import struct

def convert_ply_to_splat(input_path, output_path):
    plydata = PlyData.read(input_path)
    vertices = plydata['vertex']
    num_points = len(vertices)

    with open(output_path, 'wb') as f:
        f.write(b'SPLT')  # magic
        f.write(struct.pack('I', num_points))

        for v in vertices:
            x, y, z = v['x'], v['y'], v['z']
            r = v['red'] if 'red' in v else 255
            g = v['green'] if 'green' in v else 255
            b = v['blue'] if 'blue' in v else 255

            f.write(struct.pack('3f', x, y, z))                 # position
            f.write(struct.pack('3f', 1.0, 0.0, 0.0))           # rotation (dummy)
            f.write(struct.pack('3f', 0.01, 0.01, 0.01))        # scale
            f.write(struct.pack('3f', r/255.0, g/255.0, b/255.0))  # color
            f.write(struct.pack('f', 1.0))                      # opacity

    print(f"✅ Converted {num_points} points to {output_path}")

if __name__ == "__main__":
    convert_ply_to_splat(
        "./public/models/my_model.ply",
        "./public/models/my_model.splat"
    )
