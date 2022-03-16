# M1_Algo_Project
## Introduction

This project was done in the context of an algorithms course in the first year of Master's of Bioinformatics (Software development and Data analysis) at the University of Aix-Marseille.  
_To know more about Burrows–Wheeler transform:_  
https://en.wikipedia.org/wiki/Burrows%E2%80%93Wheeler_transform  
_To know more about Huffman compression:_  
https://en.wikipedia.org/wiki/Huffman_coding

## Main goals
- Create a user-friendly GUI using tkinter on python that groups the two algorithms.
- The user should be able to compress a DNA motif containing "A", "T", "C", "G", "N" or BWT-transfrom it.
- Or even enter a compressed sequence and decompress it back into its original decompressed state.
- Two different types of operations:  
    1 - Final result (Directly shows the result of the operation)  
    2 - Pedagogic step-by-step (By clicking "next", each click shows the next step.)
 ## Secondary goals
 - Huffman tree representation for the different letter values.  
 - Some tools that might be interesting for the user (Ex: taking a screenshot, changing the theme...).


## Requirements
To run this program, python3 is needed to be installed along with the packages mentioned inside:
- tkinter (includes .filedialog, .messagebox, .ttk...)
- codecs
- networkx
- matplotlib
- PIL (pillow)
- webbrowser
- asyncio
- pyscreenshot

And the following pngs:
- done.png
- not_done.png
- logo.png
- github_logo.png
- mail.png

And finally the following python scripts:  
- main.py
- huffman.py
- bwt.py
- model.py
- controller.py
- view.py
- customtext.py
- tooltip.py

All the files should be in the same directory.  
Also, it's recommended to run the main.py script from terminal. Sometimes the IDE doesn't allow for backend modification, which will fail to run the program

## Technical information
### Pedagogic Mode
Using python generators, with yield and next. Doesn't store each result in memory, rather overwrites the result before.
### Final Result
Returns the last item of the generator.
### CustomText
Highlights the BWT transformed or reconstructed sequences when using the pedagoic mode.
### ToolTip
Shows tips for the user when he hovers over the different buttons.  Also shows the real-time 

## About main.py
To run the program, we should call
```bash
python3 main.py
```
which directly runs the GUI mode on tkinter.

## To run the script

```bash
git clone https://github.com/GeorgeAlehandro/M1_Algo_Project/
python3 main.py
```

## Author
George Alehandro Saad
