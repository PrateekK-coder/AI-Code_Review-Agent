from pathlib import Path


class DependencyResolver:

    def __init__(self, code_files):
        self.code_files = code_files

    def resolve_python_import(self, module_name):

        module_path = module_name.replace(".", "/")

        for code_file in self.code_files:

            file_path = Path(code_file.file_path)

            if file_path.stem == module_path.split("/")[-1]:

                normalized_path = str(file_path).replace("\\", "/")

                expected_suffix = "/" + module_path + ".py"

                if normalized_path.endswith(expected_suffix):
                    return code_file

        return None