from copy import deepcopy
from inspect import isclass
import random
import tensorflow as tf
from tensorflow.keras import layers
import typing

class CoreLayer(layers.Layer):
    """The Base Class of Chaotic Layers. Follows Keras Functional API.
    
    Applies a different function by virtue of deterministic function.
    
    This Base Class serves as fundamental building block of all Chaotic Layers."""
    def __init__(self,
                 DeterministicFunction: typing.Callable = lambda s: 0,
                 RandomFunction: typing.Callable = lambda: random.random(),
                 LayerSizeUnits: int = 32,
                 SuperInitArgs: dict = {},
                 DetFuncArgs: dict = {},
                 RandFuncArgs: dict = {},
                 Functions: list = [lambda s, i: tf.reduce_sum(i)],
                 **OtherVars):
        """Creates a new Chaos Core Layer. A Chaos Layer can have any number functions that might be applied to input, by virtue of the Deterministic Function.

        Args:
            DeterministicFunction (`typing.Callable`, optional): Internally used deterministic function, return must be must be a numerical value. Defaults to `lambda:0`.
            RandomFunction (`typing.Callable`, optional): Internally used random function, for entropy, may be used externally by `self.use_rand()`. Defaults to `lambda:random.random()`.
            LayerSizeUnits (`int`, optional): Size or Number of Units in the Layer . Defaults to `32`.
            SuperInitArgs (`dict`, optional): Arguments to be passed to `super()` initializing  `tensorflow.keras.layers.Layer`. Defaults to `{}`.
            DetFuncArgs (`dict`, optional): Optional arguments to be passed to the deterministic function when called, arguments are recorded. Defaults to `{}`.
            RandFuncArgs (`dict`, optional): Optional arguments to be passed to the random function when called, arguments are recorded. Defaults to `{}`.
            Functions (`list`, optional): List of functions that might be applied, must be at least one (1) function. Defaults to `[lambda s, i: tf.reduce_sum(i)]`.
            OtherVars (`typing.Any`, optional): Arguments that will be stored in the object, may override existing stored. Defaults to `{}`.
            
        The result of the deterministic function maybe trivial, hence use the additional argument `interpreter_function=` to bind an interpreter.
        """
        if (len(Functions) < 1):
            raise ValueError("Function list must contain at least one (1) function.")
        super(CoreLayer, self).__init__(**SuperInitArgs)
        self.nature = "Core"
        self.deterministic_function = DeterministicFunction
        self.entropy_function = RandomFunction
        self.functions = Functions
        self.local_history = {"dfunc_args": DetFuncArgs, "rfunc_args": RandFuncArgs}
        self.units = LayerSizeUnits
        for var in OtherVars:
            setattr(self, var, OtherVars[var])
        
    def __repr__(self):
        return "Chaos {} Layer [{}]: {} unit(s), {} function(s)".format(self.nature, self.name, self.units, len(self.functions))
    
    def ensure_in_range(self, index: typing.SupportsFloat):
        if hasattr(self, "interpreter_function"):
            return self.interpreter_function(index)
        return int((index * len(self.functions)) % len(self.functions))
    
    def call(self,
             inputs:tf.Tensor):
        """Computes input tensor.
        
        Calculates the deterministic function given the saved arguments.
        Current input and calculated entropy, is saved at `local_history`

        Args:
            inputs (tf.Tensor): input tensor to be computed.

        Returns:
            tf.Tensor: computed tensor.
        """
        self.local_history["current_input"] = input
        self.local_history["current_entropy"] = self.use_rand()
        index = self.ensure_in_range(self.deterministic_function(self, **self.local_history["dfunc_args"]))
        self.local_history["current_targetfunc"] = index
        return self.functions[index](self, inputs)
        
    def build(self,
              input_shape: typing.Iterable,
              WeightArgs: dict = {},
              BiasArgs: dict = {}):
        """Builds chaos layer.

        Args:
            input_shape (typing.Iterable): iterable shape of inputs.
            WeightArgs (dict, optional): Arguments to be passed on `self.add_weight()` for `self.w`, with exception to be shape. Defaults to {}.
            BiasArgs (dict, optional): Arguments to be passed on `self.add_weight()` for `self.b`, with exception of the shape. Defaults to {}.
        """
        self.w = self.add_weight(
            shape=(input_shape[-1], self.units),
            **WeightArgs
        )
        self.b = self.add_weight(
            shape=(self.units,),
            **BiasArgs
        )
        
    def use_rand(self, NewArgs = None):
        if NewArgs is not None:
            self.local_history["rfunc_args"] = NewArgs
        return self.entropy_function(**self.local_history["rfunc_args"])if isinstance(self.local_history["rfunc_args"], dict) else self.entropy_function(self.local_history["rfunc_args"])
    
