import re

input_file = "./EFchem_hBN/hBN_project/hBN.in.data"
output_file = "./EFchem_hBN/hBN_project/new_hBN.in.data"

x_ratio, y_ratio, z_ratio = 1, 1, 0.10

xlo, xhi = -3.9006362984379528e+01, 4.3344360484379528e+01
ylo, yhi = -3.7533609150731806e+01, 4.2542710950745985e+01
zlo, zhi = -3.2057278850357676e+01, 4.5329282050343650e+01

xlen, ylen, zlen = xhi - xlo, yhi - ylo, zhi - zlo
zhi_new, zlo_new = zlo + (zlen/2) + (zlen * z_ratio / 2), zlo + (zlen/2) - (zlen * z_ratio / 2)
print(zhi_new, zlo_new)

with open(input_file, 'r') as file:
    data = file.readlines()

new_atoms = {}
atom_id_mapping = {}
new_atom_id = 1
for i in range(17, 58385):
    line = data[i]
    parts = line.split()
    atom_id = parts[0]
    x, y, z = map(float, parts[4:7])
    if xlo <= x <= xhi and ylo <= y <= yhi and zlo_new <= z <= zhi_new:
        new_atoms[str(new_atom_id)] = ' '.join([str(new_atom_id)] + parts[1:4] + [str(x), str(y), str(z)] + parts[7:])
        atom_id_mapping[atom_id] = str(new_atom_id)
        new_atom_id += 1

new_velocities = {}
for i in range(58388, 116756): 
    line = data[i]
    parts = line.split()
    atom_id = parts[0]
    if atom_id in atom_id_mapping:
        new_velocities[atom_id_mapping[atom_id]] = ' '.join(parts[1:])

with open(output_file, 'w') as new_file:
    new_file.write('Atoms\n\n')
    for atom_id, atom_data in new_atoms.items():
        new_file.write(f"{atom_data}\n")
    
    new_file.write('\nVelocities\n\n')
    for atom_id, velocity_data in new_velocities.items():
        new_file.write(f"{atom_id} {velocity_data}\n")
