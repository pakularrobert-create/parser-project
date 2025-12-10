# TaskFlow Parser Projekt

## Áttekintés

A TaskFlow egy egyszerű, de hatékony feladatkezelő és automatizáló nyelv, amely feladatok definiálására és végrehajtási logikájuk leírására szolgál. Ez a projekt egy teljes körű lexikális és szintaktikai elemzőt (parser) implementál Python és Lark használatával.

## Célok

- **Egyszerű szintaxis**: Könnyen olvasható és írható feladatdefiníciók
- **Automatizálás**: Workflow-k és feladatok összeállítása
- **Függőségkezelés**: Feladatok közötti függőségek kezelése
- **Prioritások**: Feladatok fontossági sorrendjének meghatározása

## Telepítés

### Követelmények

- Python 3.8 vagy újabb
- pip csomag kezelő

### Telepítési lépések

```bash
# Függőségek telepítése
pip install -r requirements.txt
```

## Használat

### Parser használata Python kódból

```python
from src.parser import TaskFlowParser

# Parser példány létrehozása
parser = TaskFlowParser()

# TaskFlow kód elemzése string-ből
source_code = """
task example {
    priority: high
    log "Hello, TaskFlow!"
}
"""

ast = parser.parse(source_code)
print(ast)

# TaskFlow fájl elemzése
ast = parser.parse_file("examples/backup_workflow.tf")
```

### Példa programok futtatása

```bash
# Tesztek futtatása
pytest tests/ -v

# Egyetlen teszt futtatása
pytest tests/test_parser.py::TestTaskFlowParser::test_simple_task -v
```

## Nyelvi Specifikáció

### Kulcsszavak

- `task` - Feladat definíció kezdete
- `let` - Változó deklaráció
- `if`, `else` - Feltételes utasítások
- `repeat`, `times` - Ismétlés ciklus
- `while` - Feltételes ciklus
- `run` - Parancs végrehajtás
- `log` - Üzenet naplózás
- `priority` - Feladat prioritás (high, medium, low)
- `depends` - Feladat függőségek
- `and`, `or`, `not` - Logikai operátorok
- `true`, `false` - Boolean literálok

### Szimbólumok és Operátorok

- `{ }` - Blokk határolók
- `[ ]` - Lista határolók
- `( )` - Kifejezés csoportosítás
- `=` - Értékadás
- `+`, `-`, `*`, `/`, `%` - Aritmetikai operátorok
- `==`, `!=`, `<`, `>`, `<=`, `>=` - Összehasonlító operátorok
- `:` - Opció határolás
- `,` - Lista elválasztó
- `"..."` - String literálok
- `//` - Egysoros megjegyzés

### Grammatika (EBNF)

```ebnf
Program        ::= TaskDef+
TaskDef        ::= "task" Identifier "{" TaskBody "}"
TaskBody       ::= TaskOption* Statement*
TaskOption     ::= PriorityOpt | DependsOpt
PriorityOpt    ::= "priority" ":" ("high" | "medium" | "low")
DependsOpt     ::= "depends" ":" "[" (Identifier ("," Identifier)*)? "]"

Statement      ::= VarDecl | Assignment | IfStmt | RepeatStmt 
                 | WhileStmt | RunStmt | LogStmt
VarDecl        ::= "let" Identifier "=" Expression
Assignment     ::= Identifier "=" Expression
IfStmt         ::= "if" Expression "{" Statement* "}" ElseClause?
ElseClause     ::= "else" "{" Statement* "}"
RepeatStmt     ::= "repeat" Expression "times" "{" Statement* "}"
WhileStmt      ::= "while" Expression "{" Statement* "}"
RunStmt        ::= "run" String
LogStmt        ::= "log" Expression

Expression     ::= OrExpr
OrExpr         ::= AndExpr ("or" AndExpr)*
AndExpr        ::= NotExpr ("and" NotExpr)*
NotExpr        ::= "not" NotExpr | Comparison
Comparison     ::= Additive (CompOp Additive)?
CompOp         ::= "==" | "!=" | "<" | ">" | "<=" | ">="
Additive       ::= Multiplicative (("+"|"-") Multiplicative)*
Multiplicative ::= Unary (("*"|"/"|"%") Unary)*
Unary          ::= "-" Unary | Primary
Primary        ::= Number | String | Boolean | Identifier 
                 | "(" Expression ")" | ListExpr
ListExpr       ::= "[" (Expression ("," Expression)*)? "]"

Identifier     ::= [a-zA-Z_][a-zA-Z0-9_]*
Number         ::= [0-9]+(\.[0-9]+)?
String         ::= '"' [^"]* '"'
Boolean        ::= "true" | "false"
```