class CoreLayerNoBlindOverride(layers.Layer):
    """A Variation of Base Class of Chaotic Layers. Follows Keras Functional API.
    
    Applies a different function by virtue of deterministic function.
    No Blind Ovveride means that hidden overriding feature is disabled.
    
    This Base Class serves as fundamental building block of all Chaotic Layers."""
    def __init__(self,
                 DeterministicFunction: typing.Callable = lambda s: 0,
                 RandomFunction: typing.Callable = lambda: random.random(),
                 LayerSizeUnits: int = 32,
                 SuperInitArgs: dict = {},
                 DetFuncArgs: dict = {},
                 RandFuncArgs: dict = {},
                 Functions: list = [lambda s, i: tf.reduce_sum(i)],
                 **OtherVars):
        """Creates a new Chaos Core Layer. A Chaos Layer can have any number functions that might be applied to input, by virtue of the Deterministic Function.

        Args:
            DeterministicFunction (`typing.Callable`, optional): Internally used deterministic function, return must be must be a numerical value. Defaults to `lambda:0`.
            RandomFunction (`typing.Callable`, optional): Internally used random function, for entropy, may be used externally by `self.use_rand()`. Defaults to `lambda:random.random()`.
            LayerSizeUnits (`int`, optional): Size or Number of Units in the Layer . Defaults to `32`.
            SuperInitArgs (`dict`, optional): Arguments to be passed to `super()` initializing  `tensorflow.keras.layers.Layer`. Defaults to `{}`.
            DetFuncArgs (`dict`, optional): Optional arguments to be passed to the deterministic function when called, arguments are recorded. Defaults to `{}`.
            RandFuncArgs (`dict`, optional): Optional arguments to be passed to the random function when called, arguments are recorded. Defaults to `{}`.
            Functions (`list`, optional): List of functions that might be applied, must be at least one (1) function. Defaults to `[lambda s, i: tf.reduce_sum(i)]`.
            OtherVars (`typing.Any`, optional): Arguments that will be stored in the object, may override existing stored. Defaults to `{}`.
            
        The result of the deterministic function maybe trivial, hence use the additional argument `interpreter_function=` to bind an interpreter.
        """
        if (len(Functions) < 1):
            raise ValueError("Function list must contain at least one (1) function.")
        super(CoreLayerNoBlindOverride, self).__init__(**SuperInitArgs)
        self.nature = "Core"
        self.deterministic_function = DeterministicFunction
        self.entropy_function = RandomFunction
        self.functions = Functions
        self.local_history = {"dfunc_args": DetFuncArgs, "rfunc_args": RandFuncArgs}
        self.units = LayerSizeUnits
        for var in OtherVars:
            if hasattr(self, var):
                continue
            setattr(self, var, OtherVars[var])
        
    def __repr__(self):
        return "Chaos {} Layer [{}]: {} unit(s), {} function(s)".format(self.nature, self.name, self.units, len(self.functions))
    
    def ensure_in_range(self, index: typing.SupportsFloat):
        if hasattr(self, "interpreter_function"):
            return self.interpreter_function(index)
        return int((index * len(self.functions)) % len(self.functions))
    
    def call(self,
             inputs:tf.Tensor):
        """Computes input tensor.
        
        Calculates the deterministic function given the saved arguments.
        Current input and calculated entropy, is saved at `local_history`

        Args:
            inputs (tf.Tensor): input tensor to be computed.

        Returns:
            tf.Tensor: computed tensor.
        """
        self.local_history["current_input"] = input
        self.local_history["current_entropy"] = self.use_rand()
        index = self.ensure_in_range(self.deterministic_function(self, **self.local_history["dfunc_args"]))
        self.local_history["current_targetfunc"] = index
        return self.functions[index](self, inputs)
        
    def build(self,
              input_shape: typing.Iterable,
              WeightArgs: dict = {},
              BiasArgs: dict = {}):
        """Builds chaos layer.

        Args:
            input_shape (typing.Iterable): iterable shape of inputs.
            WeightArgs (dict, optional): Arguments to be passed on `self.add_weight()` for `self.w`, with exception to be shape. Defaults to {}.
            BiasArgs (dict, optional): Arguments to be passed on `self.add_weight()` for `self.b`, with exception of the shape. Defaults to {}.
        """
        self.w = self.add_weight(
            shape=(input_shape[-1], self.units),
            **WeightArgs
        )
        self.b = self.add_weight(
            shape=(self.units,),
            **BiasArgs
        )
        
    def use_rand(self, NewArgs = None):
        if NewArgs is not None:
            self.local_history["rfunc_args"] = NewArgs
        return self.entropy_function(**self.local_history["rfunc_args"]) if isinstance(self.local_history["rfunc_args"], dict) else self.entropy_function(self.local_history["rfunc_args"])
    
