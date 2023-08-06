import random
import numpy as np
import os
import pandas as pd
import time
from scipy.special import expit

binary = np.vectorize(np.binary_repr)

class GA(object):
    """
    All genes are parameters intepreted as binary numbers of fixed size
    """
    def __init__(self,
    population_size,
    chromosome_size,
    fitness,
    resolution=8,
    generations=10,
    crossover=0.5,
    mutation=0.5,
    elitism=True,
    iterations=10,
    range_mask=None,
    has_mask=False,
    logging=True,
    time_print=.1,
    maximize = True
    ):
        self.bits = resolution
        self.m = population_size
        self.n = chromosome_size
        self.gen = generations
        self.crossover = crossover
        self.mutation = mutation
        self.elite = elitism
        self.chrbits = self.bits*self.n
        self.G = np.random.random_integers(0,2**(self.bits)-1,(self.m,self.n))
        #self.G = np.hstack([np.zeros((self.m,1)),self.G]).astype(int)
        self.F = np.zeros(self.m)
        self.f = fitness
        self.T = iterations
        self.mask = range_mask
        self.has_mask = has_mask
        self.logging = logging
        self.M = self.G.copy()
        self.C = self.G.copy()
        self.R = np.array([0])
        self.time_print=time_print
        self.ftime = 0
        self.maximize = maximize

    def sorted(self):
        """
        Sorts the population with respect to the fitness in ascending order
        """
        if self.maximize:
            self.G = self.G[self.F.argsort()[::-1]]
            self.F.sort()
            self.F = self.F[::-1]
        else:
            self.G = self.G[self.F.argsort()]
            self.F.sort()

    def crossover_func(self):
        """
        Performs a single point crossover over the matrix G excluding one or two
        chromosomes in the elite case.
        """
        #Sorts by G[0] in increasing order
        upper_bound = 0
        if self.elite:
            upper_bound = 1 + (1-self.m&1)
            self.G[-1] = self.G[0].copy()
            self.F[-1] = self.F[0].copy()
        k = np.random.randint(0,self.bits)
        mask = 2**k-1
        p = self.F[upper_bound:].copy()
        #p = 1. + p/np.max(np.abs(p))
        p = expit(p)
        p[np.isnan(p)]=0
        if not self.maximize:
            p = 1.0-p
        if p.sum()==0:
            p = np.ones(p.shape)/p.shape[0]
        else:
            p = p/p.sum() #probability array for the tournament
        L = self.m-upper_bound
        rng_size = (L//2,2)
        rng = np.arange(upper_bound,self.m)
        #rng = list(range(upper_bound,self.m))
        #indices = np.random.choice(rng,size=rng_size,p=p, replace=False)
        indices = random.choices(range(self.m-upper_bound), weights=list(p), k=self.m-upper_bound)
        indices = np.array(indices).reshape(rng_size)
        #print("indices: ", indices, "mask: ", mask)
        #
        # M=np.hstack([self.G[indices]&mask,self.G[indices]&~mask]).reshape((self.m-upper_bound)//2,2,2*self.n)
        # U=M[:,0]|M[:,1][:,::-1]
        #self.G[upper_bound:]=U.reshape((self.m-upper_bound,self.n))
        # print("2",self.G.shape)
        U = self.G[indices]&mask
        V  = self.G[indices]&~mask
        self.G[upper_bound:] = np.vstack([U[:,0]|V[:,1],U[:,1]|V[:,0]])

        if self.logging:
            self.C = self.G.copy()

    def mutation_func(self):
        """
        Chooses a random entry of G[:,1:] to mutate,
        except the elite chromosome if elitism=True
        """
        upper_bound = self.elite + 0
        p=np.array([1.-self.mutation,self.mutation])
        # M = np.random.choice(np.array([0,1]),size=(self.m-upper_bound,self.bits),p=p)
        # M = M.dot(1<<np.arange(M.shape[-1]-1,-1,-1)).reshape(self.m-upper_bound,1)
        #M=np.random.random_integers(0,self.chrbits,(1,self.m-upper_bound))
        pos = np.array([i for i in range(0,2**self.bits)])#possibilities
        count = np.array(list(map(lambda x: bin(x).count("1"),pos)))
        indp = (p[1]**count)*(p[0]**(self.bits-count))
        M = np.random.choice(pos, size=self.G[upper_bound:].shape, p=indp)
        self.G[upper_bound:] = self.G[upper_bound:]^M
        if self.logging:
            self.M = self.G.copy()
    def fitness_call(self):
        """
        Makes a call to the assigned fitness function.
        The fitness function must return a vector containing the corresponding values
        of the chromosomes in order.
        Results are already cumulative probabilities.
        """


        # p = np.array([(2**self.bits-1)<<i*self.bits for i in range(self.n)])
        # G_copy = self.G[:].copy()
        # G_copy.resize((self.m,1))
        # self.R = (G_copy&p)>>np.array([[i*self.bits for i in range(self.n)]])

        self.R = self.G.copy()

        if self.has_mask:
            self.R = self.mask[:,0] + self.R*(self.mask[:,1]-self.mask[:,0])/(2**self.bits)
        ta = time.time()
        self.F = np.array(self.f(self.R)) #Scale and modify to matrix shape
        tb = time.time()
        self.ftime = tb-ta
        # print("0", self.G.shape, "F", self.F.shape)
        self.sorted()
        # print("1", self.G.shape)

    def write(self,i):
        os.system("clear")
        print("Step",i+1," of {}".format(self.T))
        P = pd.DataFrame(self.R)
        P["Fitness"] = self.F
        print("ftime(sec): ", self.ftime)
        print(P)

    def run(self):
        t=0
        for i in range(self.T):
            self.fitness_call()
            u = abs(time.time()-t)
            if self.logging and u>self.time_print:
                self.write(i)
                t = time.time()
            self.crossover_func()
            self.mutation_func()
        self.sorted()
        return self.G
