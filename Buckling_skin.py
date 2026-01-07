#import DesignOptions as desOp
import matplotlib.pyplot as plt
import math
import var as var
import Skin_buckling_var as svar
import scipy.optimize
import scipy.optimize
import critical as cr
import fn as fn
import normalstresses as stress
import numpy as np
#When we're running multicell just divide B/2; ribs are for now every 0.5 m

#n=int(input("Number of ribs"))
#n_spar = int(input("Number of spars"))
n_spar = int(3)

pos=[0.793, 1.546, 2.261, 2.942, 3.595, 4.223, 5.2, 5.989, 6.546,
  7.091, 7.624, 8.2, 8.661, 9.168, 9.669, 10.164, 10.655, 11.143, 11.628,
  12.112, 12.595, 13.079, 13.564, 14.052, 14.543, 15.04, 15.542, 16.053, 16.572,
  17.103, 17.648, 18.208, 18.788, 19.391, 20.022, 20.686, 21.392]

#for i in range (n):
#    pos.append(float(input("Give positions:")))     #Five position of ribs along the wingspan

pos.append(float(var.b/2))
pos.insert(0,float(0))      #Add zero position
print('positions:',pos)
B=[]
for i in range (len(pos)-1):
    b1 = svar.Cr*0.45-(svar.Cr*0.45*(1-svar.taper)/(var.b/2))*pos[i]
    if n_spar == 2:
        b1 = b1/(var.n_string_upper-1)
    if n_spar == 3:
        b1 = b1/(var.n_string_upper-2)
    B.append(b1)
print('bay width: ',B)

# if n_spar > 2: 
#     for i in range (len(pos)-1):
#         B[i] = B[i]/(n_spar-1)

A=[]
for i in range (len(pos)-1):
    A.append(pos[i+1]-pos[i])
print('bay length: ',A)

'''Applied stress calculation'''
z=[]
for i in range (len(pos)-1):
    z.append(stress.max_z(pos[i]))


def find_max_stress(lower_limit, upper_limit):
    max_y=scipy.optimize.fminbound(lambda y: -stress.normalstress(y), lower_limit, upper_limit)
    #min_x=scipy.optimize.fminbound(lambda y: Internal_normal_stress(y), lower_limit, upper_limit)
    Smax=abs(stress.normalstress(max_y))
    #Smin=abs(Internal_normal_stress(min_x))
    return Smax

def find_max_stress_internal(lower_limit, upper_limit,z):
    max_y=scipy.optimize.fminbound(lambda y: -stress.bendingstress(y,z), lower_limit, upper_limit)
    Smax=abs(stress.bendingstress(max_y,z))
    return Smax

def Normal_stress_discrete(pos_list):
    Normal_stress_list=[]
    for i in range(len(pos_list)-1):
        Normal_stress_list.append(find_max_stress(pos_list[i], pos_list[i+1]))

    return Normal_stress_list

def Bending_stress_discrete(pos_list, z):
    Bending_stress_list=[]
    for i in range(len(pos_list)-1):
        Bending_stress_list.append(find_max_stress_internal(pos_list[i], pos_list[i+1],z[i]))

    return Bending_stress_list

def stress_applied(pos_list):
    applied=[]
    normal_list=Normal_stress_discrete(pos_list)
    bending_list = Bending_stress_discrete(pos_list,z)

    for i in range(len(pos_list)-1):
        applied.append(normal_list[i]+bending_list[i])
    return applied

'''critical stress calculation '''

def plate_AR(A, B):
    """Return (AR_list, possibly_adjusted_B). If A/B < 1, we swap (so B <= A) as original code did."""
    AR = []
    B_adj = B.copy()
    for i in range(len(A)):
        if A[i] / B[i] < 1:
            AR.append(B[i] / A[i])
            B_adj[i] = A[i]   # original code set B[i] = A[i] for that case
        else:
            AR.append(A[i] / B[i])
    return AR, B_adj

