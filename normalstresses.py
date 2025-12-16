import fn
import critical as cr
import var

def max_z(y):
    h_spar1 = var.h_root1 - var.h_root1 * (1 - var.taper) * y / var.b
    z = h_spar1/2

    return z


def bendingstress(y, z):
    return cr.Mpf(y)/fn.WP4_2_Ixx(y) * z

def normalstress(y):
    geo = fn.WP4_2_wingbox_shape(y)
    if var.multi:
        return cr.Npf(y)/geo[7]
    else:
        return cr.Npf(y)/geo[5]

