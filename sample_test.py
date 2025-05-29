# sample_test.py

def simple_function():
    return sum([1, 2, 3])


def medium_complexity(x):
    if x > 0:
        for i in range(x):
            print(i)
    else:
        print("No items")


def high_complexity(x):
    result = []
    for i in range(x):
        if i % 2 == 0:
            for j in range(i):
                if j % 3 == 0:
                    result.append((i, j))
                else:
                    result.append(j)
        else:
            result.append(i * 2)
    return result


def style_issues():
    a=1+2
    print(  a)
    long_line = "This is a very long line that will exceed the standard seventy-nine character limit for Python code, causing a PEP8 warning"
    print("This line is indented with spaces")


# Expected Result

# Analysis for sample_test.py:

# Cyclomatic Complexity:
# simple_function (line 3): complexity 1    [green]
# medium_complexity (line 7): complexity 3  [green]
# high_complexity (line 15): complexity 5   [green]
# style_issues (line 29): complexity 1      [green]

# Average complexity: 2.50

# Style Issues (PEP8):
# sample_test.py:30:6: E225 missing whitespace around operator         [purple]
# sample_test.py:31:11: E201 whitespace after '('                     [purple]
# sample_test.py:32:80: E501 line too long (exceeds 79 characters)   [purple]
# sample_test.py:33:47: W292 no newline at end of file               [purple]