class UniversalCoreLayer(layers.Layer):
    """A Universal Variation of the Base Class of Chaotic Layers. Follows Keras Functional API.
    
    Applies a different function by virtue of deterministic function.
    
    This Base Class serves as fundamental building block of all Chaotic Layers."""
    def __init__(self,
                 Overwrite = False,
                 DeterministicFunction: typing.Callable = lambda s: 0,
                 RandomFunction: typing.Callable = lambda: random.random(),
                 LayerSizeUnits: int = 32,
                 SuperInitArgs: dict = {},
                 DetFuncArgs: dict = {},
                 RandFuncArgs: dict = {},
                 Functions: list = [lambda s, i: tf.reduce_sum(i) * s.b],
                 **OtherVars):
        """Creates a new Chaos Core Layer. A Chaos Layer can have any number functions that might be applied to input, by virtue of the Deterministic Function.

        Overwriting is controlled by the `Overwrite` argument.
        When `True`, object creation will cause all named variables in `OtherVars` be overwritten.

        Args:
            DeterministicFunction (`typing.Callable`, optional): Internally used deterministic function, return must be must be a numerical value. Defaults to `lambda:0`.
            RandomFunction (`typing.Callable`, optional): Internally used random function, for entropy, may be used externally by `self.use_rand()`. Defaults to `lambda:random.random()`.
            LayerSizeUnits (`int`, optional): Size or Number of Units in the Layer . Defaults to `32`.
            SuperInitArgs (`dict`, optional): Arguments to be passed to `super()` initializing  `tensorflow.keras.layers.Layer`. Defaults to `{}`.
            DetFuncArgs (`dict`, optional): Optional arguments to be passed to the deterministic function when called, arguments are recorded. Defaults to `{}`.
            RandFuncArgs (`dict`, optional): Optional arguments to be passed to the random function when called, arguments are recorded. Defaults to `{}`.
            Functions (`list`, optional): List of functions that might be applied, must be at least one (1) function. Defaults to `[lambda s, i: tf.reduce_sum(i)]`.
            OtherVars (`typing.Any`, optional): Arguments that will be stored in the object, may override existing stored. Defaults to `{}`.
            
        The result of the deterministic function maybe trivial, hence use the additional argument `interpreter_function=` to bind an interpreter.
        """
        if (len(Functions) < 1):
            raise ValueError("Function list must contain at least one (1) function.")
        super(UniversalCoreLayer, self).__init__(**SuperInitArgs)
        self.nature = "Core"
        self.deterministic_function = DeterministicFunction
        self.entropy_function = RandomFunction
        self.functions = Functions
        self.local_history = {"dfunc_args": DetFuncArgs, "rfunc_args": RandFuncArgs}
        self.units = LayerSizeUnits
        for var in OtherVars:
            if Overwrite:
                setattr(self, var, OtherVars[var])
        
    def __repr__(self):
        return "Chaos {} Layer [{}]: {} unit(s), {} function(s)".format(self.nature, self.name, self.units, len(self.functions))
    
    def ensure_in_range(self, index: typing.SupportsFloat):
        if hasattr(self, "interpreter_function"):
            return self.interpreter_function(index)
        return int((index * len(self.functions)) % len(self.functions))
    
    def call(self,
             inputs:tf.Tensor):
        """Computes input tensor.
        
        Calculates the deterministic function given the saved arguments.
        Current input and calculated entropy, is saved at `local_history`

        Args:
            inputs (tf.Tensor): input tensor to be computed.

        Returns:
            tf.Tensor: computed tensor.
        """
        self.local_history["current_input"] = input
        self.local_history["current_entropy"] = self.use_rand()
        index = self.ensure_in_range(self.deterministic_function(self, **self.local_history["dfunc_args"]))
        self.local_history["current_targetfunc"] = index
        return self.functions[index](self, inputs) if not isinstance(self.functions[index], layers.Layer) else self.functions[index](inputs)
        
    def build(self,
              input_shape: typing.Iterable,
              WeightArgs: dict = {},
              BiasArgs: dict = {}):
        """Builds chaos layer.

        Args:
            input_shape (typing.Iterable): iterable shape of inputs.
            WeightArgs (dict, optional): Arguments to be passed on `self.add_weight()` for `self.w`, with exception to be shape. Defaults to {}.
            BiasArgs (dict, optional): Arguments to be passed on `self.add_weight()` for `self.b`, with exception of the shape. Defaults to {}.
        """
        self.w = self.add_weight(
            shape=(input_shape[-1], self.units),
            **WeightArgs
        )
        self.b = self.add_weight(
            shape=(self.units,),
            **BiasArgs
        )
        
    def use_rand(self, NewArgs = None):
        if NewArgs is not None:
            self.local_history["rfunc_args"] = NewArgs
        return self.entropy_function(**self.local_history["rfunc_args"])if isinstance(self.local_history["rfunc_args"], dict) else self.entropy_function(self.local_history["rfunc_args"])
    
