# Chaos-Intelligence

A Layer API built on top of `tensorflow.keras` Functional API. Allows application of chaos theory deterministic functions to neural networks.

A dataset is said to be deterministic chaotic when:

1. Sensitive to initial conditions;
2. Topologically transistive; and
3. Have dence periodic orbits

![Chaos Dynamics Image]()

The API can be thought as an API that is used to specialize a model for a specific chaotic data model. It provides tools to make dynamically changing layers; responsive to the deterministic function.