#Calculate the a/b
#Use simply supported case(graph C), even though normally we have combination of simply supported and claped (at the root)
def k_c_calculation(AR_list):
    K_C=[]
    for i in range (len(AR_list[0])):
        k_c_element=4
        if (AR_list[0][i])<2:
            print('a/b = ', AR_list[0][i])
            k_c_element=float(input("Input the value for kc"))
        K_C.append(k_c_element)
    return K_C
        
# find smallest skin thickness of each bay
def skin_thickness(pos_list):
    t = []
    for i in range(len(pos_list)-1):
        t.append(var.tskin(pos_list[i+1]))
    return t
print('skin_thicknesses:',skin_thickness(pos))

'''Margin of Safety calculation'''

def margin_of_safety(crit_list, applied_list):
    Margin_of_safety=[]
    for i in range (len(crit_list)):
        if applied_list[i] == 0: 
            Margin_of_safety.append(0)
        else:
            Margin_of_safety.append(crit_list[i]/applied_list[i])
    return Margin_of_safety



# 3) Compute applied stresses
#applied = Applied_stress(normal_forces, areas)
applied=stress_applied(pos)
print("\n===== DEBUG: raw values at one span location =====")

y_test = pos[0] +20   # root panel (you can also try mid-span later)

print("y_test =", y_test)

print("Normal force Npf(y) =", cr.Npf(y_test))
print("Bending moment Mpf(y) =", cr.Mpf(y_test))

geo = fn.WP4_2_wingbox_shape(y_test)
print("Wingbox geometry array =", geo)

Ixx = fn.WP4_2_Ixx(y_test)
print("Second moment Ixx =", Ixx)

z_val = stress.max_z(y_test)
print("z (distance to extreme fibre) =", z_val)

print("Normal stress =", stress.normalstress(y_test))
print("Bending stress =", stress.bendingstress(y_test, z_val))

print("================================================\n")

print('applied stress:',applied)

# 4) Compute k_c list (AR list must be passed)
k_c = k_c_calculation(plate_AR(A,B))
print(k_c)

# 5) Compute critical stresses
B_adj = plate_AR(A,B)[1]
skin_t_list = skin_thickness(pos)
crit = []
for i in range(len(B_adj)):
    crit_val = math.pi**2 * k_c[i] * var.E / (12*(1-svar.v**2)) * ((skin_t_list[i] / B_adj[i])**2)
    crit.append(crit_val)
print("crit=",crit )
# 6) Margin of safety
MOS = margin_of_safety(crit, applied)
MOS = [float(x) for x in MOS]
print("MOS:")
for value in MOS:
    print(value)

#400-17y area of stringer in mm^2
# 7) Plot
# plt.plot(MOS)
# plt.show()

print('pos:')
for value in pos:
    print(value)

#  #Margins 
# print(margin_of_safety(crit,applied))
# plt.plot(margin_of_safety(desOp.t_skin1))


# # plot critical stress
# plt.plot(pos,crit)

# # plot applied stress
# plt.plot(pos,applied)

#### for clarity
# pos = pos[:-4]
# MOS = MOS[:-4]

# plt.scatter(pos, MOS,
#             s=30,        # marker size
#             marker='o'    # marker style
#             )
# plt.grid()
# plt.xlabel('Distance along Wingspan [m]')
# plt.ylabel('Margin of Safety [-]')
# plt.title('Variation of skin buckling margin of safety along span')

# plt.show()

#### for clarity
pos = pos[:-1]

MOS = MOS[:-1]

MOS_extended = MOS + [MOS[-1]]
plt.step(pos, MOS_extended, where='post')
plt.grid()
plt.xlabel('Distance along Wingspan [m]')
plt.ylabel('Margin of Safety [-]')
plt.title('Variation of skin buckling margin of safety along span')
plt.xlim(left=0)
plt.ylim(bottom=0)
plt.axhline(y=1, color='red', linestyle='--')

plt.show()