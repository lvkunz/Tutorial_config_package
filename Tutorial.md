# Tutorial for python code structuration


## How to use the config class in your own code

The Config class is a class already specified in the package architecture provided. You can create an instance of it and initialize it with the path to your config file (see example.py and the config.txt file for an example).
Keep in mind that the config file needs to be in the same folder as the python script you're running. 
If you're not using the whole package architecture, you can copy the config.py file into your own folder and import it in your python script with a normal import statement (from config import Config).
You can then use the following

```python
config = pack.Config(config_file)
```

The example.py shows how you can specify the config name as an argument when running the python script

You can specify rules/check for your parameters in the config.py script and access any variable:
    
```python
config.variable_name
```

## How to setup a python environment

### Using conda

I recommend setting up a conda environment to run your python code. This will allow you to install all the packages you need without having to worry about dependencies.
To do so you need to install conda on your computer. You can follow the instructions on the [conda website](https://docs.conda.io/projects/conda/en/latest/user-guide/install/).
Then you can create a new environment with the following command (replace myenv by the name of your environment):
```bash 
conda create --name myenv python=3.9 
```

You can then activate your environment with the following command:
```bash
conda activate myenv
```

You can install packages with the following command:
```bash
conda install -c conda-forge numpy
```

You can also install packages with pip but it is not recommended as it might cause dependency issues:
```bash
pip install numpy
```

You can list all the packages installed in your environment with the following command:
```bash
conda list
```

It is better to install all package at once to optimize dependencies. You can do so by calling to the requirements.txt file that contains all the packages you want to install.
```bash
conda install --file requirements.txt
```


## How to make your code into a package
Once your environnement is nicely set up, you can start looking into package your own code.
For this, you need to put all your scripts into a single repository whose name is the name of your package and that contains a __init__.py file.

You then need to modify the requirements.txt, README.md, setup.py and __init__.py files for your own package. Once this is done update the install.sh with the proper name. 
TODO statements should help you find where you need to modify the files. (You can navigate them with the TODO menu on PyCharm)

You can then install your package on your virtual environment with the following commands:

```bash
conda activate myenv
bash install.sh
```

You can then import your package in your python script with the following command:

```python
import mypackage as pack
```

See the example.py file for an example of how to use it in more details.

## How to run on the cluster

First make sure the path to your virtual environnement is correct. You can make sure of that by adding the line shown at the beginning of the example.py file.
You can run your python script on the cluster with the following command:

```bash
bash run_MyPackage.sh example.py <n_iter> CONFIG
```

You might need to change the shell script for your own cluster. Again TODO statements should help you find where you need to modify the file.

Where <n_iter> is the number of iterations you want to run. You can then decide which parameters you want to change in the CONFIG file for each iteration.
For example when prompted 
```
Enter a parameter name to change, or type 'none' to continue: 
```

you can reply 'dt' to change the time step for each iteration. Choose all the parameters you want to change, then type 'none' to continue.
Then you will be prompted to enter the values for each parameter you chose to change for each iteration.

The script will then run all simulations and store them in an output folder. You'll find that the folder hierarchy goes through dates, name of config file and python
script, and then the iteration number. The output folder will contain all the data from the simulation, including the CONFIG file used for each iteration.
The output folder will also contain a log file with the date and time of the simulation, as well as the parameters used for each iteration stored in a .csv file.


## How to plot the results from cluster simulations
To easily read the results of your simulations you can run the plotting.py script by changing the output folder directory you want to use and the name of the parameters you want to look at.

