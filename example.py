import sys
import os
#TODO: change this to the path of the amber package on your own cluster (hot fix, there might be a better way to do this)
sys.path.insert(0, '/PHShome/lk001/.conda/envs/myenv/lib/python3.9/site-packages') #cluster

#TODO: import your own package here and rename it however you want
import MyPackage as pack

#import other packages not imported by your own package
import numpy as np

print('python version', sys.version)
print('Current working directory:', os.getcwd())
#print the directory of amber
print('MyPackage directory:', pack.__file__)
print('MyPackage version:',pack.__version__)

# this reads the argument/parameter you mention after the python script when you run:
# python example.py CONFIG_FILE
# if you don't specify a config file, it will raise an error

if len(sys.argv) > 1:
    config_file = sys.argv[1]
else:
    raise ValueError('No config file specified')

config = pack.Config(config_file)

#set seed for reproducibility

print('Config file', config_file)
seed = config.seed
print('Seed', seed)
np.random.seed(seed)

# print all the parameters in the config file for debugging
print('#'*80)

for key, value in config.__dict__.items():
    print(key, value)

print('#'*80)

#TODO: replace this with your main function (simulator, etc.)

pack.my_function(config.example)

myclassinstance = pack.MyClass()
myclassinstance.my_method()