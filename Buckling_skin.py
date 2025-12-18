import DesignOptions as desOp
import matplotlib.pyplot as plt
import math
import var as var
import scipy.optimize
import scipy.optimize
import critical as cr
import fn as fn
import normalstresses as stress
#When we're running multicell just divide B/2; ribs are for now every 0.5 m

n=int(input("Number of ribs"))
n_spar = int(input("Number of spars"))
pos=[]
for i in range (n):
    pos.append(float(input("Give positions:")))     #Five position of ribs along the wingspan

pos.append(float(var.b/2))
pos.insert(0,float(0))      #Add zero position
print(pos)
B=[]
for i in range (len(pos)-1):
    b1 = var.Cr-(var.Cr*(1-var.taper)/(var.b/2))*pos[i]
    B.append(b1)

if n_spar > 2: 
    for i in range (len(pos)-1):
        B[i] = B[i]/(n-1)

A=[]
for i in range (len(pos)-1):
    A.append(pos[i+1]-pos[i])
    
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

y_test = pos[0]   # root panel (you can also try mid-span later)

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
crit = []
for i in range(len(B_adj)):
    crit_val = math.pi**2 * k_c[i] * var.E / (12*(1-var.v**2)) * ((desOp.t_skin1 / B_adj[i])**2)
    crit.append(crit_val)
print("crit=",crit )
# 6) Margin of safety
MOS = margin_of_safety(crit, applied)
print("MOS:", MOS)

#400-17y area of stringer in mm^2
# 7) Plot
# plt.plot(MOS)
# plt.show()

#  #Margins 
# print(margin_of_safety(crit,applied))
# plt.plot(margin_of_safety(desOp.t_skin1))
pos = pos[:-1]
plt.scatter(pos, MOS,
            s=50,        # marker size
            marker='o'    # marker style
            )
plt.xlabel("span")
plt.ylabel("MOS")
plt.title("Variation of MOS along span")

plt.show()