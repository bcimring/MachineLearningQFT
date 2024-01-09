#! /usr/bin/python
import numpy as np
from scipy.constants import c, hbar, elementary_charge, Boltzmann

n_samples    = 1              # Number of examples to produce for training/validating
datapoints = 50000
Regression = True
overwrite = False
gather_all_data_before_training = False
rerun_datapoints = False

### Parameters of the quantum field ###
sigma = 18e-3                 # Detector Smearing [m]
Ksig = 16/sigma                    # Determines UV Cutoff [m^-1]
a = np.pi/Ksig      # Lattice spacing induced by UV Cutoff [m]
latlen = 100         # Determines IR Cutoff [a]
mcc = 0.1*1e9*hbar                     # Field mass [eV]
wD = 10*1e9*hbar                    # Detector gap [eV]
lam = 10*1e9*hbar                   # Coupling energy [eV]
Tmean = 0


### Units used are hbar = c = a = 1 ###
E0 = hbar*c/a   # Energy unit
Temp0 = a*Boltzmann/(hbar*c)   # Energy unit
L0 = a   # Energy unit
T0 = a/c   # Energy unit

### Unitless Parameters ###
sigma = sigma/L0            # Normalized Smearing
mcc = mcc/E0               # Normalized Field Mass
wD = wD/E0                 # Normalized Detector Gap   
lam = lam/E0               # Normalized Coupling Energy
Tmean = Tmean/Temp0  # convert to hbar = c = a = k_b = 1 units
Tdev = 0*Tmean             # Size of Temperature range


### Measurement Options ###
time_min = -13           # Start of first measurement window   [s]
time_max = -8      # End of last measurement window      [s]
n_windows = 1*(time_max-time_min)+1

plot_times_max = np.logspace(time_min,time_max,n_windows,endpoint=True) # Linearly spaces measurement windows
plot_times_max = plot_times_max/T0
plot_times_min = plot_times_max*plot_times_max[0]/plot_times_max[1]


measurements_per_window = 32 			          # Number of measurement times considered in each window
n_tom = 1e8                    # Number of times to repeat the whole experiment

### Defining Classes for Classification ###
TDev = 0             # Size of Temperature range

                                             
### Setting Active Cases (Label, Probability, Y-label, Details) ###
LPYD = [['Case Name',  'Abv'  , 'Prob', 'y', 'Boundary Type','Distance to Boundary','Temperature', 'Smearing', 'Dim'],]


for i in range(datapoints):

    d = np.random.uniform()
    LPYD.append([str(i),str(i), 1, d/100, 1, d, Tmean, 'gaussian', 1])

# notes
# use 3 node hidden layer, train for 25 epochs

LPYD = np.asarray(LPYD, dtype=object)
LPYD[1:, 3] = np.around(np.asarray(LPYD[1:, 3], dtype=float), 3)
#print(LPYD)

### PCA Options ###
RunPCAonData = True               # Whether or not to do PCA
PCA_var_keep = 1                  # Fraction of variance to be kept after PCA (0 to 1 or 'All') 
N_PCA_plot   = 1000               # Number of data points to ploted in PCA 

### Neural Network Options ###
RunNNonData = True                # Whether or not to train the Neural Network
f_train = 75                      # Fraction of data used for training 
f_valid = 20                      # Fraction of data used for validation
f_test = 5                        # Fraction of data reserved for testing
fsum = f_train + f_valid + f_test # Normalize
f_train = f_train/fsum
f_valid = f_valid/fsum
f_test  = f_test/fsum

nH1 = 32                         # Number of neurons in the first hidden layer
L2reg = 1e-4                    # L2 Regularizer
learning_rate = 1e-3             # Learning Rate
n_epochs = 20                  # Number of epoch to train over
minibatch_size = 256             # Minibatch size

experiment_name = "position_regression_v2" + \
                  "_ntom=1e" + str(int(np.log10(n_tom))).replace('.', 'p') + \
                  "_T=" + str(Tmean*Temp0).replace('.', 'p') + \
                  "K_nH1=" + str(nH1) + \
                  "_n_epochs=" + str(n_epochs) + \
                  "_l2reg=1e" + str(np.log10(L2reg)).replace('.', 'p') + \
                  "_lr=1e" +str(np.log10(learning_rate)).replace('.', 'p')

