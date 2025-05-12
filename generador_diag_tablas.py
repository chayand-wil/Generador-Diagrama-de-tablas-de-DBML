#!/usr/bin/env python3
import re
import argparse
import sys


class Table:
    def __init__(self, name, fields=None):
        self.name = name
        self.fields = fields or []
        self.references = []
    
    def add_reference(self, from_field, to_table, to_field):
        self.references.append(Reference(self.name, from_field, to_table, to_field))
    
    def generate_dbml(self):
        dbml = f"Table {self.name} {{"
        for field in self.fields:
            dbml += f"\n  {field}"
        dbml += "\n}"
        return dbml


class Reference:
    def __init__(self, from_table, from_field, to_table, to_field):
        self.from_table = from_table
        self.from_field = from_field
        self.to_table = to_table
        self.to_field = to_field
    
    def generate_dbml(self):
        return f"Ref: {self.from_table}.{self.from_field} > {self.to_table}.{self.to_field}"


def extract_datatype(field_type):
    """Extract clean data type from SQL field definition"""
    # Handle specific format types like VARCHAR(100) or DECIMAL(10,2)
    match = re.match(r'(\w+)(?:\((.*?)\))?', field_type)
    if match:
        base_type = match.group(1).upper()
        params = match.group(2)
        
        if params:
            return f"{base_type}({params})"
        return base_type
    
    return field_type.upper()


def parse_sql(sql_content):
    """Parse SQL content and extract table definitions and relationships"""
    # Regex patterns for CREATE TABLE statements
    table_pattern = re.compile(r"CREATE\s+TABLE\s+(?:`|\")?(\w+)(?:`|\")?\s*\((.*?)\);", re.DOTALL | re.IGNORECASE)
    
    # Pattern for individual field definitions
    field_pattern = re.compile(r"(?:`|\")?(\w+)(?:`|\")?\s+([^,\n]+?)(?:,|$)", re.DOTALL)
    
    # Pattern for foreign keys
    foreign_key_pattern = re.compile(
        r"FOREIGN\s+KEY\s+\(\s*(?:`|\")?(\w+)(?:`|\")?\s*\)\s+REFERENCES\s+(?:`|\")?(\w+)(?:`|\")?\s*\(\s*(?:`|\")?(\w+)(?:`|\")?\s*\)", 
        re.IGNORECASE
    )
    
    tables = []
    table_dict = {}  # To quickly look up tables by name
    references = []  # Store all references to add after all tables are processed
    
    # Extract table definitions
    for table_match in table_pattern.finditer(sql_content):
        table_name = table_match.group(1)
        fields_str = table_match.group(2)
        
        # Create table object
        table = Table(table_name)
        table_dict[table_name] = table
        
        # Extract field definitions
        field_entries = []
        for field_match in field_pattern.finditer(fields_str):
            field_name = field_match.group(1)
            field_type_raw = field_match.group(2).strip()
            
            # Skip if this is actually a constraint definition
            if re.match(r"(PRIMARY|FOREIGN|UNIQUE|CHECK|KEY)", field_type_raw, re.IGNORECASE):
                continue
                
            # Clean up the field type
            field_type = extract_datatype(field_type_raw.split()[0])
            
            # Add the field to the table
            field_entries.append(f"{field_name} {field_type}")
        
        table.fields = field_entries
        tables.append(table)
        
        # Extract foreign key constraints
        for fk_match in foreign_key_pattern.finditer(fields_str):
            from_field = fk_match.group(1)
            to_table = fk_match.group(2)
            to_field = fk_match.group(3)
            references.append((table_name, from_field, to_table, to_field))
    
    # Now add all references after all tables are processed
    for ref in references:
        from_table, from_field, to_table, to_field = ref
        if from_table in table_dict:
            table_dict[from_table].add_reference(from_field, to_table, to_field)
    
    return tables


def generate_dbml(tables):
    """Generate DBML code from parsed tables"""
    dbml_code = ""
    
    # Generate table definitions
    for table in tables:
        dbml_code += table.generate_dbml() + "\n\n"
    
    # Generate relationships
    for table in tables:
        for ref in table.references:
            dbml_code += ref.generate_dbml() + "\n"
    
    return dbml_code.strip()


def generate_dbml_from_sql(sql_content):
    """Main function to generate DBML from SQL content"""
    try:
        tables = parse_sql(sql_content)
        if not tables:
            return "// No tables found in the SQL file"
        dbml_code = generate_dbml(tables)
        return dbml_code
    except Exception as e:
        return f"// Error generating DBML: {str(e)}"


def main():
    parser = argparse.ArgumentParser(description='Convert SQL schema to DBML format')
    parser.add_argument('sql_file', help='Path to SQL file', nargs='?')
    parser.add_argument('-o', '--output', help='Output DBML file path')
    
    args = parser.parse_args()
    
    # Handle input
    if args.sql_file:
        try:
            with open(args.sql_file, 'r', encoding='utf-8') as file:
                sql_content = file.read()
        except Exception as e:
            print(f"Error reading SQL file: {str(e)}", file=sys.stderr)
            return 1
    else:
        # Read from stdin if no file is provided
        print("Reading SQL from stdin (press Ctrl+D to finish input)...")
        print("Pega el codigo sql (presiona ctrl+D para continuar)...")
        sql_content = sys.stdin.read()
    
    dbml_code = generate_dbml_from_sql(sql_content)
    
    # Handle output
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as file:
                file.write(dbml_code)
        except Exception as e:
            print(f"Error writing DBML file: {str(e)}", file=sys.stderr)
            return 1
    else:
        # Print to stdout if no output file is provided
        print('\n\n\n\t\t\tMade By Chayand and Claudia \n\n\n')
        print(dbml_code)
        print('\n\n\n\t\t\tsucces, codigo generado correctamente')

    
    return 0


if __name__ == "__main__":
    sys.exit(main())