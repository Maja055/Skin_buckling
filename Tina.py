import skinParameters as par
import math
import var as var

A = []
B = []
plate_AR = []

def chord(x):
    c = -((var.Cr - var.taper*var.Cr)/(var.span/2)) * x + var.Cr

    return c

for i in range(len(A)):
    if A[i]/B[i] < 1:
        plate_AR.append(B[i]/A[i])
        B[i] = A[i]
    else:
        plate_AR.append(A[i]/B[i])