def _Core_test_standard_deterministic_function(TargetCallable: typing.Any,
                                               **InitArgs):
    """Tests whether `TargetCallable` follows standard deterministic function specifications.

    If `TargetCallable` is a class, initialization arguments can be specified for instatialization.
    Otherwise, creates a copy of `TargetCallable` with `copy.deepcopy` to prevent unwanted usage of object.

    Args:
        TargetCallable (`typing.Any`): Class name or object to be tested.

    Returns:
        `bool`: True if the target object passes test, otherwise False.
    """
    var = TargetCallable(**InitArgs) if isclass(TargetCallable) else deepcopy(TargetCallable)
    if not callable(var):
        return False
    else:
        if isclass(TargetCallable):
            if (var.__call__.__code__.co_argcount - (len(var.__call__.__defaults__) if var.__call__.__defaults__ is not None else 0)) > 2:
                return False
        else:
            if (var.__code__.co_argcount - (len(var.__defaults__) if var.__defaults__ is not None else 0)) > 2:
                return False
    return True
    
def _Core_test_standard_entropy_function(TargetCallable: typing.Any,
                                         Threshold: typing.SupportsFloat,
                                         Tolerance: float = 15,
                                         TestCyle: int = 100,
                                         InitArgs = {},
                                         **EntropyArgs):
    """Tests whether `TargetCallable` follows standard entropy function specifications.

    If `TargetCallable` is a class, initialization arguments can be specified for instatialization in argument `InitArgs`.
    Otherwise, creates a copy of `TargetCallable` with `copy.deepcopy` to prevent unwanted usage of object.

    Arguments to be passed to the random function can be optionally specified.
    
    As a rule, entropy must be a pseudo-random, hence a threshold and tolerance must be specified.
    Therefore, random mean must be within the threshold tolerances to pass this test.
    For widely random entropy functions, the centroid of peak and trough is recommended to be specified while a tolerance of percent apparent to peak/trough.
    
    Args:
        TargetCallable (`typing.Any`): Class name or object to be tested.
        Threshold (`typing.SupportsFloat`): Randomnity threshold, mean within the test cycle.
        Tolerance (`float`): Percent tolerance of threshold. Defaults to `15`.
        TestCyle (`int`, optional): Amount of random uses. Defaults to `100`.
        InitArgs (`dict`, optional): Initialization arguments to be used when `TargetCallable` is a class name. Defaults to `{}`.

    Returns:
        `bool`: True if the target object passes test, otherwise False.
    """
    if not callable(TargetCallable):
        return False
    var = TargetCallable(**InitArgs) if isclass(TargetCallable) else deepcopy(TargetCallable)
    buffer = 0.0
    cycle = 0
    while cycle < TestCyle:
        buffer += abs(var(**EntropyArgs))
    return bool((Threshold * (1 - (Tolerance / 100))) <= (buffer / (cycle + 1)) <= (Threshold * (1 + (Tolerance / 100))))

