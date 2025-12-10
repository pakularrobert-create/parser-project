"""
Lark Transformer for building AST from parse tree.
"""

from lark import Transformer, Token
from .ast_nodes import *


class TaskFlowTransformer(Transformer):
    """Transform Lark parse tree into TaskFlow AST."""
    
    def start(self, items):
        """Program is a list of task definitions."""
        return Program(tasks=items)
    
    def task_def(self, items):
        """Task definition: task name { body }"""
        name = str(items[0])
        body = items[1]
        if isinstance(body, TaskDef):
            body.name = name
            return body
        return TaskDef(name=name, statements=body)
    
    def task_body(self, items):
        """Task body contains options and statements."""
        task = TaskDef(name="", priority=None, depends=None, statements=[])
        
        for item in items:
            if isinstance(item, tuple):
                key, value = item
                if key == "priority":
                    task.priority = value
                elif key == "depends":
                    task.depends = value
            elif isinstance(item, Statement):
                task.statements.append(item)
        
        return task
    
    def task_option(self, items):
        """Task option (priority or depends)."""
        return items[0]
    
    def priority_opt(self, items):
        """Priority option."""
        return ("priority", str(items[0]))
    
    def depends_opt(self, items):
        """Depends option."""
        if items:
            return ("depends", items[0])
        return ("depends", [])
    
    def name_list(self, items):
        """List of names."""
        return [str(item) for item in items]
    
    def statement(self, items):
        """Statement."""
        return items[0]
    
    def var_decl(self, items):
        """Variable declaration: let name = value"""
        return VarDecl(name=str(items[0]), value=items[1])
    
    def assignment(self, items):
        """Assignment: name = value"""
        return Assignment(name=str(items[0]), value=items[1])
    
    def if_stmt(self, items):
        """If statement with optional else clause."""
        condition = items[0]
        then_body = items[1] if len(items) > 1 and isinstance(items[1], list) else []
        else_body = items[2] if len(items) > 2 else None
        
        # Flatten statement lists
        if not isinstance(then_body, list):
            then_body = [then_body] if then_body else []
        if else_body and not isinstance(else_body, list):
            else_body = [else_body] if else_body else []
            
        return IfStmt(condition=condition, then_body=then_body, else_body=else_body)
    
    def else_clause(self, items):
        """Else clause."""
        return items if items else []
    
    def repeat_stmt(self, items):
        """Repeat statement."""
        count = items[0]
        body = items[1:] if len(items) > 1 else []
        if not isinstance(body, list):
            body = [body] if body else []
        return RepeatStmt(count=count, body=body)
    
    def while_stmt(self, items):
        """While statement."""
        condition = items[0]
        body = items[1:] if len(items) > 1 else []
        if not isinstance(body, list):
            body = [body] if body else []
        return WhileStmt(condition=condition, body=body)
    
    def run_stmt(self, items):
        """Run statement."""
        # items[0] should be a Literal from STRING token
        if isinstance(items[0], Literal):
            command = items[0].value
        else:
            command = str(items[0])
            # Remove quotes from string if present
            if command.startswith('"') and command.endswith('"'):
                command = command[1:-1]
        return RunStmt(command=command)
    
    def log_stmt(self, items):
        """Log statement."""
        return LogStmt(message=items[0])
    
    def expression(self, items):
        """Expression."""
        return items[0]
    
    def or_expr(self, items):
        """Logical OR expression."""
        if len(items) == 1:
            return items[0]
        result = items[0]
        for i in range(1, len(items)):
            result = BinaryOp(operator="or", left=result, right=items[i])
        return result
    
    def and_expr(self, items):
        """Logical AND expression."""
        if len(items) == 1:
            return items[0]
        result = items[0]
        for i in range(1, len(items)):
            result = BinaryOp(operator="and", left=result, right=items[i])
        return result
    
    def not_expr(self, items):
        """Logical NOT expression."""
        if len(items) == 2:  # "not" expr
            return UnaryOp(operator="not", operand=items[1])
        return items[0]
    
    def comparison(self, items):
        """Comparison expression."""
        if len(items) == 1:
            return items[0]
        return BinaryOp(operator=str(items[1]), left=items[0], right=items[2])
    
    def additive(self, items):
        """Additive expression (+ -)."""
        if len(items) == 1:
            return items[0]
        result = items[0]
        i = 1
        while i < len(items) - 1:
            op = str(items[i])
            result = BinaryOp(operator=op, left=result, right=items[i + 1])
            i += 2
        return result
    
    def multiplicative(self, items):
        """Multiplicative expression (* / %)."""
        if len(items) == 1:
            return items[0]
        result = items[0]
        i = 1
        while i < len(items) - 1:
            op = str(items[i])
            result = BinaryOp(operator=op, left=result, right=items[i + 1])
            i += 2
        return result
    
    def unary(self, items):
        """Unary expression (-)."""
        if len(items) == 2:  # "-" expr
            return UnaryOp(operator="-", operand=items[1])
        return items[0]
    
    def primary(self, items):
        """Primary expression."""
        item = items[0]
        # If it's a string (NAME token), wrap it in Identifier
        if isinstance(item, str):
            return Identifier(name=item)
        return item
    
    def list_expr(self, items):
        """List expression."""
        return ListExpr(elements=items if items else [])
    
    def bool_literal(self, items):
        """Boolean literal."""
        value = str(items[0]) if items else "true"
        return Literal(value=(value == "true"), type='boolean')
    
    def NAME(self, token):
        """Identifier token."""
        value = str(token)
        # Return as-is for use in context, will be wrapped in Identifier when needed
        return value
    
    def NUMBER(self, token):
        """Number literal."""
        value = str(token)
        if '.' in value:
            return Literal(value=float(value), type='number')
        return Literal(value=int(value), type='number')
    
    def STRING(self, token):
        """String literal."""
        value = str(token)
        # Remove quotes
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        return Literal(value=value, type='string')
    
    def PRIORITY_LEVEL(self, token):
        """Priority level token."""
        return str(token)
    
    def COMP_OP(self, token):
        """Comparison operator token."""
        return str(token)
