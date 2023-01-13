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
            if k == 'SyCos':
                line_match[2]=str(round(uniform(var['min'],var['max']),5))
            if k == 'SySin':
                line_match[4]=str(round(uniform(var['min'],var['max']),5))
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
            elif j['var_name']=='y' and j['search_name'] in line_match:
                line_match[3]=str(round(uniform(j['min'],j['max']),5))
            elif j['var_name']=='z' and j['search_name'] in line_match:
                line_match[4]=str(round(uniform(j['min'],j['max']),5))
            elif j['var_name']=='biso' and j['search_name'] in line_match:
                line_match[5]=str(round(uniform(j['min'],j['max']),5))
# Transform the list into string, which is the new line 
    line_replace='     '.join(line_match)
    return str(line_replace)+'\n'

def create_inp(sim_inp,ref,vrbls,cifs):
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

            
    with open(sim_inp,'w') as sim_f, open(ref,'r') as ref_f:
        for line in ref_f:
# When Zero (and SySin and SyCos) line is found, replace the variables that are
# dicts (stored in dict_vars) with function rep_zero
                p=True
                if 'Zero' in line:
                    sim_f.write(line)
                    line_match=next(ref_f).split()
                    sim_f.write(rep_zero(line_match,dict_vars))
# Avoid printing again the header '!  Zero...'                    
                    p=False
                for j in cifs:
                    if j in line:
                        cif=j
# Loop over all lists of dicts (X, Y, Z and biso)
                for i in range(len(list_vars)):
# Loop over all dicts contained on each list item (atoms for which X, Y, Z or
# biso must be changed)
                    for j in list_vars[i]:
# If one atom is present (must be refined) in one coordinate, enter the loop in
# rep_xyzbiso and check for more coordinates that should be refined, and change
# the value. Enter the loop of rep_xyzbiso just once.
                        if j['search_name'] in line:
                            sim_f.write(rep_xyzbiso(line.split(),list_vars))
# Avoid printing the old (original) line too
                            p=False
                    break
                if p:
                    sim_f.write(line)