def _Core_test_standard_functionality(TargetCallable: typing.Any,
                                      **InitArgs):
    """Tests whether `TargetCallable` follows standard chaos layer functionality specifications.
    
    If `TargetCallable` is a class, initialization arguments can be specified for instatialization.
    Otherwise, creates a copy of `TargetCallable` with `copy.deepcopy` to prevent unwanted usage of object.

    Args:
        TargetCallable (`typing.Any`): Class name or object to be tested.

    Returns:
        `bool`: True if the target object passes test, otherwise False.
    """
    var = TargetCallable(**InitArgs) if isclass(TargetCallable) else TargetCallable
    if not callable(var):
        return False
    else:
        if not isinstance(var, layers.Layer):
            if isclass(TargetCallable):
                if (var.__call__.__code__.co_argcount - (len(var.__call__.__defaults__) if var.__call__.__defaults__ is not None else 0)) > 2:
                    return False
            else:
                if (var.__code__.co_argcount - (len(var.__defaults__) if var.__defaults__ is not None else 0)) > 2:
                    return False
    return True
    
def _Core_test_qualified_chaos_core(TargetName: typing.Any,
                                    **InitArgs):
    """Tests whether `TargetName` is a qualified subclass of a chaos layer.

    If `TargetName` is a class, initialization arguments can be specified for instatialization.
    Otherwise, creates a copy of `TargetName` with `copy.deepcopy` to prevent unwanted usage of object.

    Args:
        TargetName (`typing.Any`): Class name or object to be tested.

    Returns:
        `bool`: True if the target object passes test, otherwise False.
    """
    if not isclass(TargetName):
        if not issubclass(TargetName, layers.Layer):
            return False
    else:
        if not isinstance(TargetName, layers.Layer):
            return False
    var = TargetName(**InitArgs) if isclass(TargetName) else TargetName
    if not callable(var):
        return False
    if not (hasattr(var, "deterministic_function")
            and hasattr(var, "entropy_function")
            and hasattr(var, "functions")
            and hasattr(var, "local_history")):
        return False
    return True
    
