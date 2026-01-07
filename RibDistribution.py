import numpy as np
import var

fixed_ribs = [0, 5.2, 8.2, var.b/2]   # Your mandatory ribs


#def rib_distribution(min_spacing=1, density=3):
#    semi_span = var.b / 2
#
#    N = 100  # high-resolution distribution
#
#    # Master parameter 0 → 1
#    mu = np.linspace(0, 1, N)
#
#    # Root clustering
#    root = mu ** density
#
#    # Normalize → scale to semi-span
#    base_distribution = semi_span * root
#    # Add mandatory ribs
#    pts = np.concatenate((base_distribution, fixed_ribs))
#    pts = np.unique(np.sort(pts))
#
#    # Enforce minimum spacing
#    final = [pts[0]]
#    for x in pts[1:]:
#        if x - final[-1] >= min_spacing * 0.999:
#            final.append(x)
#        else:
#            # Keep mandatory ribs even if spacing is small
#            if x in fixed_ribs:
#                final[-1] = x
#
#    return final


def rib_density(y, base_strength = 2.0, bump_width = 1.0, bump_strength = 2.0):
    semi_span = var.b / 2

    base_density = (1 - y/semi_span)**base_strength
    bumps = 0
    for rib in fixed_ribs:
        bumps += bump_strength * np.exp(-0.5*((y-rib)/bump_width)**2)
    
    return base_density + bumps

def generate_rib_distribution()