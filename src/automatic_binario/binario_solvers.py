import numpy as np

class EasyBinarioSolver:

    def _solve_adjacent_rule(self, line):
        length = len(line)
        line = line.copy()

        # Create sliding windows of lenth 3
        for i in range(length - 2):
            window = line[i:i + 3]

            # No empty spaces to fill in -> move on
            if -1 not in window:
                continue

            # Find position of empty space in window
            missing_index = np.where(window == -1)[0][0]

            # Two 0s -> empty space must be 1
            if np.sum(window == 0) == 2:
                line[i + missing_index] = 1

            # Two 1s -> empty space must be 0
            if np.sum(window == 1) == 2:
                line[i + missing_index] = 0

        return line

    def _solve_equality_rule(self, line):
        half = len(line) // 2
        line = line.copy()

        # Half of spaces are 0s -> remaining spaces must be 1s
        if np.sum(line == 0) == half:
            line[line == -1] = 1

        # Half of spaces are 0s -> remaining spaces must be 1s
        if np.sum(line == 1) == half:
            line[line == -1] = 0

        return line

    def _solve_line(self, line):
        line = self._solve_adjacent_rule(line)
        line = self._solve_equality_rule(line)
        return line

    def _check_adjacent_rule(self, line):
        # Create sliding windows of lenth 3
        length = len(line)
        for i in range(length - 2):
            window = line[i:i + 3]

            # If the three elements are all 0s or all 1s, line is incorrect
            if np.sum(window == 0) == 3 or np.sum(window == 1) == 3:
                return False

        return True

    def _check_equality_rule(self, line):
        # If more than half of the line are 0s or 1s, line is incorrect
        half = len(line) // 2

        if np.sum(line == 0) > half or np.sum(line != 1) > half:
            return False

        return True

    def _check_line(self, line):
        # Check that the input line follows adjacent and equality rule
        adjacent_rule = self._check_adjacent_rule(line)
        equality_rule = self._check_equality_rule(line)
        return adjacent_rule and equality_rule

    def _check_unique_rows(self, puzzle):
        # Iterate through all rows in the puzzle
        for i, row in enumerate(puzzle):
            # Compare current row to all rows after it
            for other in puzzle[i+1:]:
                if np.array_equal(row, other):
                    return False
        return True

    def check_puzzle(self, puzzle, complete=True):
        # (Default) Check if puzzle is complete
        if complete:
            check_incomplete = np.any(puzzle == -1)

            if check_incomplete:
                print("Puzzle is not complete")
                return False

        # Check each row and column follows the adjacent and equality rule
        check_rows = all(np.apply_along_axis(self._check_line, axis=1, arr=puzzle))
        if not check_rows:
            print("Puzzle's rows do not meet adjacent/equality rule")
            return False

        check_cols = all(np.apply_along_axis(self._check_line, axis=0, arr=puzzle))
        if not check_cols:
            print("Puzzle's cols do not meet adjacent/equality rule")
            return False

        # Check that each row is unique
        check_unqiue_rows = self._check_unique_rows(puzzle)
        if not check_unqiue_rows:
            print("Puzzle's rows are not unique")
            return False

        # Check that each col is unique by transposing the puzzle
        check_unqiue_cols = self._check_unique_rows(puzzle.T)
        if not check_unqiue_cols:
            print("Puzzle's cols are not unique")
            return False

        print("Puzzle is correct!")

        return True

    def run(self, puzzle):
        puzzle = puzzle.copy()

        move_made = True
        while move_made:
            move_made = False
            prev_puzzle_state = puzzle.copy()

            # Solve rows
            puzzle = np.apply_along_axis(self._solve_line, axis=1, arr=puzzle)

            # Solve columns
            puzzle = np.apply_along_axis(self._solve_line, axis=0, arr=puzzle)

            # Check if any moves made
            move_made = not np.array_equal(puzzle, prev_puzzle_state)

        return puzzle