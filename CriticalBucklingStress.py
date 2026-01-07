import math
import var

#Constants:
E = 72.4*10**9
v = 0.33

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

# --- Main Loop ---
results = []
rib_locations = [0.0]
location = 0.0

rib_amount = 10
rib_spacing = (var.b/2)/(rib_amount-1)

for i in range(rib_amount):
    location += rib_spacing
    rib_locations.append(location)
    
for bay_start, bay_end in zip(rib_locations[:-1], rib_locations[1:]):
    length = bay_end - bay_start
    
    c_start = 6.53 - (4.62 / (var.b / 2)) * bay_start
    c_end   = 6.53 - (4.62 / (var.b / 2)) * bay_end

    bay_data = [
        round(get_critical_buckling_stress(0.128 * c_start, length, False, var.t_spar) / 10**6, 1), 
        round(get_critical_buckling_stress(0.100 * c_start, length, False, var.t_spar) / 10**6, 1), 
        round(get_critical_buckling_stress(0.128 * c_end,   length, False, var.t_spar) / 10**6, 1), 
        round(get_critical_buckling_stress(0.100 * c_end,   length, False, var.t_spar) / 10**6, 1)  
    ]

    results.append(bay_data)

filtered_results = [[min(r[0], r[1]), min(r[2], r[3])] for r in results]