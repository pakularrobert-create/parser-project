# TaskFlow Nyelvi Specifikáció

## 1. Bevezetés

### 1.1 Nyelv Célja

A TaskFlow egy domain-specifikus nyelv (DSL) feladatok automatizálására és workflow-k definiálására. A nyelv célja, hogy egyszerű, olvasható szintaxissal lehessen leírni összetett feladatláncokat, függőségeket és végrehajtási logikát.

### 1.2 Motiváció

Modern DevOps és automatizálási környezetekben gyakran szükség van:
- Feladatok közötti függőségek kezelésére
- Prioritások meghatározására
- Feltételes végrehajtásra
- Ciklusok használatára a repetitív feladatokhoz
- Változók és állapot kezelésére

A TaskFlow ezeket a követelményeket egy egységes, könnyen tanulható nyelvben egyesíti.

### 1.3 Tervezési Elvek

1. **Egyszerűség**: A szintaxis könnyen olvasható és írható
2. **Kifejezőerő**: Komplex logikák leírhatók
3. **Biztonság**: Típusbiztos kifejezések
4. **Bővíthetőség**: Könnyen kiegészíthető új konstrukciókkal

## 2. Lexikális Elemek

### 2.1 Tokenek

#### 2.1.1 Kulcsszavak (Keywords)

A következő szavak rezerváltak és nem használhatók azonosítóként:

```
task        - Feladat definíció
let         - Változó deklaráció
if          - Feltételes utasítás
else        - Alternatív ág
repeat      - Ciklus kulcsszó
times       - Ismétlés szám jelzője
while       - Feltételes ciklus
run         - Parancs végrehajtás
log         - Naplózás
priority    - Prioritás opció
depends     - Függőség opció
and         - Logikai ÉS
or          - Logikai VAGY
not         - Logikai NEGÁCIÓ
true        - Boolean igaz érték
false       - Boolean hamis érték
high        - Magas prioritás
medium      - Közepes prioritás
low         - Alacsony prioritás
```

#### 2.1.2 Azonosítók (Identifiers)

Azonosítók változók és feladatok neveinek megadására szolgálnak.

**Szabály**: 
```
Identifier ::= [a-zA-Z_][a-zA-Z0-9_]*
```

**Példák**:
- `my_task`
- `variable1`
- `_private_var`
- `TaskName`

**Érvénytelen**:
- `123start` (számmal kezdődik)
- `my-task` (kötőjel nem megengedett)
- `task` (kulcsszó)

#### 2.1.3 Literálok

##### Számok (Numbers)

```
Number ::= [0-9]+ ('.' [0-9]+)?
```

**Példák**:
- `42` (egész szám)
- `3.14` (lebegőpontos)
- `0.5`
- `1000`

##### Karakterláncok (Strings)

```
String ::= '"' [^"]* '"'
```

**Példák**:
- `"Hello, World!"`
- `"Üzenet magyarul"`
- `"echo test"`
- `""`

**Megjegyzés**: Jelenleg az escape szekvenciák (`\"`, `\n`, stb.) nem támogatottak.

##### Boolean Értékek

```
Boolean ::= 'true' | 'false'
```

#### 2.1.4 Operátorok

##### Aritmetikai Operátorok

- `+` - Összeadás
- `-` - Kivonás, előjel
- `*` - Szorzás
- `/` - Osztás
- `%` - Maradékos osztás

##### Összehasonlító Operátorok

- `==` - Egyenlő
- `!=` - Nem egyenlő
- `<` - Kisebb
- `>` - Nagyobb
- `<=` - Kisebb vagy egyenlő
- `>=` - Nagyobb vagy egyenlő

##### Logikai Operátorok

- `and` - Logikai ÉS
- `or` - Logikai VAGY
- `not` - Logikai NEGÁCIÓ

#### 2.1.5 Szimbólumok

