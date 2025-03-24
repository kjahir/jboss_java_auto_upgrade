import os
import tempfile
from file_updater import load_template, update_files

def test_simple_replacement():
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = os.path.join(temp_dir, 'sample.py')
        with open(test_file, 'w') as f:
            f.write("def old_function():\n    pass\n")

        template = """
FILES:*.py
FROM:
def old_function():
    pass
TO:
def new_function():
    print("updated")
"""

        template_file = os.path.join(temp_dir, 'template.txt')
        with open(template_file, 'w') as f:
            f.write(template)

        rules = load_template(template_file)
        update_files(temp_dir, rules)

        with open(test_file, 'r') as f:
            content = f.read()

        assert "def new_function()" in content
        assert "print(\"updated\")" in content