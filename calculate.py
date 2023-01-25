import math
def fig_merit(exp_point,exp_intensity,exp_std,sim_point,sim_intensity):
    if len(exp_point) != len(sim_point):
        print('Dimensions of experimental and simulated intensities differ')
        print('Adjust in line 14-15 (Thmin, Step, Thmax) of reference *.pcr')
    else:
        chi=0
        rpden=0
        rpnum=0
        wpfnum=0
        wpfden=0
        for i in range(len(exp_point)):
#            if round(exp_point[i],2)==round(sim_point[i],2):
                print(round(exp_point[i],3),round(sim_point[i],3))
                w=1/(exp_std[i]**2)
#                w=1/(exp_intensity[i])
                chi=chi+((1/(exp_std[i]**2))*((exp_intensity[i]-sim_intensity[i])**2))
#                chi=chi+((1/exp_intensity[i])*((exp_intensity[i]-sim_intensity[i])**2))
                rpnum=rpnum+abs(exp_intensity[i]-sim_intensity[i])
                rpden=rpden+exp_intensity[i]
                wpfnum=wpfnum+(w*((exp_intensity[i]-sim_intensity[i])**2))
                wpfden=wpfden+(w*exp_intensity[i]**2)
                pf=100*rpnum/rpden
                wpf=100*math.sqrt(wpfnum/wpfden)
    return(chi,pf,wpf)
