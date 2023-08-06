<img src="https://runnalls.s3.eu-central-1.amazonaws.com/makalogo.png" width="200" height="200" />

## Online script monitoring and control

## Installation

Install the MAKA python package from PYPI:

`pip install maka`

## Usage

```python
from maka import monitor

m = monitor("1Afn2445nb5b5", "log")

m.log("Testing")
m.error("Testing")
```