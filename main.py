# Alan Thomas
# 107846842
# CSE 307

import sys
import tpg

class SemanticError(Exception):
    """
    This is the class of the exception that is raised when a semantic error
    occurs.
    """

# These are the nodes of our abstract syntax tree.
class Node(object):
    """
    A base class for nodes. Might come in handy in the future.
    """

    def evaluate(self):
        """
        Called on children of Node to evaluate that child.
        """
        raise Exception("Not implemented.")

class IntLiteral(Node):
    """
    A node representing integer literals.
    """

    def __init__(self, value):
        self.value = int(value)

    def evaluate(self):
        return self.value

class RealLiteral(Node):
    """
    A node representing real literals.
    """

    def __init__(self, value):
        self.value = float(value)

    def evaluate(self):
        return self.value

class StringLiteral(Node):
    """
    A node representing string literals.
    """

    def __init__(self, value):
        self.value = value[1:len(value)-1]

    def evaluate(self):
        return self.value

class Array(Node):
    """
    A node representing arrays
    """

    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

class Or(Node):
    """
    A node representing boolean OR.
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int):
            raise SemanticError()
        if not isinstance(right, int):
            raise SemanticError()
        return 1 if (left or right) else 0

class Not(Node):
    """
    A node representing boolean NOT.
    """

    def __init__(self, child):
        self.child = child

    def evaluate(self):
        child = self.child.evaluate()
        if not isinstance(child, int):
            raise SemanticError()
        return 1 if (not child) else 0

class And(Node):
    """
    A node representing boolean AND.
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int):
            raise SemanticError()
        if not isinstance(right, int):
            raise SemanticError()
        return 1 if (left and right) else 0

class Comparison(Node):
    """
    A node representing boolean comparison.
    """

    def __init__(self, left, op, right):
        self.left = left
        self.right = right
        self.op = op

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        op = self.op
        if not isinstance(left, int):
            raise SemanticError()
        if not isinstance(right, int):
            raise SemanticError()
        if op == ">":
            return 1 if(left > right) else 0
        elif op == ">=":
            return 1 if(left >= right) else 0
        elif op == "<":
            return 1 if(left < right) else 0
        elif op == "<=":
            return 1 if(left <= right) else 0
        elif op == "==":
            return 1 if(left == right) else 0
        elif op == "<>":
            return 1 if ((left and not right) or (not left and right)) else 0
        else:
            return 0

class In(Node):
    """
    A node representing the 'in' operation.
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not (isinstance(right, list) or isinstance(right, str)):
            raise SemanticError()
        if (isinstance(right, str) and not isinstance(left, str) ):
            raise SemanticError()
        if (isinstance(right, list)):
            for r in right:
                if r.evaluate() == left:
                    return 1
            return 0
        else:
            return 1 if(left in right) else 0

class Floordiv(Node):
    """
    A node representing floor division.
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int):
            raise SemanticError()
        if not isinstance(right, int):
            raise SemanticError()
        return left//right

class Modulus(Node):
    """
    A node representing modulus.
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int):
            raise SemanticError()
        if not isinstance(right, int):
            raise SemanticError()
        return left%right

class Exponent(Node):
    """
    A node representing exponent.
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int):
            raise SemanticError()
        if not isinstance(right, int):
            raise SemanticError()
        return left**right

class Index(Node):
    """
    A node representing exponent.
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not (isinstance(left, list) or isinstance(left, str)):
            raise SemanticError()
        if not isinstance(right, int):
            raise SemanticError()
        if isinstance(left, list):
            try:
                return left[right].evaluate()
            except IndexError:
                raise SemanticError()
        else:
            try:
                return left[right]
            except IndexError:
                raise SemanticError()

class Add(Node):
    """
    A node representing addition.
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()

        if (isinstance(left, str) and not isinstance(right, str)):
            raise SemanticError()
        if (not isinstance(left, str) and isinstance(right, str)):
            raise SemanticError()
        if (isinstance(left, list) and not isinstance(right, list)):
            raise SemanticError()
        if (not isinstance(left, list) and isinstance(right, list)):
            raise SemanticError()

        return left + right

