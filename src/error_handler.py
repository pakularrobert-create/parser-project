"""
Error handler for TaskFlow parser with user-friendly error messages.
"""

from lark import exceptions


class TaskFlowError(Exception):
    """Base exception for TaskFlow parser errors."""
    
    def __init__(self, message, line=None, column=None, context=None):
        self.message = message
        self.line = line
        self.column = column
        self.context = context
        super().__init__(self.format_error())
    
    def format_error(self):
        """Format error message with context."""
        lines = []
        
        if self.line is not None and self.column is not None:
            lines.append(f"Szintaktikai hiba a(z) {self.line}. sor {self.column}. oszlopában:")
        else:
            lines.append("Szintaktikai hiba:")
        
        lines.append(f"  {self.message}")
        
        if self.context:
            lines.append("")
            lines.append("Kontextus:")
            lines.append(f"  {self.context}")
            if self.column:
                lines.append("  " + " " * (self.column - 1) + "^")
        
        return "\n".join(lines)


class TaskFlowErrorHandler:
    """Handle parser errors and convert them to user-friendly messages."""
    
    def handle_unexpected_token(self, error: exceptions.UnexpectedToken):
        """Handle unexpected token error."""
        line = error.line
        column = error.column
        
        # Get context from the error
        context = None
        if hasattr(error, 'get_context'):
            context = error.get_context(error.token.value if hasattr(error, 'token') else "")
        
        # Format expected tokens
        expected = []
        if hasattr(error, 'expected'):
            expected = list(error.expected)
        
        if expected:
            expected_str = ", ".join(sorted(expected))
            message = f"Váratlan token. Várt tokenek: {expected_str}"
        else:
            message = "Váratlan token"
        
        if hasattr(error, 'token') and error.token:
            message += f". Kapott: '{error.token}'"
        
        return TaskFlowError(message, line, column, context)
    
    def handle_unexpected_char(self, error: exceptions.UnexpectedCharacters):
        """Handle unexpected character error."""
        line = error.line
        column = error.column
        
        # Get context
        context = None
        if hasattr(error, 'get_context'):
            context = error.get_context("")
        
        char = error.char if hasattr(error, 'char') else '?'
        message = f"Érvénytelen karakter: '{char}'"
        
        # Add allowed characters if available
        if hasattr(error, 'allowed') and error.allowed:
            allowed_str = ", ".join(f"'{c}'" for c in sorted(error.allowed))
            message += f". Engedélyezett karakterek: {allowed_str}"
        
        return TaskFlowError(message, line, column, context)
    
    def handle_unexpected_eof(self, error: exceptions.UnexpectedEOF):
        """Handle unexpected end of file error."""
        message = "Váratlan fájl vége. A fájl hiányos lehet."
        
        if hasattr(error, 'expected') and error.expected:
            expected_str = ", ".join(sorted(error.expected))
            message += f" Várt tokenek: {expected_str}"
        
        return TaskFlowError(message)
