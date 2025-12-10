"""
TaskFlow Parser - Egyszerűsített verzió
Lexikális és szintaktikai elemző egy fájlban.
"""

from lark import Lark, Transformer, v_args

# ============================================================
# 1. GRAMMATIKA - A nyelv szabályai
# ============================================================

GRAMMAR = """
    start: task+
    
    task: "task" NAME "{" task_body "}"
    
    task_body: option* statement*
    
    option: "priority" ":" PRIORITY     -> priority_opt
          | "depends" ":" "[" names? "]" -> depends_opt
    
    PRIORITY: "high" | "medium" | "low"
    names: NAME ("," NAME)*
    
    statement: "let" NAME "=" expr      -> var_decl
             | NAME "=" expr            -> assignment
             | "if" expr "{" statement* "}" ["else" "{" statement* "}"] -> if_stmt
             | "repeat" expr "times" "{" statement* "}"  -> repeat_stmt
             | "while" expr "{" statement* "}"           -> while_stmt
             | "run" STRING                              -> run_stmt
             | "log" expr                                -> log_stmt
    
    expr: or_expr
    or_expr: and_expr ("or" and_expr)*
    and_expr: comp ("and" comp)*
    comp: sum (COMP_OP sum)?
    COMP_OP: "==" | "!=" | "<" | ">" | "<=" | ">="
    sum: product (("+"|"-") product)*
    product: atom (("*"|"/") atom)*
    atom: NUMBER | STRING | "true" | "false" | NAME | "(" expr ")" | list
    list: "[" [expr ("," expr)*] "]"
    
    NAME: /[a-zA-Z_][a-zA-Z0-9_]*/
    NUMBER: /[0-9]+/
    STRING: /"[^"]*"/
    
    %import common.WS
    %ignore WS
    %ignore /\\/\\/.*/
"""

# ============================================================
# 2. PARSER OSZTÁLY
# ============================================================

class TaskFlowParser:
    """Egyszerű TaskFlow parser."""
    
    def __init__(self):
        self.parser = Lark(GRAMMAR, parser='lalr', start='start')
    
    def parse(self, code):
        """Kód elemzése - visszaadja a parse tree-t."""
        return self.parser.parse(code)
    
    def parse_file(self, filepath):
        """Fájl elemzése."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return self.parse(f.read())


# ============================================================
# 3. DEMO
# ============================================================

def demo():
    """Parser bemutatása."""
    
    parser = TaskFlowParser()
    
    # Példa kód
    code = '''
    task backup {
        priority: high
        depends: [init, validate]
        
        let count = 3
        
        if count > 0 {
            repeat count times {
                run "backup.sh"
                log "Backup done"
            }
        } else {
            log "Skip backup"
        }
        
        let i = 0
        while i < 5 {
            log i
            i = i + 1
        }
    }
    
    task cleanup {
        priority: low
        run "cleanup.sh"
    }
    '''
    
    print("="*60)
    print("TaskFlow Parser Demo")
    print("="*60)
    print("\nBemenet:")
    print(code)
    print("\n" + "="*60)
    
    try:
        tree = parser.parse(code)
        print("✅ Elemzés sikeres!")
        print("\nParse Tree:")
        print(tree.pretty())
    except Exception as e:
        print(f"❌ Hiba: {e}")


def test_error():
    """Hibakezelés bemutatása."""
    
    parser = TaskFlowParser()
    
    # Hibás kód
    bad_code = '''
    task broken {
        let x 10
    }
    '''
    
    print("\n" + "="*60)
    print("Hibakezelés teszt")
    print("="*60)
    print("\nHibás bemenet:")
    print(bad_code)
    
    try:
        parser.parse(bad_code)
    except Exception as e:
        print(f"\n❌ Hiba felismerve:\n{e}")


if __name__ == "__main__":
    demo()
    test_error()
