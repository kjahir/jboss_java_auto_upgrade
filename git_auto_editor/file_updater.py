import os
import re
import fnmatch

def load_template(template_path):
    with open(template_path, 'r') as f:
        content = f.read()

    blocks = content.strip().split('---')
    rules = []

    for block in blocks:
        condition = None
        file_pattern = '*'
        from_str = ''
        to_str = ''
        is_regex = False

        lines = block.strip().split('\n')
        mode = None

        for line in lines:
            if line.startswith("CONDITION:"):
                condition = line[len("CONDITION:"):].strip()
            elif line.startswith("FILES:"):
                file_pattern = line[len("FILES:"):].strip()
            elif line.startswith("FROM:REGEX:"):
                is_regex = True
                mode = 'FROM'
                from_str = line[len("FROM:REGEX:"):].strip() + '\n'
            elif line.startswith("FROM:"):
                is_regex = False
                mode = 'FROM'
                from_str = line[len("FROM:"):].strip() + '\n'
            elif line.startswith("TO:"):
                mode = 'TO'
                to_str = line[len("TO:"):].strip() + '\n'
            else:
                if mode == 'FROM':
                    from_str += line + '\n'
                elif mode == 'TO':
                    to_str += line + '\n'

        rules.append({
            "condition": condition,
            "file_pattern": file_pattern,
            "from": from_str.rstrip('\n'),
            "to": to_str.rstrip('\n'),
            "is_regex": is_regex
        })

    return rules

def match_file_pattern(file_name, pattern):
    return fnmatch.fnmatch(file_name, pattern)

def update_files(folder_path, rules):
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except:
                continue  # Skip unreadable files

            original_content = content
            updated = False

            for rule in rules:
                if not match_file_pattern(file, rule["file_pattern"]):
                    continue

                if rule["condition"] and rule["condition"] not in content:
                    continue

                if rule["is_regex"]:
                    content, count = re.subn(rule["from"], rule["to"], content, flags=re.MULTILINE)
                    if count > 0:
                        updated = True
                else:
                    if rule["from"] in content:
                        content = content.replace(rule["from"], rule["to"])
                        updated = True

            if updated:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)