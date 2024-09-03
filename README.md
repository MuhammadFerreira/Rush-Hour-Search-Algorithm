https://github.com/HamzahSheikh/COMP472-MP2

# COMP472-MP2
Mini Project 2 for AI

***Important: Install all dependencies before proceedong!

### About this repo

In this mini-project a variety of search algorithms were implemented and analysed to play Rush Hour. 

### Running the Application

Clone the Repository

```
git clone https://github.com/HamzahSheikh/COMP472-MP2.git
```

Change directory into COMP472-MP2

```
cd COMP472-MP2
```

Run the following command

```
python rush-hour.py
```

## To add the path to a file containing an input, change line 103 with the appropriate path:

```
102 f = open(r"C:\Users\Hamzah\Projects\COMP472-MP2\Sample\sample-input.txt", 'r')
```

## To change the path where the ouput files will be stored, change line 20 and 85 to the appropriate path:

```
20 f = open(r"C:\Users\Hamzah\Projects\COMP472-MP2\results\\"+str(searchType)+"-sol-"+str(gameNumber)+".txt", 'w')
...
85 f = open(r"C:\Users\Hamzah\Projects\COMP472-MP2\results\\"+str(searchType)+"-search-"+str(gameNumber)+".txt", 'w')
```