- `{` `}` - Blokk kezdet és vég
- `[` `]` - Lista kezdet és vég
- `(` `)` - Kifejezés csoportosítás
- `=` - Értékadás
- `:` - Opció elválasztó
- `,` - Lista elem elválasztó

#### 2.1.6 Megjegyzések

```
Comment ::= '//' [^\n]* '\n'
```

**Példa**:
```taskflow
// Ez egy egysoros megjegyzés
task example {
    // További megjegyzés
    log "test"
}
```

### 2.2 Whitespace

A szóközök, tabulátorok és sorvége karakterek whitespace-nek számítanak és figyelmen kívül maradnak (kivéve megjegyzéseken belül).

## 3. Szintaktikai Szabályok

### 3.1 Program Struktúra

Egy TaskFlow program egy vagy több feladat definícióból áll.

```ebnf
Program ::= TaskDef+
```

### 3.2 Feladat Definíció

```ebnf
TaskDef ::= 'task' Identifier '{' TaskBody '}'
```

**Szemantika**: 
- Feladat definiál egy végrehajtható egységet
- Az azonosító egyedi legyen a programon belül
- A feladat teste opciókat és utasításokat tartalmaz

**Példa**:
```taskflow
task my_task {
    log "Hello"
}
```

### 3.3 Feladat Teste

```ebnf
TaskBody ::= TaskOption* Statement*
```

A feladat teste két részből áll:
1. Opcionális konfigurációs beállítások (priority, depends)
2. Végrehajtandó utasítások

### 3.4 Feladat Opciók

#### 3.4.1 Priority (Prioritás)

```ebnf
PriorityOpt ::= 'priority' ':' ('high' | 'medium' | 'low')
```

**Szemantika**: A feladat fontossági szintjét határozza meg.

**Példa**:
```taskflow
task urgent {
    priority: high
    log "Fontos feladat"
}
```

#### 3.4.2 Depends (Függőségek)

```ebnf
DependsOpt ::= 'depends' ':' '[' (Identifier (',' Identifier)*)? ']'
```

**Szemantika**: Meghatározza, mely feladatok befejezése után hajtható végre ez a feladat.

**Példa**:
```taskflow
task deploy {
    depends: [build, test]
    log "Deployment"
}
```

### 3.5 Utasítások (Statements)

#### 3.5.1 Változó Deklaráció

```ebnf
VarDecl ::= 'let' Identifier '=' Expression
```

**Szemantika**: Új változót hoz létre és értéket ad neki.

**Példa**:
```taskflow
let count = 10
let name = "TaskFlow"
let ready = true
```

#### 3.5.2 Értékadás

```ebnf
Assignment ::= Identifier '=' Expression
```

**Szemantika**: Meglévő változó értékét módosítja.

**Példa**:
```taskflow
count = count + 1
name = "Updated"
```

#### 3.5.3 If-Else Utasítás

```ebnf
IfStmt     ::= 'if' Expression '{' Statement* '}' ElseClause?
ElseClause ::= 'else' '{' Statement* '}'
```

**Szemantika**: Feltételes végrehajtás. Ha a feltétel igaz, a `then` ág fut, különben az opcionális `else` ág.

**Példa**:
```taskflow
if x > 10 {
    log "Nagy érték"
} else {
    log "Kis érték"
}
```

#### 3.5.4 Repeat Ciklus

```ebnf
RepeatStmt ::= 'repeat' Expression 'times' '{' Statement* '}'
```

**Szemantika**: A blokk utasításait N-szer hajtja végre.

**Példa**:
```taskflow
repeat 5 times {
    log "Ismétlés"
}
```

#### 3.5.5 While Ciklus

```ebnf
WhileStmt ::= 'while' Expression '{' Statement* '}'
```

**Szemantika**: A blokk utasításait addig ismétli, amíg a feltétel igaz.

**Példa**:
```taskflow
while count < 100 {
    count = count + 1
}
```

