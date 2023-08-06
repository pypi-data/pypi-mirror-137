import abc
import math
import random
import tensorflow as tf
import typing

class BaseDeterministicFunction():
    """Base Class of Deterministic Function Classes.
    
    Deterministic functions must be sensitive to initial conditions, hence with a functor, these variables can be tracked.
    
    This object does nothing, aside from defining required contents of the functor. 
    """
    def __init__(self, **InitialConditions):
        """Creates a new Base Deterministic Function object.
        
        Args:
            InitialConditions (`dict[str, any]`, optional): Initial conditions to be saved in the object (saved in `.initial_conditions`). 
        """
        self.initial_conditions = {}
        for var in InitialConditions:
            self.initial_conditions[var] = InitialConditions[var]
    
    def __call__(self, target_object: object = None, **args):
        """See {}.call() for information.
        """.format(type(self).__name__)
        return self.call(target_object, **args)
    
    @abc.abstractmethod
    def call(self, TargetObject: object = object()):
        """Applies the functor on the input.
        
        Required functionality of all daughter classes, not implemented on base class.

        Raises:
            NotImplementedError: Functionality must be defined.
            
        Args:
            TargetObject (`object`, optional): Standard argument for daughter classes, object to be accessed in operations. Defaults to `object()`.
        """
        raise NotImplementedError("Functionality must be defined.")
    
    @abc.abstractmethod
    def reset(self):
        """Applies the functor on the input.
        
        Required functionality of all daughter classes, not implemented on base class.

        Raises:
            NotImplementedError: [description]
        """
        raise NotImplementedError("Functionality must be defined.")
    
    def __repr__(self):
        return "Deterministic Function [{}]: {}".format(type(self).__name__, self.initial_conditions)

class LorenzAttractor(BaseDeterministicFunction):
    """A Functor following a chaotic solution to the Lorenz System, a Lorenz Attractor.
    
    Calculates the partial derivatives of the attractor, given the initial conditions \u03D0, \u03C1 and \u03C3.

    Values of x, y and z can be given during calculation but when absent, randomly determined with the maximum values given in the initial conditions.
    """
    def __init__(self,
                 beta: typing.SupportsFloat = 0,
                 rho: typing.SupportsFloat = 28,
                 sigma: typing.SupportsFloat = 10,
                 x_max: typing.SupportsFloat = random.randint(0, 10000),
                 y_max: typing.SupportsFloat = random.randint(0, 10000),
                 z_max: typing.SupportsFloat = random.randint(0, 10000)):
        """Creates a new Lorenz Attractor Instance.
        
        Possible values of x, y, z in calculation is defined as uniform distribution within [0, max].

        Args:
            beta (`typing.SupportsFloat`, optional): \u03D0 to be used in calculations. Defaults to `0`.
            rho (`typing.SupportsFloat`, optional): \u03C1 to be used in calculations. Defaults to `28`.
            sigma (`typing.SupportsFloat`, optional): \u03C3 to be used in calculations. Defaults to `10`.
            x_max (`typing.SupportsFloat`, optional): Maximum value of `x` in calculation. Defaults to `random.randint(0, 10000)`.
            y_max (`typing.SupportsFloat`, optional): Maximum value of `y` in calculation. Defaults to `random.randint(0, 10000)`.
            z_max (`typing.SupportsFloat`, optional): Maximum value of `z` in calculation. Defaults to `random.randint(0, 10000)`.
        """
        super(LorenzAttractor, self).__init__(beta=beta, rho=rho, sigma=sigma)
        self.x_max, self.y_max, self.z_max = x_max, y_max, z_max
    
    def call(self,
             TargetObject: object = None,
             EntropyFunction: typing.Callable = random.uniform,
             SingleOutput: bool = False,
             var_x: typing.SupportsFloat = None,
             var_y: typing.SupportsFloat = None,
             var_z: typing.SupportsFloat = None):
        """Performs the calculation partial derivatives.
        
        If vars `var_x`, `var_y`, `var_z` is not given, x y z in calculation is determined by random.

        Args:
            target_object (`object`): Non-arbitrary (conform only to standard) object to be accessed in calculation. Defaults to `object()`.
            EntropyFunction (`typing.Callable`, optional): Randomnity function to be used in calculation, may not be used. Defaults to `random.uniform`.
            SingleOutput (`bool`, optional): Switch to single output mode, output is determined randomly from the partial derivatives calculated. Defaults to `False`.
            var_x (`typing.SupportsFloat`, optional): Optional value of x to be used in calculation. Defaults to `None`.
            var_y (`typing.SupportsFloat`, optional): Optional value of y to be used in calculation. Defaults to `None`.
            var_z (`typing.SupportsFloat`, optional): Optional value of z to be used in calculation. Defaults to `None`.

        Returns:
            tf.Constant: calculated tensor of partial derivatives.
            float (SingleOutput = True): random partial derivative calculated.
        """
        index = EntropyFunction(0, 2)
        xx = EntropyFunction(0, self.x_max) if var_x is None else float(var_x) 
        yy = EntropyFunction(0, self.y_max) if var_y is None else float(var_y)
        zz = EntropyFunction(0, self.z_max) if var_z is None else float(var_z)
        x_dot = self.initial_conditions["sigma"] * (yy - xx)
        y_dot = self.initial_conditions["rho"] * xx - yy - xx * zz
        z_dot = xx * yy - self.initial_conditions["beta"] * zz
        if SingleOutput:
            return ([x_dot, y_dot, z_dot])[int(index)]
        else:
            return tf.constant([x_dot, y_dot, z_dot])
    
    def reset(self,
              beta: typing.SupportsFloat = 0, 
              rho: typing.SupportsFloat = 28, 
              sigma: typing.SupportsFloat = 10,
              x_max: typing.SupportsFloat = None, 
              y_max: typing.SupportsFloat = None, 
              z_max: typing.SupportsFloat = None):
        """Resets the instance with new initial conditions.
        
        Maxes, when not given, will be retained. Use this function to change the initial conditions.

        Args:
            beta (`typing.SupportsFloat`, optional): \u03D0 to be used in calculations. Defaults to `0`.
            rho (`typing.SupportsFloat`, optional): \u03C1 to be used in calculations. Defaults to `28`.
            sigma (`typing.SupportsFloat`, optional): \u03C3 to be used in calculations. Defaults to `10`.
            x_max (`typing.SupportsFloat`, optional): Maximum value of `x` in calculation. Defaults to `None`.
            y_max (`typing.SupportsFloat`, optional): Maximum value of `y` in calculation. Defaults to `None`.
            z_max (`typing.SupportsFloat`, optional): Maximum value of `z` in calculation. Defaults to `None`.
        """
        self.initial_conditions["beta"] = beta
        self.initial_conditions["rho"] = rho
        self.initial_conditions["sigma"] = sigma
        self.x_max = x_max if x_max is not None else self.x_max
        self.y_max = y_max if y_max is not None else self.y_max
        self.z_max = z_max if z_max is not None else self.z_max