def MakeCoreLayer(TargetObject: layers.Layer,
                  TargetCoreLayerName: typing.Any = CoreLayer,
                  Specifics: list = [],
                  **InitArgs):
    """Converts `TargetObject` to an Chaos Core Layer variation as specified in `TargetCoreLayerName`.
    
    This creates a new instance of `TargetCoreLayerName` with initialization parameters specified.
    When an attribute already exists in this new instance, value shall not be copied over.
    However, excluding those specified as initialization arguments, value shall be forced to be copied over from `TargetObject` when specified in `Specifics`.

    When specified attribute exists already in the new instance, it will be attempted to be deleted to have clean copy over.
    This, however, can cause an error when the object denies attribute deletion.

    This function does not overwrite-converts `TargetObject`.

    Args:
        TargetObject (`layers.Layer`): Object whose data shall be copied over and be converted.
        TargetCoreLayerName (`typing.Any`, optional): Specific variation of Chaos Core Layer. Defaults to CoreLayer.
        Specifics (`list`, optional): Specific attributes to be forced copied over. Defaults to [].

    Raises:
        ValueError: Thrown when `TargetObject` is already a subclass of a Chaos Core variation.
        ValueError: Thrown when `TargetCoreLayerName` is a Chaos Core Variation.

    Returns:
        (`CoreLayer` | `ChaosLayerNoBlindOverride` | `UniversalCoreLayer`): Conversion result.
    """
    if isinstance(TargetObject, (CoreLayer, CoreLayerNoBlindOverride, UniversalCoreLayer)):
        raise ValueError("`TargetObject` is already a core layer instance")
    if TargetCoreLayerName not in (CoreLayer, CoreLayerNoBlindOverride, UniversalCoreLayer):
        raise ValueError("`TargetCoreLayerName` must be either CoreLayer, CoreLayerNoBlindOverride or UniversalCoreLayer")
    buf = TargetCoreLayerName(**InitArgs)
    internal = deepcopy(TargetObject)
    data = [x for x in dir(internal) if x not in dir(buf)]
    for ii in data:
        setattr(buf, ii, getattr(internal, ii))
    for ii in Specifics:
        if not hasattr(internal, ii) or ii in InitArgs.keys():
            continue
        if hasattr(buf, ii):
            delattr(buf, ii) if not callable(getattr(buf, ii)) else None
        setattr(buf, ii, getattr(internal, ii))
    return buf

def __common_core_private_repr__(self):
    return "Chaos {} Layer [{}]: {} unit(s), {} function(s)".format(self.nature, self.name, self.units, len(self.functions))

def __common_core_public_build__(self,
                                 input_shape: typing.Iterable,
                                 WeightArgs: dict = {},
                                 BiasArgs: dict = {}):
    """Builds chaos layer.

    Args:
        input_shape (typing.Iterable): iterable shape of inputs.
        WeightArgs (dict, optional): Arguments to be passed on `self.add_weight()` for `self.w`, with exception to be shape. Defaults to {}.
        BiasArgs (dict, optional): Arguments to be passed on `self.add_weight()` for `self.b`, with exception of the shape. Defaults to {}.
    """
    self.w = self.add_weight(
        shape=(input_shape[-1], self.units),
        **WeightArgs
    )
    self.b = self.add_weight(
        shape=(self.units,),
        **BiasArgs
    )
    
def __common_core_public_call__(self,
                                inputs:tf.Tensor):
    """Computes input tensor.

    Calculates the deterministic function given the saved arguments.
    Current input and calculated entropy, is saved at `local_history`

    Args:
        inputs (tf.Tensor): input tensor to be computed.

    Returns:
        tf.Tensor: computed tensor.
    """
    self.local_history["current_input"] = input
    self.local_history["current_entropy"] = self.use_rand()
    index = self.ensure_in_range(self.deterministic_function(self, **self.local_history["dfunc_args"]))
    self.local_history["current_targetfunc"] = index
    return self.functions[index](self, inputs) if not isinstance(self.functions[index], layers.Layer) else self.functions[index](inputs)

