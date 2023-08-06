# attlesnake: Attitude Dynamics in Python

A Python library for handling rigid body attitude dynamics (tailored for spacecraft).

## Installation

Install with pip:

```bash
pip install attlesnake
```


## Basic Usage

```python
>>> import numpy as np
>>> import attlesnake as att
>>> ea321 = att.EulerAngle321(np.pi/2, 0, 0)
>>> print(ea321)
1.5708, 0.0000, 0.0000
>>> dcm = att.DCM.from_ea321(ea321)
>>> print(dcm)
0.0,	1.0,	-0.0
-1.0,	0.0,	0.0
0.0,	0.0,	1.0
```
