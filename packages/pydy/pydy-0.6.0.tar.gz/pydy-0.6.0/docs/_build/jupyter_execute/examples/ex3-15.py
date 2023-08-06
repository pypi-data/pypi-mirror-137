#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sympy.physics.mechanics import dynamicsymbols, msprint
from sympy.physics.mechanics import ReferenceFrame, Point
from sympy import solve, symbols

# Define generalized coordinates, speeds, and constants:
q0, q1, q2 = dynamicsymbols('q0 q1 q2')
q0d, q1d, q2d = dynamicsymbols('q0 q1 q2', level=1)
u1, u2, u3 = dynamicsymbols('u1 u2 u3')
LA, LB, LP = symbols('LA LB LP')
p1, p2, p3 = symbols('p1 p2 p3')

E = ReferenceFrame('E')
# A.x of Rigid Body A is fixed in Reference Frame E and is rotated by q0.
A = E.orientnew('A', 'Axis', [q0, E.x])
# B.y of Rigid Body B is fixed in Reference Frame A and is rotated by q1.
B = A.orientnew('B', 'Axis', [q1, A.y])
# Reference Frame C has no rotation relative to Reference Frame B.
C = B.orientnew('C', 'Axis', [0, B.x])
# Reference Frame D has no rotation relative to Reference Frame C.
D = C.orientnew('D', 'Axis', [0, C.x])

pO = Point('O')
# The vector from Point O to Point A*, the center of mass of A, is LA * A.z.
pAs = pO.locatenew('A*', LA * A.z)
# The vector from Point O to Point P, which lies on the axis where
# B rotates about A, is LP * A.z.
pP = pO.locatenew('P', LP * A.z)
# The vector from Point P to Point B*, the center of mass of B, is LB * B.z.
pBs = pP.locatenew('B*', LB * B.z)
# The vector from Point B* to Point C*, the center of mass of C, is q2 * B.z.
pCs = pBs.locatenew('C*', q2 * B.z)
# The vector from Point C* to Point D*, the center of mass of D,
# is p1 * B.x + p2 * B.y + p3 * B.z.
pDs = pCs.locatenew('D*', p1 * B.x + p2 * B.y + p3 * B.z)

# Define generalized speeds as:
# u1 = q0d
# u2 = q1d
# u3 = q2d
A.set_ang_vel(E, u1 * A.x) # A.x = E.x
B.set_ang_vel(A, u2 * B.y) # B.y = A.y
pCs.set_vel(B, u3 * B.z)

pO.set_vel(E, 0) # Point O is fixed in Reference Frame E
pAs.v2pt_theory(pO, E, A) # Point A* is fixed in Reference Frame A
pP.v2pt_theory(pO, E, A) # Point P is fixed in Reference Frame A
pBs.v2pt_theory(pP, E, B) # Point B* is fixed in Reference Frame B
pCs.v1pt_theory(pBs, E, B) # Point C* is moving in Reference Frame B
pDs.set_vel(B, pCs.vel(B)) # Point D* is fixed relative to Point C* in B
pDs.v1pt_theory(pBs, E, B) # Point D* is moving in Reference Frame B

# Write generalized speeds as kinematic equations:
kinematic_eqs = []
kinematic_eqs.append(u1 - q0d)
kinematic_eqs.append(u2 - q1d)
kinematic_eqs.append(u3 - q2d)
soln = solve(kinematic_eqs, [q0d, q1d, q2d])
print("kinematic equations:")
for qd in [q0d, q1d, q2d]:
   print("{0} = {1}".format(msprint(qd), msprint(soln[qd])))


# In[2]:


ang_vels = ["\nangular velocities:"]
ang_accs = ["\nangular accelerations:"]
for rf in [A, B, C, D]:
   ang_v = getattr(rf, 'ang_vel_in')(E)
   ang_a = getattr(rf, 'ang_acc_in')(E)
   express_rf = B
   if rf == A:
      express_rf = A
   ang_vels.append("ang vel {0} wrt {1} = {2}".format(
            rf, E, ang_v.express(express_rf)))
   ang_accs.append("ang acc {0} wrt {1} = {2}".format(
            rf, E, ang_a.express(express_rf)))

vels = ["\nvelocities:"]
accs = ["\naccelerations:"]
for point in [pAs, pBs, pCs, pDs]:
   v = getattr(point, 'vel')(E)
   a = getattr(point, 'acc')(E)
   express_rf = B
   if point == pAs:
      express_rf = A
   vels.append("vel {0} wrt {1} = {2}".format(
            point, E, v.express(express_rf)))
   accs.append("acc {0} wrt {1} = {2}".format(
            point, E, a.express(express_rf)))

for results in ang_vels + ang_accs + vels + accs:
   print(results)