## Nyelvi Elemek és Komplexitás

A TaskFlow nyelv megfelel a következő követelményeknek:

1. **Szekvencia**: Utasítások egymás után hajtódnak végre
2. **Választás (Alternáció)**: `if-else` szerkezetek, priority értékek (high/medium/low)
3. **Ismétlés**: `repeat N times` és `while` ciklusok
4. **Opcionális elemek**: `priority`, `depends`, `else` ág
5. **Aggregáció**: Task blokkok, lista kifejezések

### Grammatikai szabályok (10+)

1. Program → Task definíciók sorozata
2. Task definíció → név és törzsblokk
3. Változó deklaráció → `let` név `=` kifejezés
4. If-else feltétel → `if` feltétel `{` ... `}` opcionális `else` ág
5. Repeat ciklus → `repeat` N `times` `{` ... `}`
6. While ciklus → `while` feltétel `{` ... `}`
7. Run utasítás → parancs végrehajtás
8. Log utasítás → üzenet naplózás
9. Priority opció → prioritás beállítás
10. Depends opció → függőségek definiálása
11. Lista kifejezés → elemek listája
12. Kifejezések → aritmetikai és logikai műveletek

## Példa Programok

### Egyszerű Feladat

```taskflow
task simple_task {
    log "Hello, TaskFlow!"
}
```

### Változók és Műveletek

```taskflow
task calculations {
    let x = 10
    let y = 20
    let sum = x + y
    let product = x * y
    log sum
}
```

### Feltételes Utasítások

```taskflow
task conditional {
    let age = 25
    
    if age >= 18 {
        log "Felnőtt"
    } else {
        log "Gyermek"
    }
}
```

### Ciklusok

```taskflow
task loops {
    let counter = 0
    
    repeat 5 times {
        log "Ismétlés"
        counter = counter + 1
    }
    
    while counter < 10 {
        counter = counter + 1
    }
}
```

### Komplex Workflow

```taskflow
task setup {
    priority: high
    log "Környezet előkészítése"
    run "mkdir -p /tmp/project"
}

task build {
    priority: medium
    depends: [setup]
    log "Projekt fordítása"
    run "make build"
}

task test {
    priority: low
    depends: [build]
    log "Tesztek futtatása"
    run "make test"
}
```

További példák az `examples/` könyvtárban találhatók.

## Tesztelés

A projekt 16+ tesztesetet tartalmaz, melyek helyes és hibás bemeneteket egyaránt lefednek.

### Tesztek futtatása

```bash
# Összes teszt futtatása
pytest tests/ -v

# Teszt lefedettség ellenőrzése
pytest tests/ --cov=src --cov-report=html

# Egyedi teszt futtatása
pytest tests/test_parser.py::TestTaskFlowParser::test_simple_task -v
```

### Tesztesetek

#### Helyes bemenetek (Valid tests)
1. Egyszerű feladat definíció
2. Változók és műveletek
3. Feltételes utasítások
4. Ciklusok (repeat, while)
5. Komplex workflow több feladattal
6. Teljes példa minden nyelvi elemmel

#### Hibás bemenetek (Invalid tests)
7. Hiányzó záró kapcsos zárójel
8. Érvénytelen kulcsszó
9. Szintaktikai hiba
10. Hiányzó kifejezés
11. Érvénytelen kifejezés

#### További tesztek
12. Priority kezelés
13. Depends kezelés
14. Run utasítás
15. Komplex kifejezések
16. Lista kifejezések

