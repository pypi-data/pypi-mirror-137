#Imports
import math
from dataclasses import dataclass
import torch

#botorch
from botorch.acquisition import qExpectedImprovement
from botorch.fit import fit_gpytorch_model
from botorch.generation import MaxPosteriorSampling
from botorch.models import FixedNoiseGP, SingleTaskGP
from botorch.optim import optimize_acqf
#from botorch.test_functions import Ackley
from botorch.utils.transforms import unnormalize
from decimal import Decimal

#gpytorch
import gpytorch
from gpytorch.constraints import Interval
from gpytorch.likelihoods import GaussianLikelihood
from gpytorch.mlls import ExactMarginalLogLikelihood
from gpytorch.priors import HorseshoePrior

#torch (we import functions from modules for small speed ups in performance)
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.init as init
import torch.optim as optim
from torch import nn, optim
from torch.autograd import Variable
from torch.autograd import grad
from torch.autograd import Function as Function
from torch.quasirandom import SobolEngine
from torch import matmul, pinverse, hstack, eye, ones, zeros, cuda, Generator, rand, randperm, no_grad, normal, tensor, vstack, cat, dot, ones_like, zeros_like
from torch import clamp, prod, where, randint, stack
from torch import device as torch_device
from torch.cuda import is_available as cuda_is_available
from torch.nn import Linear, MSELoss, Tanh, NLLLoss, Parameter

#other packages
from dataclasses import dataclass
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import seaborn as sns
import time

from sklearn.linear_model import ElasticNet

from .custom_loss import *
from .defs import *
import re
import matplotlib.gridspec as gridspec

from copy import deepcopy

# def sigmoid_derivative(x):
#     s = sigmoid(x)
#     ds = s*(1-s)
#     return ds

def inverse_hyperbolic_tangent(z):
    # z_max = z.abs().max()  + 0.0001
    # z = z/z_max
    return (1/2)*torch.log((1+z)/(1-z))

@ray.remote(num_gpus=n_gpus, max_calls=1)
def execute_objective(parallel_arguments, parameters, X_turbo_spec, trust_region_id):
    optimize(**parameters)

@ray.remote(num_gpus=n_gpus, max_calls=1)
def execute_backprop(args,  y0, lr = 0.05, plott = False, reg = None, plot_every_n_epochs = 2000, SAVE_AFTER_EPOCHS = 1):

    # esn, 
    # 
    # epochs = 45000,
    # custom_loss = custom_loss,
    # EPOCHS_TO_TERMINATION = None,
    # f = force,
    # force_t = None,
    # lr = 0.05, 
    # 
    # plott = False,
    # 


    #RC = args["rc"]
    custom_loss = args["custom_loss"]
    epochs = args["epochs"]
    new_X = args["New_X"]
    states_dot = args["states_dot"]
    LinOut = args["out_W"]
    force_t = args["force_t"]
    criterion = args["criterion"]
    spikethreshold = args["spikethreshold"]
    t = args["t"]
    G = args["G"]
    g, g_dot = G
    gamma_cyclic = args["gamma_cyclic"]
    gamma = args["gamma"]
    init_conds = args["init_conds"]
    ode_coefs = args["ode_coefs"]
    enet_strength = args["enet_strength"]
    enet_alpha = args["enet_alpha"]
    init_conds[0] = y0

    optimizer = optim.Adam([LinOut.weight, LinOut.bias], lr = lr)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=1, gamma=gamma)

    if gamma_cyclic:
        cyclic_scheduler = torch.optim.lr_scheduler.CyclicLR(optimizer, 10**-6, 0.01,
                                            gamma = gamma_cyclic,#0.9999,
                                            mode = "exp_range", cycle_momentum = False)
    if plott:
      #use pl for live plotting
      fig, ax = pl.subplots(1,3, figsize = (16,4))

    loss_history = []
    lrs = []
    previous_loss = 0
    floss_last = 0
    best_score = 10000
    pow_ = -4


    with torch.enable_grad():
        
        #begin optimization loop
        for e in range(epochs):

            optimizer.zero_grad()

            N = LinOut( new_X)
            
            N_dot = states_dot @ LinOut.weight.T #esn.calc_Ndot(states_dot)
            
            y = g *N 

            ydot = g_dot * N + g * N_dot

            for i in range(y.shape[1]):
                y[:,i] = y[:,i] + init_conds[i]

            # y[:,0] = y[:,0] + init_conds[0]
            # y[:,1] = y[:,1] + init_conds[1]

            #assert N.shape == N_dot.shape, f'{N.shape} != {N_dot.shape}'

            #assert esn.LinOut.weight.requires_grad and esn.LinOut.bias.requires_grad

            #total_ws = esn.LinOut.weight.shape[0] + 1
            #weight_size_sq = torch.mean(torch.square(esn.LinOut.weight))

            loss = custom_loss(t, y, ydot, LinOut.weight, reg = reg, ode_coefs = ode_coefs,
                    init_conds = init_conds, enet_alpha= enet_alpha, enet_strength = enet_strength, force_t = force_t)
            loss.backward()
            optimizer.step()
            if gamma_cyclic and e > 100 and e <5000:
                cyclic_scheduler.step()
                lrs.append(optimizer.param_groups[0]["lr"])


            floss = float(loss)
            loss_history.append(floss)


            if e > 0:
                loss_delta = float(np.log(floss_last) - np.log(floss)) 
                if loss_delta > spikethreshold:# or loss_delta < -3:
                    lrs.append(optimizer.param_groups[0]["lr"])
                    scheduler.step()


            # if not e and not best_score:
            #     

            if e > SAVE_AFTER_EPOCHS:
                if not best_score:
                    best_score = min(loss_history)
                if floss < best_score:  
                    best_bias, best_weight = LinOut.bias.detach(), LinOut.weight.detach()
                    best_score = float(loss)
                    best_fit = y.clone()
                    best_ydot = ydot.clone()
            else:
                best_bias, best_weight, best_fit = LinOut.bias.detach(), LinOut.weight.detach(), y.clone()

            floss_last = floss

            # else:
            #     if floss < best_score:
            #         best_bias, best_weight = esn.LinOut.bias.detach(), esn.LinOut.weight.detach()
            #         best_score = float(loss)
            #         best_fit = y.clone()
            #         best_ydot = ydot.clone()
            
            # if e >= EPOCHS_TO_TERMINATION and EPOCHS_TO_TERMINATION:
            #     return {"weights": best_weight, "bias" : best_bias, "y" : best_fit, 
            #           "loss" : {"loss_history" : loss_history},  "best_score" : torch.tensor(best_score),
            #           "RC" : esn}
            
            # if plott and e:

            #     if e % plot_every_n_epochs == 0:
            #         for param_group in optimizer.param_groups:
            #             print('lr', param_group['lr'])
            #         ax[0].clear()
            #         logloss_str = 'Log(L) ' + '%.2E' % Decimal((loss).item())
            #         delta_loss  = ' delta Log(L) ' + '%.2E' % Decimal((loss-previous_loss).item())

            #         print(logloss_str + ", " + delta_loss)
            #         ax[0].plot(y.detach().cpu())
            #         ax[0].set_title(f"Epoch {e}" + ", " + logloss_str)
            #         ax[0].set_xlabel("t")

            #         ax[1].set_title(delta_loss)
            #         ax[1].plot(ydot.detach().cpu(), label = "ydot")
            #         #ax[0].plot(y_dot.detach(), label = "dy_dx")
            #         ax[2].clear()
            #         #weight_size = str(weight_size_sq.detach().item())
            #         #ax[2].set_title("loss history \n and "+ weight_size)

            #         ax[2].loglog(loss_history)
            #         ax[2].set_xlabel("t")

            #         #[ax[i].legend() for i in range(3)]
            #         previous_loss = loss.item()

            #         #clear the plot outputt and then re-plot
            #         display.clear_output(wait=True) 
            #         display.display(pl.gcf())


    return {"weights": best_weight, "bias" : best_bias, "y" : best_fit, "ydot" : best_ydot, 
          "loss" : {"loss_history" : loss_history}, "best_score" : torch.tensor(best_score)}
          #"RC" : esn}






#pytorch elastic net regularization:
#https://github.com/jayanthkoushik/torch-gel

#TODO: unit test setting interactive to False.

#TODO: repair esn documentation (go strait to reinier's, copy and make adjustments)

#TODO: rename some pyesn variables.



#TODO: improve documentation.
def sech2(z):
    return (1/(torch.cosh(z)))**2

def sigmoid_derivative(z):
    s = torch.sigmoid(z)
    return s*(1-s)#(1/(torch.cosh(z)))**2

class Recurrence(Function):
    """
    TODO doctstring
    """

    @staticmethod
    def forward(ctx, states, esn, X, y, weights):
        """
        TODO doctstring
        """
        states, states_dot = esn.train_states(X, y, states)
        ctx.states = states
        ctx.states_dot = states_dot
        return states, states_dot

    @staticmethod
    def backward(ctx, grad_output, weights):
        """
        TODO doctstring
        """
        if grad_output is None:
            return None, None
        output = torch.matmul(ctx.states_dot, weights.T)

        return output, None, None, None, None

def dfx(x,f, retain_graph = True, create_graph = True, requires_grad = True, grad_outputs = None):
    """
    TODO doctstring
    """
    try:
        assert not grad_outputs
        return grad([f],[x], grad_outputs=ones_like(f), 
                    create_graph = create_graph, retain_graph = retain_graph)[0]
    except:
        return grad([f],[x], grad_outputs=ones_like(f), create_graph = create_graph, 
                             retain_graph = retain_graph)[0]


def check_x(X, y, tensor_args = {}, supervised = False):
    """
    TODO doctstring
    """
    if X is None:
        if supervised:
            X = ones((y.shape[0],1), **tensor_args) #*y.shape,
        else:
            X = torch.linspace(0, 1, steps = y.shape[0], **tensor_args)
    elif type(X) == np.ndarray:
        X = torch.tensor(X,  **tensor_args)
    
    if len(X.shape) == 1:
        X = X.view(-1, 1)
    return X

def check_y(y, tensor_args = {}):
    """
    TODO doctstring
    """
    if type(y) == np.ndarray:
         y = torch.tensor(y, **tensor_args)
    elif y.device != tensor_args["device"]:
        y = y.to(tensor_args["device"])
    if len(y.shape) == 1:
        y = y.view(-1, 1)
    return y


def printn(param: torch.nn.parameter):
    """TODO"""
    print(param._name_ + "\t \t", param.shape)

def NRMSELoss(yhat,y):
    """TODO"""
    return torch.sqrt(torch.mean((yhat-y)**2)/y**2)

def sinsq(x):
    """TODO"""
    return torch.square(torch.sin(x))

def printc(string_, color_, end = '\n') :
    """TODO"""
    colorz = {
          "header" : '\033[95m',
          "blue" : '\033[94m',
          'cyan' : '\033[96m',
          'green' : '\033[92m',
          'warning' : '\033[93m',
          'fail' : '\033[91m',
          'endc' : '\033[0m',
           'bold' :'\033[1m',
           "underline" : '\033[4m'
        }
    print(colorz[color_] + string_ + colorz["endc"] , end = end)

def convert_ode_coefs(ode_coefs_, X):
    """
    TODO doctstring
    """
    #print('type_X', type_X)
    ode_coefs = ode_coefs_.copy()
    if type(ode_coefs_) == list:
        for i, coef in enumerate(ode_coefs_):
            if type(coef) == str:
                if coef[0] == "t" and (coef[1] == "^" or (coef[1] == "*" and coef[2] == "*")):
                    pow_ = float(re.sub("[^0-9.-]+", "", coef))
                    ode_coefs[i]  = X ** pow_
            elif type(coef) in [float, int, type(X)]:
                pass
            else:
                assert False, "ode_coefs must be a list of floats or strings of the form 't^pow', where pow is a real number."
    else:
        assert False, "ode_coefs must be a list of floats or strings of the form 't^pow', where pow is a real number."
    return ode_coefs

# def execute_backprop(RC):

#     gd_weights = []
#     gd_biases = []
#     ys = []
#     ydots =[]
#     scores = []
#     Ls = []
#     init_conds_clone = init_conditions.copy()
#     if not SOLVE:
#         orig_weights = self.LinOut.weight.clone()
#         orig_bias = self.LinOut.bias.clone()
        
#     for i, y0 in enumerate(init_conds_clone[0]):
#         #print("w", i)
#         if SOLVE:
#             self.LinOut.weight = Parameter(self.weights_list[i].view(self.n_outputs, -1)).requires_grad_(True)
#             self.LinOut.bias = Parameter(self.biases_list[i].view(1, self.n_outputs)).requires_grad_(True)
#         else:
#             self.LinOut.weight = Parameter(orig_weights.view(self.n_outputs, -1))
#             self.LinOut.bias = Parameter(orig_bias.view(1, self.n_outputs))
#         self.init_conds[0] = float(y0)
#         #print(self.init_conds[0])
#         with torch.enable_grad():
#             weight_dict = backprop_f(self, force_t = self.force_t, custom_loss = ODE_criterion, epochs = epochs)

#         score=weight_dict["best_score"]
#         y = weight_dict["y"]
#         ydot = weight_dict["ydot"]
#         loss, gd_weight, gd_bias = weight_dict["loss"]["loss_history"], weight_dict["weights"],  weight_dict["bias"]
#         scores.append(score)
#         ys.append(y)
#         ydots.append(ydot)
#         gd_weights.append(gd_weight)
#         gd_biases.append(gd_bias)
#         Ls.append(loss)


tanh_activation = Tanh()

def sech2_(z):
    return (1/(np.cosh(z)))**2

def identity(z):
    return z

def neg_sin(z):
    return -  torch.sin(z)

def neg_double_sin(z):
    return - torch.sin(2* z)

def double_cos(z):
    return torch.cos(2 * z)

tanh_at_2 = 0.9640275800
tanh_at_2_half = 0.48201379003

def my_relu_i(z, lim = 2):
    """
    TODO doctstring
    """
    if z >= lim:
        return np.tanh(z)#tanh_at_2
    elif z <= -lim:
        return np.tanh(z)#tanh_at_2 
    else:
        return tanh_at_2_half*z

def rnn_relu(z):
    return z.apply_(my_relu_i)

def my_relu_i_prime(z, lim = 2):
    """
    TODO doctstring
    """
    if (z >= lim) or (z <= -lim):
        return sech2_(z)
    else:
        return tanh_at_2_half

def rnn_relu_prime(z):
    return z.apply_(my_relu_i_prime)

def log_sin(z):
    return torch.sin(torch.log(z))

def log_sin_prime(z):
    return (1/x)*torch.cos(log(z))

def sin2(z):
    s = torch.sin(5 * z)*torch.sin(5*z)*2 - 1
    return s**2

def sin2_derivative(z):
    s = 10*torch.sin(10 * z)
    return s**2

def sincos(z):
    return torch.sin(z)*torch.cos(z)

def sincos_derivative(z):
    return torch.cos(2*z)


def convert_activation_f(string, derivative  = False, both = True):
    """
    TODO doctstring
    """

    if string == "sigmoid":
        act_f, act_f_prime =  torch.sigmoid, sigmoid_derivative
    elif string == "tanh":
        act_f, act_f_prime =   torch.tanh, sech2
    elif string == "sin":
        act_f, act_f_prime =   torch.sin, torch.cos
    elif string == "cos":
        act_f, act_f_prime =   torch.cos, neg_sin
    elif string == "double_cos":
        act_f, act_f_prime =   double_cos, neg_double_sin
    elif string == "relu":
        act_f, act_f_prime =   rnn_relu, rnn_relu_prime
    elif string == "log_sin":
        act_f, act_f_prime =   log_sin, log_sin_prime
    elif string == "sin2":
        act_f, act_f_prime =   sin2, sin2_derivative
    elif string == "sincos":
        act_f, act_f_prime =   sincos, sincos_derivative
    else:
        assert False, f"activation function '{activation_function}' not yet implimented"
    if both:
        return act_f, act_f_prime
    if not derivative:
        return act_f
    else:
        return act_f_prime


