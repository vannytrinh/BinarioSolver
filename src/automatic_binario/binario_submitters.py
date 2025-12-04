import numpy as np
import requests
import re

class PuzzleBinarioSubmitter:
    URL = "https://www.puzzle-binairo.com/"

    def __init__(self, api_token):
        self.cookies = {"api_token": api_token}

    def _get_puzzle(self, puzzle):
        # Define request details
        url = self.URL + puzzle
        print(f"Getting puzzle from {url}")
        data = {"new": "+++New+Puzzle+++"}

        # Complete request
        response = requests.post(url, data=data, cookies=self.cookies)

        # Extract information from response
        # TODO: Extract puzzle number of rows and columns from response
        # TODO: Consider errors, task/param not found
        task = re.search(r"var\s+task\s*=\s*'([^']+)'", response.text).group(1)
        param = re.search(r'name="param" value="(.*?)"', response.text).group(1)

        # Print statements
        print(f"Task: {task}")

        return task, param

    def _submit_solution(self, param, serialized_soltuion, puzzle):
        # Define request details
        url = self.URL + puzzle
        data = {
            "param": param,
            "ansH": serialized_soltuion,
            "robot": 1,
            "ready": "+++Done+++",
        }

        # Complete request
        response = requests.post(url, data=data, cookies=self.cookies)

        # Check if puzzle successfully submitted
        # TODO: Check for other messages in response (Mistakes in solution, correct so far)
        success_msg = re.search(r'<p class="succ">([^<]+)</p>', response.text)
        if success_msg:
            print("Success message:", success_msg.group(1))
        else:
            print("No success message found.")

        # Extract information from response
        solparams = re.search(r'name="solparams"\s+value="([^"]+)"', response.text)
        if not solparams:
            print("No solparams found")
        else:
            solparams = solparams.group(1)
            print("Solparams found")

        return solparams

    def _submit_hall(self, solparams):
        # Define request details
        url = self.URL + "hallsubmit.php"
        data= {
            "submitscore": 1,
            "solparams": solparams,
            "robot": 1,
            "email": "vantrinh9903+bot@gmail.com"
        }

        # Complete request
        response = requests.post(url, data=data, cookies=self.cookies)

        # TODO: Check response for submission confirmation
        print("Submitted to hall of fame")

        return response

    def _decode_binairo_task(self, task, rows, cols):
        grid = []
        current_row = []

        for c in task:
            if c.isdigit():
                # Digit = filled cell
                current_row.append(int(c))
            elif c.isalpha():
                # Letter = skip this many empty cells
                skips = ord(c.lower()) - ord('a') + 1
                current_row.extend([-1] * skips)
            else:
                continue  # ignore anything else

            # If row is full, push to grid and start new row
            while len(current_row) >= cols:
                grid.append(current_row[:cols])
                current_row = current_row[cols:]

        # If any remaining cells in current_row, fill with -1
        if current_row:
            current_row.extend([-1]*(cols-len(current_row)))
            grid.append(current_row)

        return np.array(grid)

    def _serialize_solution(self, grid):
        return "".join(str(cell) for row in grid for cell in row)

    def run(self, solver, puzzle_type, rows, cols):
        # Get a new puzzle from the server
        task, param = self._get_puzzle(puzzle_type)

        # Decode puzzle
        puzzle = self._decode_binairo_task(task, rows, cols)
        print("Puzzle found:")
        print(puzzle)

        # Solve puzzle using input solver
        solution = solver.run(puzzle)
        print("Puzzle solved:")
        print(solution)

        # Serialize solution and submit
        serialized_soltuion = self._serialize_solution(solution)
        solparams = self._submit_solution(param, serialized_soltuion, puzzle_type)

        # If solution successfully submitted and solparams found, submit to hall of fame
        if solparams:
            response = self._submit_hall(solparams)
            return response