class HasseAlghorithm(BaseDeterministicFunction):
    """A Functor following Hasse\'s Algorithm (Collatz Conjecture); hailstone stepping systems.

    Seed given at creation is saved as initial condition, if not given, determined randomly.
    
    When algorithm, reaches lock point (i.e. `1`), a new seed is determined randomly (or can be reserved during call).
    
    Random function and random max can be defined.
    """
    def __init__(self,
                 Seed: int = None,
                 EntropyFunction: typing.Callable = random.randint,
                 EntropyLimit: int = 1000000):
        """Create a new Hasse Algorithm instance.

        Whenever the algorithm hits the lock point, a new seed is generated [1, Limit] using the entropy function.
        
        Args:
            Seed (`int`, optional): Initial seed to start hailstone stepping calculation. Defaults to None.
            EntropyFunction (`typing.Callable`, optional): Internal random function, when . Defaults to `random.randint`.
            EntropyLimit (`int`, optional): [description]. Defaults to `1000000`.
        """
        if Seed is None:
            Seed = int(EntropyFunction(1, EntropyLimit))
        super(HasseAlghorithm, self).__init__(Seed=Seed)
        self.cycle = 0
        self.current = Seed
        self.next = Seed
        self.entropy_function = EntropyFunction
        self.entropy_limit = int(EntropyLimit)
        self.hit_lock_point = False
        
    def call(self,
             TargetObject: object = None):
        self.current = self.next
        if self.hit_lock_point:
            self.reset()
        self.next = int(3 * self.current + 1) if (self.current & 1) else int(self.current / 2)
        self.hit_lock_point = True if self.current == 1 else False
        self.cycle += 1
        return self.current
    
    def reset(self,
                 Seed: int = None,
                 EntropyFunction: typing.Callable = None,
                 EntropyLimit: int = None):
        """Resets the instance with the given initial condition. Automatically called whenever the lock point is reached.

        Entropy function and limit, when not given, is retained. Use this function to change the initial condition. 
        
        Args:
            Seed (`int`, optional): Initial seed to start hailstone stepping calculation. Defaults to None.
            EntropyFunction (`typing.Callable`, optional): Internal random function, when . Defaults to `None`.
            EntropyLimit (`int`, optional): [description]. Defaults to `None`.
        """
        if Seed is None:
            Seed = int(EntropyFunction(1, EntropyLimit))
        self.initial_conditions["Seed"] = Seed
        self.cycle = 0
        self.current = Seed
        self.entropy_function = EntropyFunction if EntropyFunction is not None else self.entropy_function
        self.entropy_limit = int(EntropyLimit) if EntropyLimit is not None else self.entropy_limit
        self.hit_lock_point = False 

class CommonPiecewiseFunction(BaseDeterministicFunction):
    def __init__(self,
                 Conditionals: list = [lambda x: x < 0, lambda x: x > 0, lambda x: x == 0],
                 Functions: list = [lambda x: abs(x), lambda x: math.log10(x), lambda x: x]):
        if (len(Conditionals) < 1):
            raise ValueError("Conditional function list must contain at least one (1) function.")
        if (len(Functions) < 1):
            raise ValueError("Function list must contain at least one (1) function.")
        if (len(Conditionals) != len(Functions)):
            raise ValueError("Conditionals and Functions list do not match in length")
        super(CommonPiecewiseFunction, self).__init__(Conditionals=Conditionals,
                                                      Functions=Functions)
        
    def __repr__(self):
        return "Deterministic Function [{}]: {} Conditions, {} Functions".format(type(self).__name__, len(self.initial_conditions["Conditionals"]), len(self.initial_conditions["Functions"]))
        
    def call(self,
             TargetObject: object = None,
             Value: typing.Any = None):
        for condition, func in self.initial_conditions["Conditionals"], self.initial_conditions["Functions"]:
            if (condition(Value)):
                return func(Value)
    
    def reset(self,
              Conditionals: list = [lambda x: x < 0, lambda x: x > 0, lambda x: x == 0],
              Functions: list = [lambda x: abs(x), lambda x: math.log10(x), lambda x: x]):
        self.initial_conditions["Conditionals"] = Conditionals
        self.initial_conditions["Functions"] = Functions
