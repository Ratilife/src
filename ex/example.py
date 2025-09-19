# example.py
import os
import sys
from math import sqrt

PI = 3.14

class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return PI * (self.radius ** 2)

def greet(name):
    print(f"Hello, {name}")
