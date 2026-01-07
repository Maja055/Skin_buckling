import fn
import critical as cr
import var
import Skin_buckling_var as svar
import matplotlib.pyplot as plt

def max_z(y):
    h_spar1 = svar.h_root1 - svar.h_root1 * (1 - svar.taper) * y / (var.b/2)
    z = h_spar1/2

    return z


def bendingstress(y, z):
    return cr.Mpf(y)/fn.WP4_2_Ixx(y) * z           # Louis says it is in N/m

def normalstress(y):
    geo = fn.WP4_2_wingbox_shape(y)
    if var.multi:
        return cr.Npf(y)/geo[7]
    else:
        return cr.Npf(y)/geo[5]
    

# y_list = []
# bending_stress_list = []

# for i in range(440):
#     y_list.append(i/20)
#     z_ref = max_z(y_list[i])
#     bending_stress_list.append(bendingstress(y_list[i], z_ref))

# plt.plot(y_list, bending_stress_list)
# plt.show()