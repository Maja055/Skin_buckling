import numpy as np

t_skin = 0.003
t_spar = 0.010
n_string_upper = 8
n_string_lower = 8
A_stringer = 4.0*10**(-4)
b = 22.15*2 # [m]
E = 72.4*10**9 #Elastic modulus
G = 28*10**9 #Shear modulus
v = 0.33
Cr= 6.53 # [m]
taper = 0.2925

t_skin = 0.0025            # [m]
t_str = 0.005               # [m]
t_spar = 0.004              # [m]
n_spar = 2              
n_str = 24
h_str = 0.040              # [m]
w_str = 0.040              # [m]
h_root1 = 0.840           # [m]
h_root2 = 0.658148       # [m]
h_root3 = 0.745951       # [m]



t_skin = 0.002
t_spar_root = 0.008
t_spar_tip = 0.002

n_string_upper = 15
n_string_lower = 15
A_stringer = (4*10**(-4))
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

