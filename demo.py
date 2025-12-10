#!/usr/bin/env python
"""
TaskFlow Parser - Demo Script
Demonstrates parsing TaskFlow code and displaying the AST.
"""

from src.parser import TaskFlowParser
from src.error_handler import TaskFlowError
import sys


def print_ast(node, indent=0):
    """Pretty print AST node."""
    prefix = "  " * indent
    node_type = type(node).__name__
    
    if hasattr(node, '__dict__'):
        attrs = {k: v for k, v in node.__dict__.items() if not k.startswith('_')}
        print(f"{prefix}{node_type}({', '.join(f'{k}={v!r}' if not isinstance(v, list) else f'{k}=[...]' for k, v in attrs.items() if not isinstance(v, object) or isinstance(v, (str, int, float, bool, type(None))))})")
        
        # Print lists recursively
        for k, v in attrs.items():
            if isinstance(v, list):
                print(f"{prefix}  {k}:")
                for item in v:
                    if hasattr(item, '__dict__'):
                        print_ast(item, indent + 2)
                    else:
                        print(f"{prefix}    {item!r}")
    else:
        print(f"{prefix}{node!r}")


def main():
    parser = TaskFlowParser()
    
    if len(sys.argv) > 1:
        # Parse file from command line argument
        filepath = sys.argv[1]
        try:
            print(f"Parsing: {filepath}")
            print("-" * 60)
            ast = parser.parse_file(filepath)
            print("\nAST:")
            print("-" * 60)
            print_ast(ast)
            print("\n✓ Parsing successful!")
        except TaskFlowError as e:
            print(f"\n✗ Parsing failed:")
            print(str(e))
            sys.exit(1)
        except FileNotFoundError:
            print(f"✗ File not found: {filepath}")
            sys.exit(1)
    else:
        # Demo with inline code
        demo_code = """
task demo {
    priority: high
    
    let count = 10
    let message = "Hello, TaskFlow!"
    
    log message
    
    if count > 5 {
        log "Count is greater than 5"
    }
    
    repeat 3 times {
        run "echo iteration"
    }
}
"""
        print("Demo: Parsing inline TaskFlow code")
        print("-" * 60)
        print(demo_code)
        print("-" * 60)
        
        try:
            ast = parser.parse(demo_code)
            print("\nAST:")
            print("-" * 60)
            print_ast(ast)
            print("\n✓ Parsing successful!")
            print("\nUsage: python demo.py <taskflow_file.tf>")
        except TaskFlowError as e:
            print(f"\n✗ Parsing failed:")
            print(str(e))
            sys.exit(1)


if __name__ == "__main__":
    main()
