"""
TaskFlow Parser tesztek - 16 teszteset
"""

import pytest
from taskflow_parser import TaskFlowParser

parser = TaskFlowParser()

# ============================================================
# HELYES BEMENETEK (11 teszt)
# ============================================================

def test_1_simple_task():
    """1. Egyszerű task."""
    code = 'task hello { log "Hello" }'
    tree = parser.parse(code)
    assert tree is not None

def test_2_variables():
    """2. Változók."""
    code = '''
    task vars {
        let x = 10
        let y = 20
        let z = x + y
    }
    '''
    tree = parser.parse(code)
    assert tree is not None

def test_3_if_else():
    """3. If-else (választás)."""
    code = '''
    task cond {
        let x = 5
        if x > 3 {
            log "nagy"
        } else {
            log "kicsi"
        }
    }
    '''
    tree = parser.parse(code)
    assert tree is not None

def test_4_repeat():
    """4. Repeat ciklus (ismétlés)."""
    code = '''
    task rep {
        repeat 5 times {
            log "hello"
        }
    }
    '''
    tree = parser.parse(code)
    assert tree is not None

def test_5_while():
    """5. While ciklus (ismétlés)."""
    code = '''
    task wh {
        let i = 0
        while i < 10 {
            i = i + 1
        }
    }
    '''
    tree = parser.parse(code)
    assert tree is not None

def test_6_priority():
    """6. Priority (opcionális)."""
    code = '''
    task prio {
        priority: high
        log "fontos"
    }
    '''
    tree = parser.parse(code)
    assert tree is not None

def test_7_depends():
    """7. Depends (opcionális + lista)."""
    code = '''
    task dep {
        depends: [task1, task2, task3]
        log "függőségek"
    }
    '''
    tree = parser.parse(code)
    assert tree is not None

def test_8_run():
    """8. Run utasítás."""
    code = '''
    task runner {
        run "echo hello"
        run "make build"
    }
    '''
    tree = parser.parse(code)
    assert tree is not None

def test_9_expressions():
    """9. Kifejezések."""
    code = '''
    task expr {
        let a = 10 + 20 * 3
        let b = (5 + 3) * 2
        let c = a > b and true
        let d = a == 70 or b != 16
    }
    '''
    tree = parser.parse(code)
    assert tree is not None

def test_10_list():
    """10. Lista (aggregáció)."""
    code = '''
    task lst {
        let nums = [1, 2, 3, 4, 5]
        let names = ["a", "b", "c"]
    }
    '''
    tree = parser.parse(code)
    assert tree is not None

def test_11_complex():
    """11. Komplex workflow (szekvencia + aggregáció)."""
    code = '''
    task init {
        priority: high
        log "init"
    }
    
    task build {
        priority: medium
        depends: [init]
        run "make"
    }
    
    task test {
        priority: low
        depends: [build]
        repeat 3 times {
            run "pytest"
        }
    }
    '''
    tree = parser.parse(code)
    assert tree is not None

# ============================================================
# HIBÁS BEMENETEK - NEGATÍV TESZTEK (5 teszt)
# ============================================================

def test_12_missing_brace():
    """12. Hiányzó }"""
    code = 'task broken { log "x"'
    with pytest.raises(Exception):
        parser.parse(code)

def test_13_invalid_keyword():
    """13. Hibás kulcsszó."""
    code = 'taaask hello { log "x" }'
    with pytest.raises(Exception):
        parser.parse(code)

def test_14_missing_equals():
    """14. Hiányzó = jel."""
    code = 'task t { let x 10 }'
    with pytest.raises(Exception):
        parser.parse(code)

def test_15_invalid_priority():
    """15. Hibás priority érték."""
    code = 'task t { priority: invalid }'
    with pytest.raises(Exception):
        parser.parse(code)

def test_16_unclosed_string():
    """16. Lezáratlan string."""
    code = 'task t { log "hello }'
    with pytest.raises(Exception):
        parser.parse(code)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
