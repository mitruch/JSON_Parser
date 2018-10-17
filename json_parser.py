import sys
import ast

class Parser:

    def __init__(self, file_path):
        self.file_path = file_path
        self.file = None
        self.marks_stack = []
        self.marks_pairs = {'[': ']', ']': '[', '{': '}', '}': '{', '"': '"'}

    def open_file(self):
        with open(self.file_path) as f:
            self.file = f.readlines()

    def is_open_mark(self, mark):
        if mark in '{[':
            return True
        else:
            return False

    def is_close_mark(self, mark):
        if mark in '}]':
            return True
        else:
            return False

    def parse(self):
        recent_mark = None  # Mark that was parsed before
        string_mode = False  # Flag for ignore syntax in string

        self.open_file()

        for idx, line in enumerate(self.file):
            print(line)
            for mark in line:
                # Ignore white spaces
                if mark.isspace():
                    continue

                # Check start keyword for object
                if recent_mark == '{' and mark != '"':
                    print('Syntax Error in line number {}'.format(idx + 1))
                    print('Error message: Expected keyword')
                    return
                # Check syntax at begin of structure
                elif self.marks_stack and self.marks_stack[0] != '{':
                    print('Syntax Error in line number {}'.format(idx + 1))
                    print('Error message: Expected \'{\' at the beggining of json structure')
                    return

                # Parse string
                if string_mode:
                    if mark == '"' and recent_mark != '\\':
                        string_mode = False # Finish string mode
                    else:
                        recent_mark = mark
                        continue
                elif mark == '"':
                    string_mode = True  # Start string mode

                # Add open mark on stack
                if self.is_open_mark(mark):
                    self.marks_stack.append(mark)

                # Remove mark from stack
                elif self.is_close_mark(mark):
                    if recent_mark == ',':
                        print('Syntax Error in line number {}'.format(idx + 1))
                        print('Error message: Unexpected \'{}\' at the end of structure '.format(recent_mark))
                        return

                    if self.marks_stack:
                        if self.marks_stack[-1] == self.marks_pairs[mark]:
                            self.marks_stack.pop()
                        else:
                            print('Syntax Error in line number {}'.format(idx + 1))
                            print('Error message: Unexpected end of \'{}\' '.format(self.marks_stack[-1]))
                            return

                # Remember recent mark for the next step in loop
                recent_mark = mark

        # After loop
        # Check if something wait on stack
        if len(self.marks_stack) != 0:
            print('Syntax Error at the EOF')
            print('Error message: Unexpected end of \'{}\' '.format(self.marks_stack[-1]))
            return
        else:
            try:
                ast.literal_eval(''.join(self.file))  # Ensure that paring is ok for Python
            except SyntaxError as se:
                print('SyntaxError: Invalid syntax in line {} at position {}'.format(se.lineno, se.offset))
                return

        # If everything ok
        print('Good json file')
        return 'OK'


def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        print('Required path to json file in the first argument')
        sys.exit()

    parser = Parser(file_path)  # Init Parse object with path to file
    parser.parse()  # Start parse


if __name__ == "__main__":
    main()