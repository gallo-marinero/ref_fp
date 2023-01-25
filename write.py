import sys, os, shutil
from random import uniform
# Function to replace variables that appear only once in the input file
def rep_zero(line_match,vrbls):
# Loop over all these variables
    for k in ['Zero','SyCos','SySin']:
# Retrieve them from vrbls and store them in var
        var=list(filter(lambda var: var['search_name'] == k, vrbls))[0]
        if var:
# Matched line is stripped into list, to be able to replace in the corresponding
# position. If the variable is not contained in vrbls, do nothing
            if k == 'Zero':
                line_match[0]=str(round(uniform(var['min'],var['max']),5))
                var['new_value']=line_match[0]
            if k == 'SyCos':
                line_match[2]=str(round(uniform(var['min'],var['max']),5))
                var['new_value']=line_match[2]
            if k == 'SySin':
                line_match[4]=str(round(uniform(var['min'],var['max']),5))
                var['new_value']=line_match[4]
# Transform the list into string, which is the new line 
    line_replace='   '.join(line_match)
    return str(line_replace)+'\n'

def rep_xyzbiso(line_match,list_vars):
    for i in list_vars:
        for j in i:
            if j['var_name']=='x' and j['search_name'] in line_match:
# Matched line is stripped into list, to be able to replace in the corresponding
# position. If the variable is not contained in vrbls, do nothing
                line_match[2]=str(round(uniform(j['min'],j['max']),5))
                j['new_value']=line_match[2]
            elif j['var_name']=='y' and j['search_name'] in line_match:
                line_match[3]=str(round(uniform(j['min'],j['max']),5))
                j['new_value']=line_match[3]
            elif j['var_name']=='z' and j['search_name'] in line_match:
                line_match[4]=str(round(uniform(j['min'],j['max']),5))
                j['new_value']=line_match[4]
            elif j['var_name']=='biso' and j['search_name'] in line_match:
                line_match[5]=str(round(uniform(j['min'],j['max']),5))
                j['new_value']=line_match[5]
# Transform the list into string, which is the new line 
    line_replace='    '.join(line_match)
    return str(line_replace)+'\n'

def rep_uy(line_match,list_vars,cif):
    for i in ['U','Y']:
        for j in list_vars:
            if j[0]['search_name']==i:
                for k in j:
                    if k['cif']==cif:
                        if i=='U':
                            line_match[0]=str(round(uniform(k['min'],k['max']),5))
                            k['new_value']=line_match[0]
                        elif i=='Y':
                            line_match[4]=str(round(uniform(k['min'],k['max']),5))
                            k['new_value']=line_match[4]
    line_replace='     '.join(line_match)
    return '     '+str(line_replace)+'\n'

def rep_abc(line_match,list_vars,cif):
    for j in list_vars:
        if j[0]['var_name']=='abc':
            for i in j:
                if i['cif']==cif and i['search_name']=='a':
                    line_match[0]=str(round(uniform(i['min'],i['max']),5))
                    i['new_value']=line_match[0]
                elif i['cif']==cif and i['search_name']=='b':
                    line_match[1]=str(round(uniform(i['min'],i['max']),5))
                    i['new_value']=line_match[1]
                elif i['cif']==cif and i['search_name']=='c':
                    line_match[2]=str(round(uniform(i['min'],i['max']),5))
                    i['new_value']=line_match[2]
# If a=b=c, same value
                elif i['cif']==cif and i['search_name']=='abc':
                    line_match[0]=str(round(uniform(i['min'],i['max']),5))
                    line_match[1]=line_match[0]
                    line_match[2]=line_match[0]
                    i['new_value']=line_match[0]
    line_replace='  '.join(line_match)
    return '     '+str(line_replace)+'\n'

# Write the file with all the variables that are being refined
def ml_input(list_vars,dict_vars,sim_num,chi,pf,wpf):
# Print headers only first time
    ml_f = open('ml.dat','a')
# Remove the file 'ml.dat' if present
    if sim_num==0:
        if os.path.exists('ml.dat'):
            os.remove('ml.dat')
        ml_f = open('ml.dat','a')
        for i in dict_vars:
            ml_f.write(i['search_name']+' ')
        for i in list_vars:
            for j in i:
                ml_f.write(j['var_name']+'_'+j['search_name']+'_'+j['cif']+' ')