class Subtract(Node):
    """
    A node representing subtraction.
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not isinstance(left, int):
            raise SemanticError()
        if not isinstance(right, int):
            raise SemanticError()
        return left - right

class Multiply(Node):
    """
    A node representing multiplication.
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not (isinstance(left, int) or isinstance(left, float)):
            raise SemanticError()
        if not (isinstance(right, int) or isinstance(right, float)):
            raise SemanticError()
        return left * right

class Divide(Node):
    """
    A node representing division
    """

    def __init__(self, left, right):
        # The nodes representing the left and right sides of this
        # operation.
        self.left = left
        self.right = right

    def evaluate(self):
        left = self.left.evaluate()
        right = self.right.evaluate()
        if not (isinstance(left, int) or isinstance(left, float)):
            raise SemanticError()
        if not (isinstance(right, int) or isinstance(right, float)):
            raise SemanticError()
        if right == 0:
            raise SemanticError()
        ret = left / right
        if ret.is_integer():
            return int(ret)
        else:
            return ret

def make_op(s):
    return {
    '+': lambda x,y: x+y,
    '-': lambda x,y: x-y,
    '*': lambda x,y: x*y,
    '/': lambda x,y: x/y,
    }[s]

# This is the TPG Parser that is responsible for turning our language into
# an abstract syntax tree.
class Parser(tpg.Parser):
    """
    token string '\"[^\";]+\"' StringLiteral;
    token real  '(\d+\.\d*|\d*\.\d+)' RealLiteral;
    token int   '\d+' IntLiteral;

    separator spaces '\s+';

    START/a -> expression/a ;

    expression/a -> boolor/a ;

    boolor/a -> booland/a ( "or" booland/b $ a = Or(a,b) $ )* ;

    booland/a -> boolnot/a ( "and" boolnot/b $ a = And(a,b) $ )* ;

    boolnot/a -> comparison/a | "not" expression/b $ a = Not(b) $ ;

    comparison/a -> isin/a (
    ("<>"/op | "<="/op | ">="/op | "=="/op | "<"/op | ">"/op)
    isin/b $ a = Comparison(a, op, b) $ )* ;

    isin/a -> addsub/a ("in" addsub/b $ a = In(a, b) $ )* ;

    addsub/a -> floordiv/a
    ( "\+" floordiv/b $ a = Add(a, b) $
    | "-"  floordiv/b $ a = Subtract(a, b) $
    )* ;

    floordiv/a -> exponent/a ("//" exponent/b $ a = Floordiv(a,b) $ )* ;

    exponent/a -> modulus/a ("\*\*" modulus/b $ a = Exponent(a,b) $ )* ;

    modulus/a -> muldiv/a ("%" muldiv/b $ a = Modulus(a,b) $ )* ;

    muldiv/a -> index/a
    ( "\*" index/b $ a = Multiply(a, b) $
    | "/"  index/b $ a = Divide(a, b) $
    )* ;

    index/a -> parens/a ( "\[" expression/b "\]" $ a = Index(a, b) $ )* ;

    parens/a -> "\(" expression/a "\)" | literal/a ;

    literal/a -> (array/a | int/a | real/a | string/a) ;

    array/a ->  "\["                $ a = Array([]) $
                expression/b        $ a.value.append(b) $
                ( "," expression/b  $ a.value.append(b) $ ) *
                "\]"
                | "\[" "\]" $ a = Array([]) $ ;

    """

# Make an instance of the parser. This acts like a function.
parse = Parser()

# Set the amount of space for printing output
justify = 30

# This is the driver code, that reads in lines, deals with errors, and
# prints the output if no error occurs.

# Open the file containing the input.
try:
    f = open(sys.argv[1], "r")
except(IndexError, IOError):
    f = open("input1.txt", "r")

# For each line in f
for l in f:
    try:
        # Try to parse the expression.
        node = parse(l)

        # Try to get a result.
        result = node.evaluate()

        # Print the representation of the result.

        print(l[:-1].ljust(justify), repr(result))

    # If an exception is thrown, print the appropriate error.
    except tpg.Error:
        print(l[:-1].ljust(justify), "SYNTAX ERROR")
        # Uncomment the next line to re-raise the syntax error,
        # displaying where it occurs. Comment it for submission.
        # raise

    except SemanticError:
        print(l[:-1].ljust(justify), "SEMANTIC ERROR")
        # Uncomment the next line to re-raise the semantic error,
        # displaying where it occurs. Comment it for submission.
        # raise

f.close()
