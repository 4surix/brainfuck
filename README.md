Mini interpreter [Brainfuck](https://fr.wikipedia.org/wiki/Brainfuck) in [Python](https://www.python.org/).

## Commands

### Basic  

Symbol | Name | Desc
| --- | --- | --- |
| `<` | left | |
| `>` | right | |
| `+` | increment | |
| `-` | decrement | |
| `.` | print | |
| `,` | input | |
| `[` | begin | |
| `]` | end | |

### Bonus  

| Symbol | Name | Desc |
| --- | --- | --- |
| `!` | show | |
| `:` | macro | |


## Macro

### Exemples

```brainfuck
:5 {+++++}

:5:5:5 !
```
-> `15`

```brainfuck
:5 {+++++}

; Constantes
< :5:5:5:5:5:5++ :space {< . >}

; Variables
< + :_a {<<} :a_ {>>}
< + :_b {<<<} :b_ {>>>}
< + :_c {<<<<} :c_ {>>>>}

[>]

:_a +++++ ! :a_
:space
:_b :5 +++ ! :b_
:space
:_c :5:5:5 - ! :c_
```
-> `6 9 15`
