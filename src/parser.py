"""
Main TaskFlow parser implementation.
"""

from lark import Lark, exceptions
from pathlib import Path
from .transformer import TaskFlowTransformer
from .error_handler import TaskFlowErrorHandler


class TaskFlowParser:
    """Parser for TaskFlow language."""
    
    def __init__(self):
        """Initialize parser with grammar and transformer."""
        grammar_path = Path(__file__).parent / "grammar.lark"
        with open(grammar_path) as f:
            grammar = f.read()
        
        self.parser = Lark(
            grammar,
            parser='lalr',
            transformer=TaskFlowTransformer(),
            propagate_positions=True
        )
        self.error_handler = TaskFlowErrorHandler()
    
    def parse(self, source: str):
        """
        Parse TaskFlow source code and return AST.
        
        Args:
            source: TaskFlow source code as string
            
        Returns:
            Program AST node
            
        Raises:
            TaskFlowError: If parsing fails
        """
        try:
            return self.parser.parse(source)
        except exceptions.UnexpectedToken as e:
            raise self.error_handler.handle_unexpected_token(e)
        except exceptions.UnexpectedCharacters as e:
            raise self.error_handler.handle_unexpected_char(e)
        except exceptions.UnexpectedEOF as e:
            raise self.error_handler.handle_unexpected_eof(e)
    
    def parse_file(self, filepath: str):
        """
        Parse a TaskFlow file.
        
        Args:
            filepath: Path to TaskFlow source file
            
        Returns:
            Program AST node
            
        Raises:
            TaskFlowError: If parsing fails
            FileNotFoundError: If file doesn't exist
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            return self.parse(f.read())
