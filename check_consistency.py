import re
from graphql import build_schema, GraphQLObjectType
from pathlib import Path

def extract_schema_fields(schema_str):
    schema = build_schema(schema_str)
    type_map = schema.type_map
    fields_map = {}
    for type_name, gql_type in type_map.items():
        if isinstance(gql_type, GraphQLObjectType) and not type_name.startswith("__"):
            fields_map[type_name] = list(gql_type.fields.keys())
    return fields_map

def extract_rules_fields(rules_str):
    rules_map = {}
    current_type = None
    for line in rules_str.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.endswith(":") and not line.startswith("-"):
            current_type = line[:-1]
            rules_map[current_type] = []
        elif line.startswith("-") and current_type:
            match = re.match(r'-\s*([a-zA-Z0-9_]+):', line)
            if match:
                rules_map[current_type].append(match.group(1))
    return rules_map

def compare(schema_fields, rules_fields):
    issues = []
    for t, fields in schema_fields.items():
        if t in rules_fields:
            missing = set(fields) - set(rules_fields[t])
            extra = set(rules_fields[t]) - set(fields)
            if missing:
                issues.append(f"⚠️ {t}: fields missing in rules → {', '.join(missing)}")
            if extra:
                issues.append(f"⚠️ {t}: rules mention non-existent fields → {', '.join(extra)}")
        else:
            issues.append(f"⚠️ Type {t} defined in schema but missing in rules")
    for t in rules_fields.keys() - schema_fields.keys():
        issues.append(f"⚠️ Type {t} defined in rules but not in schema")
    return issues

if __name__ == "__main__":
    schema = Path("schema.graphql").read_text()
    rules = Path("rules.txt").read_text()
    schema_fields = extract_schema_fields(schema)
    rules_fields = extract_rules_fields(rules)
    issues = compare(schema_fields, rules_fields)
    if issues:
        print("Consistency check found issues:")
        for i in issues:
            print(" -", i)
    else:
        print("✅ Schema and rules are consistent")
