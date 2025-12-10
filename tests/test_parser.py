"""
Test suite for TaskFlow Parser.
"""

import pytest
from pathlib import Path
from src.parser import TaskFlowParser
from src.error_handler import TaskFlowError
from src.ast_nodes import *


class TestTaskFlowParser:
    """Test cases for TaskFlow parser."""
    
    @pytest.fixture
    def parser(self):
        """Create parser instance."""
        return TaskFlowParser()
    
    @pytest.fixture
    def valid_dir(self):
        """Path to valid test files."""
        return Path(__file__).parent / "valid"
    
    @pytest.fixture
    def invalid_dir(self):
        """Path to invalid test files."""
        return Path(__file__).parent / "invalid"
    
    # Valid test cases
    
    def test_simple_task(self, parser, valid_dir):
        """Test 1: Parse simple task definition."""
        ast = parser.parse_file(valid_dir / "simple_task.tf")
        assert isinstance(ast, Program)
        assert len(ast.tasks) == 1
        assert ast.tasks[0].name == "simple_task"
    
    def test_variables(self, parser, valid_dir):
        """Test 2: Parse variable declarations."""
        ast = parser.parse_file(valid_dir / "variables.tf")
        assert isinstance(ast, Program)
        assert len(ast.tasks) == 1
        task = ast.tasks[0]
        assert task.name == "variables"
        # Check for variable declarations
        var_decls = [s for s in task.statements if isinstance(s, VarDecl)]
        assert len(var_decls) >= 3
    
    def test_conditionals(self, parser, valid_dir):
        """Test 3: Parse if-else statements."""
        ast = parser.parse_file(valid_dir / "conditionals.tf")
        assert isinstance(ast, Program)
        task = ast.tasks[0]
        # Check for if statements
        if_stmts = [s for s in task.statements if isinstance(s, IfStmt)]
        assert len(if_stmts) >= 2
    
    def test_loops(self, parser, valid_dir):
        """Test 4: Parse repeat and while loops."""
        ast = parser.parse_file(valid_dir / "loops.tf")
        assert isinstance(ast, Program)
        task = ast.tasks[0]
        # Check for loop statements
        repeat_stmts = [s for s in task.statements if isinstance(s, RepeatStmt)]
        while_stmts = [s for s in task.statements if isinstance(s, WhileStmt)]
        assert len(repeat_stmts) >= 1
        assert len(while_stmts) >= 1
    
    def test_complex_workflow(self, parser, valid_dir):
        """Test 5: Parse complex workflow with multiple tasks."""
        ast = parser.parse_file(valid_dir / "complex_workflow.tf")
        assert isinstance(ast, Program)
        assert len(ast.tasks) == 3
        # Check task names
        task_names = [t.name for t in ast.tasks]
        assert "setup" in task_names
        assert "build" in task_names
        assert "test" in task_names
    
    def test_full_example(self, parser, valid_dir):
        """Test 6: Parse full example with all language features."""
        ast = parser.parse_file(valid_dir / "full_example.tf")
        assert isinstance(ast, Program)
        task = ast.tasks[0]
        assert task.name == "full_example"
        assert task.priority == "high"
        assert task.depends is not None
    
    # Invalid test cases (negative tests)
    
    def test_missing_brace(self, parser, invalid_dir):
        """Test 7: Detect missing closing brace."""
        with pytest.raises((TaskFlowError, Exception)):
            parser.parse_file(invalid_dir / "missing_brace.tf")
    
    def test_invalid_keyword(self, parser, invalid_dir):
        """Test 8: Detect invalid keyword."""
        with pytest.raises((TaskFlowError, Exception)):
            parser.parse_file(invalid_dir / "invalid_keyword.tf")
    
    def test_syntax_error(self, parser, invalid_dir):
        """Test 9: Detect syntax error."""
        with pytest.raises((TaskFlowError, Exception)):
            parser.parse_file(invalid_dir / "syntax_error.tf")
    
    def test_missing_expression(self, parser, invalid_dir):
        """Test 10: Detect missing assignment expression."""
        with pytest.raises((TaskFlowError, Exception)):
            parser.parse_file(invalid_dir / "missing_semicolon.tf")
    
    def test_invalid_expression(self, parser, invalid_dir):
        """Test 11: Detect invalid expression."""
        with pytest.raises((TaskFlowError, Exception)):
            parser.parse_file(invalid_dir / "invalid_expression.tf")
    
    # Additional unit tests
    
    def test_priority_parsing(self, parser):
        """Test 12: Parse priority option."""
        source = """
        task with_priority {
            priority: high
            log "test"
        }
        """
        ast = parser.parse(source)
        assert ast.tasks[0].priority == "high"
    
    def test_depends_parsing(self, parser):
        """Test 13: Parse depends option."""
        source = """
        task with_deps {
            depends: [task1, task2]
            log "test"
        }
        """
        ast = parser.parse(source)
        assert ast.tasks[0].depends == ["task1", "task2"]
    
    def test_run_statement(self, parser):
        """Test 14: Parse run statement."""
        source = """
        task runner {
            run "echo hello"
        }
        """
        ast = parser.parse(source)
        run_stmts = [s for s in ast.tasks[0].statements if isinstance(s, RunStmt)]
        assert len(run_stmts) == 1
        assert run_stmts[0].command == "echo hello"
    
    def test_expressions(self, parser):
        """Test 15: Parse complex expressions."""
        source = """
        task expr_test {
            let x = 10 + 20 * 3
            let y = (5 + 3) * 2
            let z = true and false or not true
        }
        """
        ast = parser.parse(source)
        var_decls = [s for s in ast.tasks[0].statements if isinstance(s, VarDecl)]
        assert len(var_decls) == 3
    
    def test_list_expression(self, parser):
        """Test 16: Parse list expressions."""
        source = """
        task list_test {
            let items = [1, 2, 3, 4, 5]
            let names = ["alice", "bob", "charlie"]
        }
        """
        ast = parser.parse(source)
        var_decls = [s for s in ast.tasks[0].statements if isinstance(s, VarDecl)]
        assert len(var_decls) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
