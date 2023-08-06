import numpy as np
from scipy.special import softmax

"""
Genetic Algorithm for optimization. Uses arrays of binary numbers to store genetic code. Uses elitism.
"""

def packbits(X):
    """
    Expects array of three axes. The third axis determines the number of bits.
    """
    n,m,b = X.shape
    Y = np.zeros((n,m))
    for j in range(b):
        Y += X[:,:,j]<<j
    return Y

class GA:
    def __init__(
        self,
        population_size,
        mutation_probability,
        resolution,
        ranges,
        elitism,
        generations = None
    ):
        """
        ranges list of pairs:
            Maxima and minima that each parameter can cover.
        resolution int:
            Number of bits for each parameter.
        generations int:
            Number of generations to cover.
        mutation_probability:
            Probability of mutation for a single bit.            
        population_size int:
            Size of population.
        elitism bool:
            If True keeps the best individual of the last generation intact.
        """
        self.f = None #Function to be maximized
        self.pop_size = population_size
        self.mp = mutation_probability
        self.generations = generations
        self.r = resolution
        self.linmap = np.array(ranges)
        self.n_param = len(self.linmap)
        self.elitism = elitism + 0
        self.total_bits = self.n_param*self.r
        self.G = np.random.randint(0,2,size=(self.pop_size,self.total_bits)) #Genetic Algorithm state. Lines are individuals.
        
    def mutation(self):
        i = self.elitism
        mutation_distribution = [self.mp, 1-self.mp]
        mask = np.random.choice([1,0], size=self.G.shape, p=mutation_distribution)#Ones change the bit and zero does not
        mutated = self.G^mask
        
        if self.elitism:
            i = self.fitness.argmax()
            elite = self.G[i].copy()
            mutated[i] = elite
        
        self.G = mutated
        
    def view(self,x,linmap):
        """
        Converts binary population matrix into real representation.
        """
        partitioned_bits = x.reshape((x.shape[0],self.n_param,self.r)) #Dividing in chinks of size self.r
        
        packed_bits = packbits(partitioned_bits)
        
        t = packed_bits/(2**self.r - 1)
        parameters = t*linmap[:,0] + (1-t)*linmap[:,1]
        return parameters
    
    def view_g(self):
        return self.view(self.g,self.linmap)
    
    def inverse_view(self,x,linmap=None):
        """
        Inverse transform of `view`
        """
        if linmap is None:
            linmap = self.linmap
        a = (2**self.r - 1)
        y = a*(x-linmap[:,1])/(linmap[:,0]-linmap[:,1])
        B = []
        for row in y:
            u = []
            for e in row:
                u+=list(np.binary_repr(e,self.r))
            B.append(np.array(u).astype(np.uint0))
        return B

    def ask_oracle(self):
        """
        Needs the function to receive the entire matrix and return a list of results equal
        to the population size.
        """
        
        parameters = self.view(self.G,self.linmap)
        #Ask Oracle
        self.fitness = np.array(self.f(parameters)) #Used for crossover. Assumes it is a list or 1d array
        self.p = softmax(self.fitness)

        
    def crossover(self):
        """
        Performs crossover generating pairs of individuals until the population matrix is full. If elistism
        is selected, the fittest individual of the last generation lives on and replaces one of the
        generated individuals.
        """
        cut = np.random.randint(0,self.total_bits)
        cross_size = self.pop_size//2 + 1
        
        pairs = np.random.choice(range(self.pop_size),p=self.p,size=(cross_size,2))
        """
        Example of children generation:
        [[0, 0, 1, 1, 1, 0],[1, 1, 1, 0, 0, 1]]
        Becomes
        [[1, 1, 1, 1, 1, 0],[0, 0, 1, 0, 0, 1]]
        On cut=2
        """
        children = np.concatenate([self.G[pairs][:,::-1,:cut],self.G[pairs][:,:,cut:]],axis=2)
        children = children.reshape((2*cross_size,self.total_bits))
        
        if self.elitism:
            i = self.fitness.argmax()
            elite = self.G[i].copy()
            children[i] = elite
            
        self.G = children[:self.pop_size,:]
            
        
    """
    TODO
    Use crossover probability and self.fitness to perform crossover.
    """
    
    
    def run(self):
        for i in range(self.generations):
            self.ask_oracle()
            self.crossover()
            self.mutation()
        self.ask_oracle()
        i = self.fitness.argmax()
        self.fittest = np.array([self.G[i]])
        x = self.view(self.fittest, np.array([self.linmap[i]]))
        return self.G, x