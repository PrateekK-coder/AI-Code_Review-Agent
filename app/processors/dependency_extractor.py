import ast

class DependencyExtractor:
    def extract_python_imports(self, code: str):

        dependencies = []

        try:
            tree = ast.parse(code)
        except SyntaxError:
            return dependencies

        for node in ast.walk(tree):

            # Handles:
            # import os
            # import Users.models
            if isinstance(node, ast.Import):

                for alias in node.names:
                    dependencies.append(alias.name)

            # Handles:
            # from Users.models import User
            # from Shares.services import calculate_price
            elif isinstance(node, ast.ImportFrom):

                if node.module:
                    dependencies.append(node.module)

        return list(set(dependencies))