class RcNetwork(nn.Module):
    """Class with all functionality to train Echo State Nets.
    Builds and echo state network with the specified parameters.
    In training, testing and predicting, x is a matrix consisting of column-wise time series features.
    Y is a zero-dimensional target vector.
    Parameters
    ----------
    n_nodes : int
        Number of nodes that together make up the reservoir
    input_scaling : float
        The scaling of input values into the network
    feedback_scaling : float
        The scaling of feedback values back into the reservoir
    spectral_radius : float
        Sets the magnitude of the largest eigenvalue of the transition matrix (weight matrix)
    leaking_rate : float
        Specifies how much of the state update 'leaks' into the new state
    connectivity : float
        The probability that two nodes will be connected
    regularization : float
        The L2-regularization parameter used in Ridge regression for model inference
    feedback : bool
        Sets feedback of the last value back into the network on or off
    random_seed : int
        Seed used to initialize RandomState in reservoir generation and weight initialization
    
    
    BACKPROP ARGUMENTS (not needed for the homework)
    backprop: bool
        if true the network initiates backpropogation.
    classification: bool
        if true the network assumes a categorical response, initiates backprop. Not yet working.
    criterion: torch.nn.Loss function
        loss function for backprogation training
    epochs: int
        the number of epochs to train the network for.
    l2_prop: float (between 0 and 1)
        this is the proportion of the l2 norm. if 1, ridge regression. if 0, lasso. in between it's elastic net regularization.
        **Please note that a significant slowdown will occur with values other than 0**

    
    Methods
    -------
    train(y, x=None, burn_in=100)
        Train an Echo State Network
    test(y, x=None, y_start=None, scoring_method='mse', alpha=1.)
        Tests and scores against known output
    predict(n_steps, x=None, y_start=None)
        Predicts n values in advance
    predict_stepwise(y, x=None, steps_ahead=1, y_start=None)
        Predicts a specified number of steps into the future for every time point in y-values array (NOT IMPLIMENTED)

    Arguments to be implimented later:
        obs_idx = None, resp_idx = None, input_weight_type = None, model_type = "uniform", PyESNnoise=0.001, 
        regularization lr: reg_lr = 10**-4, 
        change bias back to "uniform"
    """
    def __init__(self, 
                 n_nodes = 1000, bias = 0, connectivity = 0.1, leaking_rate = 0.99, spectral_radius = 0.9, noise = None, #<-- important hyper-parameters
                 regularization = None, feedback = False, enet_alpha = None, gamma_cyclic = None,  
                 mu = None, sigma = None,                     #<-- activation, feedback
                 input_scaling = 0.5, feedback_scaling = 0.5,                                    #<-- hyper-params not needed for the hw
                 approximate_reservoir = False, device = None, id_ = None, random_state = 123, reservoir = None, #<-- process args
                 classification = False, l2_prop = 1, n_inputs = None, n_outputs = None,
                  dtype = None, calculate_state_grads = False, dt = None,
                 activation_function = "tanh", enet_strength = None,
                 output_activation = "identity", input_weight_dist = "uniform", input_connectivity = None,
                 #act_f_prime = sech2,  
                 gamma = None, spikethreshold = None, reservoir_weight_dist = "uniform", solve_sample_prop = 1,
                 feedback_weight_dist = "uniform", feedback_connectivity = None,
                 **kwargs): #<-- this line is backprop arguments #beta = None
        super().__init__()

        np.random.seed(random_state)
        for key, val in kwargs.items():
            if key != 'self':
                setattr(self, key, val)

        #assign attributes to self
        for key, val in locals().items():
            if key != 'self':
                setattr(self, key, val)

        self.dev = {"device" : self.device, "dtype" : self.dtype, "requires_grad" : False}

        if type(activation_function) == str:
            self.activation_function, self.act_f_prime = convert_activation_f(activation_function)
        elif type(activation_function) == list:
            self._act_fs = [convert_activation_f(act_f, derivative = False, both = False) for act_f in activation_function]
            self._act_f_primes = [convert_activation_f(act_f, derivative = False, both = False) for act_f in activation_function]
            #mask = torch.tensor(np.random.choice(list(range(len(self._act_fs))), size = n_nodes)) #(torch.tensor(np.ones(n_nodes)) * torch.rand(250) < 0.5)*1

            n_fs = list(range(len(self._act_fs)))
            self._act_mask = torch.tensor(np.random.choice(n_fs, size = self.n_nodes)) #(torch.tensor(np.ones(n_nodes), **self.dev) * torch.rand(n_nodes) < 0.5)*1
            self.activation_function = self._multiple_act_f
            self.act_f_prime = self._multiple_act_f_prime
        elif type(activation_function) == dict:
            self.activation_function = self._multiple_act_f
            self._act_fs = []
            self._act_f_primes = []
            probs = []
            for act_f,  prop in activation_function.items():
                self._act_fs.append(convert_activation_f(act_f, derivative = False, both = False))
                self._act_f_primes.append(convert_activation_f(act_f, derivative = False, both = False))
                probs.append(prop)

            probs = np.array(probs)
            probs = probs / np.sum(probs)
            n_fs = list(range(len(self._act_fs)))
            self._act_mask = torch.tensor(np.random.choice(n_fs, size = self.n_nodes, p = probs))
        else:
            assert False, f'inproper activation function input'

        self.LinOut = None

        if output_activation == "identity":
            self.output_f, self.output_f_inv  = identity, identity
            self._normalize = False
        elif output_activation == "tanh":
            self._normalize = True
            self.output_f, self.output_f_inv = torch.tanh, inverse_hyperbolic_tangent
        elif output_activation == "sin":
            self._normalize = True
            self.output_f, self.output_f_inv = torch.sin, torch.asin
        else:
            assert False, f"output_activation {self.output_f} not yet implimented"
        
        self.n_nodes = int(self.n_nodes)
        #activation function

        if self.reservoir_weight_dist == "uniform":
            if isinstance(self.mu, float) or isinstance(self.sigma, float):
                if self.mu != 0:
                    assert False, "to use mu and sigma hps use reservoir_weight_dist = 'normal'"
        

        self.leaking_rate = [leaking_rate, 1 - leaking_rate]
        self.leaking_rate_orig = deepcopy(self.leaking_rate)

        #https://towardsdatascience.com/logistic-regression-on-mnist-with-pytorch-b048327f8d19
        self.classification = classification

        if self.enet_alpha:
            assert self.enet_strength > 0
            assert self.enet_alpha >= 0 and self.enet_alpha <=1

        # if self.activation_function != tanh_activation and self.act_f_prime == sech2:
        #     assert False, f'your activation f is not tanh but act_f_prime is sech2'

        #cuda (gpu)
        if not device:
            self.device = torch_device("cuda" if cuda_is_available() else "cpu")
        else:
            self.device = device
        self.dtype = dtype

        # random state and default tensor arguments
        self.random_state = Generator(device=self.device).manual_seed(random_state)
        self.no_grad_ = {"requires_grad" : False}
        self.tensor_args = {"device": self.device, "generator" : self.random_state, **self.no_grad_}

        # hyper-parameters:
        torch.manual_seed(random_state)
        
        

        #Feedback
        

        #For speed up: approximate implimentation and preloaded reservoir matrices.
        

        #elastic net attributes: (default is 1, which is ridge regression for speed)
        
        
        #Reservoir layer
        self.LinRes = Linear(self.n_nodes, self.n_nodes, bias = False)

        """
        if self.classification:
            self.reg = Linear(self.n_nodes, 2)
            #self.criterion = criterion #torch.nn.CrossEntropyLoss()
        else:
            #self.criterion = MSELoss()
        """
        
        with no_grad():
            self.gen_reservoir()

        #, "requires_grad": self.track_in_grad}
        
        #scaler = "standardize"
        #if scaler == "standardize":
        #    self.scale   = self.stardardize
        #    self.descale = self.destandardize

        """TODO: additional hyper-parameters
        noise from pyesn — unlike my implimentation it happens outside the activation function. 
        TBD if this actually can improve the RC.
        self.PyESNnoise = 0.001
        self.external_noise = rand(self.n_nodes, device = self.device)
        colorz = {
          "header" : '\033[95m',
          "blue" : '\033[94m',
          'cyan' : '\033[96m',
          'green' : '\033[92m',
          'warning' : '\033[93m',
          'fail' : '\033[91m',
          'endc' : '\033[0m',
           'bold' :'\033[1m',
           "underline" : '\033[4m'
        }"""



    def __repr__(self):
        n_nodes = str(self.n_nodes)
        connect = str(self.connectivity)
        spect   = str(self.spectral_radius)

        strr = "{" + f"n_nodes : {n_nodes}, connectivity : {connect}, spectral_radius : {spect}" + "}"
        return f"EchoStateNetwork: " + strr

    def _multiple_act_f(self, X):
        new_X = X
        for i, activation_function in enumerate(self._act_fs):

            mask = self._act_mask == i
            new_X[mask] = activation_function(new_X[mask])
        return new_X

    def _multiple_act_f_prime(self, X):
        new_X = X
        for i, activation_function in enumerate(self._act_f_primes):
            mask = self._act_masks[i]
            new_X[mask] = activation_function(new_X[mask])
        return new_X


    # def plot_reservoir(self):
    #     """Plot the network weights"""
    #     sns.histplot(self.weights.cpu().numpy().view(-1,))

    # def forward(self, t, input_, current_state, output_pattern):
    #     """
    #     Arguments:
    #         t: the current timestep
    #         input_: the input vector for timestep t
    #         current_state: the current hidden state at timestep t
    #         output_pattern: the output pattern at timestep t.
    #     Returns:
    #         next_state: a torch.tensor which is the next hidden state
    #     """
    #     # generator = self.random_state, device = self.device)

    #     preactivation = self.LinIn(input_) + self.bias_ + self.LinRes(current_state)

    #     if self.feedback:
    #         preactivation += self.LinFeedback(output_pattern)
        
    #     #alternative: uniform noise
    #     #self.noise = rand(self.n_nodes, **self.tensor_args).view(-1,1) if noise else None

    #     update = self.activation_function(preactivation) # + self.PyESNnoise * (self.external_noise - 0.5)
    #     if self.noise != None:
    #         #noise_vec = torch.normal(mean = torch.zeros(self.n_nodes, device = self.device), 
    #         #                              std = torch.ones(self.n_nodes, device = self.device),
    #         #                              generator = self.random_state)* self.noise
    #         noise_vec = rand(self.n_nodes, **self.tensor_args) * self.noise
    #         update += noise_vec 
    #     next_state = self.leaking_rate[0] * update + self.leaking_rate[1] * current_state
    #     return next_state

    # def preactivation_beta(self, t, input_vector, recurrent_vec, bias, betas):
    #     return input_vector + recurrent_vec +  self.bias * self.beta[t-1,:]

    def _preactivation_vanilla(self, t, input_vector, recurrent_vec, bias): #, betas):
        return input_vector + recurrent_vec +  self.bias

    def _preactivation_noise(self, t, input_vector, recurrent_vec, bias):
        return input_vector + recurrent_vec +  self.bias + self.noise_z[:, t]

    # def activate(self, dt):
    #     alpha = self.alpha ** dt, self.alpha ** (1 - dt)


    def _train_state_feedback(self, t, X, state, y, output = False, retain_grad = False):
        """
        Arguments:
            t: the current timestep
            input_: the input vector for timestep t
            current_state: the current state at timestep t
            output_pattern: the output pattern at timestep t.
        Returns:
            next_state: a torch.tensor which is the next hidden state
        """
        try:
            input_ = torch.hstack((X,y.squeeze()))
        except:
            breakpoint()

        input_vector = self.LinIn(input_)
        recurrent_vec = self.LinRes(state)
        preactivation = self.preactivation(t, input_vector, recurrent_vec, self.bias)#, self.beta)

        #feedback_vec = self.LinFeedback(y)

        #preactivation = preactivation + feedback_vec

        update = self.activation_function(preactivation)
        next_state = self.leaking_rate[0][t-1] * update + self.leaking_rate[1][t-1] * state
        # if output:
        #     return next_state, self.LinOut(cat([X, next_state], axis = 0).view(self.n_outputs,-1))
        #next_extended_state = hstack((X, next_state)).view(1,-1)

        #breakpoint()
        #output = self.LinOut(next_extended_state)
        #assert False, f'{X.shape} {next_state.shape} {self.LinOut.weight.shape}, {output.shape} '
        
        return next_state, None#output #.view(self.n_outputs,-1))

    def _train_state_feedback_unsupervised(self, t, X, state, y, output = False, retain_grad = False):
        """
        Arguments:
            t: the current timestep
            input_: the input vector for timestep t
            current_state: the current state at timestep t
            output_pattern: the output pattern at timestep t.
        Returns:
            next_state: a torch.tensor which is the next hidden state
        """
        #try:
        input_ = torch.hstack((X,y.squeeze()))
        # except:
        #     breakpoint()

        input_vector = self.LinIn(input_)
        recurrent_vec = self.LinRes(state)
        preactivation = self.preactivation(t, input_vector, recurrent_vec, self.bias)#, self.beta)

        update = self.activation_function(preactivation)
        next_state = self.leaking_rate[0][t-1] * update + self.leaking_rate[1][t-1] * state
        
        next_extended_state = hstack((X, next_state)).view(1,-1)

        output = self.LinOut(next_extended_state)
        #assert False, f'{X.shape} {next_state.shape} {self.LinOut.weight.shape}, {output.shape} '
        
        return next_state, output

    def _train_state_vanilla(self, t, X, state, y, output = False, retain_grad = False):
        """
        Arguments:
            t: the current timestep
            input_: the input vector for timestep t
            current_state: the current state at timestep t
            output_pattern: the output pattern at timestep t.

        The function split makes sense for a speedup (remove the if statement)
        """
        #assert False
        input_vector = self.LinIn(X)
        recurrent_vec = self.LinRes(state)

        preactivation = self.preactivation(t, input_vector, recurrent_vec, self.bias)#, self.beta)

        update = self.activation_function(preactivation)
        next_state = self.leaking_rate[0][t-1] * update + self.leaking_rate[1][t-1] * state
        # if output:
        #     return next_state, self.LinOut(cat([X, next_state], axis = 0).view(self.n_outputs,-1))
        # else:
        return next_state, None

    def _train_state_vanilla_rs(self, t, X, state, y, output = False, retain_grad = False):
        """
        Arguments:
            t: the current timestep
            input_: the input vector for timestep t
            current_state: the current state at timestep t
            output_pattern: the output pattern at timestep t.

        The function split makes sense for a speedup (remove the if statement)
        """
        #assert False
        input_vector = self.LinIn(X)
        recurrent_vec = self.LinRes(state)

        preactivation = self.preactivation(t, input_vector, recurrent_vec, self.bias)#, self.beta)

        update = self.activation_function(preactivation)
        next_state = self.leaking_rate[0][t-1] * update + self.leaking_rate[1][t-1] * state
        # if output:
        #     return next_state, self.LinOut(cat([X, next_state], axis = 0).view(self.n_outputs,-1))
        # else:
        return next_state, None

    def _output_i(self, x, next_state):
        extended_state = cat([x.view(-1,), next_state], axis = 0).view(1,-1)
        return self.LinOut(extended_state)

    def forward(self, extended_states):
        """

        TODO doctstring

        if self.burn_in:
            #extended_states = extended_states[self.burn_in:]
            extended_states = torch.cat((self.extended_states[0,:].view(1,-1), self.extended_states[(self.burn_in + 1):,:]), axis = 0)
        """
        output = self.LinOut(extended_states)
        return output

    def _calc_Ndot(self, states_dot, cutoff = True):
        """
        Parameters
        ----------
        cutoff: whether or not to cutoff
        """
        #if self.burn_in and cutoff:
        #    states_dot = torch.cat((states_dot[0,:].view(1,-1), states_dot[(self.burn_in + 1):,:]), axis = 0)
        #else:
        #    states_dot = states_dot
        dN_dx = states_dot @ self.LinOut.weight.T
        return dN_dx

    def gen_discrete_weights(self, sigma, dim, connectivity):
        """
        TODO doctstring
        """
        sparcity, c = (1 - connectivity), connectivity/2
        np_weights = np.random.choice([0, -sigma, sigma],  p = [sparcity, c, c], size = dim)
        weights = torch.tensor(np_weights, **self.dev)
        return weights

    # in_weights = rand(n, m, generator = self.random_state, device = self.device, requires_grad = False)
    #                 in_weights =  (in_weights * 2) - 1
    #                 if self.input_connectivity is not None:
    #                     accept = rand(n, m, **self.tensor_args) < self.input_connectivity
    #                     in_weights *= accept

    def gen_uniform_weights(self, dim, connectivity = None):
        """
        TODO doctstring
        """
        n, m  = dim[0], dim[1]
        weights = rand(n, m, generator = self.random_state, device = self.device, requires_grad = False)
        weights =  (weights * 2) - 1
        if connectivity is not None:
            accept = rand(n, m, **self.tensor_args) < connectivity
            weights *= accept
        return weights

    def gen_reservoir(self, obs_idx = None, targ_idx = None, load_failed = None):
        """Generates random reservoir from parameters set at initialization."""
        # Initialize new random state

        #random_state = np.random.RandomState(self.random_state)

        max_tries = 1000  # Will usually finish on the first iteration
        n = self.n_nodes

        #if the size of the reservoir has changed, reload it.
        if self.reservoir:
            self.reservoir = ray.get(self.reservoir)
            if self.reservoir.n_nodes_ != self.n_nodes:
                load_failed = 1

        already_warned = False
        book_index = 0
        for i in range(max_tries):
            if i > 0:
                printc(str(i), 'fail', end = ' ')

            #only initialize the reservoir and connectivity matrix if we have to for speed in esn_cv.
            if not self.reservoir or not self.approximate_reservoir or load_failed == 1:

                self.accept = rand(self.n_nodes, self.n_nodes, **self.tensor_args) < self.connectivity
               
                if self.reservoir_weight_dist == "uniform":
                    self.weights = rand(self.n_nodes, self.n_nodes, **self.tensor_args) * 2 - 1
                elif self.reservoir_weight_dist == "normal":
                    shape_tuple = (self.n_nodes, self.n_nodes)
                    ones_tensor, zeros_tensor = torch.ones(shape_tuple, **self.dev), torch.zeros(shape_tuple, **self.dev)
                    self.weights = torch.normal(mean = ones_tensor, std = zeros_tensor) * self.sigma + self.mu
                elif self.reservoir_weight_dist == "discrete":
                    dim = (self.n_nodes, self.n_nodes)
                    self.weights = self.gen_discrete_weights(sigma = self.reservoir_sigma, dim = dim, connectivity = self.connectivity)
                    # sigma = self.reservoir_sigma
                    # sparcity, c = (1 - self.connectivity), self.connectivity/2
                    # dim = (self.n_nodes, self.n_nodes)
                    # np_weights = np.random.choice([0, -sigma, sigma],  p = [sparcity, c, c], size = dim)
                    # self.weights = torch.tensor(np_weights, **self.dev)
                else:
                    assert False, "{self.reservoir_weight_dist} reservoir_weight_distribution not yet implimented"


                self.weights *= self.accept
                #self.weights = csc_matrix(self.weights)
            else:
                #print("LOADING MATRIX", load_failed)
                try:
                    if self.approximate_reservoir:
                        self.weights = self.reservoir.get_approx_preRes(self.connectivity, i).to(self.device)
                    else:
                        self.weights = self.reservoir.reservoir_pre_weights < self.connectivity
                        self.weights *= self.reservoir.accept
                        self.weights = self.weights

                        del self.accept; del self.reservoir.reservoir_pre_weights;

                    #printc("reservoir successfully loaded (" + str(self.weights.shape) , 'green') 
                except:
                    assert 1 == 0
                    if not i:
                        printc("approx reservoir " + str(i) + " failed to load ...regenerating...", 'fail')
                    #skip to the next iteration of the loop
                    if i > self.reservoir.number_of_preloaded_sparse_sets:
                        load_failed = 1
                        printc("All preloaded reservoirs Nilpotent, generating random reservoirs, connectivity =" + str(round(self.connectivity,8)) + '...regenerating', 'fail')
                    continue
                else:
                    assert 1 == 0, "TODO, case not yet handled."

            max_eigenvalue = torch.linalg.eigvals(self.weights).abs().max() #.type(torch.float32) .sort(descending = True).values.
             
            #max_eigenvalue = self.weights.eig(eigenvectors = False)[0].abs().max()
            
            if max_eigenvalue > 0:
                break
            else: 
                if not already_warned:
                    printc("Loaded Reservoir is Nilpotent (max_eigenvalue ={}), connectivity ={}.. .regenerating".format(max_eigenvalue, round(self.connectivity,8)), 'fail')
                already_warned = True
                #if we have run out of pre-loaded reservoirs to draw from :
                if i == max_tries - 1:
                    raise ValueError('Nilpotent reservoirs are not allowed. Increase connectivity and/or number of nodes.')

        # Set spectral radius of weight matrix
        self.weights = self.weights * self.spectral_radius / max_eigenvalue
        self.weights = Parameter(self.weights, requires_grad = False)

        self.LinRes.weight = self.weights
        
        if load_failed == 1 or not self.reservoir:
            self.state = zeros(1, self.n_nodes, device=torch_device(self.device), **self.no_grad_)
        else:
            self.state = self.reservoir.state

        # Set output weights to none to indicate untrained ESN
        self.out_weights = None
             

    def set_Win(self): #inputs
        """
        Build the input weights.
        Currently only uniform implimented.

        Arguments:
            inputs:
        """
        with no_grad():
            n, m, o = self.n_nodes, self.n_inputs, self.n_outputs
            #weight
            if not self.reservoir or 'in_weights' not in dir(self.reservoir): 
                
                #print("GENERATING IN WEIGHTS")
                if self.input_weight_dist == "uniform":
                    in_weights = self.gen_uniform_weights(dim = (n,m), connectivity = self.input_connectivity)
                    # in_weights = rand(n, m, generator = self.random_state, device = self.device, requires_grad = False)
                    # in_weights =  (in_weights * 2) - 1
                    # if self.input_connectivity is not None:
                    #     accept = rand(n, m, **self.tensor_args) < self.input_connectivity
                    #     in_weights *= accept
                elif self.input_weight_dist == "discrete":

                    #input_scaling is input sigma.
                    in_weights = self.gen_discrete_weights(sigma = 1, dim = (n, m), connectivity = self.input_connectivity)

                else:
                    assert False, f'input_weight_dist {self.input_weight_dist} not implimented, try uniform or discrete.'
                
            else:
                
                in_weights = self.reservoir.in_weights #+ self.noise * self.reservoir.noise_z One possibility is to add noise here, another is after activation.
                
                ##### Later for speed re-add the feedback weights here.

                if self.feedback:
                    
                    feedback_weights = self.feedback_scaling * self.reservoir.feedback_weights
                
                    #in_weights = hstack((in_weights, feedback_weights)).view(self.n_nodes, -1)

            in_weights *= self.input_scaling

            #if there is white noise add it in (this will be much more useful later with the exponential model)
            #populate this bias matrix based on the noise

            #bias
            #uniform bias can be seen as means of normal random variables.
            if self.bias == "uniform":
                #random uniform distributed bias
                bias = bias * 2 - 1
            elif type(self.bias) in [type(1), type(1.5)]:
                bias = bias = zeros(n, 1, device = self.device, **self.no_grad_)
                bias = bias + self.bias

                #you could also add self.noise here.
            
            self.bias_ = bias
            if self.bias_.shape[1] == 1:
                self.bias_ = self.bias_.squeeze()

            if self.feedback:

                if self.feedback_weight_dist == "uniform":
                    feedback_weights = self.gen_uniform_weights(dim = (n,o), connectivity = self.feedback_connectivity) #rand(self.n_nodes, self.n_outputs, device = self.device, requires_grad = False, generator = self.random_state) * 2 - 1
                    feedback_weights *= self.feedback_scaling
                    feedback_weights = feedback_weights.view(self.n_nodes, -1)

                elif self.feedback_weight_dist == "discrete":

                    #input_scaling is input sigma.
                    feedback_weights = self.gen_discrete_weights(sigma = 1, dim = (n, o), connectivity = self.feedback_connectivity)

                else:
                    assert False, f'feedback weight dist {self.feedback_weight_dist} not implimented. Try uniform or discrete'

                
                feedback_weights = Parameter(feedback_weights, requires_grad = False)
                if self.ODE_order:
                    self.train_state = self._train_state_feedback_unsupervised
                else:
                    self.train_state = self._train_state_feedback 

            else:
                feedback_weights = None
                if self.ODE_order:
                    #self.train_state = self.train_state_feedback_unsupervised
                    self.train_state = self._train_state_vanilla_rs
                else:
                    #self.train_state = self.train_state_feedback 
                    self.train_state = self._train_state_vanilla

        if feedback_weights is not None:
            in_weights = torch.hstack((in_weights, feedback_weights))
   
        in_weights = Parameter(in_weights, requires_grad = False)
        #in_weights._name_ = "in_weights"

        return in_weights#(in_weights, feedback_weights)
    
    def check_device_cpu(self):
        """TODO: make a function that checks if a function is on the cpu and moves it there if not"""
        pass

    def display_in_weights(self):
        """TODO"""
        sns.heatmap(self.in_weights)

    def display_out_weights(self):
        """TODO"""
        sns.heatmap(self.out_weights)

    def display_res_weights(self):
        """TODO"""
        sns.heatmap(self.weights)

    def plot_states(self, n= 10):
        """TODO"""
        for i in range(n):
            plt.plot(list(range(len(self.state[:,i]))), RC.state[:,i], alpha = 0.8)

    def freeze_weights(self):
        """
        TODO doctstring
        """
        names = []
        for name, param in zip(self.state_dict().keys(), self.parameters()):
            names.append(name)
            if name != "LinOut.weight":
                param.requires_grad_(False)
            else:
                self.LinOut.weight.requires_grad_(True)
                self.LinOut.bias.requires_grad_(True)
                assert self.LinOut.weight.requires_grad
            #print('param:', name,  params.requires_grad)

    def _train_states_supervised(self, X, y, states, calc_grads = True, outputs = True):
        """
        TODO doctstring
        """
        #self.state_grads = []
        #self.state_list = []

        with no_grad():


            for t in range(1, X.shape[0]):
                #print("super")
                # self.state[t, :] = self.forward(t, input_ = X[t, :].T,
                #                                        current_state = self.state[t-1,:], 
                #                                        output_pattern = y[t-1]).squeeze()
                input_t =  X[t, :].T
                state_t, _ = self.train_state(t, X = input_t, state = states[t-1,:], y = y[t-1,:])

                states = cat([states, state_t.view(-1, self.n_nodes)], axis = 0)
            # for t in range(0, X.shape[0]):
            #     input_t =  X[t, :].T
            #     state_t, _ = self.train_state(t, X = input_t,
            #                               state = states[t,:], 
            #                               y = y[t,:],
            #                               output = False)


            #     states = cat([states, state_t.view(-1, self.n_nodes)], axis = 0)

        return states

    def _train_states_unsupervised(self, X, y, states, calc_grads = True, outputs = True):
        """
        TODO doctstring
        """
        #self.state_grads = []
        #self.state_list = []
        with no_grad():

            #output_prev = y[0]

            for t in range(1, X.shape[0]):
                input_t =  X[t, :].T
                #assert False,f'y {y.shape} input_t {input_t.shape}'
                state_t, output_t = self.train_state(t, X = input_t,
                                                     state = states[t-1,:], 
                                                     y = y[t-1,:],
                                                     output = False)


                states = cat([states, state_t.view(-1, self.n_nodes)], axis = 0)
                #output_prev = output_t

        #outputs = self.LinOut(states)
        return states

    def _extend_X(self, X, random_sampling):
        """
        TODO doctstring
        """
        if self.burn_in and self.ODE_order and not random_sampling:
            start = float(X[0] - self.burn_in * self.dt)
            neg_X = torch.linspace(start, float(X[0]), self.burn_in).view(-1, 1).to(self.device)
            X_extended = torch.cat([neg_X, X], axis = 0)
        elif self.burn_in and self.ODE_order and random_sampling:
            dt_mu = torch.mean(self.dt)
            start = float(X[0] - self.burn_in * dt_mu)
            neg_X = torch.linspace(start, float(X[0]), self.burn_in).view(-1, 1).to(self.device)
            X_extended = torch.cat([neg_X, X], axis = 0)
            assert False, "implementation incomplete"

            alpha = self.leaking_rate_orig**dt_mu
            self.leaking_rate_new = (1- alpha), alpha
        else:
            X_extended = X
        return X_extended

    def _calc_bias(self, weights):
        """
        TODO doctstring
        """
        return self._y_means - self._x_means @ weights

    def _solve_supervised(self, y, return_states, SCALE):
        """

        TODO doctstring

        if the esn has data, this fork.
        """
        train_x = self.extended_states
        if not self.random_sampling:
            n_time_points  = y.shape[0]
            bool_mask = torch.rand(n_time_points) <= self.solve_sample_prop

            
            # ones_row = ones( train_x.shape[0], 1, **self.dev)
            # train_x = hstack((ones_row, train_x))

            train_x = train_x[bool_mask]
            y = y[bool_mask]
            

        self._x_means = torch.mean(train_x, axis = 0)
        self._y_means = torch.mean(y, axis = 0)
        

        
        train_x = train_x - self._x_means

        biases = []
        weights = []
        
        ridge_x = matmul(train_x.T, train_x) + self.regularization * eye(train_x.shape[1], **self.dev)
        
        try:
            ridge_x_inv = pinverse(ridge_x)
        except:
            ridge_x_inv = torch.inverse(ridge_x)


        for i in range(y.shape[1]):
            train_y = y[:, i].view(-1,1)
            train_y = train_y

   
            ridge_y = matmul(train_x.T, train_y)
            weight = ridge_x_inv @ ridge_y


            #intercept line, pyds inspired
            #self.intercept_ = self._y_mean - self._x_means @ self.coef_
        
            bias = self._y_means[i] - self._x_means @ weight
            #bias = self._y_means[i] - self._x_means @ weight

            biases.append(bias)
            weights.append(weight)

        
        self.LinOut.weight = Parameter(hstack(weights).T)
        self.LinOut.bias = Parameter(hstack(biases).view(-1, self.n_outputs))

        # self.N = self.LinOut(self.extended_states)
                
        # # Store last y value as starting value for predictions
        # self.lastoutput = y[-1, :]

        # if self.burn_in:
        #     self.N = self.N[self.burn_in:,:]
        #     self.N = self.N.view(-1, self.n_outputs)
        #     self.X = self.X[self.burn_in:]
            
        # # Return all data for computation or visualization purposes (Note: these are normalized)
        # if return_states:
        #     return extended_states, (y[1:,:] if self.feedback else y), self.burn_in
        # else:
        #     print("burn in", self.burn_in, "ex", self.extended_states.shape, "linout", self.LinOut.weight.shape)
        #     #self.yfit = self.LinOut(self.extended_states)
        #     if SCALE:   
        #         self.yfit = self._output_stds * self.N + self._output_means
        #     if not SCALE:
        #         assert False
        #     return self.yfit
        if return_states:
            return self.extended_states, (y[1:,:] if self.feedback else y), burn_in
        else:
            yfit_norm = self.LinOut(self.extended_states) #self.LinOut.weight.cpu()@self.extended_states.T.cpu() + self.LinOut.bias.cpu()
            #yfit = self._output_stds.cpu()* (yfit_norm)+ self._output_means.cpu()

            self.yfit = self._descale(outputs = yfit_norm, normalize = self._normalize).view(-1, self.n_outputs).detach().numpy()
            return self.yfit

    # def fit_unsupervised(self):
    #     """
    #     if the esn is unsupervised, this fork.
    #     """
    #     pass

    # def fit_hamiltonian(self):
    #     """
    #     for the new project
    #     """

    def _center_H(self, inputs = None, outputs = None, keep = False):
        """

        TODO doctstring

        INSTRUCTIONS:
        1. assign `_x_means` to self, along the axis such that 
           the numbers of means matches the number of features (2)
        2. assign `_y_mean` to self (y.mean())
        3. subtract _x_means from X and assign it to X_centered
        4. subtract _y_mean from y and assign it to y_centered
        """
        if inputs is not None:
            X = inputs

            if keep:
                self._x_means = X.mean(axis=0)
                self._x_stds = X.std(axis = 0)

            X_centered = (X - self._x_means)/self._x_stds
            return X_centered
        if outputs is not None:
            y = outputs

            if keep:
                self._y_means = y.mean(axis = 0)

            y_centered = y - self._y_means #(y - y_means)/y_stds

            return y_centered

    def assign_random_sampling(self, X):
        """
        TODO doctstring
        """
        x1, x2 = X[1:], X[:-1]
        self.dt = x1-x2
        

        alpha = self.leaking_rate[0]**self.dt
        #breakpoint()

        
        self.leaking_rate =  alpha, (1- alpha)

        self.alpha = self.leaking_rate[0] / self.dt
        self.alpha = self.alpha.view(-1,1)

    def assign_const_leaking_rate(self, X):
        """
        TODO doctstring
        """
        #self.leaking_rate_orig = self.leaking_rate.copy()

        ones= torch.ones((X.shape[0], 1)).to(self.device)
        try:
            self.leaking_rate[0] = self.leaking_rate_orig[0] * ones
            self.leaking_rate[1] = self.leaking_rate_orig[1] * ones
        except:
            self.leaking_rate[0] = float(self.leaking_rate_orig[0][0]) * ones
            self.leaking_rate[1] = float(self.leaking_rate_orig[1][0]) * ones
        


    def fit(self, y = None, X=None, burn_in=0, input_weight=None, verbose = False , 
            learning_rate = 0.005, return_states = False, criterion =  MSELoss(), 
            optimizer = None, out_weights = None, ODE_order = None, SOLVE = True,
            reparam_f = None, init_conditions = None, force = None, #nl_f = None, 
            ode_coefs = None, train_score = False, ODE_criterion = None, 
            preloaded_states_dict = None, q = None, eq_system = None, nl = False,
            backprop_f = None, epochs = None, hamiltonian = None,
            n_inputs = None, n_outputs = None, random_sampling = False, sample_timepoints = 100): #beta = None, 
        # if verbose:
        #     if nl:
        #         print("nonlinear!")
        #     else:
        #         print("linear")


        """

        TODO doctstring

        NLLLoss(),
        Train the network.
        
        Arguments: TODO
            y: response matrix
            x: observer matrix
            burn in: obvious
            input_weight : ???
            learning_rate: 
            verbose:
        """
        
        with no_grad():
            
            non_assign_keys = ["X", "self", "y"]
            for key, val in locals().items():
                if key not in non_assign_keys:
                    setattr(self, key, val)

            # if random_sampling and not self.ODE_order:
            #     assert False, "random sampling not implimented in supervised case"


            #self.reparam = reparam_f

            
            
            
            self.track_in_grad = False #track_in_grad

            if self.noise is not None:
                self.preactivation = self._preactivation_noise
            else:
                self.preactivation = self._preactivation_vanilla

            ########################### beta arguments are currently silenced #################
            #self.beta = beta
            # if beta is None:
            #     self.preactivation = self.preactivation_vanilla 
            # else:
            #     self.preactivation = self.preactivation_beta
            ########################### beta arguments are currently silenced #################
            

            #assert len(init_conditions) == ODE_order
            
            #SCALE = True
            if not self.ODE_order:
                SCALE = True
            else:
                SCALE = False
            
            #ensure that y is a 2-dimensional tensor with pre-specified arguments.
            if self.ODE_order: 

                self.train_states = self._train_states_unsupervised
                
                assert init_conditions
                if len(init_conditions) > 1:
                    if type(init_conditions[1]) == list or type(init_conditions[1]) == np.ndarray:
                        #weird randomization condition
                        multiple_ICs = self.multiple_ICs = True
                        #print('randomizing init conds')
                        for i in range(len(init_conditions)):
                            init_conditions[i] = np.random.uniform(low = init_conditions[i][0], high = init_conditions[i][1])
                        init_conditions[0] = [init_conditions[i]]
                    elif type(init_conditions[0]) == list or type(init_conditions[0]) == np.ndarray:
                        multiple_ICs = self.multiple_ICs = True
                    else:
                        multiple_ICs = self.multiple_ICs = False
                elif type(init_conditions[0]) == list or type(init_conditions[0]) == np.ndarray:
                    multiple_ICs = self.multiple_ICs = True

                elif type(init_conditions[0]) in [float,  int, np.float64, np.float32, np.int32, np.float64]:
                    multiple_ICs = self.multiple_ICs = False
                else:
                    assert False, f'malformed ICs, either use a list, a float or an integer'
                init_conds = init_conditions
                
                if self.dt != None:
                    

                    start, stop = float(X[0]), float(X[-1])

                    if not random_sampling:
                        self.alpha = self.leaking_rate[0] / self.dt
                        nsteps = int((stop - start) / self.dt)
                        X = torch.linspace(start, stop, steps = nsteps, requires_grad=False).view(-1, 1).to(self.device)
                    else:
                        X = torch.rand(sample_timepoints + 2) * (stop - start) + start

                        X = X.sort().values
                        x1, x2 = X[1:], X[:-1]
                        self.dt = x1-x2
                        
                        #if not hasattr(self, "leaking_rate_orig"):
                            
                        alpha = self.leaking_rate[0]**self.dt
                        self.leaking_rate_orig = deepcopy(self.leaking_rate)
                        self.leaking_rate = (1- alpha), alpha
                        self.alpha = self.leaking_rate[0] / self.dt
                        self.alpha = self.alpha.view(-1,1)
                    
                        
                        
                        X = X[:-1].reshape(-1,1)
                elif type(X) == type([]) and len(X) == 3:
                    x0, xf, nsteps = X #6*np.pi, 100
                    X = torch.linspace(x0, xf, steps = nsteps, requires_grad=False).view(-1, 1).to(self.device)
                else:
                    assert False, "Please input start, stop, dt"

                if y is None:
                    y =torch.ones((X.shape[0], self.n_outputs), **self.dev)

                
                
            else:
                #ensure that X is a two dimensional tensor, or if X is None declare a tensor.

                X = check_x(X, y, self.dev, supervised = True)
                X.requires_grad_(False)
                y = check_y(y, tensor_args = self.dev) 
                



                if random_sampling:
                    #X = torch.rand(sample_timepoints + 2)
                    idx = np.random.choice(range(X.shape[0]),sample_timepoints, replace = False)
                    idx.sort()

                    X = X[idx]
                    y = y[idx]

                    idx = torch.tensor(idx, **self.dev)


                    self.assign_random_sampling(idx)
                    assert False

                    #self.leaking_rate_orig = [new_predict_lr, 1-new_predict_lr]
                    #X = X[:-1]
                else:
                    self.assign_const_leaking_rate(X)
                
                
                    

                self.y_tr = y
                
                if SCALE:
                    y = self._scale(outputs=y, keep=True, normalize = self._normalize)    
                y.requires_grad_(False)

                self.lastoutput = y[ -1, :]
                self.multiple_ICs = multiple_ICs = False
                self.train_states = self._train_states_supervised

            self.unscaled_X = Parameter(X, requires_grad = self.track_in_grad)

            if self.unscaled_X.device != self.device:
                self.unscaled_X.data = self.unscaled_X.data.to(self.device)


            if self.unscaled_X.std() != 0:
                self.X = self.unscaled_X#.clone()

                if SCALE:
                    self.X.data = self._scale(inputs = self.unscaled_X, keep = True, normalize = False)#.clone()
            else:
                self._input_stds = None
                self._input_means = None
                self.X = self.unscaled_X


            ##at this point you can take a random sample? now it must happen sooner.


            self.X_extended = self._extend_X(self.X, self.random_sampling)
            if self.ODE_order and self.burn_in:
                x1, x2 = X[1:], X[:-1]
                
                y_extended = torch.ones((self.X_extended.shape[0], y.shape[1])).to(self.device)
            else:
                y_extended = y

            # if self.betas is None:
            #     self.betas = torch.ones_like(X[:,0].view(-1,1))

            start_index = 1 if self.feedback else 0 
            rows = X.shape[0] - start_index
            
            self.n_inputs = self.X.shape[1] 
            if not self.n_outputs and not self.ODE_order:
                self.n_outputs = y.shape[1]
            else:
                if not self.n_outputs:
                    assert False, 'you must enter n_outputs'

            if self.noise is not None:
                self.noise_z = normal(0, 1, size = (self.n_nodes, self.X_extended.shape[0]), **self.dev) * self.noise
            
            self.lastinput = self.X[-1, :]
            
            start_index = 1 if self.feedback else 0 
            rows = X.shape[0] - start_index

            
            combined_weights = True

            if not self.LinOut:

                self.LinOut = Linear(self.n_nodes+1, self.n_outputs)

                if combined_weights:
                    self.LinIn = Linear(2*self.n_inputs, self.n_nodes,  bias = False)
                    #self.LinFeedback = Linear(self.n_inputs, self.n_nodes, bias = False)
                    #self.LinFeedback = Linear(self.n_inputs, self.n_nodes, bias = False)

                else:
                    self.LinIn = Linear(self.n_inputs, self.n_nodes,  bias = False)
                    self.LinFeedback = Linear(self.n_inputs, self.n_nodes, bias = False)

                #self.LinIn = Linear(self.n_inputs, self.n_nodes,  bias = False)
                
                #self.LinIn.weight, self.LinFeedback.weight = self.set_Win()
                self.LinIn.weight = self.set_Win()


                # assert isinstance(n_inputs, int), "you must enter n_inputs. This is the number of input time series (int)"
                # assert isinstance(n_outputs, int), "you must enter n_outputs. This is the number of output time series (int)"

            #self.LinOutDE = Linear(self.n_nodes + 1, self.n_outputs)

            ################################################################################################
            #+++++++++++++++++++++++++++         FORWARD PASS AND SOLVE             ++++++++++++++++++++++++
            ################################################################################################
            with torch.set_grad_enabled(self.track_in_grad):
                self.freeze_weights()
                if out_weights:
                    #self.SOLVE = SOLVE = False
                    self.LinOut.weight =  Parameter(out_weights["weights"].to(self.device))
                    self.LinOut.bias = Parameter(out_weights["bias"].to(self.device)) 
                else:
                    try:
                        assert self.LinOut.weight.device == self.device
                    except:
                        self.LinOut.weight = Parameter(self.LinOut.weight.to(self.device))
                        self.LinOut.bias = Parameter(self.LinOut.bias.to(self.device))

                # CUSTOM_AUTOGRAD_F = False
                # if CUSTOM_AUTOGRAD_F:
                #     #for more information on custom pytorch autograd functions see the following link:
                #     #https://pytorch.org/tutorials/beginner/examples_autograd/two_layer_net_custom_function.html
                #     recurrence = Recurrence.apply

                #     self.states, self.states_dot, states_dot = recurrence(self.states, self, self.X_extended, y)
                # else:

                

                self.states = zeros((1, self.n_nodes), **self.dev)
                

                #drop the first state and burned states
                
                self.states = self.train_states(self.X_extended, y_extended, self.states)
                    
                if self.burn_in:
                    self.X.data = self.X.data[burn_in:]
                    self.states = self.states[self.burn_in:]

                # calculate hidden state derivatives
                if self.ODE_order:
                    if self.feedback:
                        input_ = torch.hstack((self.X, y))
                        updates = self.LinIn(input_) + self.bias + self.LinRes(self.states)
                    else:
                        updates = self.LinIn(self.X) + self.bias + self.LinRes(self.states)

                    self.states_dot = - self.alpha * self.states + self.alpha * self.activation_function(updates.T).T
                    # if self.ODE_order == 2:
                    #     self.states_dot2 = - self.alpha * self.states_dot + self.alpha * self.act_f_prime(updates) * (self.LinIn.weight.T + self.bias + self.LinRes(self.states_dot))
                    #     self.states_dot2 = torch.cat((zeros_like(self.X), self.states_dot2), axis = 1)

                    self.states_dot = torch.cat((ones_like(self.X), self.states_dot), axis = 1)

                    self.G = G = self.reparam_f(self.X)#, order = self.ODE_order)

                #append columns for the data:
                self.extended_states = torch.cat((self.X, self.states), axis = 1)
                #self.extended_states = hstack((self.X, self.states))

                self.laststate = self.states[-1, :]

                del self.states

                #add rows corresponding to bias to the states 
                self.sb = states_with_bias = torch.cat((ones_like(self.extended_states[:,0].view(-1,1)), self.extended_states), axis = 1)

                if self.ODE_order:
                    self.sb1 = states_dot_with_bias = torch.cat((zeros_like(self.states_dot[:,0].view(-1,1)), self.states_dot), axis = 1)

                    # do the same for the second derivatives
                    # if self.ODE_order == 2:
                    #     self.sb2 = states_dot2_with_bias = torch.cat((zeros_like(self.states_dot2[:,0].view(-1,1)), self.states_dot2), axis = 1)
                    g, g_dot = G
                    self.g = g

                    self.init_conds = init_conditions.copy()
                    ode_coefs = convert_ode_coefs(self.ode_coefs, self.X)



                #self.laststate = self.extended_states[-1, 1:]

                if self.ODE_order:
                    self.force = force
                    self.force_t = self.force(self.X)
                
                with no_grad():

                    # if not SOLVE and not self.ODE_order:
                    #     train_x = self.extended_states
                    #     ones_row = ones( train_x.shape[0], 1, **self.dev)
                    #     train_x = hstack((ones_row, train_x))

                    if SOLVE: #and not out_weights:
                        #print("SOLVING!")

                        #include everything after burn_in 
                        if not self.ODE_order:
                            return self._solve_supervised(y, return_states, SCALE)

                        bias = None

                        #print("ridge regularizing")
                        with torch.set_grad_enabled(False):

                            if self.ODE_order:
                                if multiple_ICs:
                                    #only implemented for first order

                                    try:
                                        self.As = As = [y0 * g.pow(0) for y0 in self.init_conds[0]]
                                    except:
                                        assert False, f'{self.init_conds}, {self.init_conds}'
                                    init_cond_list = self.init_conds
                                    #init_cond_list = [[y0, self.init_conds[1]] for y0 in self.init_conds[0]]
                                     
                                else:
                                    A = self.A = [init_conds[i] * g.pow(i) for i in range(self.ODE_order)] 


                                t = self.X


                                # if self.Hargun_changes:
                                #     H, H_dot = self.extended_states, self.states_dot #
                                # else:
                                H, H_dot = states_with_bias, states_dot_with_bias
                                
                                
                                self.gH = gH = g * H

                                self.gH_mu = self.gH.mean()
                                self.gH_dot = gH_dot =  g_dot * H +  g * H_dot

                                if eq_system:
                                    
                                    S, S_dot = self.gH, gH_dot

                                    if multiple_ICs:
                                        p0 = self.init_conds[1]
                                        ones_vec = torch.ones_like(X).T 
                                        p0_vec = ones_vec * p0
                                        self.Cxs = Cxs = []
                                        self.Cps = Cps = []
                                        for y0 in self.init_conds[0]:
                                            #print("y0", y0)
                                            y0_vec = ones_vec * y0
                                            Cx = -y0_vec @ S + p0_vec @ S_dot
                                            Cp = -y0_vec @ S_dot - p0_vec @ S
                                            Cxs.append(Cx)
                                            Cps.append(Cp)

                                    else:
                                        y0, p0 = self.init_conds
                                        ones_vec = torch.ones_like(X).T 

                                        y0_vec = ones_vec * y0
                                        p0_vec = ones_vec * p0

                                        self.Cx = Cx = -y0_vec @ S + p0_vec @ S_dot
                                        self.Cp = Cp = -y0_vec @ S_dot - p0_vec @ S

                                    sigma1 = S.T @ S + S_dot.T @ S_dot

                                    self.Sigma=Sigma = sigma1 + self.regularization * eye(sigma1.shape[1], **self.dev)

                                    self.Delta=Delta = S.T @ S_dot - S_dot.T @ S

                                    #try:
                                    delta_inv = pinverse(Delta)
                                    sigma_inv = pinverse(Sigma)
                                    D_H = Sigma @ delta_inv + Delta @ sigma_inv
                                    self.Lam=Lam = pinverse(D_H)
                                    
                                    #assert False, f'{Cx.shape}, {Cp.shape} {Lam.shape} {Sigma.shape} {Delta.shape}'
                                    if not multiple_ICs:

                                        self.Wy = Wy =  Lam.T @ (Cx @ delta_inv  + Cp @  sigma_inv).T/len(self.X)
                                        self.Wp = Wp =  Lam.T @ (Cp @ delta_inv  - Cx @  sigma_inv).T/len(self.X)
                                        
                                        self.weight = weight = torch.cat((Wy.view(-1,1), Wp.view(-1,1)), axis = 1)

                                        bias = weight[0]
                                        weight = weight[1:].view(self.n_outputs, -1)

                                    else:
                                        self.weights_list = []
                                        self.biases_list = []
                                        Wys, Wps =  [], []
                                        for i in range(len(Cps)):
                                            Cx, Cp, nX = Cxs[i], Cps[i], len(self.X)
                                            Wy = Lam.T @ (Cx @ delta_inv  + Cp @  sigma_inv).T/nX
                                            Wp = Lam.T @ (Cp @ delta_inv  - Cx @  sigma_inv).T/nX
                                            Wys.append(Wy)
                                            Wps.append(Wp)

                                            weight = torch.cat((Wy.view(-1,1), Wp.view(-1,1)), axis = 1)

                                            bias = weight[0]
                                            weight = weight[1:].view(self.n_outputs, -1)

                                            self.weights_list.append(weight)
                                            self.biases_list.append(bias)
                                        weights = self.weights_list
                                        biases = self.biases_list
                                    
                                else:

                                
                                    #if self.ODE_order == 1:

                                    #oscillator
                                    #########################################################
                                    
                                    #########################################################

                                    #nonlinear:
                                    #########################################################
                                    if multiple_ICs:
                                        if nl:
                                            self.y0s = y0s  = init_conds[0]
                                            p = self.ode_coefs[0];
                                            self.D_As = D_As = [y0*(p+y0*self.q) - self.force_t for y0 in y0s]
                                        else:
                                            D_As = [A*ode_coefs[0]- self.force_t for A in As]
                                    else:

                                        if nl:
                                            y0  = init_conds[0]
                                            p = self.ode_coefs[0];
                                            #q=0.5
                                            self.D_A = D_A =  y0*(p+y0*self.q) - self.force_t
                                        else:
                                            ######x###################################################
                                            #population:
                                            self.D_A = D_A = A[0] * ode_coefs[0] - self.force_t   
                                    
                                        
                                    # D_A = A[0] * ode_coefs[0] - force(t)                                  
                                    """
                                    try:
                                        D_A = A * ode_coefs[0] - force(t)
                                    except:
                                        assert False, f'{ode_coefs[0].shape} {self.X.shape} {A[0].shape} {force(t).shape}'
                                    """
                                    # elif self.ODE_order == 2:
                                    #     w= self.ode_coefs[0]
                                    #     y0, v0 = init_conds[0], init_conds[1]
                                    #     D_A = v0 *(g_dot2 + w**2*g )+ w**2 * y0 -force(t)

                                    if nl:                                
                                        if not multiple_ICs:
                                            self.DH = DH =  gH_dot + p*gH + 2*self.q*y0*gH 
                                        else:
                                            self.DHs = DHs = [gH_dot + p*gH + 2*self.q*y0*gH for y0 in y0s]
                                    else:
                                        #assert False
                                        self.DH = DH = ode_coefs[0] * gH + ode_coefs[1] * gH_dot   

                                    # if self.ODE_order == 2:

                                    #     H_dot2 = states_dot2_with_bias
                                    #     DH = 2 * H *(g_dot ** 2 + g*g_dot2) + g*(4*g_dot*H_dot + g*H_dot2)  + w**2 * g**2*H
                                    #     term1 = 2*H*g_dot**2
                                    #     term2 = 2*g*(2*g_dot*H_dot + H*g_dot2)
                                    #     term3 = g**2*(w**2*H + H_dot2)
                                    #     DH = term1 +  term2 + term3
                                    #there will always be the same number of initial conditions as the order of the equation.
                                    #D_A = G[0] + torch.sum([ G[i + 1] * condition for i, condition in enumerate(initial_conditions)])
                                    if not nl:
                                        #################
                                        DH = DH[:, 1:]
                                        #DH = self._center_H(inputs = DH, keep = True)


                                        #self.extended_states = self.extended_states - self.extended_states.mean(axis = 0)
                                        #################
                                        DH1 = DH.T @ DH

                                        #xx, _ = self._center_data(DH, D_As[0])

                                        #if nl:
                                        #    DH1 = DH1 -2 * self.q* D_A.T * gH.T @ gH
                                        
                                        self.DH1 = DH1 = DH1 + self.regularization * eye(DH1.shape[1], **self.dev)
                                        DHinv = pinverse(DH1)
                                        self.DH2 = DH2 = DHinv @ DH.T
                                        if not multiple_ICs:
                                            weight = matmul(-DH2, D_A)

                                            bias = weight[0]
                                            weight = weight[1:]
                                        else:
                                            weights, biases = [], []

                                            DH = self._center_H(inputs = -DH, keep = True)

                                            for i, D_A in enumerate(D_As):


                                                _  = self._center_H(outputs = D_A, keep = True)
                                                weight = matmul(-DH2, D_A)
                                                bias = self._calc_bias(weight)
                                                biases.append(bias)
                                                weights.append(weight)

                                            self.biases_list = biases
                                            self.weights_list = weights

                                    else:
                                        ################################
                                        DH1s = [DH.T @ DH for DH in DHs]

                                        #gH_sq = gH.T @ gH 
                                        #DH1p2s = [-2 * self.q* D_A.T * gH_sq for D_A in D_As]
                                        nl_corrections = [2 * self.q* D_A.T * gH.T @ gH  for D_A in D_As]
                                        #self.DH1 -2 * self.q* D_A.T * gH.T @ gH

                                        self.DH1s = DH1s = [DH1s[i] - 0 for i, correction in enumerate(nl_corrections)]
                                        
                                        #DH1 = DH1 + self.regularization * eye(DH1.shape[1], **self.dev)

                                        DHinvs = [pinverse(DH1 + self.regularization * eye(DH1s[0].shape[1], **self.dev))for DH1 in DH1s]
                                        self.DH2s = DH2s = [DHinv @ DHs[i].T for i, DHinv in enumerate(DHinvs)]

                                        weights, biases = [], []



                                        for i in range(len(D_As)):
                                            DH2 = DH2s[i]
                                            D_A = D_As[i]
                                            init_weight = matmul(-DH2, D_A)

                                            biases.append(init_weight[0])
                                            weights.append(init_weight[1:])
                                        #assert False
                                        self.biases_list = biases
                                        self.weights_list = weights

                                    
                                        


                        #     elif not self.ODE_order:
                        #         ones_row = ones( train_x.shape[0], 1, **self.dev)
                            
                        #         ridge_x = matmul(train_x.T, train_x) + \
                        #                            self.regularization * eye(train_x.shape[1], **self.dev)

                        #         ridge_y = matmul(train_x.T, train_y)

                        #         ridge_x_inv = pinverse(ridge_x)
                        #         weight = ridge_x_inv @ ridge_y

                        #         bias = weight[0]
                        #         weight = weight[1:]

                        # if not multiple_ICs:
                        #     self.LinOut.weight = Parameter(weight.view(self.n_outputs, -1))
                        #     self.LinOut.bias = Parameter(bias.view(1, self.n_outputs))

            if multiple_ICs:
                if not backprop_f:
                    init_conds_clone = init_conditions.copy()
                    ys = []
                    ydots = []
                    scores = []
                    last_outputs = []
                    #init_conds_clone = init_conds.copy()
                    for i, weight in enumerate(self.weights_list):
                        #print("w", i)
                        self.LinOut.weight = Parameter(weight.view(self.n_outputs, -1))
                        self.LinOut.bias = Parameter(biases[i].view(1, self.n_outputs))
                        if SOLVE:
                            self.LinOut.weight.requires_grad_(False)
                            self.LinOut.bias.requires_grad_(False)
                        

                        self.init_conds[0] = float(init_conds_clone[0][i])

                        N = self.LinOut(self.extended_states)
                        N_dot = self._calc_Ndot(self.states_dot, cutoff = False)
                        yfit = g*N
                        
                        if not eq_system:
                            yfit[:, 0] = yfit[:,0] + init_conds[0][i]
                        else:
                            
                            yfit[:, 0] = yfit[:,0] + init_conds[0][i]
                            for j, cond in enumerate(1, init_conds):
                                yfit[:, j] = yfit[:,j] + cond
                        
                        if train_score:
                            ydot = g_dot * N +  g * N_dot
                            ydots.append(ydot)
                            score = ODE_criterion(X, yfit.data, ydot.data, self.LinOut.weight.data, 
                                                    ode_coefs = ode_coefs, init_conds = init_cond_list, 
                                                    enet_strength = self.enet_strength, enet_alpha = self.enet_alpha,
                                                    force_t = self.force_t)
                            scores.append(score)

                        last_outputs.append(y[-1, :])
                        ys.append(yfit)

                    self.lastoutput = y[-1, :]#.clone()
                    self.init_conds = init_conditions
                    if train_score:
                        return {"scores" : scores, 
                                "weights": weights, 
                                "biases" : biases,
                                "ys"     : ys,
                                "ydots"  : ydots}
                    else:
                        return ys, ydots
                else:

                    # if self.parallel_backprop:

                    # results = ray.get([execute_objective.remote(parallel_args_id, cv_samples, parameter_lst[i], i) for i in range(num_processes)])
                    # else:
                    gd_weights = []
                    gd_biases = []
                    ys = []
                    ydots =[]
                    scores = []
                    Ls = []
                    init_conds_clone = init_conditions.copy()
                    if not SOLVE:
                        orig_weights = self.LinOut.weight#.clone()
                        orig_bias = self.LinOut.bias#.clone()

                    self.parallel_backprop = True

                    weight_dicts = []
                    if self.parallel_backprop:
                        new_out_W = Linear(self.LinOut.weight.shape[1], self.n_outputs)

                        if SOLVE:
                            new_out_W.weight = Parameter(self.weights_list[i].view(self.n_outputs, -1)).requires_grad_(True)
                            new_out_W.bias = Parameter(self.biases_list[i].view(1, self.n_outputs)).requires_grad_(True)
                        else:
                            try:

                                new_out_W.weight = Parameter(orig_weights.view(self.n_outputs, -1)).requires_grad_(True)
                                new_out_W.bias = Parameter(orig_bias.view(1, self.n_outputs)).requires_grad_(True)
                            except:
                                new_out_W.weight = Parameter(orig_weights.reshape(self.n_outputs, -1)).requires_grad_(True)
                                new_out_W.bias = Parameter(orig_bias.reshape(1, self.n_outputs)).requires_grad_(True)



                        data2save = {#"rc" : self, 
                                     "custom_loss" : self.ODE_criterion, 
                                     "epochs" : self.epochs,
                                     "New_X" : self.extended_states.detach(),
                                     "states_dot": self.states_dot.detach().requires_grad_(False),
                                     #"orig_bias" : orig_bias,
                                     #"orig_weights" : orig_weights,
                                     "out_W" : new_out_W,
                                     "force_t" : self.force_t,
                                     "criterion" : torch.nn.MSELoss(),
                                     #"optimizer" : optim.Adam(      self.parameters(), lr = 0.05),
                                     "t"  : self.X,
                                     "G" : self.G,
                                     "gamma" : self.gamma,
                                     "gamma_cyclic" : self.gamma_cyclic,
                                     #"parameters" : self.parameters(),
                                     "spikethreshold": self.spikethreshold,
                                     "ode_coefs" : self.ode_coefs,
                                     "enet_alpha" : self.enet_alpha,
                                     "enet_strength" : self.enet_strength,
                                     "init_conds" : self.init_conds
                                     }

                        self_id = ray.put(data2save)

                        weight_dicts = ray.get([execute_backprop.remote(self_id, y0) for y0 in init_conds_clone[0]])
                    
                    else:
                        for i, y0 in enumerate(init_conds_clone[0]):
                            #print("w", i)
                            if SOLVE:
                                self.LinOut.weight = Parameter(self.weights_list[i].view(self.n_outputs, -1)).requires_grad_(True)
                                self.LinOut.bias = Parameter(self.biases_list[i].view(1, self.n_outputs)).requires_grad_(True)
                            else:
                                self.LinOut.weight = Parameter(orig_weights.view(self.n_outputs, -1))
                                self.LinOut.bias = Parameter(orig_bias.view(1, self.n_outputs))
                            self.init_conds[0] = float(y0)
                            #print(self.init_conds[0])
                            #breakpoint()
                            with torch.enable_grad():
                                weight_dict = backprop_f(self, force_t = self.force_t, custom_loss = ODE_criterion, epochs = epochs)
                            weight_dicts.append(weight_dict)
                    last_outputs = []
                    for weight_dict in weight_dicts:
                        score=weight_dict["best_score"]
                        y = weight_dict["y"]
                        ydot = weight_dict["ydot"]
                        loss, gd_weight, gd_bias = weight_dict["loss"]["loss_history"], weight_dict["weights"],  weight_dict["bias"]
                        scores.append(score)
                        ys.append(y)
                        ydots.append(ydot)
                        gd_weights.append(gd_weight)
                        gd_biases.append(gd_bias)
                        Ls.append(loss)
                        last_outputs.append(y[-1, :])

                    self.init_conds = init_conditions


                    self.lastoutput = y[-1, :]

                    self.weights_list = gd_weights
                    self.biases_list = gd_biases
                    if train_score:
                        return {"scores" : scores, 
                                "weights": gd_weights, 
                                "biases" : gd_biases,
                                "ys"     : ys,
                                "ydots"  : ydots,
                                "losses" : Ls}
                    else:
                        return ys, ydots

                        #{"weights": best_weight, "bias" : best_bias, "loss" : backprop_args, "ydot" : ydot, "y" : y}


            else:

                # self.biases_list = [bias]
                # self.weights_list = [weight]

                self.LinOut.weight = Parameter(weight.view(self.n_outputs, -1))
                self.LinOut.bias = Parameter(bias.view(1, self.n_outputs))

                self.N = self.LinOut(self.extended_states)
                
                # Store last y value as starting value for predictions
                self.lastoutput = y[-1, :]

                if self.ODE_order >= 1:
                    #calc Ndot just uses the weights
                    #self.states_dot @ self.LinOut.weight
                    # if not SOLVE:
                    #     ones_row = ones( X.shape[0], 1, **self.dev)
                    #     #print(f'adjusting extended_states, shape before: {self.extended_states.shape}')
                    #     self.extended_states = hstack((ones_row, self.extended_states))
                    #     #print(f'adjusting extended_states, shape after: {self.extended_states.shape}')
                        
                    #     zeros_row = zeros( X.shape[0], 1, **self.dev)
                    #     self.states_dot = hstack((zeros_row, self.states_dot))
                    
                    N_dot = self._calc_Ndot(self.states_dot, cutoff = False)
                    #1st order
                    # self.ydot = g_dot * self.N +  g * N_dot
                    #2nd order
                    #if self.ODE_order == 1:
                        
                    if not eq_system:
                        self.yfit = init_conds[0] + g.pow(1) * self.N
                        self.lastoutput = self.yfit[-1, :]
                        self.ydot = g_dot * self.N +  g * N_dot
                    else:

                        self.yfit = g*self.N
                        self.lastoutput = self.yfit[-1, :]
                        
                        for i, cond in enumerate(self.init_conds):
                            self.yfit[:, i] = self.yfit[:,i] + cond

                        self.ydot = g_dot * self.N +  g * N_dot

                    return {#"scores" : scores, 
                                "weight": self.LinOut.weight.data, 
                                "bias" : self.LinOut.bias.data,
                                "y"     : self.yfit,
                                "ydot"  : self.ydot}

                    if train_score:
                        return ODE_criterion(X, self.yfit.data, self.ydot.data, self.LinOut.weight.data, 
                                                ode_coefs = ode_coefs, init_conds = self.init_conds, 
                                                enet_strength = self.enet_strength, enet_alpha = self.enet_alpha,
                                                force_t = self.force_t)
                    else:
                        return self.yfit, self.ydot

            # if self.ODE_order >= 2:
            #     v0 = self.init_conds[1]
            #     self.ydot =  g_dot*(v0+2*g*self.N) + g**2*N_dot 

            #     #self.ydot2 = gH_dot2[:,1:] @ self.LinOut.weight
            #     N_dot2 = self.states_dot2 @ self.LinOut.weight.T 
            #     term2_1 = 4*g*g_dot*N_dot
            #     term2_2 = v0*g_dot2 
            #     term2_3 = 2*self.N*(g_dot**2 + g*g_dot2)
            #     term2_4 = g**2*N_dot2
            #     self.ydot2 = term2_1 +term2_2 + term2_3 + term2_4
            #     self.yfit = init_conds[0] + init_conds[1] * g + g.pow(self.ODE_order) * self.N
            #     self.lastoutput = self.yfit[-1, :]
            #     if train_score:
            #         return ODE_criterion(X= X, 
            #                              y = self.yfit.data, 
            #                              ydot = self.ydot.data,
            #                              ydot2 = self.ydot2.data, 
            #                              out_weights = self.LinOut.weight.data, 
            #                              ode_coefs = ode_coefs,
            #                              init_conds = self.init_conds,
            #                              enet_strength = self.enet_strength, 
            #                              enet_alpha = self.enet_alpha)
            #     return self.yfit, self.ydot, self.ydot2
            

            # if not ODE_order and burn_in:
            #     self.N = self.N[self.burn_in:,:]
            #     self.N = self.N.view(-1, self.n_outputs)
            #     self.X = self.X[self.burn_in:]
            
            # # Return all data for computation or visualization purposes (Note: these are normalized)
            # if return_states:
            #     return extended_states, (y[1:,:] if self.feedback else y), burn_in
            # else:
            #     self.yfit = self.LinOut(self.extended_states)
            #     if SCALE:   
            #         self.yfit = self._output_stds * self.yfit + self._output_means
            #     return self.yfit


    # def calculate_n_grads(self, X, y,  n = 2, scale = False):
    #     self.grads = []

    #     #X = X.reshape(-1, self.n_inputs)

    #     assert y.requires_grad, "entended doesn't require grad, but you want to track_in_grad"
    #     for i in range(n):
    #         print('calculating derivative', i+1)
    #         if not i:
    #             grad = dfx(X, y)
    #         else:
    #             grad = dfx(X, self.grads[i-1])

    #         self.grads.append(grad)

    #         if scale:
    #             self.grads[i] = self.grads[i]/(self._input_stds)
    #     with no_grad():
    #         self.grads = [self.grads[i][self.burn_in:] for i in range(n)]
                
    #         #self.yfit = self.yfit[self.burn_in:]
    #     #assert extended_states.requires_grad, "entended doesn't require grad, but you want to track_in_grad"
    
    def _scale(self, inputs=None, outputs=None, keep=False, normalize = False):
        """Normalizes array by column (along rows) and stores mean and standard devation.

        Set `store` to True if you want to retain means and stds for denormalization later.

        Parameters
        ----------
        inputs : array or None
            Input matrix that is to be normalized
        outputs : array or No ne 
        no_grads            Output column vector that is to be normalized
        keep : bool
            Stores the normalization transformation in the object to denormalize later

        Returns
        -------
        transformed : tuple or array
            Returns tuple of every normalized array. In case only one object is to be returned the tuple will be
            unpacked before returning

        """
        self.tanh_bound_limit = 1 #.9
        # Checks
        if inputs is None and outputs is None:
            raise ValueError('Inputs and outputs cannot both be None')

        # Storage for transformed variables
        transformed = []
        if not inputs is None:

            if normalize:
                if keep:
                    # Store for denormalization
                    self._input_mins = inputs.min(axis = 0).values
                    self._input_ranges = inputs.max(axis = 0).values - self._input_mins 

                # Transform
                if not self.ODE_order:
                    #normalize to between -0.5 and 0.5 for echostate purposes
                    if self.output_activation == "sin":
                        normalized = (((inputs - self._input_mins) / self._input_ranges) - 0.5)*2
                    else:
                        normalized = (((inputs - self._input_mins) / self._input_ranges) - 0.5)*self.tanh_bound_limit

                    preped = self.output_f_inv(normalized)

                    transformed.append( self._scale(inputs=preped, keep = keep))

                else:
                    assert False, "normalization not implimented for ODEs"
                    #transformed.append( inputs / self._input_stds)

            else:
                if keep:
                    # Store for destandardization
                    self._input_means = inputs.mean(axis=0)
                    self._input_stds = inputs.std(dim = 0)

                # Transform
                #if not self.ODE_order:
                transformed.append((inputs - self._input_means) / self._input_stds)
                #else: 
                #    transformed.append( inputs / self._input_stds)

        if not outputs is None:
            if normalize:
                if keep:
                    # Store for denormalization
                    self._output_mins = outputs.min(axis = 0).values
                    self._output_ranges = outputs.max(axis = 0).values - self._output_mins

                # Transform
                if not self.ODE_order:
                    #normalize to between -0.5 and 0.5 for echostate purposes
                    normalized = (((outputs - self._output_mins) / self._output_ranges) - 0.5)*self.tanh_bound_limit

                    preped = self.output_f_inv(normalized)

                    transformed.append( self._scale(outputs=preped, keep = keep))
                else: 
                    assert False, "normalization not implimented for ODEs"
                    #transformed.append( inputs / self._input_stds)
            else:
                if keep:
                    # Store for denormalization
                    self._output_means = outputs.mean(axis=0)
                    self._output_stds = outputs.std(dim = 0)#, ddof=1)

                # Transform
                if self.ODE_order:
                    transformed.append(outputs)
                else:
                    transformed.append((outputs - self._output_means) / self._output_stds)
                
                self._output_means = self._output_means
                self._output_stds = self._output_stds
        # Syntactic sugar
        return tuple(transformed) if len(transformed) > 1 else transformed[0]

    def error(self, predicted, target, method='nmse', alpha=1.):
        """Evaluates the error between predictions and target values.

        Parameters
        ----------
        predicted : array
            Predicted value
        target : array
            Target values
        method : {'mse', 'tanh', 'rmse', 'nmse', 'nrmse', 'tanh-nmse', 'log-tanh', 'log'}
            Evaluation metric. 'tanh' takes the hyperbolic tangent of mse to bound its domain to [0, 1] to ensure
            continuity for unstable models. 'log' takes the logged mse, and 'log-tanh' takes the log of the squeezed
            normalized mse. The log ensures that any variance in the GP stays within bounds as errors go toward 0.
        alpha : float
            Alpha coefficient to scale the tanh error transformation: alpha * tanh{(1 / alpha) * error}.
            This squeezes errors onto the interval [0, alpha].
            Default is 1. Suggestions for squeezing errors > n * stddev of the original series
            (for tanh-nrmse, this is the point after which difference with y = x is larger than 50%,
             and squeezing kicks in):
             n  |  alpha
            ------------
             1      1.6
             2      2.8
             3      4.0
             4      5.2
             5      6.4
             6      7.6

        Returns
        -------
        error : float
            The error as evaluated with the metric chosen above

        """
        errors = predicted - target

        # Adjust for NaN and np.inf in predictions (unstable solution)
        #if not torch.all(torch.isfinite(predicted)):
        #    # print("Warning: some predicted values are not finite")
        #    errors = torch.inf
        
        def nmse(y, yhat):
            """
            normalized mean square error
            """
            return ((torch.sum(torch.square(y - yhat)) / torch.sum(torch.square(y)))) / len(y.squeeze())
            
        #### attempt at loss function when steps ahead > 2 

        # def step_ahead_loss(y, yhat, plot = False, decay = 0.9):
        #     loss = zeros(1,1, device = self.device)
        #     losses = []
        #     total_length = len(y)
        #     for i in range(1, total_length - self.steps_ahead):
        #         #step ahead == i subsequences
        #         #columnwise
        #         #   yhat_sub = yhat[:(total_length - i), i - 1]
        #         #   y_sub = y[i:(total_length),0]
        #         #row-wise
        #         yhat_sub = yhat[i-1, :]
        #         y_sub = y[i:(self.steps_ahead + i),0]
        #         assert(len(yhat_sub) == len(y_sub)), "yhat: {}, y: {}".format(yhat_sub.shape, y_sub.shape)

        #         loss_ = nmse(y_sub.squeeze(), yhat_sub.squeeze())

        #         if decay:
        #             loss_ *= (decay ** i)

        #         #if i > self.burn_in:
        #         loss += loss_
        #         losses.append(loss_)

        #     if plot:
        #         plt.plot(range(1, len(losses) + 1), losses)
        #         plt.title("loss vs step ahead")
        #         plt.xlabel("steps ahead")
        #         plt.ylabel("avg loss")
        #     return loss.squeeze()

        # if predicted.shape[1] != 1:
        #     return step_ahead_loss(y = target, yhat = predicted) 

        # Compute mean error
        if type(method) != type("custom"):
            #assert self.custom_criterion, "You need to input the argument `custom criterion` with a proper torch loss function that takes `predicted` and `target` as input"
            try:
                error = method(self.X_test, target, predicted)
            except:
                error = method(target = target, predicted = predicted)

            """
            try:
                error = 
            except:
                if type(method) == type("custom"):
                    pass
                else:
                assert False, "bad scoring method, please enter a string or input a valid custom loss function"
            """
        elif method == 'mse':
            error = torch.mean(torch.square(errors))
        elif method == "combined":
            nmse = torch.mean(torch.square(errors)) / torch.square(target.squeeze().std())

            kl = torch.sigmoid(torch.exp(torch.nn.KLDivLoss(reduction= 'sum')(
                torch.softmax(predicted, dim = -1), 
                torch.softmax(target, dim = -1))))
            error = nmse + kl
            print('score', 'nmse', nmse, 'kl', kl, 'combined', error)
        elif method == "trivial_penalty":
            mse = torch.mean(torch.square(errors))
            penalty = torch.square((1/predicted).mean())
            error = mse + penalty
            print('score', 'mse', mse.data, 'penalty', penalty.data, 'combined', error.data)
        elif method == "smoothing_penalty":
            mse = torch.mean(torch.square(errors))
            penalty = torch.square(self.dydx2).mean()
            error = mse + 0.1 * penalty
            print('score', 'mse', nmse, 'penalty', penalty, 'combined', error)
        elif method == "combined_penalties":
            mse = torch.mean(torch.square(errors))
            #we should include hyper-parameters here.
            dxpenalty = torch.log(torch.abs(self.dydx2))
            dxpenalty_is_positive = (dxpenalty > 0)*1
            dxpenalty = dxpenalty * dxpenalty_is_positive
            dxpenalty = dxpenalty.mean()
            nullpenalty = torch.square((1/predicted).mean())
            error = mse + dxpenalty + nullpenalty
            print('score', 'mse', mse.data, 'dydx^2_penalty', dxpenalty.data, "penalty2", nullpenalty.data, 'combined', error.data)
        elif method == 'tanh':
            error = alpha * torch.tanh(torch.mean(torch.square(errors)) / alpha)  # To 'squeeze' errors onto the interval (0, 1)
        elif method == 'rmse':
            error = torch.sqrt(torch.mean(torch.square(errors)))
        elif method == 'nmse':
            error = torch.mean(torch.square(errors)) / torch.square(target.squeeze().std())#ddof=1))
        elif method == 'nrmse':
            error = torch.sqrt(torch.mean(torch.square(errors))) / target.flatten().std()#ddof=1)
        elif method == 'tanh-nrmse':
            nrmse = torch.sqrt(torch.mean(torch.square(errors))) / target.flatten().std(ddof=1)
            error = alpha * torch.tanh(nrmse / alpha)
        elif method == 'log':
            mse = torch.mean(torch.square(errors))
            error = torch.log(mse)
        elif method == 'log-tanh':
            nrmse = torch.sqrt(torch.mean(torch.square(errors))) / target.flatten().std(ddof=1)
            error = torch.log(alpha * torch.tanh((1. / alpha) * nrmse))
        else:
            raise ValueError('Scoring method not recognized')
        return error#.type(self.dtype)
    

    # def back(self, tensor_spec, retain_graph = True):
    #     return tensor_spec.backward(torch.ones(*tensor_spec.shape, device = tensor_spec.device), retain_graph = retain_graph)

    def test(self, y, X=None, y_start=None, steps_ahead=None, scoring_method='nmse', 
                  alpha=1., scale = False, criterion = None, reparam = None,
                  ODE_criterion = None): # beta = None
        """Tests and scores against known output.

        Parameters
        ----------
        y : array
            Column vector of known outputs
        x : array or None
            Any inputs if required
        y_start : float or None
            Starting value from which to start testing. If None, last stored value from trainging will be used
        steps_ahead : int or None
            Computes average error on n steps ahead prediction. If `None` all steps in y will be used.
        scoring_method : {'mse', 'rmse', 'nrmse', 'tanh'}
            Evaluation metric used to calculate error
        alpha : float
            Alpha coefficient to scale the tanh error transformation: alpha * tanh{(1 / alpha) * error}

        Returns
        -------
        error : float
            Error between prediction and knwon outputs

        """ 

        ########################## betas are currently silenced ################
        #self.beta = beta
        ########################## betas are currently silenced ################


        if not self.ODE_order:

            y = check_y(y, tensor_args = self.dev)
            X = check_x(X , y, self.dev, supervised = True).requires_grad_(True)
            final_t =y.shape[0]
            self.y_val = y
            self.steps_ahead = steps_ahead
            self.leaking_rate = self.leaking_rate_orig
            self.assign_const_leaking_rate(X)
            
            
        else:
            if self.dt != None:
                

                start, stop = float(X[0]), float(X[-1])
                nsteps = int((stop - start) / self.dt)
                X = torch.linspace(start, stop, steps = nsteps, requires_grad=False).view(-1, 1)#.to(self.device)
            elif type(X) == type([]) and len(X) == 3:
                x0, xf, nsteps = X #6*np.pi, 100
                X = torch.linspace(x0, xf, steps = nsteps, requires_grad=False).view(-1, 1)#.to(self.device)
            final_t =X.shape[0]

            ode_coefs = convert_ode_coefs(self.ode_coefs, X)

        X.requires_grad_(False)

        assert X.requires_grad == False#self.track_in_grad
        
        # Run prediction

        if steps_ahead is None:
            if not self.ODE_order:
                self._pred = self.predict(n_steps = y.shape[0], X=X, y_start=y_start, scale = True)
                
                score = self.error(predicted = self._pred, target = y, method = scoring_method, alpha=alpha)
                if self.id_ == None:
                    return score, self._pred.data #{"yhat": y_predicted.data, "ytest": y}, X[self.burn_in:]
                else:
                    
                    score.detach()
                    self._pred.detach()
                    return score.detach(), self._pred.detach(), self.id_
            else:
                val_force_t = self.force(X)
                assert not scale
                if not self.multiple_ICs:

                    returns = self.predict(n_steps = X.shape[0], X=X, y_start=y_start, scale = scale,
                                   continue_force = True)

                    if self.ODE_order == 1:
                        y_predicted, ydot = returns
                    elif self.ODE_order == 2:
                        y_predicted, ydot, ydot2 = returns

                    if self.ODE_order == 1:
                        score = self.ODE_criterion(X, y_predicted.data, ydot.data, 
                                                self.LinOut.weight.data, 
                                                ode_coefs = ode_coefs, 
                                                init_conds = self.init_conds,
                                                force_t = val_force_t,
                                                enet_alpha = self.enet_alpha, 
                                                enet_strength = self.enet_strength) 
                    # elif self.ODE_order == 2:
                    #     score = ODE_criterion(X, y_predicted.data, ydot.data, ydot2.data, self.LinOut.weight.data, ode_coefs = ode_coefs, init_conds = self.init_conds,
                    #                           enet_alpha = self.enet_alpha, enet_strength = self.enet_strength) #error(predicted = y_predicted, target = dy_dx_val, method = scoring_method, alpha=alpha)
                    # # else:
                    # #     assert False
                    # #     score = self.error(predicted = y_predicted, target = y, method = scoring_method, alpha=alpha)
                    # Return error

                    self._pred = y_predicted
                    #print("score", score.detach())
                    return score.detach(), y_predicted.detach(), self.id_

                else:
                    y_preds, ydots = self.predict(n_steps = X.shape[0], X=X, y_start=y_start, scale = scale,
                                   continue_force = True)
                    scores = []
                    for i, pred in enumerate(y_preds):
                        ydot = ydots[i]
                        if not self.eq_system:
                            
                            score = self.ODE_criterion(X, pred.data, ydot.data, 
                                                  self.LinOut.weight.data, 
                                                  ode_coefs = ode_coefs, 
                                                  init_conds = self.init_conds,
                                                  enet_alpha = self.enet_alpha, 
                                                  enet_strength = self.enet_strength,
                                                  force_t = val_force_t)
                            
                        else:
                            init_conds_system =[self.init_conds[0][i]] + self.init_conds[1:]
                            y0, p0 = init_conds_system
                            #ham0 = 
                            score = self.ODE_criterion(X, pred.data, ydot.data, 
                                                  self.LinOut.weight.data, 
                                                  ode_coefs = ode_coefs, 
                                                  init_conds = init_conds_system,
                                                  enet_alpha = self.enet_alpha, 
                                                  enet_strength = self.enet_strength,
                                                  #ham0 = (1/2)*p0**2 - 3*y0**2 + (21/4)*y0**4,
                                                  force_t = val_force_t)
                        scores.append(score)
                        #print("score", score.detach())
                    
                    return scores, y_preds, self.id_



                #y_predicted, ydot = self.reparam(self.y0, X, N, N_dot)
            #printc("predicting "  + str(y.shape[0]) + "steps", 'blue')
        else:
            assert False, f'predict_stepwise not implimented'
            y_predicted = self.predict_stepwise(y, X, steps_ahead=steps_ahead, y_start=y_start)[:final_t,:]

    def _supervised_val_states(self, n_samples, inputs, states, outputs):
        """
        TODO doctstring
        """
        for t in range(n_samples):

            #assert False, f'inputs[t+1, :] :, {inputs[t+1, :]}'
            input_t, state_t, output_prev = inputs[t+1, :], states[t,:], outputs[t,:]

            state_t, _ = self.train_state(t, X = input_t, state = state_t, y = output_prev)

            states = cat([states, state_t.view(-1, self.n_nodes)], axis = 0)

            output_t = self._output_i(input_t, state_t)

            outputs = cat([outputs, output_t], axis = 0)
            
        return states, outputs

    def _unsupervised_val_states(self, n_samples, inputs, states, outputs):
        """
        TODO doctstring
        """
        for t in range(n_samples):

            input_t, state_t, output_prev = inputs[t+1, :], states[t,:], outputs[t,:]

            state_t, output_t  = self.train_state(t, X = input_t, state = state_t, y = output_prev)
            states = vstack((states, state_t.view(-1, self.n_nodes)))

            output_t = self._output_i(input_t, state_t)

            outputs = vstack((outputs, output_t))

        return states, outputs

    def predict(self, n_steps, X=None, y_start=None, continuation = True, scale = True, continue_force = True):
        """Predicts n values in advance.

        Prediction starts from the last state generated in training.

        Parameters
        ----------
        n_steps : int
            The number of steps to predict into the future (internally done in one step increments)
        x : numpy array or None
            If prediciton requires inputs, provide them here
        y_start : float or None
            Starting value from which to start prediction. If None, last stored value dfrom training will be used

        Returns
        -------
        y_predicted : numpy array
            Array of n_step predictions

        """
        # Check if ESN has been trained
        assert self.lastoutput is not None, 'Error: ESN not trained yet'

        self.unscaled_Xte = X

        # Normalize the inputs (like was done in train)
        if not X is None:
            if scale and self.unscaled_X.std() != 0:
                self.X_val = Parameter(self._scale(inputs=self.unscaled_Xte, normalize = False))
            else:
                self.X_val = Parameter(X)

        if y_start is not None:
            continuation = False

        if self.noise is not None:
            self.noise_z = normal(0, 1, size = (self.n_nodes, self.X_val.shape[0]), **self.dev) * self.noise

        # try:
        #     assert self.X_val.device == self.device, ""
            
        # except:
        #     self.X_val.data = self.X_val.to(self.device)

        self.X_val_extended =  self.X_val
        #assert False, f'X mean {self.X_val.mean()} std {self.X_val.std()}'
        # if not continue_force:
        #     if self.ODE_order:
        #         continuation = False
        dev = {"device" : self.device, "dtype" : self.dtype, "requires_grad": False}

        n_samples = self.X_val_extended.shape[0]

        # if y_start: #if not x is None:
        #     if scale:
        #         previous_y = self.scale(outputs=y_start)[0]
        #     else:
        #         previous_y = y_start[0]
        assert self.lastinput.device == self.device
        if continuation:
            #if self.ODE_order >=2:
            #    lasthdot2 = self.lasthdot2
            #lasthdot = self.lasthdot
            laststate = self.laststate
            lastinput = self.lastinput
            lastoutput = self.lastoutput
        else:
            #if self.ODE_order >=2:
            #    lasthdot2 = zeros(self.n_nodes, **dev)
            #lasthdot = zeros(self.n_nodes, **dev)
            laststate = zeros(self.n_nodes, **dev)
            lastinput = zeros(self.n_inputs, **dev).view(-1, self.n_inputs)
            lastoutput = zeros(self.n_outputs, **dev)
        #if self.ODE_order:
        #    lastoutput = zeros(self.n_outputs, **dev)


        if not y_start is None:

            lastoutput = self._scale(outputs=y_start, normalize = self._normalize)# self.scale(inputs=X)

        inputs = vstack([lastinput, self.X_val_extended]).view(-1, self.X_val_extended.shape[1])
        
        states = zeros((1, self.n_nodes), **dev)
        states[0,:] = laststate
        outputs = lastoutput.view(1, self.n_outputs)

        #assert False, f"last output {lastoutput}, ystart {y_start}"
        

        #dt = inputs[1,:] - inputs[0,:]
        with no_grad():
            
            if self.ODE_order:
                states_dot = zeros((1, self.n_nodes), **dev)
                #states, outputs = self.unsupervised_val_states(n_samples, inputs, states, outputs)
                states, outputs = self._unsupervised_val_states(n_samples, inputs, states, outputs)

            else:
                #states = vstack((states, states))
                states, outputs = self._supervised_val_states(n_samples, inputs, states, outputs)

            #drop first state and first output (final train-set datapoints which were already used)
            self.val_states = states = states[1:]
            outputs = outputs[1:]

            #if self.burn_in:
            #    states = states[self.burn_in:]
            #    outputs = outputs[self.burn_in:]

            

            if not self.ODE_order:
                # try:
                #     if scale:
                yhat = self._descale(outputs = outputs, normalize = self._normalize).view(-1, self.n_outputs) 
                # except:
                #     yhat = outputs
                return yhat
            else:
                # calculate hidden state derivatives
                if not self.feedback:
                    updates = self.LinIn(self.X_val) + self.bias + self.LinRes(states)
                else:
                    input_ = torch.hstack((self.X_val, outputs))
                    updates = self.LinIn(input_) + self.bias + self.LinRes(states)

                states = torch.cat((self.X_val, states), axis = 1)
                time = self.X_val
                states_dot = - self.alpha * states[:,1:] + self.alpha * self.activation_function(updates)
                # if self.ODE_order == 2:
                #     states_dot2 = - self.alpha * states_dot + self.alpha * self.act_f_prime(updates) * (self.LinIn.weight.T + self.bias + self.LinRes(states_dot))
                #     states_dot2 = torch.cat((zeros_like(self.X_val), states_dot2), axis = 1)
                states_dot = torch.cat((ones_like(self.X_val), states_dot), axis = 1)
                assert states.shape == states_dot.shape

                G = self.reparam_f(self.X_val, order = self.ODE_order)
                g, g_dot = G

                self.val_states_dict = {"s" : states, "s1" : states_dot, "G" :  G}


                # if self.ODE_order == 2:
                #     #derivative of  g_dot * states_with_bias
                #     #gH_dot2_p1 =  g_dot * states_dot  + g_dot2 * states

                #     #derivative of  g * states_dot_with_bias
                #     #gH_dot2_p2 =  g * states_dot2  + g_dot * states_dot
                    
                #     #gH_dot2 = gH_dot2_p1 + gH_dot2_p2

                #     #ydot2 = self.LinOut(gH_dot2)

                #     N_dot2 = states_dot2 @ self.LinOut.weight.T #self.calc_Ndot(states_dot2, cutoff = False)
                #     ydot2 = 4*g*g_dot*N_dot + self.init_conds[1]*g_dot2
                #assert False, f'o {outputs.shape} t {time.shape} dN {N_dot.shape}'
                assert type(self.reparam_f) != type(None), "you must input a reparam function with ODE"
                
                if not self.multiple_ICs:

                    A = self.init_conds[0] * g.pow(self.ODE_order)

                    #the code may be useful for solving higher order:
                    ##########################
                    #A = [ self.init_conds[i] * g.pow(i) for i in range(self.ODE_order)]
                    # for i in range(self.ODE_order):
                    #     A_i = self.init_conds[i] * g.pow(i) #self.ode_coefs[i] * 
                    #     if not i:
                    #         A = A_i # + ode_coefs[1] * v0 * g.pow(1) + ... + ode_coefs[m] * accel_0 * g.pow(m)
                    #     else:
                    #         A = A + A_i
                else:
                    As = [y0 * g.pow(0) for y0 in self.init_conds[0]]

                if not self.multiple_ICs:
                    if not self.eq_system:
                        N = self.LinOut(states)
                        N_dot = self._calc_Ndot(states_dot, cutoff = False)

                        y = A + g * N

                        for i, cond in enumerate(range(y.shape[1])):
                            

                            y[:, i] = y[:,i] + self.init_conds[i]

                        ydot = g_dot * N +  g * N_dot
                        
                        #self.N = self.N.view(-1, self.n_outputs)
                        #gH = g * states
                        #gH_dot =  g_dot * states  +  g * states_dot

                        
                        #elf.yfit = init_conds[0] + g.pow(1) * self.N
                        #self.ydot = g_dot * self.N +  g * N_dot
                    else:
                        y = g * self.LinOut(states)
                        ydot = g_dot * N + N_dot * g
                        for i, cond in enumerate(self.init_conds):

                            y[:, i] = y[:,i] + cond
                    return y, ydot
                else:
                    if not self.eq_system:
                        ys = []
                        ydots = []
                        for i, weight in enumerate(self.weights_list):
                            #print("w", i)
                            self.LinOut.weight = Parameter(weight.view(self.n_outputs, -1))
                            self.LinOut.bias = Parameter(self.biases_list[i].view(1, self.n_outputs))

                            N = self.LinOut(states)
                            N_dot = self._calc_Ndot(states_dot, cutoff = False)
                            yfit = g*N


                            yfit[:, 0] = yfit[:,0] + self.init_conds[0][i]
                            
                            ydot = g_dot * N +  g * N_dot

                            ys.append(yfit)
                            ydots.append(ydot)

                        return ys, ydots
                    else:
                        ys = []
                        ydots = []
                        #loop
                        for i, weight in enumerate(self.weights_list):
                            self.LinOut.weight = Parameter(weight.view(self.n_outputs, -1))
                            self.LinOut.bias = Parameter(self.biases_list[i].view(1, self.n_outputs))

                            N = self.LinOut(states)
                            N_dot = self._calc_Ndot(states_dot, cutoff = False)

                            #reparameterize
                            y = g*N
                            ydot = g_dot * N + N_dot * g

                            #add initial conditions
                            y[:, 0] = y[:,0] + self.init_conds[0][i]
                            for j in range(1, y.shape[1]):
                                y[:, j] = y[:,j] + self.init_conds[j]
                            
                            ys.append(y)
                            ydots.append(ydot)

                        return ys, ydots

                
                # if self.ODE_order == 2:
                #     y0, v0 = self.init_conds
                #     ydot =  g_dot*(v0+2*g*N) + g**2*N_dot 

                #     #self.ydot2 = gH_dot2[:,1:] @ self.LinOut.weight
                #     N_dot2 = states_dot2 @ self.LinOut.weight.T 
                #     term2_1 = 4*g*g_dot*N_dot
                #     term2_2 = v0*g_dot2 
                #     term2_3 = 2*N*(g_dot**2 + g*g_dot2)
                #     term2_4 = g**2*N_dot2
                #     ydot2 = term2_1 +term2_2 + term2_3 + term2_4
                #     y = y0 + v0 * g + g.pow(self.ODE_order) * N
                #     #y = A + g**2 * N
                #     return y, ydot, ydot2
                
        #https://towardsdatascience.com/in-place-operations-in-pytorch-f91d493e970e



    # def predict_stepwise(self, y, x=None, steps_ahead=1, y_start=None):
    #     """Predicts a specified number of steps into the future for every time point in y-values array.
    #     E.g. if `steps_ahead` is 1 this produces a 1-step ahead prediction at every point in time.
    #     Parameters
    #     ----------
    #     y : numpy array
    #         Array with y-values. At every time point a prediction is made (excluding the current y)
    #     x : numpy array or None
    #         If prediciton requires inputs, provide them here
    #     steps_ahead : int (default 1)
    #         The number of steps to predict into the future at every time point
    #     y_start : float or None
    #         Starting value from which to start prediction. If None, last stored value from training will be used
    #     Returns
    #     -------
    #     y_predicted : numpy array
    #         Array of predictions at every time step of shape (times, steps_ahead)
    #     """

    #     # Check if ESN has been trained
    #     if self.out_weights is None or self.y_last is None:
    #         raise ValueError('Error: ESN not trained yet')

    #     # Normalize the arguments (like was done in train)
    #     y = self.scale(outputs=y)
    #     if not x is None:
    #         x = self.scale(inputs=x)

    #     # Timesteps in y
    #     t_steps = y.shape[0]

    #     # Check input
    #     if not x is None and not x.shape[0] == t_steps:
    #         raise ValueError('x has the wrong size for prediction: x.shape[0] = {}, while y.shape[0] = {}'.format(
    #             x.shape[0], t_steps))

    #     # Choose correct input
    #     if x is None and not self.feedback:
    #         #pass #raise ValueError("Error: cannot run without feedback and without x. Enable feedback or supply x")
    #         inputs = ones((t_steps + steps_ahead, 2), **dev) 
    #     elif not x is None:
    #         # Initialize input
    #         inputs = ones((t_steps, 1), **dev)  # Add bias term
    #         inputs = hstack((inputs, x))  # Add x inputs
    #     else:
    #         # x is None
    #         inputs = ones((t_steps + steps_ahead, 1), **dev)  # Add bias term
        
    #     # Run until we have no further inputs
    #     time_length = t_steps if x is None else t_steps - steps_ahead + 1

    #     # Set parameters
    #     y_predicted = zeros((time_length, steps_ahead), dtype=self.dtype, device=self.device)

    #     # Get last states
    #     previous_y = self.y_last
    #     if not y_start is None:
    #         previous_y = self.scale(outputs=y_start)[0]

    #     # Initialize state from last availble in train
    #     current_state = self.state[-1]

    #     # Predict iteratively
    #     with no_grad():
            
    #         for t in range(time_length):

    #             # State_buffer for steps ahead prediction
    #             prediction_state = current_state.clone().detach()
                
    #             # Y buffer for step ahead prediction
    #             prediction_y = previous_y.clone().detach()
            
    #             # Predict stepwise at from current time step
    #             for n in range(steps_ahead):
                    
    #                 # Get correct input based on feedback setting
    #                 prediction_input = inputs[t + n] if not self.feedback else hstack((inputs[t + n], prediction_y))
                    
    #                 # Update
    #                 prediction_update = self.activation_function(matmul(self.in_weights, prediction_input.T) + 
    #                                                matmul(self.weights, prediction_state))
                    
    #                 prediction_state = self.leaking_rate * prediction_update + (1 - self.leaking_rate) * prediction_state
                    
    #                 # Store for next iteration of t (evolves true state)
    #                 if n == 0:
    #                     current_state = prediction_state.clone().detach()
                    
    #                 # Prediction. Order of concatenation is [1, inputs, y(n-1), state]
    #                 prediction_row = hstack((prediction_input, prediction_state))
    #                 if not self.backprop:
    #                     y_predicted[t, n] = matmul(prediction_row, self.out_weights)
    #                 else:
    #                     y_predicted[t, n] = self.LinOut.weight.T @ prediction_row[1:]
    #                 prediction_y = y_predicted[t, n]

    #             # Evolve true state
    #             previous_y = y[t]

    #     # Denormalize predictions
    #     y_predicted = self.descale(outputs=y_predicted)
        
    #     # Return predictions
    #     return y_predicted

    def plot_residuals(self, fig = True) -> None:
        """
        TODO doctstring
        """
        
        if fig:
            plt.figure(figsize = (16, 4))
        plt.plot(self.tr_idx, 
                 self.tr_resids)

        plt.plot(self.te_idx, 
                 self.te_resids)

        plt.yscale("log") 

    def _plot_prep(self, gt_tr_override = None, gt_te_override = None):
        """
        TODO doctstring
        """
        #for noise predictions, ground truth over-ride

        

        if gt_tr_override is None:
            self._gt_te = self.y_val
            self._gt_tr = self.y_tr
            self._override = False
        else:
            self._gt_te = gt_te_override
            self._gt_tr = gt_tr_override

            self._override = True
            #self._gt_tr = gt_tr_override #self._gt_tr = fit_args["y"]

        # if gt_te_override is None:
        #     self._gt_te = self.y_val
        # else:
        #     self._gt_te = gt_te_override

        self._len_te = len(self._pred)
        self._len_tr = len(self.yfit)

        self.te_idx = list(range(self._len_tr, self._len_te + self._len_tr))
            

        #save resids
        self.te_resids = (self._gt_te - self._pred)**2
        self.tr_resids = (self._gt_tr - self.yfit)**2

        self._xte = self.unscaled_Xte

        self._len_tr = len(self.yfit)
        self.tr_idx = list(range(self._len_tr))
        

    def plot_prediction(self, gt_tr_override = None, gt_te_override = None, lw_vert = None,
                              fig = None, prep = True, ylabel = None, axis_label_fontsize = None,
                              tick_fontsize = None) -> None:
        """plots the RC predictions

        Arguments
        ---------
        gt_tr_override: if you want to calculate residuals from a non-noisy real training set,
            residuals will be calculated from it not say noisy inputs

        gt_te_override: if you want to calculate residuals from a non-noisy real validation set,
            residuals will be calculated from it not say noisy inputs
        fig: a matplotlib figure to plot on. 

        ylabel: the users desired ylabel
        """

        if not fig:
            plt.figure(figsize = (16, 4))

        lw = 3
        
        if prep:
            self._plot_prep(gt_tr_override, gt_te_override)

        #do you want discrete time steps or the actual value of the input?
        try:
            #if you want actual value
            input_train, input_test = self.t_tr, self.t_te  
        except:
            #if you want the discrete indices/ don't supply the input.
            #assert False, "fix this later"
            input_train, input_test = self.tr_idx, self.te_idx


        if not self._override:
            pred_alpha = 0.4
            gt_alpha = 1
            plt.plot(input_train, self.yfit,  alpha = pred_alpha, linewidth = lw+2, #color = "blue",
                label = "train")

            plt.plot(input_test, self._pred, alpha = pred_alpha, linewidth = lw+2, #color = "red", 
                    label = "test")
            try:
                input_train, input_test = list(input_train.ravel()), list(input_test.ravel())
            except:
                pass

            plt.plot(input_train + input_test,
                     np.concatenate((self._gt_tr, self._gt_te), axis = 0),
                     '--',
                     color = "black",
                     alpha = gt_alpha,
                     linewidth = lw-1,

                     label = "ground truth")

        else:
            pred_alpha = 0.9
            gt_alpha = 0.3
            plt.plot(input_train + input_test, #self.tr_idx + self.te_idx,
                     np.concatenate((self.y_tr, self.y_val), axis = 0),
                     '--',
                     color = "black",
                     alpha = gt_alpha,
                     linewidth = lw-1,
                     label = "ground truth")

        
            plt.plot(input_train, self.yfit,  alpha = pred_alpha, linewidth = lw, #color = "blue",
                label = "train")
            plt.plot(input_test, self._pred, alpha = pred_alpha, linewidth = lw, #color = "red", 
                    label = "test")

        plt.axvline(input_train[-1], linestyle = ':', color = 'darkblue',  linewidth = lw_vert)
        
        if ylabel is not None:
            plt.ylabel(ylabel, fontdict = {"fontsize": axis_label_fontsize})
        #plt.legend()
        if tick_fontsize is not None:
            for axis in ['x', 'y']:
                plt.tick_params(axis=axis, labelsize=tick_fontsize)

    def plot_residuals(self, gt_tr_override = None, gt_te_override = None, lw_vert = None, ylabel = None,
                             fig = None, prep = True, axis_label_fontsize = None, tick_fontsize = None) -> None:
        """
        TODO doctstring
        """
        if prep:
            self._plot_prep(gt_tr_override, gt_te_override)
        if not fig:
            plt.figure(figsize = (16, 4))

        #do you want discrete time steps or the actual value of the input?
        try:
            #if you want actual value
            input_train, input_test = self.t_tr, self.t_te  
        except:
            #if you want the discrete indices/ don't supply the input.
            #assert False, "fix this later"
            input_train, input_test = self.tr_idx, self.te_idx

        
        plt.plot(input_train, self.tr_resids)
        plt.plot(input_test, self.te_resids)
        
        plt.axvline(input_train[-1], linestyle = ':', color = 'darkblue',  linewidth = lw_vert)
        if ylabel is not None:
            plt.ylabel(ylabel, fontdict = {"fontsize": axis_label_fontsize})
        plt.xlabel(r"$t$", fontdict = {"fontsize": axis_label_fontsize})
        plt.yscale("log")


        if tick_fontsize is not None:
            for axis in ['x', 'y']:
                plt.tick_params(axis=axis, labelsize=tick_fontsize)

    def combined_plot(self, t_tr = None, t_te = None, fig = None, gt_tr_override = None, gt_te_override = None,  
                            axis_label_fontsize = None,
                            lw_vert = 2, 
                            tight_layout_args = None, 
                            ylabel_pred = None, 
                            tick_fontsize= None ,
                            ylabel_resid = None,
                            grid_spec_x = 7,
                            labelsize  = 20,
                            resid_blocks = 4) -> None:
        """
        make a plot of your prediction

        Arguments:
            tight_layout_args: must be a dictionary,
            for example: {'pad'=0.4, 'w_pad'=0.5, 'h_pad'=1.0}
            #https://matplotlib.org/stable/tutorials/intermediate/tight_layout_guide.html
            
        """
        #assign the time train and time test, if they exist.
        if t_tr is not None:
            self.t_tr = t_tr
        if t_te is not None:
            self.t_te = t_te

        self._plot_prep(gt_tr_override, gt_te_override)
        if not fig:
            fig = plt.figure(figsize = (16,7))
            g = grid_spec_x
            gs1 = gridspec.GridSpec(g, g);
        ax = plt.subplot(gs1[:resid_blocks, :])

        self.plot_prediction(gt_tr_override, 
                             gt_te_override, 
                             fig = 1, 
                             prep = True, 
                             axis_label_fontsize = axis_label_fontsize, 
                             tick_fontsize = tick_fontsize,
                             lw_vert = lw_vert, 
                             ylabel = ylabel_pred)

        ax.tick_params(labelbottom=False, labelsize = tick_fontsize)

        #[ (plt.sca(ax[i]), plt.xticks(fontsize=tick_fontsize), plt.yticks(fontsize=tick_fontsize)) for i in range(3)]

        ax = plt.subplot( gs1[resid_blocks:, :] )
        
        self.plot_residuals(fig = 1, 
                            prep = False, 
                            lw_vert = lw_vert, 
                            ylabel = ylabel_resid,
                            axis_label_fontsize = axis_label_fontsize, 
                            tick_fontsize = tick_fontsize)
        
        if tight_layout_args is not None:
            plt.tight_layout(**tight_layout_args)
        else:
            plt.tight_layout()
    
    

    def _descale(self, inputs=None, outputs=None, normalize = False):
        """Denormalizes array by column (along rows) using stored mean and standard deviation.

        Parameters
        ----------
        inputs : array or None
            Any inputs that need to be transformed back to their original scales
        outputs : array or None
            Any output that need to be transformed back to their original scales

        Returns
        -------
        transformed : tuple or array
            Returns tuple of every denormalized array. In case only one object is to be returned the tuple will be
            unpacked before returning

        """
        if inputs is None and outputs is None:
            raise ValueError('Inputs and outputs cannot both be None')

        # Storage for transformed variables
        transformed = []
        
        #for tensor in [train_x, train_y]:
        #     print('device',tensor.get_device())
        
        if normalize:
            if self.ODE_order:
                    assert False, "not implimented"
            if not inputs is None:
                assert False, f' there is no need to normalize the input, standardize instead'
                #transformed.append(( (inputs + 0.5) * self._input_ranges) + self._input_mins)

            if not outputs is None:

                destandardized = self._descale(outputs = outputs, normalize = False)

                if self.output_activation == "sin":
                    denormalized = ( self.output_f(destandardized/2) + 0.5) * self._output_ranges + self._output_mins

                else:

                    denormalized = ( self.output_f(destandardized/self.tanh_bound_limit) + 0.5) * self._output_ranges + self._output_mins

                transformed.append(denormalized)
        else:
            if not inputs is None:
                # if self.ODE_order:
                #     transformed.append(inputs * self._input_stds)
                # else:
                transformed.append((inputs * self._input_stds) + self._input_means)

            if not outputs is None:
                if self.ODE_order:
                    transformed.append(outputs)
                else:
                    transformed.append((outputs * self._output_stds) + self._output_means)

        # Syntactic sugar
        return tuple(transformed) if len(transformed) > 1 else transformed[0]

