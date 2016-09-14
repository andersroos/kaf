import re

rules = []

def rule(regex, builder):
    regex = re.compile(regex)
    rules.append((regex, builder))


__all__ = ["rule"]

