"""
AST Node classes for TaskFlow language.
"""

from dataclasses import dataclass
from typing import List, Optional, Any


@dataclass
class ASTNode:
    """Base class for all AST nodes."""
    pass


@dataclass
class Program(ASTNode):
    """Root node representing the entire program."""
    tasks: List['TaskDef']


@dataclass
class TaskDef(ASTNode):
    """Task definition node."""
    name: str
    priority: Optional[str] = None
    depends: Optional[List[str]] = None
    statements: List['Statement'] = None
    
    def __post_init__(self):
        if self.statements is None:
            self.statements = []


@dataclass
class Statement(ASTNode):
    """Base class for all statements."""
    pass


@dataclass
class VarDecl(Statement):
    """Variable declaration: let name = value"""
    name: str
    value: 'Expression'


@dataclass
class Assignment(Statement):
    """Variable assignment: name = value"""
    name: str
    value: 'Expression'


@dataclass
class IfStmt(Statement):
    """If statement with optional else clause."""
    condition: 'Expression'
    then_body: List[Statement]
    else_body: Optional[List[Statement]] = None


@dataclass
class RepeatStmt(Statement):
    """Repeat N times loop."""
    count: 'Expression'
    body: List[Statement]


@dataclass
class WhileStmt(Statement):
    """While loop."""
    condition: 'Expression'
    body: List[Statement]


@dataclass
class RunStmt(Statement):
    """Run command statement."""
    command: str


@dataclass
class LogStmt(Statement):
    """Log statement."""
    message: 'Expression'


@dataclass
class Expression(ASTNode):
    """Base class for all expressions."""
    pass


@dataclass
class BinaryOp(Expression):
    """Binary operation: left op right"""
    operator: str
    left: Expression
    right: Expression


@dataclass
class UnaryOp(Expression):
    """Unary operation: op operand"""
    operator: str
    operand: Expression


@dataclass
class Literal(Expression):
    """Literal value (number, string, boolean)."""
    value: Any
    type: str  # 'number', 'string', 'boolean'


@dataclass
class Identifier(Expression):
    """Variable reference."""
    name: str


@dataclass
class ListExpr(Expression):
    """List expression."""
    elements: List[Expression]
