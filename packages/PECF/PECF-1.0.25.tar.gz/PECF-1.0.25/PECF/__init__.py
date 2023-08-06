__author__ = "Zedikon"
__copyright__ = "Copyright zedikon 2022, all rights reserved."
__version__ = "1.0.23"
__emal__ = "mrzedikon@gmail.com"


stack = []

tokens = {
    "meaning": ":",
    "string": "str",
    "integer": "int",
    "next": ","
}

def decode(x, name):
    stack.append(x)
    strstack = tokens["next"].join(stack)
    try:
        result = strstack.split()
        positions = result.index(name + ":")
        try:
            if result[positions + 2] == tokens["string"]:
                res = str(result[positions + 1])
                return res
            if result[positions + 2] == tokens["integer"]:
                res = int(result[positions + 1])
                return res
            else:
                return result[positions + 1]
        except Exception:
            return result[positions + 1]
    except Exception:
        return f"PECF: Sorry, but i can't find {name} variable."