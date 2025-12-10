# TaskFlow Parser

Egyszerű lexikális és szintaktikai elemző a TaskFlow nyelvhez.

## Telepítés

```bash
pip install lark
```

## Használat

```bash
# Demo futtatása
python taskflow_parser.py

# Tesztek futtatása
python -m pytest test_taskflow.py -v
```

## A TaskFlow nyelv

### Kulcsszavak
`task`, `let`, `if`, `else`, `repeat`, `times`, `while`, `run`, `log`, `priority`, `depends`, `and`, `or`, `true`, `false`

### Szimbólumok
`{ }` `[ ]` `( )` `=` `:` `,` `+` `-` `*` `/` `==` `!=` `<` `>` `<=` `>=`

### Példa

```taskflow
task backup {
    priority: high
    depends: [init]
    
    let count = 3
    
    if count > 0 {
        repeat count times {
            run "backup.sh"
        }
    } else {
        log "Skip"
    }
}
```

## Nyelvi komplexitás

| Elem | Példa |
|------|-------|
| Szekvencia | Utasítások egymás után |
| Választás | `if-else`, `priority: high \| medium \| low` |
| Ismétlés | `repeat N times`, `while` |
| Opcionális | `priority`, `depends`, `else` ág |
| Aggregáció | Task blokkok, listák `[a, b, c]` |

## Grammatikai szabályok (12 db)

1. Program → task+
2. Task → "task" NAME "{" body "}"
3. Priority → "priority" ":" (high|medium|low)
4. Depends → "depends" ":" "[" names "]"
5. VarDecl → "let" NAME "=" expr
6. Assignment → NAME "=" expr
7. IfStmt → "if" expr "{" stmt* "}" ["else" "{" stmt* "}"]
8. RepeatStmt → "repeat" expr "times" "{" stmt* "}"
9. WhileStmt → "while" expr "{" stmt* "}"
10. RunStmt → "run" STRING
11. LogStmt → "log" expr
12. List → "[" expr ("," expr)* "]"

## Tesztek

16 teszteset:
- 11 helyes bemenet
- 5 hibás bemenet (negatív tesztek)