def WrapToCoreLayer(TargetObject: layers.Layer,
                    TargetCoreLayerName: typing.Any = CoreLayer,
                    DeterministicFunction: typing.Callable = lambda s: 0,
                    RandomFunction: typing.Callable = lambda: random.random(),
                    LayerSizeUnits: int = 32,
                    DetFuncArgs: dict = {},
                    RandFuncArgs: dict = {},
                    Functions: list = [lambda s, i: tf.reduce_sum(i)],
                    RepresentationFunction: typing.Callable = __common_core_private_repr__,
                    BuildFunction: typing.Callable = __common_core_public_build__,
                    CallFunction: typing.Callable = __common_core_public_call__,
                    **OtherVars):
    """Wraps `TargetObject` to be a Chaos Core Layer variation `TargetCoreLayerName`.
    
    This function converts `TargetObject` by binding standard attributes using `setattr`.
    Therefore, the behavior of this function is subject to the overwritability of the attributes.

    Args:
        TargetObject (`layers.Layer`): Object whose data shall be copied over and be wrapped.
        TargetCoreLayerName (`typing.Any`, optional): Specific variation of Chaos Core Layer. Defaults to CoreLayer.
        DeterministicFunction (`typing.Callable`, optional): Internally used deterministic function, return must be must be a numerical value. Defaults to `lambda:0`.
        RandomFunction (`typing.Callable`, optional): Internally used random function, for entropy, may be used externally by `self.use_rand()`. Defaults to `lambda:random.random()`.
        LayerSizeUnits (`int`, optional): Size or Number of Units in the Layer . Defaults to `32`.
        DetFuncArgs (`dict`, optional): Optional arguments to be passed to the deterministic function when called, arguments are recorded. Defaults to `{}`.
        RandFuncArgs (`dict`, optional): Optional arguments to be passed to the random function when called, arguments are recorded. Defaults to `{}`.
        Functions (`list`, optional): List of functions that might be applied, must be at least one (1) function. Defaults to `[lambda s, i: tf.reduce_sum(i)]`.
        RepresentationFunction (typing.Callable, optional): `__repr__` to be bound, overwrites previously bound function. Defaults to __common_core_private_repr__.
        BuildFunction (typing.Callable, optional): `build` function to be bound, overwrites previously bound function. Defaults to __common_core_public_build__.
        CallFunction (typing.Callable, optional): `call` function to be bound, overwrites previously bound function. Defaults to __common_core_public_call__.

    Raises:
        ValueError: Thrown when `TargetObject` is already a subclass of a Chaos Core variation.
        ValueError: Thrown when `TargetCoreLayerName` is a Chaos Core Variation.

    Returns:
        (`CoreLayer` | `ChaosLayerNoBlindOverride` | `UniversalCoreLayer`): Conversion result.
    """
    if isinstance(TargetObject, (CoreLayer, CoreLayerNoBlindOverride, UniversalCoreLayer)):
        raise ValueError("`TargetObject` is already a core layer instance")
    if TargetCoreLayerName not in (CoreLayer, CoreLayerNoBlindOverride, UniversalCoreLayer):
        raise ValueError("`TargetCoreLayerName` must be either CoreLayer, CoreLayerNoBlindOverride or UniversalCoreLayer")
    internal = deepcopy(TargetObject)
    internal.__class__ = TargetCoreLayerName
    setattr(internal, "__repr__", RepresentationFunction)
    setattr(internal, "build", BuildFunction)
    setattr(internal, "call", CallFunction)
    setattr(internal, "nature", "Core")
    setattr(internal, "deterministic_function", DeterministicFunction)
    setattr(internal, "entropy_function", RandomFunction)
    setattr(internal, "functions", Functions)
    setattr(internal, "local_history", {"dfunc_args": DetFuncArgs, "rfunc_args": RandFuncArgs})
    setattr(internal, "units", LayerSizeUnits)
    for var in OtherVars:
        setattr(internal, var, OtherVars[var])
    return internal
