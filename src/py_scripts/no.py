# @VS@ echo -e "Line 1\nLine 2\nLine 3" | python _file
# Line numbers on output

import sys

def rich_branch_callback():
    from rich.console import Console
    from rich.text import Text

    console = Console()
    style_prefix = "bold blue"
    second_column = "red"
    def helper(s1, s2):
        # prefix = Text(s1, style=style_prefix)  # Style only the prefix
        # line_text = Text(s2, style=second_column)  # Plain text for the line content
        # console.print(prefix, line_text)
        return s1 + ' ' + s2
    return helper

if __name__ == "__main__":
    lines = sys.stdin.read().strip().split('\n')
    # if len(sys.argv) == 2:
    #     use_rich = bool(int(sys.argv[1]))
    # else:
    #     try:
    #         import rich
    #         use_rich = False
    #     except:
    #         use_rich = False
    use_rich = False

    if use_rich:
        print("Using rich")
        print_callback = rich_branch_callback()
    else:
        def print_callback(s1, s2):
            # print(f'{s1} {s2}')
            # print(s1 + ' ' + s2)
            if( len(s2.strip()) == 0 ):
                return ''
            return s1 + ' ' + s2
   
    num_lines = len(lines)
    col_width = len(str(num_lines))
    def delim(x):
        length = col_width - len(str(x))
        return length * " "
   
    u = ''
    for i, line in enumerate(lines):
        s1 = f"{i}{delim(i)}"
        # print(s1)
        s2 = line
        u += print_callback(s1, s2) + '\n'
    if len(sys.argv) >= 2:
        print(u)
    else:
        with open('C:\\Users\\tmasthay\\.basher\\.tmp\\no.out', 'w') as f:
            f.write(u)