"""
                                    #calculate F depending on the order of the ODE:
                                    if ODE == 1:
                                        #population eq
                                        #RHS = lam * self.y0 - f(self.X) 
                                        #self.F =  g_dot * states_  +  g * (states_dot + lam * states_)
                                        
                                        #nl eq 
                                        self.F =  g_dot * states_  +  g * states_dot
                                        if nl_f:
                                            #y0_nl, y0_nl_dot = nl_f(self.y0)
                                            self.F = self.F - 2 * self.y0 * g * states_ 
                                            #self.F = self.F - (g * ).T @ 

                                    elif ODE == 2:
                                        # without a reparameterization
                                        #self.F = torch.square(self.X) * states_dot2 + 4 * self.X * states_dot + 2 * states_ + (self.X ** 2) * states_
                                        self.G = g * states_
                                        assert self.G.shape == states_.shape, f'{self.shape} != {self.states_.shape}'
                                        self.Lambda = g.pow(2) * states_ 
                                        self.k = 2 * states_ + g * (4*states_dot - self.G*states_) + g.pow(2) * (4 * states_ - 4 * states_dot + states_dot2)
                                        self.F = self.k + self.Lambda
                                    #common F derivation:
                                    F = self.F.T
                                    F1 = F.T @ F 
                                    F1 = F1 + self.regularization * eye(F1.shape[1], **self.dev)
                                    ##################################### non-linear adustment
                                    nl_adjust = False
                                    if nl_adjust:
                                        G = g * states_
                                        G_sq = G @ G.T
                                        nl_correction = -2 * self.y0 * (G_sq)
                                        F1 = F1 + nl_correction
                                    #F1_inv = pinverse(F1)
                                    #F2 = matmul(F1_inv, F.T)
                                    #####################################
                                    #First Order equation
                                    if self.ODE_order == 1:
                                        self.y0I = (self.y0 ** 2) * ones_like(self.X)
                                        #self.y0I = self.y0I.squeeze().unsqueeze(0)
                                        #RHS = lam*self.y0I.T - f(self.X) 

                                        #REPARAM population
                                        #RHS = lam * self.y0 - f(self.X) 

                                        RHS = self.y0I

                                        #weight = matmul(-F2.T, RHS)

                                        weight = matmul(F2.T, RHS)
                                        #assert False, weight.shape

                                    #Second Order equation
                                    elif self.ODE_order == 2:
                                        
                                        #self.y0I = y0[0] * ones_like(self.X)
                                        #self.y0I = self.y0I.squeeze().unsqueeze(0)

                                        #RHS = self.y0I.T + self.X * y0[1]
                                        RHS = self.y0 + f_t * y0[1]
                                        
                                        #t = self.X
                                        #A0 = y0 + g * v0
                                        #RHS = A0 + (g - 1)*v0 - f(t)
                                        weight = matmul(-F2.T, D_A)
                                    weight = matmul(D_W, D_A)

                                    #y = y0[0] + self.X * y0[1] + self.X
"""
"""
        if self.ODE_order == 1:
            return self.reparam(t = self.X, init_conditions = self.y0, N = self.yfit, N_dot = N_dot)
        elif self.ODE_order == 2:
            N_dot2 = self.calc_hdot(states_dot2[:,1:], cutoff = False)
            return self.reparam(t = self.X, init_conditions = [y0, v0], 
                N = self.yfit, N_dot = [N_dot, N_dot2], esn = self, 
                states = states_[:,1:], states_dot = states_dot[:,1:], states_dot2 = states_dot2[:,1:])
        """
