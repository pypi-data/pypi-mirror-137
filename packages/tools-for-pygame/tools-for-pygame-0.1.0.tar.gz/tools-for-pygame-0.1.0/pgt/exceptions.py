#!/usr/bin/env python3

class InvalidPosError(Exception):
    """Exception raised when an element has an invalid position"""
    pass


class EmptyStackError(Exception):
    """Exception raised when trying to get a value from an empty stack"""
    pass
