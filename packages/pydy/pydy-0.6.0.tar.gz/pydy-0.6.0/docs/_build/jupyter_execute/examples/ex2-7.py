#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sympy.physics.mechanics import ReferenceFrame, dynamicsymbols, mprint
from sympy import solve, pi, Eq

q1, q2, q3, q4, q5 = dynamicsymbols('q1 q2 q3 q4 q5')
q1d, q2d, q3d, q4d, q5d = dynamicsymbols('q1 q2 q3 q4 q5', level=1)

ux, uy, uz = dynamicsymbols('ux uy uz')
u1, u2, u3 = dynamicsymbols('u1 u2 u3')

A = ReferenceFrame('A')
B_prime = A.orientnew('B_prime', 'Axis', [q1, A.z])
B = B_prime.orientnew('B', 'Axis', [pi/2 - q2, B_prime.x])
C = B.orientnew('C', 'Axis', [q3, B.z])

# Angular velocity based on coordinate time derivatives
w_C_in_A_qd = C.ang_vel_in(A)

# First definition of Angular velocity
w_C_in_A_uxuyuz = ux * A.x + uy * A.y + uz * A.z
print("Using w_C_A as")
print(w_C_in_A_uxuyuz)


# In[2]:


kinematic_eqs = [(w_C_in_A_qd - w_C_in_A_uxuyuz) & uv for uv in A]
print("The kinematic equations are:")
soln = solve(kinematic_eqs, [q1d, q2d, q3d])
for qd in [q1d, q2d, q3d]:
    mprint(Eq(qd, soln[qd]))


# In[3]:


# Second definition of Angular velocity
w_C_in_A_u1u2u3 = u1 * B.x + u2 * B.y + u3 * B.z
print("Using w_C_A as")
print(w_C_in_A_u1u2u3)


# In[4]:


kinematic_eqs = [(w_C_in_A_qd - w_C_in_A_u1u2u3) & uv for uv in A]
print("The kinematic equations are:")
soln = solve(kinematic_eqs, [q1d, q2d, q3d])
for qd in [q1d, q2d, q3d]:
    mprint(Eq(qd, soln[qd]))

