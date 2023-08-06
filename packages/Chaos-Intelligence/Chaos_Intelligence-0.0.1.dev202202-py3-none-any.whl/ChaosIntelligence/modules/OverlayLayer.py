from modules.Core import *
from modules.DeterministicFunctions import *

class OverlayLayer(CoreLayer):
    """A Chaos layer that overlays smaller pre-built layers or functions.
    
    This layer uses matches condition to a smaller pre-built layer.
    In terms, the condition acts as the `interpreter_function`.
    The `interpreter_function` makes the result of the `deterministic_function` non-trivial and usable index.
    
    Suppose data is needed to be transform depending on the deterministic function, such transformation is a finite set of operations.
    This calculates the deterministic function, and determines the function to be used using the interpreter function.
    
    This layer better to be used rather than the `CoreLayer`, since this has control structures placed to follow as intended by intepretation.
    Functionally speaking, use this class in operations and the `CoreLayer` in subclassing.
    """
    def __init__(self,
                 DeterministicFunction: typing.Callable = lambda s: 0,
                 RandomFunction: typing.Callable = lambda: random.random(),
                 InterpreterFunction: typing.Callable = None,
                 LayerSizeUnits: int = 32,
                 SuperInitArgs: dict = {},
                 DetFuncArgs: dict = {},
                 RandFuncArgs: dict = {},
                 Functions: list = [lambda s, i: tf.reduce_sum(i)],
                 **OtherVars):
        """Creates a new Overlaying Chaos Layer. A Chaos Layer can have any number functions that might be applied to input, by virtue of the Deterministic Function.

        Args:
            DeterministicFunction (`typing.Callable`, optional): Internally used deterministic function, return must be must be a numerical value. Defaults to `lambda:0`.
            RandomFunction (`typing.Callable`, optional): Internally used random function, for entropy, may be used externally by `self.use_rand()`. Defaults to `lambda:random.random()`.
            InterpreterFunction (`typing.Callable`, optional): Function used to interpret the deterministic function result. Defaults to `None`.
            LayerSizeUnits (`int`, optional): Size or Number of Units in the Layer . Defaults to `32`.
            SuperInitArgs (`dict`, optional): Arguments to be passed to `super()` initializing  `tensorflow.keras.layers.Layer`. Defaults to `{}`.
            DetFuncArgs (`dict`, optional): Optional arguments to be passed to the deterministic function when called, arguments are recorded. Defaults to `{}`.
            RandFuncArgs (`dict`, optional): Optional arguments to be passed to the random function when called, arguments are recorded. Defaults to `{}`.
            Functions (`list`, optional): List of functions that might be applied, must be at least one (1) function. Defaults to `[lambda s, i: tf.reduce_sum(i)]`.
            OtherVars (`typing.Any`, optional): Arguments that will be stored in the object, may override existing stored. Defaults to `{}`.
            
        When not `None`, the `InterpreterFunction` argument is bound as the interpreter for the results of the `DeterministicFunction` argument.        
        """
        super(OverlayLayer, self).__init__(DeterministicFunction=DeterministicFunction,
                                           RandomFunction=RandomFunction,
                                           LayerSizeUnits=LayerSizeUnits,
                                           SuperInitArgs=SuperInitArgs,
                                           DetFuncArgs=DetFuncArgs,
                                           RandFuncArgs=RandFuncArgs,
                                           Functions=Functions,
                                           OtherVars=OtherVars)
        del self.nature
        self.nature = "Overlay"
        if InterpreterFunction is not None:
            self.interpreter_function = InterpreterFunction
        for var in self.functions:
            if not callable(var):
                raise ValueError("Object in functions list [{}] is not a qualified callable object.".format(var.__repr__()))
            else:
                if not isinstance(var, layers.Layer):
                    if (var.__code__.co_argcount - (len(var.__defaults__) if var.__defaults__ is not None else 0)) > 2:
                        raise ValueError("Function in function list [{}] does not have qualified argument count.".format(var.__repr__()))