## Hibakezelés

A parser részletes, felhasználóbarát hibaüzeneteket biztosít:

### Példa hibaüzenet

```
Szintaktikai hiba a(z) 3. sor 10. oszlopában:
  Váratlan token. Várt tokenek: =, LBRACE. Kapott: '10'

Kontextus:
  let x 10
         ^
```

### Hibatípusok

- **Váratlan token**: Hibás vagy váratlan szimbólum
- **Hiányzó token**: Kötelező elem hiányzik
- **Érvénytelen karakter**: Nem megengedett karakter
- **Váratlan fájl vége**: A fájl hiányos

## Projekt Struktúra

```
parser-project/
├── README.md                 # Ez a fájl
├── requirements.txt          # Python függőségek
├── src/
│   ├── __init__.py          # Modul inicializáció
│   ├── grammar.lark         # Lark grammatika
│   ├── parser.py            # Fő parser implementáció
│   ├── ast_nodes.py         # AST node osztályok
│   ├── transformer.py       # Lark Transformer
│   └── error_handler.py     # Hibakezelő
├── tests/
│   ├── __init__.py
│   ├── test_parser.py       # Pytest tesztek
│   ├── valid/               # Helyes bemenetek
│   │   ├── simple_task.tf
│   │   ├── variables.tf
│   │   ├── conditionals.tf
│   │   ├── loops.tf
│   │   ├── complex_workflow.tf
│   │   └── full_example.tf
│   └── invalid/             # Hibás bemenetek
│       ├── missing_brace.tf
│       ├── invalid_keyword.tf
│       ├── syntax_error.tf
│       ├── missing_semicolon.tf
│       └── invalid_expression.tf
├── examples/
│   ├── backup_workflow.tf   # Backup automatizálás
│   ├── deployment.tf        # Deployment workflow
│   └── data_processing.tf   # Adatfeldolgozás
└── docs/
    └── SPECIFICATION.md     # Részletes nyelvi specifikáció
```

## Fejlesztési Kihívások és Döntések

### 1. Parser választás: Lark

**Döntés**: Lark parser generátor használata LALR(1) módban.

**Indoklás**:
- Tiszta, olvasható grammatika szintaxis
- Beépített transformer támogatás AST építéshez
- Jó hibakezelés és pozíció információk
- Python-natív implementáció

### 2. AST reprezentáció

**Döntés**: Dataclass-ok használata AST node-okhoz.

**Indoklás**:
- Típusbiztonság és autocompletion
- Egyszerű és tiszta kód
- Immutable objektumok
- Python 3.7+ natív támogatás

### 3. Hibakezelés stratégia

**Döntés**: Részletes, magyarul lokalizált hibaüzenetek.

**Indoklás**:
- Felhasználóbarát élmény
- Kontextus megjelenítés a hibás sorból
- Sor és oszlop pozíció
- Várt tokenek listája

### 4. Kifejezések kezelése

**Döntés**: Operátor precedencia beépítése a grammatikába.

**Indoklás**:
- Helyes műveleti sorrend garantálása
- Egyszerűbb transformer implementáció
- Nincs szükség utófeldolgozásra

### 5. Opcionális elemek

**Döntés**: `?` operátor használata a grammatikában.

**Indoklás**:
- Rugalmas szintaxis
- Egyszerűbb kód írás
- Természetesebb nyelvi konstrukciók

## Technológiai Stack

- **Python 3.8+**: Fő programozási nyelv
- **Lark 1.1.5+**: Parser generátor és transformer
- **Pytest 7.4.0+**: Tesztelési keretrendszer
- **dataclasses**: AST node reprezentáció

## Licenc

Ez egy oktatási projekt, amely a fordítóprogramok elméleti alapjainak gyakorlati megvalósítását demonstrálja.

## Szerzők

TaskFlow Parser Projekt - 2024

## További Dokumentáció

Részletes nyelvi specifikáció és szemantika: [docs/SPECIFICATION.md](docs/SPECIFICATION.md)