#### 3.5.6 Run Utasítás

```ebnf
RunStmt ::= 'run' String
```

**Szemantika**: Shell parancsot hajt végre.

**Példa**:
```taskflow
run "mkdir -p /tmp/data"
run "npm install"
```

#### 3.5.7 Log Utasítás

```ebnf
LogStmt ::= 'log' Expression
```

**Szemantika**: Üzenetet naplóz.

**Példa**:
```taskflow
log "Feladat elkezdődött"
log count
log "Érték: " + value
```

### 3.6 Kifejezések (Expressions)

A kifejezések értékeket állítanak elő és támogatják az operátor precedenciát.

#### 3.6.1 Operátor Precedencia

Csökkenő sorrendben:

1. **Primér**: literálok, azonosítók, zárójelek
2. **Unáris**: `-` (negatív), `not`
3. **Multiplikatív**: `*`, `/`, `%`
4. **Additív**: `+`, `-`
5. **Összehasonlító**: `==`, `!=`, `<`, `>`, `<=`, `>=`
6. **Logikai AND**: `and`
7. **Logikai OR**: `or`

#### 3.6.2 Kifejezés Nyelvtan

```ebnf
Expression     ::= OrExpr
OrExpr         ::= AndExpr ('or' AndExpr)*
AndExpr        ::= NotExpr ('and' NotExpr)*
NotExpr        ::= 'not' NotExpr | Comparison
Comparison     ::= Additive (CompOp Additive)?
CompOp         ::= '==' | '!=' | '<' | '>' | '<=' | '>='
Additive       ::= Multiplicative (('+' | '-') Multiplicative)*
Multiplicative ::= Unary (('*' | '/' | '%') Unary)*
Unary          ::= '-' Unary | Primary
Primary        ::= Number | String | Boolean | Identifier
                 | '(' Expression ')' | ListExpr
ListExpr       ::= '[' (Expression (',' Expression)*)? ']'
```

#### 3.6.3 Példák

**Aritmetikai**:
```taskflow
let x = 10 + 20 * 3        // 70 (nem 90)
let y = (10 + 20) * 3      // 90
let z = -x + 5
```

**Logikai**:
```taskflow
let flag = true and not false
let test = x > 10 or y < 5
let complex = (a and b) or (c and d)
```

**Lista**:
```taskflow
let numbers = [1, 2, 3, 4, 5]
let names = ["Alice", "Bob", "Charlie"]
let mixed = [1, "text", true]
```

## 4. Szemantika

### 4.1 Típusrendszer

A TaskFlow dinamikusan típusos nyelv, de a következő típusokat különbözteti meg:

- **Number**: Egész és lebegőpontos számok
- **String**: Karakterláncok
- **Boolean**: Igaz/hamis értékek
- **List**: Elemek listája

### 4.2 Változó Hatókör

- Változók a feladat szintjén érvényesek
- Nincs globális változó
- Minden feladatnak saját változó névtere van

### 4.3 Feladat Végrehajtási Modell

1. **Függőség Feloldás**: A `depends` opcióban megadott feladatok először
2. **Prioritás Kezelés**: Magasabb prioritású feladatok előnyt élveznek
3. **Szekvenciális Végrehajtás**: Egy feladaton belül utasítások sorrendben

### 4.4 Kifejezés Kiértékelés

- **Eager evaluation**: Kifejezések azonnal kiértékelődnek
- **Short-circuit evaluation**: Logikai operátoroknál

Példa short-circuit-re:
```taskflow
if x > 0 and y / x > 10 {  // y/x nem értékelődik ki ha x <= 0
    log "OK"
}
```

## 5. Példa Programok

### 5.1 Egyszerű Feladat

```taskflow
task hello {
    log "Hello, TaskFlow!"
}
```

### 5.2 Változók és Aritmetika

```taskflow
task calculator {
    let a = 10
    let b = 5
    let sum = a + b
    let product = a * b
    let quotient = a / b
    
    log sum
    log product
    log quotient
}
```

