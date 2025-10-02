# User Manual - AFDGedit

## Project Information

### Developed by:
- **David Leonardo Espíndola Núñez** - Code. 202128390  
- **Juan David Lopez Castro** - Code. 202023451  

#### Universidad Pedagógica y Tecnológica de Colombia  
###### Faculty of Engineering  
###### Systems and Computer Engineering  
---

## Starting the Simulator

### Running the Program
1. Run the `main.py` file or open the executable (currently valid for Windows only)  
2. Main interface with drawing canvas  
3. Function buttons at the top  
4. Contextual instruction bar at the bottom  

## Building the DFA

### Creating States

**Create state:**
- Click on an empty area of the canvas  
- A blue circle appears, automatically numbered (q0, q1, q2...)  

**Move states:**
- Drag by clicking and holding  
- Transitions update automatically  

### Configuring States

**Initial state:**
1. Right-click on the desired state  
2. Select "Mark as initial"  
3. The state is marked in red  
4. Only one initial state is allowed per DFA  

**Accepting states:**
1. Right-click on any state  
2. Select "Mark as accepting"  
3. The state is marked in green with a double circle  
4. Multiple accepting states are allowed  

**Remove properties:**
- Right-click → "Unmark as initial" / "Unmark as accepting"  

### Creating Transitions

**Transition between states:**
1. Click on the source state (highlighted in orange)  
2. Click on the target state  
3. Enter the transition symbol in the pop-up window  
4. A labeled arrow appears  

**Self-transition:**
1. Right-click on a state  
2. Select "Self-transition"  
3. Enter the symbol for the loop  
4. A curved arc appears over the state  

**Cancel selection:**
- Clicking on an empty area cancels the active selection  

## Editing Tools

### Eraser Mode
1. Click the "Eraser" button (turns red)  
2. Click on states or transitions to delete  
3. Click again to deactivate  

### Full Reset
- "Clear All" deletes the entire DFA  
- Resets the canvas for a new design  

## Evaluation and Analysis

### String Evaluation

**Simple evaluator:**
1. "Evaluate String" → enter sequence  
2. Result: ACCEPTED/REJECTED with traversal path  

**Multiple evaluator:**
1. "Multiple Evaluator" → interactive window  
2. Test multiple strings with history  
3. Press Enter or "Evaluate" to process each string  

### Language Generation
- "Generate Strings" shows the first 10 valid strings  
- Useful to verify DFA behavior  

### Formal Analysis
- "View Quintuple" displays the complete mathematical definition  
- Includes completeness analysis and validation  

## Persistence

### Save
1. "Save" → choose location and name  
2. Readable JSON format  

### Load
1. "Load" → select JSON file  
2. Automatically redraws with circular layout  

## Controls and Navigation

### Keyboard Shortcuts
| Key | Function |
|-----|----------|
| `Ctrl+S` | Save DFA |
| `Ctrl+O` | Load DFA |
| `F5` | Evaluate string |
| `Delete` | Delete selected element |

### Visual Indicators

**States:**
- Blue: Normal state  
- Red: Initial state  
- Green: Accepting state  
- Orange: Selected state  
- Purple: Cursor hover  

**Transitions:**
- Straight arrow: Between different states  
- Curved arc: Self-transition  
- White label: Transition symbol  

### Context Menus
**Right-click on a state:**
- Mark/unmark as initial  
- Mark/unmark as accepting  
- Create self-transition  
- Delete state  

## System Validations

### Automatic Checks
- Initial state must exist before evaluation  
- At least one accepting state must exist  
- Transition symbols must be valid  
- Valid connections between states  

### Error Messages
- "You must define an initial state"  
- "You must define at least one accepting state"  
- "The symbol 'X' does not belong to the alphabet"  
- "Error creating transition"  

## Technical Limitations

- Optimal visualization: up to 20 states  
- Symbols: single characters only  
- Type: DFA only (no NFA)  
- Platform: Python 3.7+ or executable  

## Troubleshooting

### Technical Issues
**Program won’t start:**
- Check Python 3.7+  
- Verify tkinter: `python -m tkinter`  

**Elements not drawing:**
- Restart the program  
- Use "Clear All"  

**Error loading file:**
- Verify valid JSON format  
- Check correct state references  

### Usage Issues
**DFA does not accept expected strings:**
- Verify accepting states are defined  
- Check transition completeness  
- Use "View Quintuple" for analysis  

**Transitions not appearing:**
- Verify both states exist  
- Ensure the symbol is not empty  
- Try recreating the transition  

---

**AFDGedit**  
