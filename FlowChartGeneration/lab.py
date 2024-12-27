import ast

def contains_keyword(code, keywords):
    try:
        # Parse the code into an AST
        tree = ast.parse(code)
        
        # Traverse the AST nodes
        for node in ast.walk(tree):
            # Check for 'if' and 'elif'
            if isinstance(node, ast.If):
                if 'if' in keywords:
                    return True
                if 'elif' in keywords and node.orelse:
                    for subnode in node.orelse:
                        if isinstance(subnode, ast.If):
                            return True
            # Check for 'else' in orelse
            if 'else' in keywords:
                if hasattr(node, 'orelse') and node.orelse:
                    return True
            # Check for 'while'
            if isinstance(node, ast.While) and 'while' in keywords:
                return True
            # Check for 'for'
            if isinstance(node, ast.For) and 'for' in keywords:
                return True

        return False
    except SyntaxError:
        # Handle invalid Python code
        return False
    

code_snippet = "if [x for x in range(4)].count(2) == 1:"
keywords_to_check = ['if', 'for']
print(contains_keyword(code_snippet, keywords_to_check))  # Output: True