class OverlayLayerNoBlindOverride(CoreLayerNoBlindOverride):
    """A Chaos layer that overlays smaller pre-built layers or functions.
    A variation built on top of the `CoreLayerNoBlindOverride` variation.
    
    This layer uses matches condition to a smaller pre-built layer.
    In terms, the condition acts as the `interpreter_function`.
    The `interpreter_function` makes the result of the `deterministic_function` non-trivial and usable index.
    
    Suppose data is needed to be transform depending on the deterministic function, such transformation is a finite set of operations.
    This calculates the deterministic function, and determines the function to be used using the interpreter function.
    
    This layer better to be used rather than the `CoreLayer`, since this has control structures placed to follow as intended by intepretation.
    Functionally speaking, use this class in operations and the `CoreLayer` in subclassing.
    """
    def __init__(self,
                 DeterministicFunction: typing.Callable = lambda s: 0,
                 RandomFunction: typing.Callable = lambda: random.random(),
                 InterpreterFunction: typing.Callable = None,
                 LayerSizeUnits: int = 32,
                 SuperInitArgs: dict = {},
                 DetFuncArgs: dict = {},
                 RandFuncArgs: dict = {},
                 Functions: list = [lambda s, i: tf.reduce_sum(i)],
                 **OtherVars):
        """Creates a new Overlaying Chaos Layer. A Chaos Layer can have any number functions that might be applied to input, by virtue of the Deterministic Function.

        Args:
            DeterministicFunction (`typing.Callable`, optional): Internally used deterministic function, return must be must be a numerical value. Defaults to `lambda:0`.
            RandomFunction (`typing.Callable`, optional): Internally used random function, for entropy, may be used externally by `self.use_rand()`. Defaults to `lambda:random.random()`.
            InterpreterFunction (`typing.Callable`, optional): Function used to interpret the deterministic function result. Defaults to `None`.
            LayerSizeUnits (`int`, optional): Size or Number of Units in the Layer . Defaults to `32`.
            SuperInitArgs (`dict`, optional): Arguments to be passed to `super()` initializing  `tensorflow.keras.layers.Layer`. Defaults to `{}`.
            DetFuncArgs (`dict`, optional): Optional arguments to be passed to the deterministic function when called, arguments are recorded. Defaults to `{}`.
            RandFuncArgs (`dict`, optional): Optional arguments to be passed to the random function when called, arguments are recorded. Defaults to `{}`.
            Functions (`list`, optional): List of functions that might be applied, must be at least one (1) function. Defaults to `[lambda s, i: tf.reduce_sum(i)]`.
            OtherVars (`typing.Any`, optional): Arguments that will be stored in the object, may override existing stored. Defaults to `{}`.
            
        When not `None`, the `InterpreterFunction` argument is bound as the interpreter for the results of the `DeterministicFunction` argument.        
        """
        super(OverlayLayerNoBlindOverride, self).__init__(DeterministicFunction=DeterministicFunction,
                                           RandomFunction=RandomFunction,
                                           LayerSizeUnits=LayerSizeUnits,
                                           SuperInitArgs=SuperInitArgs,
                                           DetFuncArgs=DetFuncArgs,
                                           RandFuncArgs=RandFuncArgs,
                                           Functions=Functions,
                                           OtherVars=OtherVars)
        del self.nature
        self.nature = "Overlay"
        if InterpreterFunction is not None:
            self.interpreter_function = InterpreterFunction
        for var in self.functions:
            if not callable(var):
                raise ValueError("Object in functions list [{}] is not a qualified callable object.".format(var.__repr__()))
            else:
                if not isinstance(var, layers.Layer):
                    if (var.__code__.co_argcount - (len(var.__defaults__) if var.__defaults__ is not None else 0)) > 2:
                        raise ValueError("Function in function list [{}] does not have qualified argument count.".format(var.__repr__()))
       
