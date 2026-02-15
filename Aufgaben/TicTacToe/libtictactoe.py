"""Helper module for task "Tic Tac Toe

exports:
  TicTacToe -- DataClass for holding a tic tac toe board state
"""
from dataclasses import dataclass

@dataclass
class TicTacToe:
    """An intermediary representation for tic tac toe board states"""
    raw: tuple[int]
    
    @property
    def rows(self):
        return tuple(self.raw[i:i+3] for i in range(0, 7, 3))
    
    @property
    def cols(self):
        return tuple(self.raw[i::3] for i in range(3))
    
    @property
    def diags(self):
        return (self.raw[::4], self.raw[2:7:2])
    
    @property
    def to_move(self):
        return 1 - 2 * sum(self.raw)
    
    def __post_init__(self):
        """Sanity checks to ensure that the board state is valid.
        
        These checks are similar to the ones that have to be used while reading in a state,'
        and you are free to use them in the first portion of the task
        (if you succeed in encoding a state as a `tuple[int]`)
        or adapt them as desired.
        
        Diese Checks ähneln denen, die beim Einlesen von Zuständen gemacht werden müssen.
        Sie dürfen sie für den ersten Teil der Aufgabe übernehmen
        (falls Sie Zustände korrekt als `tuple[int]` codieren konnten)
        oder sie nach Wunsch anpassen.
        """
        if (i := len(self.raw)) != 9:
            raise ValueError(f'Invalid board state: number of items {i} != 9')
        if not (s := set(self.raw)).issubset({-1, 0, 1}):
            raise ValueError(f'Invalid board state: symbols {(s - {-1, 0, 1})} invalid.')
        if (m := self.to_move) not in (-1, 1):
            faulty = "first" if m > 1 else "second"
            raise ValueError(f'Invalid board state: {faulty} player has made too many moves.')
     
    def __str__(self):
        return '\n-+-+-\n'.join(
            '|'.join(
                ('X' if i == 1 else 'O' if i == -1 else ' ')
                for i in row
            )
            for row in self.rows
        )
