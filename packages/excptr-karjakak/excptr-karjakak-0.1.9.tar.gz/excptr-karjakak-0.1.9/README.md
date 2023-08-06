# Excptr
## Decorator for catching exception and print them nicely
### [Production-Development]

## Installation
```
pip install excptr-karjakak
```

## Usage
```
@excp()
def ...

@excpcls()
class ...
```

## Example
```
Filename caller: /USERS/__MAIN__.PY

ERROR - <func_name>:
-----------------------------------------------------------------------
Start at:

line 26 in <module>:
    print(x.func_name(1, 3, '4'))

Filename: /USERS/EXCPTR.PY

line 111 in trac:
    if fn := f(*args, **kwargs):

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
<- Exception raise: TypeError ->
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

line 11 in addall:
    return(sum(args))

TypeError: unsupported operand type(s) for +: 'int' and 'str'
----------------------------------------------------------------------
```

## **Note**
- **There are 3 types of format:**
    - **-1 (by default) -> raise an exception**
    - **0 -> print exception in logical order and nicely**
    - **1 -> show exception in gui tkinter**
        - **Viewing limited in total of 60 seconds** 