class UniversalOverlayLayer(UniversalCoreLayer):
    """A Chaos layer that overlays smaller pre-built layers or functions.
    A variation 
    
    This layer uses matches condition to a smaller pre-built layer.
    In terms, the condition acts as the `interpreter_function`.
    The `interpreter_function` makes the result of the `deterministic_function` non-trivial and usable index.
    
    Suppose data is needed to be transform depending on the deterministic function, such transformation is a finite set of operations.
    This calculates the deterministic function, and determines the function to be used using the interpreter function.
    
    This layer better to be used rather than the `CoreLayer`, since this has control structures placed to follow as intended by intepretation.
    Functionally speaking, use this class in operations and the `CoreLayer` in subclassing.
    """
    def __init__(self,
                 Overwrite = False,
                 DeterministicFunction: typing.Callable = lambda s: 0,
                 RandomFunction: typing.Callable = lambda: random.random(),
                 InterpreterFunction: typing.Callable = None,
                 LayerSizeUnits: int = 32,
                 SuperInitArgs: dict = {},
                 DetFuncArgs: dict = {},
                 RandFuncArgs: dict = {},
                 Functions: list = [lambda s, i: tf.reduce_sum(i)],
                 **OtherVars):
        """Creates a new Overlaying Chaos Layer. A Chaos Layer can have any number functions that might be applied to input, by virtue of the Deterministic Function.

        Args:
            DeterministicFunction (`typing.Callable`, optional): Internally used deterministic function, return must be must be a numerical value. Defaults to `lambda:0`.
            RandomFunction (`typing.Callable`, optional): Internally used random function, for entropy, may be used externally by `self.use_rand()`. Defaults to `lambda:random.random()`.
            InterpreterFunction (`typing.Callable`, optional): Function used to interpret the deterministic function result. Defaults to `None`.
            LayerSizeUnits (`int`, optional): Size or Number of Units in the Layer . Defaults to `32`.
            SuperInitArgs (`dict`, optional): Arguments to be passed to `super()` initializing  `tensorflow.keras.layers.Layer`. Defaults to `{}`.
            DetFuncArgs (`dict`, optional): Optional arguments to be passed to the deterministic function when called, arguments are recorded. Defaults to `{}`.
            RandFuncArgs (`dict`, optional): Optional arguments to be passed to the random function when called, arguments are recorded. Defaults to `{}`.
            Functions (`list`, optional): List of functions that might be applied, must be at least one (1) function. Defaults to `[lambda s, i: tf.reduce_sum(i)]`.
            OtherVars (`typing.Any`, optional): Arguments that will be stored in the object, may override existing stored. Defaults to `{}`.
            
        When not `None`, the `InterpreterFunction` argument is bound as the interpreter for the results of the `DeterministicFunction` argument.        
        """
        super(UniversalOverlayLayer, self).__init__(Overwrite=Overwrite,
                                           DeterministicFunction=DeterministicFunction,
                                           RandomFunction=RandomFunction,
                                           LayerSizeUnits=LayerSizeUnits,
                                           SuperInitArgs=SuperInitArgs,
                                           DetFuncArgs=DetFuncArgs,
                                           RandFuncArgs=RandFuncArgs,
                                           Functions=Functions,
                                           OtherVars=OtherVars)
        del self.nature
        self.nature = "Overlay"
        if InterpreterFunction is not None:
            self.interpreter_function = InterpreterFunction
        for var in self.functions:
            if not callable(var):
                raise ValueError("Object in functions list [{}] is not a qualified callable object.".format(var.__repr__()))
            else:
                if not isinstance(var, layers.Layer):
                    if (var.__code__.co_argcount - (len(var.__defaults__) if var.__defaults__ is not None else 0)) > 2:
                        raise ValueError("Function in function list [{}] does not have qualified argument count.".format(var.__repr__()))

def _Overlay_test_qualified_chaos_overlay(TargetName: typing.Any,
                                          **InitArgs):
    internal = TargetName(**InitArgs) if isclass(TargetName) else TargetName
    if not _Core_test_qualified_chaos_core(internal):
        return False
    if not _Core_test_standard_deterministic_function(internal.deterministic_function):
        return False
    for var in internal.functions:
        if not _Core_test_standard_functionality(var):
            return False
    return True
