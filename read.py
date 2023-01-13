import sys, os, shutil, defaults, write
from importlib import import_module
from defaults import *

full_vrbls=[zero,sycos,sysin,x_temp,y_temp,z_temp,biso_temp,scale_temp,\
        u_temp,y_u_temp,abc_temp]
# Default to optimize all variables
optimize='all'
# sample_f: file with measured data
# optimize: list of strings with the variables to optimize (lower case)'
vrbls=['sample_f','optimize','x','y','z','biso','scale','u','y_u','abc']
# Read input from file
# Add path where code is executed to be able to load the input file as a module
sys.path.append(os.getcwd())
# Variable definition
nphase=0
cif_files=[]
x_coord=[]
y_coord=[]
z_coord=[]
biso_coord=[]
scale=[]
u=[]
y_u=[]
abc=[]
# Import variables in input file
inp_f=__import__(sys.argv[1])
for i in vrbls:
    # Check if the variable is present in input file
    if hasattr(inp_f,i):
# Update variable
        globals()[i] = getattr(inp_f,i)

if optimize == 'all':
# Default is to optimize all variables 
    opt_vrbls = full_vrbls
# If optimize is present in the user input, use only the variables the user gives
else:
    opt_vrbls=[]
    for i in full_vrbls:
        if i['var_name'] in optimize:
            opt_vrbls.append(i)

# Delete and create a folder where all the simulations are going to be stored
shutil.rmtree(os.path.join(os.getcwd(),'simulations'))
os.mkdir(os.path.join(os.getcwd(),'simulations'))
# Open reference simulation file
with open(sample_f,'r') as f:
    for line in f:
# Loop over all variables to be considered in the refinement
        for ovar in opt_vrbls:
            if ovar['search_name'] in line:
                if ovar['search_name'] == 'Zero':
                    zeroline=next(f).split()
                    zero['value']=zeroline[0]
                    sycos['value']=zeroline[2]
                    sysin['value']=zeroline[4]
# Save the .cif that is being refined to print it as informative output
        if 'cif' in line:
            cif_files.append(line.strip())
# Append is a variable that contains the name of the cif to differentiate the
# refined parameters that are present once per cif type (scale, U and Y)
            curr_cif=line.strip()
# Check if the line starts with one of the atoms specified in the input (Fe1,
# O1...) and if yes, store it
        if line.split()[0] in x or line.split()[0] in y or line.split()[0] in z\
        or line.split()[0] in biso:
            if line.split()[0] in x:
                x_temp['search_name']=line.split()[0]
                x_temp['value']=line.split()[2]
                x_coord.append(x_temp.copy())
            if line.split()[0] in y:
                y_temp['search_name']=line.split()[0]
                y_temp['value']=line.split()[3]
                y_coord.append(y_temp.copy())
            if line.split()[0] in z:
                z_temp['search_name']=line.split()[0]
                z_temp['value']=line.split()[4]
                z_coord.append(z_temp.copy())
            if line.split()[0] in biso:
                biso_temp['search_name']=line.split()[0]
                biso_temp['value']=line.split()[5]
                biso_coord.append(biso_temp.copy())
        if 'Scale' in line:
            scale_temp['value']=next(f).split()[0]
            scale_temp['cif']=curr_cif
            scale.append(scale_temp.copy())
        if '!       U' in line:
            u_temp['value']=next(f).split()[0]
            u_temp['cif']=curr_cif
            y_u_temp['value']=next(f).split()[4]
            y_u_temp['cif']=curr_cif
            u.append(u_temp.copy())
            y_u.append(y_u_temp.copy())
        if '!     a' in line:
# Read a, b, c parameters            
            nex=next(f).split()
            a=float(nex[0])
            b=float(nex[1])
            c=float(nex[2])
# In case of cubic cell, use only 1 variable            
            if a == b == c:
                abc_temp['var_name']='abc'
                abc_temp['search_name']='abc'
                abc_temp['value']=a
# Range is +-10%                
                abc_temp['min']=a-(a*.1)
                abc_temp['max']=a+(a*.1)
                abc.append(abc_temp.copy())
            else:
                abc_temp['var_name']='abc'
                abc_temp['search_name']='a'
                abc_temp['value']=a
                abc_temp['min']=a-(a*.1)
                abc_temp['max']=a+(a*.1)
                abc.append(abc_temp.copy())
                abc_temp['var_name']='abc'
                abc_temp['search_name']='b'
                abc_temp['value']=b
                abc_temp['min']=b-(b*.1)
                abc_temp['max']=b+(b*.1)
                abc.append(abc_temp.copy())
                abc_temp['var_name']='abc'
                abc_temp['search_name']='c'
                abc_temp['value']=c
                abc_temp['min']=c-(c*.1)
                abc_temp['max']=c+(c*.1)
                abc.append(abc_temp.copy())

# Print information on the data that is being considered
print('  Running simulations for', len(cif_files), 'phases:')
for i in cif_files:
    print('  ',i)
# Print variables that are being refined
print('  Refining the following variables:')
for i in range(len(opt_vrbls)):
    item=opt_vrbls[i]
    print('   -',item['var_name'])
# In case x, y, z are refined, print for which atoms
    if item['var_name']=='x':
        for j in x_coord:
            print('   ',j['search_name'], end=" ")
        print('\n')
        opt_vrbls[i]=x_coord
    elif item['var_name']=='y':
        for j in y_coord:
            print('   ',j['search_name'], end=" ")
        print('\n')
        opt_vrbls[i]=y_coord
    elif item['var_name']=='z':
        for j in z_coord:
            print('   ',j['search_name'], end=" ")
        print('\n')
        opt_vrbls[i]=z_coord
    elif item['var_name']=='biso':
        for j in biso_coord:
            print('   ',j['search_name'], end=" ")
        print('\n')
        opt_vrbls[i]=biso_coord
    elif item['var_name']=='scale':
        for j in scale:
            print('   ',j['search_name'], end=" ")
        print('\n')
        opt_vrbls[i]=scale
    elif item['var_name']=='u':
        for j in scale:
            print('   ',j['search_name'], end=" ")
        print('\n')
        opt_vrbls[i]=u
    elif item['var_name']=='y_u':
        for j in scale:
            print('   ',j['search_name'], end=" ")
        print('\n')
        opt_vrbls[i]=y_u
    elif item['var_name']=='abc':
        for j in scale:
            print('   ',j['search_name'], end=" ")
        print('\n')
        opt_vrbls[i]=abc

opt_vrbls=[zero,sysin,sycos,x_coord,y_coord,z_coord,biso_coord]
print('\n-----------\n')
# Loop through all the simulations the user wants to run
for i in range(1):
# Append the simulation number to each input filename
    sim_inp=os.path.join(os.getcwd(),'simulations/'+str(i+1)+'_'+sample_f)
    shutil.copy(os.path.join(os.getcwd(),sample_f),sim_inp)
    write.create_inp(sim_inp,sample_f,opt_vrbls,cif_files)
