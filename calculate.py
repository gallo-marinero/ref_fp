def fig_merit(exp_point,exp_intensity,exp_std,sim_point,sim_intensity):
    if len(exp_point) != len(sim_point):
        print('Dimensions of experimental and simulated intensities differ')
        print('Adjust in line 14-15 (Thmin, Step, Thmax) of reference *.pcr')
    else:
        chi=0
        for i in range(len(exp_point)):
            if round(exp_point[i],2)==round(sim_point[i],2):
                chi=chi+((1/(exp_std[i]**2))*(exp_intensity[i]-sim_intensity[i])**2)
    return(chi)