### 5.3 Feltételes Logika

```taskflow
task validator {
    let age = 25
    let has_license = true
    
    if age >= 18 and has_license {
        log "Jogosult vezetni"
    } else {
        log "Nem jogosult vezetni"
    }
}
```

### 5.4 Ciklusok

```taskflow
task counter {
    let i = 0
    
    // Fix ismétlés
    repeat 10 times {
        log "Fix iteráció"
        i = i + 1
    }
    
    // Feltételes ismétlés
    while i < 20 {
        log "Feltételes iteráció"
        i = i + 1
    }
}
```

### 5.5 Komplex Workflow

```taskflow
task init {
    priority: high
    log "Inicializálás"
    run "mkdir -p /tmp/project"
    let initialized = true
}

task build {
    priority: medium
    depends: [init]
    
    log "Fordítás megkezdése"
    run "make clean"
    run "make all"
    
    let build_status = "success"
    
    if build_status == "success" {
        log "Fordítás sikeres"
    } else {
        log "Fordítás sikertelen!"
    }
}

task test {
    priority: medium
    depends: [build]
    
    log "Tesztek futtatása"
    
    let test_count = 0
    repeat 5 times {
        run "pytest test_suite.py"
        test_count = test_count + 1
    }
    
    log "Összes teszt: " + test_count
}

task deploy {
    priority: low
    depends: [test]
    
    log "Deployment indítása"
    run "docker build -t app:latest ."
    run "docker push app:latest"
    
    log "Deployment befejezve"
}
```

## 6. Kiterjesztési Lehetőségek

A nyelv könnyen bővíthető az alábbi funkciókkal:

### 6.1 Jövőbeni Funkciók

- **Függvények**: Újrafelhasználható kód blokkok
- **Import/Export**: Moduláris programszerkezet
- **Try-Catch**: Kivételkezelés
- **For-in ciklus**: Iterálás listákon
- **Dictionary típus**: Kulcs-érték párok
- **String interpolation**: Változók beágyazása stringekbe
- **Típus annotációk**: Statikus típusellenőrzés

### 6.2 Lehetséges Szintaxis Kiegészítések

```taskflow
// Függvények (jövőbeni)
function calculate(x, y) {
    return x + y
}

// Try-catch (jövőbeni)
try {
    run "risky_command"
} catch error {
    log "Hiba történt: " + error
}

// For-in (jövőbeni)
for item in items {
    log item
}
```

## 7. Implementációs Részletek

### 7.1 Parser Generátor

A TaskFlow parser Lark-ot használ LALR(1) parser módban.

**Előnyök**:
- Gyors és hatékony
- Bal-rekurzió kezelése
- Jó hibaüzenetek

### 7.2 AST Struktúra

Az Abstract Syntax Tree (AST) Python dataclass-okban van reprezentálva:

- `Program`: Gyökér node, feladatok listája
- `TaskDef`: Feladat definíció
- `Statement`: Utasítás bázis osztály
- `Expression`: Kifejezés bázis osztály

### 7.3 Transformer

A Lark Transformer az parse tree-t AST-vé alakítja:

- Operátor precedencia kezelés
- Típus konverziók
- Node létrehozás

## 8. Összefoglalás

A TaskFlow egy egyszerű, de kifejező nyelv feladatok automatizálására. Fő jellemzői:

✅ **Egyszerű szintaxis**  
✅ **Függőség kezelés**  
✅ **Prioritások**  
✅ **Ciklusok és feltételek**  
✅ **Változók és kifejezések**  
✅ **Pontos hibaüzenetek**  
✅ **Könnyen bővíthető**  

A nyelv tervezése során törekedtünk az egyszerűség és kifejezőerő optimális egyensúlyára, hogy könnyen tanulható legyen, de mégis képes legyen komplex automatizálási feladatok leírására.
