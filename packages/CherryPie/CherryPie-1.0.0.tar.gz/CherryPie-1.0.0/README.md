```
 _____ _                   _____ _
|     | |_ ___ ___ ___ _ _|  _  |_|___
|   --|   | -_|  _|  _| | |   __| | -_|
|_____|_|_|___|_| |_| |_  |__|  |_|___|
                      |___| V1.0.0

🍒 Build a beautiful CLI application. 
```
---
> **CherryPie** is a simple module that builds **CLI** applications allowing python developers to create simple **navigational UI**, **Loading screens**, **Progress bars**, **Styled text** and much **MORE**
---
### # Create and display a menu
#### Input
```py
x = Menu(['Tab 1', 'Tab 2', 'Tab 3', 'Tab 4'],
         ['Content for tab 1', 'Content for tab 2', 'Content for tab 3', 'Content for tab 4'])

x.display(0)
```
#### Output
```
  ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
  │ Tab 1 │ │ Tab 2 │ │ Tab 3 │ │ Tab 4 │
┌─┘       └─┴───────┴─┴───────┴─┴───────┴──────────────────────────────────────────────────┐  
│ Content for tab 1                                                                        │  
└──────────────────────────────────────────────────────────────────────────────────────────┘
```