import var
import fn
import normalstresses


for n in range(10000):
    y_pos = n*(var.b/2)/10000

    shape = fn.WP4_2_wingbox_shape(y_pos)

    z_max = shape[0][1]
    z_min = -shape[4][1]+z_max

    stress_z_max = normalstresses.bendingstress(y_pos, z_max)
    stress_z_min = normalstresses.bendingstress(y_pos, z_min)

    stress_z_max += normalstresses.normalstress(y_pos)
    stress_z_min += normalstresses.normalstress(y_pos)

    if abs(stress_z_min) > 450e6:
        print(f'Fails at y: {y_pos:.1f} [m], z: {z_min:.2f} [m], sigma: {stress_z_min/1e6:.2f} [MPa]')
        break

    if abs(stress_z_max) > 450e6:
        print(f'Fails at y: {y_pos:.1f} [m], z: {z_max:.2f} [m], sigma: {stress_z_max/1e6:.2f} [MPa]')
        break
