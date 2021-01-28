from pyXSteam.XSteam import XSteam
import pyromat as pm

steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS) #T in celcius ( m/kg/sec/°C/bar/W)

print(steamTable.hL_p(5),(steamTable.hV_p(5)-steamTable.hL_p(5)))
print(steamTable.tsat_p(5))
print(steamTable.v_pt(5,100)-1/8.47)

print(steamTable.t_ps(6,7.127))
print(steamTable.h_pt(5,1700))

# R22 = pm.get('ig.CHClF2')
# water = pm.get('ig.H2O')
#
# print(water.h(T=424.15,p=5)) #T in kelvin!! but still doesn't work
#
# h_fin = steamTable.h_pt(14,250)
# print(h_fin)
#
# t_sat = steamTable.tsat_p(11)
# print(t_sat)
# v_2 = steamTable.v_ph(11, h_fin)
# print(v_2)
# v_2f = steamTable.vL_p(11)
# v_2g = steamTable.vV_p(11)
# print(v_2f, v_2g)
#
# a = (0.25*v_2)**2
# print(a)
#
# v = steamTable.vL_p(1) + 0.01*steamTable.vV_p(1)
#
# xx = steamTable.hV_p(10)
# print(xx)