from building_plus.basic.psychometric import psychometric

import numpy as np

def cooling_tower(building,name,water_flow,T_in,T_target,T_air,w_air):
    tower = building['cooling_tower'][name] 
    bypass = 0
    if tower['type']=='SingleSpeed':
        if water_flow>0:
            T_out_fc = tower_iteration(tower['free_convect_UA'],water_flow,tower['free_convect_flow'],T_in,T_air,w_air,T_target)
            T_out_fan = tower_iteration(tower['UA'],water_flow,tower['air_flow'],T_in,T_air,w_air,T_target)       
            if tower['capacity_control']=='fancycling':
                if T_out_fan == T_out_fc:
                    frac_fan = 0
                else:
                    frac_fan = max(0,min(1,(T_target-max(T_target,T_out_fc))/(T_out_fan - T_out_fc)))
                if frac_fan == 0:
                    bypass = 1- (T_in - T_target)/(T_in - T_out_fc)
                    P_fan = 0
                    T_out = T_target
                else:
                    P_fan = frac_fan*tower['fan_power']#Watts
                    T_out = T_out_fc - frac_fan*(T_out_fc - T_out_fan)
            else:
                P_fan = tower['fan_power']#Watts
                T_out = T_out_fan
        else:
            P_fan = 0
            T_out = T_in
            bypass = 0
    else:
        print('need cooling tower model for type__'+tower['type'])
    return P_fan,T_out,bypass

def tower_iteration(UA,water_flow,air_flow,T_in,T_air,w_air,T_wb_exit):
    Cp_water = 4186 #J/kg*K
    c_w = water_flow*Cp_water
    T_wb = psychometric({'Tdb':T_air,'w':w_air},'Twb')
    T_in = max(T_in, T_wb+4)
    T_wb_exit = max(T_wb_exit,T_wb+1)
    T0 = T_wb_exit
    ##iterate the following
    error_T = 1
    d_T = 0.1
    gain =.5
    count = 1
    while abs(error_T)>1e-2:
        Q_total,c_a = tower_heat_trans(T_in,T_air,w_air,T_wb,T_wb_exit,air_flow,c_w,UA)
        Q_total2,_ = tower_heat_trans(T_in,T_air,w_air,T_wb,T_wb_exit+d_T,air_flow,c_w,UA)
        if Q_total == Q_total2:
            T_out = T_wb_exit
            break
        Q_tran = c_a*(T_wb_exit-T_wb)#heat transfer to get to this exit temperature
        dQ_dT = (Q_total2-Q_total)/d_T#marginal heat transfer per degree Twb_exit
        error_T = (Q_tran - Q_total)/dQ_dT
        T_wb_exit = T_wb_exit - gain*error_T
        if T_wb_exit>T_in  or T_wb_exit<T_wb:
            T_wb_exit = T0
        if count>10:
            gain = max(.03125,gain*.5)
            if d_T<1e-2:
                error_T = 0
            d_T = d_T*.25
            count = 0
        count = count+1
    T_out = T_in - Q_total/c_w
    return T_out

def tower_heat_trans(T_in,T_air,w_air,T_wb,T_wb_exit,air_flow,c_w,UA):
    air_density = 1.204 #kg/m^3 #standard air density (1.204 kg/m3) adjusted for the local barometric pressure (standard barometric pressure corrected for altitude, ASHRAE 1997 HOF pg. 6.1).
    Cp_air = 1034 #J/kg*K
    # Cp_e = 2*Cp_air
    Cp_e = (psychometric({'Twb':T_wb_exit,'w':w_air},'h') - psychometric({'Tdb':T_air,'w':w_air},'h'))/(T_wb_exit - T_wb) #J/kg*K
    c_a = air_flow*air_density*Cp_e
    UA_e = UA*Cp_e/Cp_air
    c_min = min(c_w,c_a)
    c_max = max(c_w,c_a)
    NTU = UA_e/c_min
    a = -NTU*(1-c_min/c_max)
    e = float((1-np.exp(a))/(1 - c_min/c_max*np.exp(a)))
    Q_total = e*c_min*(T_in - T_wb)
    return Q_total,c_a