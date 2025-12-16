import numpy as np

t_skin = 0.003
t_spar = 0.010
n_string_upper = 8
n_string_lower = 8
A_stringer = 4.0*10**(-4)
b = 22.15*2
E = 72.4*10**9 #Elastic modulus
G = 28*10**9 #Shear modulus
v = E/(2*G)-1
Cr= 6.53
taper = 0.2925

t_skin = 2.5            # [mm]
t_str = 5               # [mm]
t_spar = 4              # [mm]
n_spar = 2              
n_str = 24
h_str = 40              # [mm]
w_str = 40              # [mm]
h_root1 = 840           # [mm]
h_root2 = 658.148       # [mm]
h_root3 = 745.951       # [mm]



t_skin = 0.002
t_spar_root = 0.008
t_spar_tip = 0.002

n_string_upper = 15
n_string_lower = 15
A_stringer = 4*10**(-4)
b = 22.15*2
E = 72.4*10**9 #Elastic modulus
G = 28*10**9 #Shear modulus

#set the variable true if the spar is present
multi = True
spar_location = 0.5

def tskin(y):
    return 15 * np.e ** ( -0.12 * y) * 10 ** (-3)

def stringerarea(y):
    return (800 - 18 * y) * 10 ** (-6)

def tspar(y):
    semi_span = b / 2
    thickness = t_spar_root - (t_spar_root - t_spar_tip) * (y / semi_span)
    return thickness

