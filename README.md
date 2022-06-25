# Connect-4

## How to use

```bash
# Clone this repository
git clone https://github.com/GouruRK/Connect-4.git

# Go in the repository
cd Connect-4

# Launch the game
python3 main.py --display <graphic|text>
```

## How it works

The whole game can be see such as a this grid

| 0  | 1  | 2  | 3  | 4  | 5  | 6  |
|----|----|----|----|----|----|----|
| 10 | 11 | 12 | 13 | 14 | 15 | 16 |
| 20 | 21 | 22 | 23 | 24 | 25 | 26 |
| 30 | 31 | 32 | 33 | 34 | 35 | 36 |
| 40 | 41 | 42 | 43 | 44 | 45 | 46 |
| 50 | 51 | 52 | 53 | 54 | 55 | 56 |

So, the main idea behind this project is just to store tokens positions in two different set depending on the player's turn, and play with indexes and step between indexes to know if someone wins

### Example :
The last players who played placed a token at position 33 :

| Directions  | Begin | End | Step | 
|-------------|-------|-----|------|
| Lines       | 30    | 36  | 1    |
| Columns     | 3     | 63  | 10   |
| Diagonal 1  | 0     | 66  | 11   |
| Diagonal 2  | 6     | 60  | 9    |

So, starting from position `x`, its basically :

| Directions  | Begin | End | Step | 
|-------------|-------|-----|------|
| Lines       | x-3   | x+3 | 1    |
| Columns     | x-30  | x+30| 10   |
| Diagonal 1  | x-33  | x+33| 11   |
| Diagonal 2  | x-27  | x+27| 9    |

* *`Diagonal 1` refers to the diagonal from top left to bottom right*

* *`Diagonal 2` refers to the diagonal from bottom left to top right*