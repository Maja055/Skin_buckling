import fn
import critical as cr
import var

def max_z(y):
    h_spar1 = var.h_root1 - var.h_root1 * (1 - var.taper) * y / (var.b/2)
    z = h_spar1/2

    return z


def bendingstress(y, z):
    return cr.Mpf(y)/fn.WP4_2_Ixx(y)*(10**3)**4 * z           #convert never mind Louis says it is in N/m

def normalstress(y):
    geo = fn.WP4_2_wingbox_shape(y)
    if var.multi:
        return cr.Npf(y)/geo[7]
    else:
        return cr.Npf(y)/geo[5]

