import critical as cr
import fn as fn
import var
from math import atan, tan, cos
import math
import numpy as np
import RibDistribution as rib
# import BucklingCoefficient as BC

#Constants:
E = 72.4*10**9
v = 0.33

#Shear and torsion distributions
Sd = cr.Spf
Td = cr.Tpf
bay_length = 1  #m

def get_shear_buckling_coefficient(dim1, dim2, simplySupported=True):
    a = max(dim1, dim2)
    b = min(dim1, dim2)    
    if simplySupported:
        return 5.35 + 4*(b/a)**2
    else:
        return 8.98 + 5.6*(b/a)**2

def get_critical_buckling_stress(dim1, dim2, simplySupported, t):
    k = get_shear_buckling_coefficient(dim1, dim2, simplySupported)
    b = min(dim1, dim2) 
    
    tau_cr = (math.pi**2*k*E)/(12*(1-v**2))*(t/b)**2
    return tau_cr

def sfcalc(y):
    # Geometry and constants
    theta = 0.0497367 # in radians
    c = 6.53 - (4.62/var.b/2)*y # chord length
    d = 0.45*c # distance between spars
    s_f = 0.128*c # length of the front spar
    s_b = 0.1*c # length of the back spar
    f = var.spar_location

    # Use variable thickness functions, not static constants
    t1 = var.tspar(y)  # Spar thickness at location y
    t2 = var.tskin(y)  # Skin thickness at location y
    # -------------------------

    l2 = s_b
    l4 = s_f
    p3 = (d, d*tan(theta)+l2)
    theta2 = atan((l4 - p3[1])/d)
    p5 = (f*d, f*d*tan(theta))
    p6 = (f*d, l4 - f*d*tan(theta2))
    l1 = d/cos(theta)
    l3 = d/cos(theta2)

    sf = []

    if not var.multi:
        area_enc = (l2+l4)*d/2
        tau_ave = Sd(y)/(s_f * t1 + s_b * t1)
        tau_torsion = Td(y)/(2*area_enc*t1)
        sf = [tau_ave, tau_torsion]
        return sf
    else:
        s1 = f*l1
        s2 = (1 - f)*l1
        s3 = l2
        s4 = (1 -f)*l3
        s5 = f*l3
        s6 = l4
        s7 = p6[1] - p5[1]

        A1 = (s6 + s7) * f * d/2
        A2 = (s7 + s3) * (1 -f) * d/2

        # Note: Added float() wrapper to avoid potential numpy scalar issues
        c1 = 1/(2*A1*var.G)*(s1/t2+s7/t1+s5/t2+s6/t1)
        c2 = -1/(2*A1*var.G)*(s7/t1)
        c3 = -1/(2*A2*var.G)*(s7/t1)
        c4 = 1/(2*A1*var.G)*(s2/t2+s3/t1+s4/t2+s7/t1)

        LHS = [[0, 2*A1, 2*A2], [-1, c1, c2], [-1, c3, c4]]
        RHS = [Td(y), 0, 0]
        sol = np.linalg.solve(LHS, RHS)

        # Updated tau_ave to include s7 (middle spar) if present
        tau_ave = Sd(y)/(s_f * t1 + s_b * t1  + s7 * t1)

        sf = [tau_ave, sol[1]/t1, (sol[1]-sol[2])/t1, sol[2]/t1]

        return sf

def tau_max(y, k_v):
    return k_v * (sfcalc(y)[0] + sfcalc(y)[1])

# --- Main Loop ---
results = []
bay_max_applied_stresses = []  # To store the worst applied stress per bay

# Create rib locations

rib_locations = rib.rib_distribution()

for bay_start, bay_end in zip(rib_locations[:-1], rib_locations[1:]):

    length = bay_end - bay_start

    #Find Max Applied Stress in this Bay
    y_stations = np.arange(bay_start, bay_end, 0.1) 

    # Calculate stress at all these points
    stresses_in_bay = [tau_max(y, 1.5) for y in y_stations]
    
    # Find the maximum stress and convert to MPa
    max_abs_stress = max(abs(stress) for stress in stresses_in_bay)
    bay_max_applied_stresses.append(round(max_abs_stress / 10**6,1)) 

    c_start = 6.53 - (4.62 / (var.b / 2)) * bay_start
    c_end   = 6.53 - (4.62 / (var.b / 2)) * bay_end
    
    bay_data = [
        round(get_critical_buckling_stress(0.128 * c_start, length, False, var.tspar(bay_start)) / 10**6, 1), 
        round(get_critical_buckling_stress(0.100 * c_start, length, False, var.tspar(bay_start)) / 10**6, 1), 
        round(get_critical_buckling_stress(0.128 * c_end,   length, False, var.tspar(bay_end)) / 10**6, 1), 
        round(get_critical_buckling_stress(0.100 * c_end,   length, False, var.tspar(bay_end)) / 10**6, 1)  
    ]
    
    results.append(bay_data)

filtered_results = [[min(r[0], r[1]), min(r[2], r[3])] for r in results]

safety_margins = [
    [
        filtered_results[r][0] / bay_max_applied_stresses[r], 
        filtered_results[r][1] / bay_max_applied_stresses[r]
    ] 
    for r in range(len(bay_max_applied_stresses))
]

for i, (value1, value2) in enumerate(safety_margins, start=1):
    print(f"Bay {i}: {value1:.2f}, {value2:.2f}")


print(rib_locations)