"""
    #assert weight.requires_grad, "weight doesn't req grad"
                            #torch.solve solves AX = B. Here X is beta_hat, A is ridge_x, and B is ridge_y
                            #weight = torch.solve(ridge_y, ridge_x).solution
                        # elif self.l2_prop == 1:
                        # else: #+++++++++++++++++++++++         This section is elastic net         +++++++++++++++++++++++++++++++

                        #     gram_matrix = matmul(train_x.T, train_x) 

                        #     regr = ElasticNet(random_state=0, 
                        #                           alpha = self.regularization, 
                        #                           l1_ratio = 1-self.l2_prop,
                        #                           selection = "random",
                        #                           max_iter = 3000,
                        #                           tol = 1e-3,
                        #                           #precompute = gram_matrix.numpy(),
                        #                           fit_intercept = True
                        #                           )
                        #     print("train_x", train_x.shape, "_____________ train_y", train_y.shape)
                        #     regr.fit(train_x.numpy(), train_y.numpy())

                        #     weight = tensor(regr.coef_, device = self.device, **self.dev)
                        #     bias = tensor(regr.intercept_, device =self.device, **self.dev)


#if not preloaded_states_dict:
                # else:
                #     sd = preloaded_states_dict
                #     self.states, self.states_dot, G, self.extended_states = sd["s"], sd["s1"], sd["G"], sd["ex"]
                #     states_with_bias, states_dot_with_bias = sd["sb"], sd["sb1"]
                #     # if self.ODE_order == 2:
                #     #     self.states_dot2 = sd["s2"]
                #     #     states_dot2_with_bias = sd["sb2"]
                #     g, g_dot = G
                #     self.g = gdef
"""
#EchoStateNetwork = RcNetwork
                                    