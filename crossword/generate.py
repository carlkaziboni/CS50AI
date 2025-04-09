import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3([])
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for domain_key in self.domains.keys():
            to_remove = set()
            for word in self.domains[domain_key]:
                if len(word) != domain_key.length:
                    to_remove.add(word)
            self.domains[domain_key] = self.domains[domain_key] - to_remove
        return

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        overlap_pair  = self.crossword.overlaps[x,y]
        if not overlap_pair:
            return revised
        to_remove_x = set()
        for x_domain_var in self.domains[x]:
            y_constraint = list(map(lambda y_domain_var: y_domain_var[overlap_pair[1]] == x_domain_var[overlap_pair[0]], self.domains[y]))
            if not any(y_constraint):
                revised = True
                to_remove_x.add(x_domain_var)
        self.domains[x] = self.domains[x] - to_remove_x
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = []
        if arcs or arcs == []:
            queue = arcs
        else:
            domain_keys = list(self.domains.keys())
            for i in range(len(domain_keys)):
                for y in range(len(domain_keys)):
                    if i == y:
                        continue
                    queue.append((domain_keys[i], domain_keys[y]))
        while queue:
            dequeued_pair = queue.pop(0)
            if self.revise(dequeued_pair[0], dequeued_pair[1]):
                if len(self.domains[dequeued_pair[0]]) == 0:
                    return False
                for z in self.crossword.neighbors(dequeued_pair[0]) - self.domains[dequeued_pair[1]]:
                    queue.append((z,dequeued_pair[0]))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        domain_keys = self.domains.keys()
        for domain_key in domain_keys:
            try:
                if assignment[domain_key] is None or len(assignment[domain_key]) == 0:
                    return False
            except KeyError:
                return False
        return True

    def consistent(self, assignment: dict):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        if sorted(list(assignment.values())) != sorted(list(set(assignment.values()))):
            return False
        domain_keys = self.domains.keys()
        for domain_key in domain_keys:
            try:
                if domain_key.length != len(assignment[domain_key]):
                    return False
                neighbors = self.crossword.neighbors(domain_key)
                for neighbor in neighbors:
                    overlap_pair = self.crossword.overlaps[domain_key, neighbor]
                    if assignment[domain_key][overlap_pair[0]] != assignment[neighbor][overlap_pair[1]]:
                        return False
            except KeyError:
                continue
        return True

    def order_domain_values(self, var, assignment:dict):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        var_words = self.domains[var]
        count = dict()
        for var_word in var_words:
            count[var_word] = 0
        neighbors = self.crossword.neighbors(var)
        assigned_vars = assignment.keys()
        for neighbor in neighbors:
            if neighbor in assigned_vars:
                continue
            paired = self.crossword.overlaps[var, neighbor]
            if paired is None:
                continue
            for var_word in var_words:
                for neighbor_word in self.domains[neighbor]:
                    if var_word[paired[0]] != neighbor_word[paired[1]]:
                        count[var_word] += 1
        final_list = list(sorted(count, key=count.get))
        return final_list

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        remaining_vars = set(self.domains.keys()) - set(assignment.keys())
        min = None
        for remaining_var in remaining_vars:
            if min is None:
                min = len(self.domains[remaining_var])
            if len(self.domains[remaining_var]) < min:
                min = len(self.domains[remaining_var])
        min_vars = []
        for remaining_var in remaining_vars:
            if min == len(self.domains[remaining_var]):
                min_vars.append(remaining_var)
        if len(min_vars) == 1:
            return min_vars[0]
        max = None
        for min_var in min_vars:
            if max == None:
                max = len(self.crossword.neighbors(min_var))
            if len(self.crossword.neighbors(min_var)) > max:
                max = len(self.crossword.neighbors(min_var))
        for min_var in min_vars:
            if max == len(self.crossword.neighbors(min_var)):
                return min_var
        return None

    def backtrack(self, assignment:dict):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        unassigned_var = self.select_unassigned_variable(assignment)
        for val in self.order_domain_values(unassigned_var, assignment):
            assignment[unassigned_var] = val
            if not self.consistent(assignment):
                del assignment[unassigned_var]
                continue
            while True:
                if not self.ac3():
                    break
            result = self.backtrack(assignment)
            if result is not None:
                return result
            del assignment[unassigned_var]
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
