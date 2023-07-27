import re
import subprocess
import os

def head():
    print('\t\t\t *** C++ Compiler *** \n')


#Input lines for CODE

multipleLines = []

print("\nEnter C++ Code: (write 'done' to exit) --->\n")

while True:
    line = input()
    if line != 'done':
        multipleLines.append(line)
    else:
        break

code = '\n'.join(multipleLines)

#SYNTAX CHECK

def run_syntax_check(code):
    # write the code to a temporary file
    with open("temp.cpp", "w") as f:
        f.write(code)
    # run the syntax check using the g++ compiler
    process = subprocess.Popen(["g++", "-fsyntax-only", "temp.cpp"], stderr=subprocess.PIPE)
    output = process.stderr.read().decode()
    # if there are no syntax errors, compile and run the code
    if output == "":
        print("\nSYNTAX CORRECT!!!\n")
        subprocess.run(["g++", "temp.cpp"])
        process = subprocess.Popen("./a.exe", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.stdout.read().decode()

    # if there are syntax errors, display them
    else:
        print("There are syntax errors in your code:\n" + output)
    
    

#CODE EXECUTER

def code_out(code):
    # write the code to a temporary file
    with open("temp.cpp", "w") as f:
        f.write(code)
    # run the syntax check using the g++ compiler
    process = subprocess.Popen(["g++", "-fsyntax-only", "temp.cpp"], stderr=subprocess.PIPE)
    output = process.stderr.read().decode()
    # if there are no syntax errors, compile and run the code
    if output == "":
        print("\nSYNTAX CORRECT!!!\n========\n OUTPUT:\n========\n")
        subprocess.run(["g++", "temp.cpp"])
        process = subprocess.Popen("./a.exe", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = process.stdout.read().decode()
        # display the output of the code
        print(output,'\n')
    # if there are syntax errors, display them
    else:
        print("There are syntax errors in your code:\n" + output)
    # delete the temporary file
    

# Define regular expressions for tokens
keywords = ['auto', 'break', 'case', 'char', 'const', 'continue', 'default',
            'do', 'double', 'else', 'enum', 'extern', 'float', 'for', 'goto',
            'if', 'int', 'long', 'register', 'return', 'short', 'signed',
            'sizeof', 'static', 'struct', 'switch', 'typedef', 'union',
            'unsigned', 'void', 'volatile', 'while']
identifier = r'[a-zA-Z_]\w*'
integer_literal = r'\d+'
floating_literal = r'\d+\.\d+f?'
string_literal = r'".*"'
punctuators = r'\{|\}|\[|\]|\(|\)|\.|->|\+\+|--|&|\*|\+|-|~|!|/|%|<<|>>|<|<=|>|>=|==|!=|^|&amp;|\||&&|\|\||\?|:|;|\.+|,|#|##|\.\.\.'

# Combine regular expressions into a single pattern
pattern = '|'.join([floating_literal, integer_literal, identifier, string_literal, punctuators] + keywords)

# Tokenize the code using the regular expression pattern
tokens = re.findall(pattern, code)


def parse(tokens):
    stack = []
    while tokens:
        token = tokens.pop(0)
        if token in keywords:
            stack.append(('keyword', token))
        elif re.match(identifier, token):
            stack.append(('identifier', token))
        elif re.match(integer_literal, token):
            stack.append(('integer', int(token)))
        elif re.match(floating_literal, token):
            stack.append(('float', float(token)))
        elif re.match(string_literal, token):
            stack.append(('string', token))
        else:
            if token == '(':
                # Recursively parse the subexpression inside the parentheses
                subexpression, tokens = parse(tokens)
                stack.append(('subexpression', subexpression))
            elif token == ')':
                # Return the stack and remaining tokens when encountering the closing parenthesis
                return stack, tokens
            else:
                stack.append(('operator', token))
    return stack, []  # Return an empty list as the second value

# Define a function to generate a parse tree from a stack
def generate_parse_tree(stack):
    parse_tree = []
    while stack:
        item = stack.pop(0)
        if item[0] == 'subexpression':
            # Recursively generate a parse tree for the subexpression
            parse_tree.append(('subexpression', generate_parse_tree(item[1])))
        else:
            parse_tree.append(item)
    return parse_tree

# Intermediate code generator

def generate_intermediate_code(parse_tree):
    intermediate_code = []
    for node in parse_tree:
        if node[0] == 'subexpression':
            intermediate_code.append(generate_intermediate_code(node[1]))
        elif node[0] == 'operator':
            if node[1] == '<<':
                # Replace cout<< with print(
                intermediate_code.append('')
            else:
                intermediate_code.append(node[1])
        elif node[0] == 'identifier':
            if node[1] == 'cout':
                # Replace cout with print(
                intermediate_code.append('print(')
            elif node[1]== 'endl':
                intermediate_code.append('')
            else:
                intermediate_code.append(node[1])
        elif node[0] == 'integer':
            intermediate_code.append(str(node[1]))
        elif node[0] == 'float':
            intermediate_code.append(str(node[1]))
        elif node[0] == 'string':
            intermediate_code.append(node[1])
        elif node[0] == 'keyword':
            intermediate_code.append(node[1])
        else:
            raise ValueError(f'Unknown node type: {node[0]}')
    code = ' '.join(intermediate_code)
    
    # Replace <<endl with )
    code = code.replace('<<endl', ')')
    
    return code



def optimize_code(code):
    # Remove all comments
    code = re.sub('//.*', '', code)

    # Remove all header files
    code = re.sub('#include\s*<\w+(\.\w+)*>\n', '', code)

    # Remove all escape sequences
    code = re.sub('\\\\\w', '', code)

    # Remove int main() and using namespace std;
    code = re.sub('\s*int main\s*\(\s*\)\s*{|using namespace std\s*;', '', code)

    # Replace cout<< with print
    code = code.replace('cout<<', 'print(')

    code = code.replace('cout <<', 'print(')

    code = code.replace('cout<< ', 'print(')
    
    code = code.replace('cout << ', 'print(')

    code = code.replace('<<', ')')

  # Replace cout<< with print
    code = code.replace('<<endl', '')
    code = code.replace(' <<endl', '')
    code = code.replace('<< endl', '')
    code = code.replace(' << endl', '')

    code = code.replace('<<endl ', '')
    code = code.replace(' <<endl ', '')
    code = code.replace('<< endl ', '')
    code = code.replace(' << endl ', '')

    code = code.replace('endl', '')
    code = code.replace(' endl', '')
    code = code.replace('endl ', '')
    code = code.replace(' endl ', '')


    # Remove all occurrences of keywords
    for keyword in keywords:
        code = re.sub('\\b' + keyword + '\\b', '', code)

    # Remove all unnecessary whitespace
    #code = re.sub('\s+', ' ', code)

    # Remove all unnecessary brackets
    code = re.sub('[{}]', '', code)

    # Remove all semicolons
    code = re.sub(';', '', code)

    return code.strip()

def generate_machine_code(code):
    # create a temporary file with .cpp extension
    temp_file_name = 'temp_file'
    temp_file_cpp = temp_file_name + '.cpp'
    temp_file_o = temp_file_name + '.o'
    
    # write the code to the temp file
    with open(temp_file_cpp, 'w') as f:
        f.write(code)
        
    # compile the temp file using g++
    subprocess.check_output(['g++', '-c', temp_file_cpp])
    subprocess.check_output(['g++', '-o', 'a.exe', temp_file_o])
    
    # delete the temp files
    os.remove(temp_file_cpp)
    os.remove(temp_file_o)
    
    # return the machine code
    with open('a.exe', 'rb') as f:
        return f.read()

def parser():
    stack, _ = parse(tokens[:])
    for item in stack:
        print(item)

head()
print('\n \t*** Your Code: ***\n', code)


def menu():
    print(
        """
        Compiler Menu: Choose an Option -->
        1. Syntax Check
        2. Tokenize
        3. Parse
        4. Parse Tree
        5. Code Optimization
        6. Code Output
        7. Machine Code
        0. Exit
        """)


Flag = True

while Flag:
    menu()
    print("\nChoice: ")
    choice = int(input())
    if choice == 1:
        print("\nSyntax of Code: --> \n")
        print('\n \t*** Your Code: ***\n', code)
        run_syntax_check(code)
    elif choice == 2:
        print("\nTokenization: --> \n")
        print(', '.join(["'" + token + "'" for token in tokens]))
    elif choice == 3:
        print("\nParse: --> \n")
        def parser():
            stack, _ = parse(tokens[:])
            for item in stack:
                print(item)
        parser()
    elif choice == 4:
        print("\nParse Tree: --> \n")
        stack, _ = parse(tokens)
        parse_tree = generate_parse_tree(stack)
        print(parse_tree)
    elif choice == 5:
        print("\nOptimized Code: --> \n")
        optimized_code = optimize_code(code)
        print(optimized_code)
    elif choice == 6:
        print("\nOutput of Code: --> \n")
        code_out(code)
    elif choice == 7:
        print("\nMachine Code: --> \n")
        machine_code = generate_machine_code(code)
        print(machine_code)
    elif choice == 0:
        print("\nProgram is about to exit..........\n\n")
        os.remove("temp.cpp")
        Flag = False
    else:
        print("Wrong Choice... Try Again.....")