#        ml_f.write('chi prof_factor wprof_factor\n')
        ml_f.write('chi \n')
# Print new values
    for i in dict_vars:
        ml_f.write(i['new_value']+' ')
    for i in list_vars:
        for j in i:
            ml_f.write(j['new_value']+' ')
# Print the figures of merit calculated
#    ml_f.write(str(chi)+' '+str(pf)+' '+str(wpf)+'\n')
    ml_f.write(str(chi)+'\n')
    ml_f.close()


def create_inp(sim_inp,ref,vrbls,cifs,sim_num):
# Recognise variables that are defined for several atoms/cifs (and therefore are
# a list, not a dict: X, Y, Z, biso, Scale, U, Y_U and abc) and store them in
# list_vars
    list_vars=[]
    dict_vars=[]
    for i in range(len(vrbls)):
        if type(vrbls[i]) == list:
            list_vars.append(vrbls[i])
        elif type(vrbls[i]) == dict:
            dict_vars.append(vrbls[i])
# Save the names as headers of the ml database                
            
    with open(sim_inp,'w') as sim_f, open(ref,'r') as ref_f: 
        for line in ref_f:
# When Zero (and SySin and SyCos) line is found, replace the variables that are
# dicts (stored in dict_vars) with function rep_zero
                p=True
                count=True
                if 'Zero' in line:
                    sim_f.write(line)
                    line_match=next(ref_f).split()
                    line_replace=rep_zero(line_match,dict_vars)
                    sim_f.write(line_replace)
# Avoid printing again the header '!  Zero...'                    
                    p=False
                for j in cifs:
                    if j in line:
                        cif=j
# Loop over all lists of dicts (X, Y, Z, biso and Scale)
                for i in range(len(list_vars)):
# Check if Scale is present and replace it (according to cif)
                    if 'Scale' in line and list_vars[i][0]['search_name']=='Scale':
                        sim_f.write(line)
# As many loops as cifs                            
                        for k in list_vars[i]:
# Guarantee current cif is being taken                                
                            if k['cif']==cif:
# Generate random number                                    
                                line_match=next(ref_f).split()
                                line_match[0]=str(uniform(k['min'],k['max']))
                                k['new_value']=line_match[0]
                                line_replace='     '.join(line_match)
                                sim_f.write(line_replace+'\n')
                                p=False
                    elif '  U  ' in line and list_vars[i][0]['search_name']=='U':
                        sim_f.write(line)
# As many loops as cifs                            
                        for k in list_vars[i]:
# Guarantee current cif is being taken                                
                            if k['cif']==cif:
# Generate random number                                    
                                line_match=next(ref_f).split()
                                line_replace=rep_uy(line_match,list_vars,cif)
                                sim_f.write(line_replace)
                                p=False
# Check if we are in a b c line                    
                    elif '#Cell Info' in line and list_vars[i][0]['var_name']=='abc':
                        sim_f.write(line)
# As many loops as cifs                            
                        for k in list_vars[i]:
                            if k['cif']==cif:
# Generate random number                                    
                                line_match=next(ref_f).split()
                                line_replace=rep_abc(line_match,list_vars,cif)
                                sim_f.write(line_replace)
                                p=False
# Enter only once
                                break
                    for j in list_vars[i]:
# Loop over all dicts contained on each list item (atoms for which X, Y, Z or
# biso must be changed)
# If one atom is present (must be refined) in one coordinate, enter the loop in
# rep_xyzbiso and check for more coordinates that should be refined, and change
# the value. Enter the loop of rep_xyzbiso just once.
                        if j['var_name'] == 'x' and 'Scale' not in line\
                        and ' U  ' not in line and '#Cell Info' not in line:
# Reset the counter each time x is read
                            count=False
                        if j['search_name'] in line and not count:
# If condition is met once, don't enter again (the function re_xyzbiso does it)
                            count=True
                            sim_f.write(rep_xyzbiso(line.split(),list_vars))
# Avoid printing the old (original) line too
                            p=False
                            break
                if p:
                    sim_f.write(line)
# Return data for ml with all the refined variables
    return list_vars,dict_vars
