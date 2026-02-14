"""
Mini SQL Compiler
A simple SQL compiler that implements lexical analysis, syntax parsing, and query execution
Supports: CREATE TABLE, INSERT, SELECT, UPDATE, DELETE, DROP TABLE
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum

class TokenType(Enum):
    """Token types for lexical analysis"""
    # Keywords
    SELECT = "SELECT"
    FROM = "FROM"
    WHERE = "WHERE"
    INSERT = "INSERT"
    INTO = "INTO"
    VALUES = "VALUES"
    UPDATE = "UPDATE"
    SET = "SET"
    DELETE = "DELETE"
    CREATE = "CREATE"
    TABLE = "TABLE"
    DROP = "DROP"
    AND = "AND"
    OR = "OR"
    
    # Data types
    INT = "INT"
    VARCHAR = "VARCHAR"
    FLOAT = "FLOAT"
    DATE = "DATE"
    
    # Operators
    EQUALS = "="
    NOT_EQUALS = "!="
    LESS_THAN = "<"
    GREATER_THAN = ">"
    LESS_EQUAL = "<="
    GREATER_EQUAL = ">="
    
    # Symbols
    LPAREN = "("
    RPAREN = ")"
    COMMA = ","
    SEMICOLON = ";"
    ASTERISK = "*"
    
    # Literals
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    NUMBER = "NUMBER"
    
    # Special
    EOF = "EOF"

class Token:
    """Represents a token in the SQL query"""
    def __init__(self, token_type: TokenType, value: Any, position: int = 0):
        self.type = token_type
        self.value = value
        self.position = position
    
    def __repr__(self):
        return f"Token({self.type}, {self.value})"

class Lexer:
    """Lexical Analyzer - converts SQL query into tokens"""
    
    KEYWORDS = {
        'SELECT': TokenType.SELECT,
        'FROM': TokenType.FROM,
        'WHERE': TokenType.WHERE,
        'INSERT': TokenType.INSERT,
        'INTO': TokenType.INTO,
        'VALUES': TokenType.VALUES,
        'UPDATE': TokenType.UPDATE,
        'SET': TokenType.SET,
        'DELETE': TokenType.DELETE,
        'CREATE': TokenType.CREATE,
        'TABLE': TokenType.TABLE,
        'DROP': TokenType.DROP,
        'AND': TokenType.AND,
        'OR': TokenType.OR,
        'INT': TokenType.INT,
        'VARCHAR': TokenType.VARCHAR,
        'FLOAT': TokenType.FLOAT,
        'DATE': TokenType.DATE,
    }
    
    def __init__(self, query: str):
        self.query = query
        self.position = 0
        self.tokens: List[Token] = []
    
    def tokenize(self) -> List[Token]:
        """Convert SQL query into list of tokens"""
        while self.position < len(self.query):
            self._skip_whitespace()
            
            if self.position >= len(self.query):
                break
            
            # Check for comments
            if self._peek() == '-' and self._peek(1) == '-':
                self._skip_comment()
                continue
            
            # Check for strings
            if self._peek() in ["'", '"']:
                self.tokens.append(self._read_string())
            # Check for numbers
            elif self._peek().isdigit():
                self.tokens.append(self._read_number())
            # Check for identifiers/keywords
            elif self._peek().isalpha() or self._peek() == '_':
                self.tokens.append(self._read_identifier())
            # Check for operators and symbols
            elif self._peek() in '(),:;*':
                self.tokens.append(self._read_symbol())
            elif self._peek() in '=!<>':
                self.tokens.append(self._read_operator())
            else:
                raise SyntaxError(f"Unexpected character: {self._peek()} at position {self.position}")
        
        self.tokens.append(Token(TokenType.EOF, None, self.position))
        return self.tokens
    
    def _peek(self, offset: int = 0) -> str:
        """Look at character without consuming it"""
        pos = self.position + offset
        if pos < len(self.query):
            return self.query[pos]
        return '\0'
    
    def _advance(self) -> str:
        """Consume and return current character"""
        char = self._peek()
        self.position += 1
        return char
    
    def _skip_whitespace(self):
        """Skip whitespace characters"""
        while self._peek().isspace():
            self._advance()
    
    def _skip_comment(self):
        """Skip SQL comments (-- comment)"""
        while self._peek() != '\n' and self._peek() != '\0':
            self._advance()
    
    def _read_string(self) -> Token:
        """Read string literal"""
        start_pos = self.position
        quote_char = self._advance()
        value = ''
        
        while self._peek() != quote_char and self._peek() != '\0':
            if self._peek() == '\\':
                self._advance()
                if self._peek() != '\0':
                    value += self._advance()
            else:
                value += self._advance()
        
        if self._peek() == quote_char:
            self._advance()
        else:
            raise SyntaxError(f"Unterminated string at position {start_pos}")
        
        return Token(TokenType.STRING, value, start_pos)
    
    def _read_number(self) -> Token:
        """Read numeric literal"""
        start_pos = self.position
        value = ''
        
        while self._peek().isdigit() or self._peek() == '.':
            value += self._advance()
        
        # Convert to appropriate type
        if '.' in value:
            return Token(TokenType.NUMBER, float(value), start_pos)
        else:
            return Token(TokenType.NUMBER, int(value), start_pos)
    
    def _read_identifier(self) -> Token:
        """Read identifier or keyword"""
        start_pos = self.position
        value = ''
        
        while self._peek().isalnum() or self._peek() == '_':
            value += self._advance()
        
        # Check if it's a keyword
        upper_value = value.upper()
        if upper_value in self.KEYWORDS:
            return Token(self.KEYWORDS[upper_value], upper_value, start_pos)
        
        return Token(TokenType.IDENTIFIER, value, start_pos)
    
    def _read_symbol(self) -> Token:
        """Read single character symbols"""
        start_pos = self.position
        char = self._advance()
        
        symbol_map = {
            '(': TokenType.LPAREN,
            ')': TokenType.RPAREN,
            ',': TokenType.COMMA,
            ';': TokenType.SEMICOLON,
            '*': TokenType.ASTERISK,
        }
        
        return Token(symbol_map[char], char, start_pos)
    
    def _read_operator(self) -> Token:
        """Read comparison operators"""
        start_pos = self.position
        char = self._advance()
        
        # Check for two-character operators
        if char == '=' and self._peek() != '=':
            return Token(TokenType.EQUALS, '=', start_pos)
        elif char == '!' and self._peek() == '=':
            self._advance()
            return Token(TokenType.NOT_EQUALS, '!=', start_pos)
        elif char == '<' and self._peek() == '=':
            self._advance()
            return Token(TokenType.LESS_EQUAL, '<=', start_pos)
        elif char == '>' and self._peek() == '=':
            self._advance()
            return Token(TokenType.GREATER_EQUAL, '>=', start_pos)
        elif char == '<':
            return Token(TokenType.LESS_THAN, '<', start_pos)
        elif char == '>':
            return Token(TokenType.GREATER_THAN, '>', start_pos)
        
        raise SyntaxError(f"Invalid operator at position {start_pos}")

class ASTNode:
    """Base class for Abstract Syntax Tree nodes"""
    pass

class CreateTableNode(ASTNode):
    def __init__(self, table_name: str, columns: List[Tuple[str, str]]):
        self.table_name = table_name
        self.columns = columns

class InsertNode(ASTNode):
    def __init__(self, table_name: str, columns: Optional[List[str]], values: List[Any]):
        self.table_name = table_name
        self.columns = columns
        self.values = values

class SelectNode(ASTNode):
    def __init__(self, columns: List[str], table_name: str, where_clause=None):
        self.columns = columns
        self.table_name = table_name
        self.where_clause = where_clause

class UpdateNode(ASTNode):
    def __init__(self, table_name: str, assignments: Dict[str, Any], where_clause=None):
        self.table_name = table_name
        self.assignments = assignments
        self.where_clause = where_clause

class DeleteNode(ASTNode):
    def __init__(self, table_name: str, where_clause=None):
        self.table_name = table_name
        self.where_clause = where_clause

class DropTableNode(ASTNode):
    def __init__(self, table_name: str):
        self.table_name = table_name

class WhereClause:
    def __init__(self, column: str, operator: str, value: Any, logical_op: str = None, next_condition=None):
        self.column = column
        self.operator = operator
        self.value = value
        self.logical_op = logical_op
        self.next_condition = next_condition

class Parser:
    """Syntax Analyzer - builds Abstract Syntax Tree from tokens"""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
    
    def parse(self) -> ASTNode:
        """Parse tokens and return AST"""
        if not self.tokens:
            raise SyntaxError("No tokens to parse")
        
        token = self._current_token()
        
        if token.type == TokenType.CREATE:
            return self._parse_create()
        elif token.type == TokenType.INSERT:
            return self._parse_insert()
        elif token.type == TokenType.SELECT:
            return self._parse_select()
        elif token.type == TokenType.UPDATE:
            return self._parse_update()
        elif token.type == TokenType.DELETE:
            return self._parse_delete()
        elif token.type == TokenType.DROP:
            return self._parse_drop()
        else:
            raise SyntaxError(f"Unexpected token: {token.type}")
    
    def _current_token(self) -> Token:
        """Get current token without consuming"""
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return self.tokens[-1]
    
    def _advance(self) -> Token:
        """Consume and return current token"""
        token = self._current_token()
        self.position += 1
        return token
    
    def _expect(self, token_type: TokenType) -> Token:
        """Expect specific token type"""
        token = self._current_token()
        if token.type != token_type:
            raise SyntaxError(f"Expected {token_type}, got {token.type}")
        return self._advance()
    
    def _parse_create(self) -> CreateTableNode:
        """Parse CREATE TABLE statement"""
        self._expect(TokenType.CREATE)
        self._expect(TokenType.TABLE)
        
        table_name = self._expect(TokenType.IDENTIFIER).value
        self._expect(TokenType.LPAREN)
        
        columns = []
        while self._current_token().type != TokenType.RPAREN:
            col_name = self._expect(TokenType.IDENTIFIER).value
            col_type_token = self._advance()
            col_type = col_type_token.value
            
            # Handle VARCHAR(n)
            if col_type_token.type == TokenType.VARCHAR:
                if self._current_token().type == TokenType.LPAREN:
                    self._advance()
                    size = self._expect(TokenType.NUMBER).value
                    self._expect(TokenType.RPAREN)
                    col_type = f"VARCHAR({size})"
            
            columns.append((col_name, col_type))
            
            if self._current_token().type == TokenType.COMMA:
                self._advance()
        
        self._expect(TokenType.RPAREN)
        return CreateTableNode(table_name, columns)
    
    def _parse_insert(self) -> InsertNode:
        """Parse INSERT INTO statement"""
        self._expect(TokenType.INSERT)
        self._expect(TokenType.INTO)
        
        table_name = self._expect(TokenType.IDENTIFIER).value
        
        # Optional column list
        columns = None
        if self._current_token().type == TokenType.LPAREN:
            self._advance()
            columns = []
            while self._current_token().type != TokenType.RPAREN:
                columns.append(self._expect(TokenType.IDENTIFIER).value)
                if self._current_token().type == TokenType.COMMA:
                    self._advance()
            self._expect(TokenType.RPAREN)
        
        self._expect(TokenType.VALUES)
        self._expect(TokenType.LPAREN)
        
        values = []
        while self._current_token().type != TokenType.RPAREN:
            token = self._advance()
            if token.type in (TokenType.STRING, TokenType.NUMBER):
                values.append(token.value)
            else:
                raise SyntaxError(f"Expected value, got {token.type}")
            
            if self._current_token().type == TokenType.COMMA:
                self._advance()
        
        self._expect(TokenType.RPAREN)
        return InsertNode(table_name, columns, values)
    
    def _parse_select(self) -> SelectNode:
        """Parse SELECT statement"""
        self._expect(TokenType.SELECT)
        
        # Parse column list
        columns = []
        if self._current_token().type == TokenType.ASTERISK:
            self._advance()
            columns = ['*']
        else:
            while True:
                columns.append(self._expect(TokenType.IDENTIFIER).value)
                if self._current_token().type == TokenType.COMMA:
                    self._advance()
                else:
                    break
        
        self._expect(TokenType.FROM)
        table_name = self._expect(TokenType.IDENTIFIER).value
        
        where_clause = None
        if self._current_token().type == TokenType.WHERE:
            where_clause = self._parse_where()
        
        return SelectNode(columns, table_name, where_clause)
    
    def _parse_update(self) -> UpdateNode:
        """Parse UPDATE statement"""
        self._expect(TokenType.UPDATE)
        table_name = self._expect(TokenType.IDENTIFIER).value
        self._expect(TokenType.SET)
        
        assignments = {}
        while True:
            col_name = self._expect(TokenType.IDENTIFIER).value
            self._expect(TokenType.EQUALS)
            value_token = self._advance()
            
            if value_token.type in (TokenType.STRING, TokenType.NUMBER):
                assignments[col_name] = value_token.value
            else:
                raise SyntaxError(f"Expected value, got {value_token.type}")
            
            if self._current_token().type == TokenType.COMMA:
                self._advance()
            else:
                break
        
        where_clause = None
        if self._current_token().type == TokenType.WHERE:
            where_clause = self._parse_where()
        
        return UpdateNode(table_name, assignments, where_clause)
    
    def _parse_delete(self) -> DeleteNode:
        """Parse DELETE statement"""
        self._expect(TokenType.DELETE)
        self._expect(TokenType.FROM)
        table_name = self._expect(TokenType.IDENTIFIER).value
        
        where_clause = None
        if self._current_token().type == TokenType.WHERE:
            where_clause = self._parse_where()
        
        return DeleteNode(table_name, where_clause)
    
    def _parse_drop(self) -> DropTableNode:
        """Parse DROP TABLE statement"""
        self._expect(TokenType.DROP)
        self._expect(TokenType.TABLE)
        table_name = self._expect(TokenType.IDENTIFIER).value
        return DropTableNode(table_name)
    
    def _parse_where(self) -> WhereClause:
        """Parse WHERE clause"""
        self._expect(TokenType.WHERE)
        
        column = self._expect(TokenType.IDENTIFIER).value
        
        operator_token = self._advance()
        operator = operator_token.value
        
        value_token = self._advance()
        if value_token.type in (TokenType.STRING, TokenType.NUMBER):
            value = value_token.value
        else:
            raise SyntaxError(f"Expected value in WHERE clause, got {value_token.type}")
        
        where_clause = WhereClause(column, operator, value)
        
        # Handle AND/OR
        if self._current_token().type in (TokenType.AND, TokenType.OR):
            logical_op = self._advance().value
            where_clause.logical_op = logical_op
            where_clause.next_condition = self._parse_where_condition()
        
        return where_clause
    
    def _parse_where_condition(self) -> WhereClause:
        """Parse a single WHERE condition (for chaining)"""
        column = self._expect(TokenType.IDENTIFIER).value
        operator_token = self._advance()
        operator = operator_token.value
        
        value_token = self._advance()
        if value_token.type in (TokenType.STRING, TokenType.NUMBER):
            value = value_token.value
        else:
            raise SyntaxError(f"Expected value in WHERE clause, got {value_token.type}")
        
        where_clause = WhereClause(column, operator, value)
        
        if self._current_token().type in (TokenType.AND, TokenType.OR):
            logical_op = self._advance().value
            where_clause.logical_op = logical_op
            where_clause.next_condition = self._parse_where_condition()
        
        return where_clause

class Database:
    """Simple in-memory database"""
    
    def __init__(self):
        self.tables: Dict[str, Dict] = {}
    
    def create_table(self, table_name: str, columns: List[Tuple[str, str]]):
        """Create a new table"""
        if table_name in self.tables:
            raise ValueError(f"Table '{table_name}' already exists")
        
        self.tables[table_name] = {
            'columns': columns,
            'rows': []
        }
    
    def insert_row(self, table_name: str, columns: Optional[List[str]], values: List[Any]):
        """Insert a row into table"""
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist")
        
        table = self.tables[table_name]
        table_columns = [col[0] for col in table['columns']]
        
        if columns is None:
            columns = table_columns
        
        if len(columns) != len(values):
            raise ValueError("Number of columns and values don't match")
        
        # Create row with all columns (fill missing with None)
        row = {}
        for col in table_columns:
            if col in columns:
                idx = columns.index(col)
                row[col] = values[idx]
            else:
                row[col] = None
        
        table['rows'].append(row)
    
    def select_rows(self, table_name: str, columns: List[str], where_clause: Optional[WhereClause] = None) -> List[Dict]:
        """Select rows from table"""
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist")
        
        table = self.tables[table_name]
        
        # Filter rows based on WHERE clause
        if where_clause:
            filtered_rows = [row for row in table['rows'] if self._evaluate_where(row, where_clause)]
        else:
            filtered_rows = table['rows']
        
        # Select specific columns
        if columns == ['*']:
            return filtered_rows
        else:
            return [{col: row.get(col) for col in columns} for row in filtered_rows]
    
    def update_rows(self, table_name: str, assignments: Dict[str, Any], where_clause: Optional[WhereClause] = None) -> int:
        """Update rows in table"""
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist")
        
        table = self.tables[table_name]
        count = 0
        
        for row in table['rows']:
            if where_clause is None or self._evaluate_where(row, where_clause):
                for col, value in assignments.items():
                    row[col] = value
                count += 1
        
        return count
    
    def delete_rows(self, table_name: str, where_clause: Optional[WhereClause] = None) -> int:
        """Delete rows from table"""
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist")
        
        table = self.tables[table_name]
        
        if where_clause is None:
            count = len(table['rows'])
            table['rows'] = []
            return count
        
        initial_count = len(table['rows'])
        table['rows'] = [row for row in table['rows'] if not self._evaluate_where(row, where_clause)]
        return initial_count - len(table['rows'])
    
    def drop_table(self, table_name: str):
        """Drop a table"""
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist")
        
        del self.tables[table_name]
    
    def _evaluate_where(self, row: Dict, where_clause: WhereClause) -> bool:
        """Evaluate WHERE clause for a row"""
        column_value = row.get(where_clause.column)
        condition_value = where_clause.value
        
        # Evaluate current condition
        result = False
        if where_clause.operator == '=':
            result = column_value == condition_value
        elif where_clause.operator == '!=':
            result = column_value != condition_value
        elif where_clause.operator == '<':
            result = column_value < condition_value
        elif where_clause.operator == '>':
            result = column_value > condition_value
        elif where_clause.operator == '<=':
            result = column_value <= condition_value
        elif where_clause.operator == '>=':
            result = column_value >= condition_value
        
        # Handle logical operators
        if where_clause.next_condition:
            next_result = self._evaluate_where(row, where_clause.next_condition)
            if where_clause.logical_op == 'AND':
                result = result and next_result
            elif where_clause.logical_op == 'OR':
                result = result or next_result
        
        return result
    
    def get_table_info(self, table_name: str) -> Dict:
        """Get table structure"""
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' does not exist")
        return {
            'columns': self.tables[table_name]['columns'],
            'row_count': len(self.tables[table_name]['rows'])
        }
    
    def list_tables(self) -> List[str]:
        """List all tables"""
        return list(self.tables.keys())

class QueryExecutor:
    """Execute parsed queries on the database"""
    
    def __init__(self, database: Database):
        self.database = database
    
    def execute(self, ast: ASTNode) -> Dict[str, Any]:
        """Execute AST node and return result"""
        if isinstance(ast, CreateTableNode):
            return self._execute_create(ast)
        elif isinstance(ast, InsertNode):
            return self._execute_insert(ast)
        elif isinstance(ast, SelectNode):
            return self._execute_select(ast)
        elif isinstance(ast, UpdateNode):
            return self._execute_update(ast)
        elif isinstance(ast, DeleteNode):
            return self._execute_delete(ast)
        elif isinstance(ast, DropTableNode):
            return self._execute_drop(ast)
        else:
            raise ValueError(f"Unknown AST node type: {type(ast)}")
    
    def _execute_create(self, node: CreateTableNode) -> Dict[str, Any]:
        """Execute CREATE TABLE"""
        self.database.create_table(node.table_name, node.columns)
        return {
            'success': True,
            'message': f"Table '{node.table_name}' created successfully",
            'type': 'CREATE'
        }
    
    def _execute_insert(self, node: InsertNode) -> Dict[str, Any]:
        """Execute INSERT"""
        self.database.insert_row(node.table_name, node.columns, node.values)
        return {
            'success': True,
            'message': f"1 row inserted into '{node.table_name}'",
            'type': 'INSERT'
        }
    
    def _execute_select(self, node: SelectNode) -> Dict[str, Any]:
        """Execute SELECT"""
        rows = self.database.select_rows(node.table_name, node.columns, node.where_clause)
        return {
            'success': True,
            'type': 'SELECT',
            'data': rows,
            'row_count': len(rows)
        }
    
    def _execute_update(self, node: UpdateNode) -> Dict[str, Any]:
        """Execute UPDATE"""
        count = self.database.update_rows(node.table_name, node.assignments, node.where_clause)
        return {
            'success': True,
            'message': f"{count} row(s) updated in '{node.table_name}'",
            'type': 'UPDATE'
        }
    
    def _execute_delete(self, node: DeleteNode) -> Dict[str, Any]:
        """Execute DELETE"""
        count = self.database.delete_rows(node.table_name, node.where_clause)
        return {
            'success': True,
            'message': f"{count} row(s) deleted from '{node.table_name}'",
            'type': 'DELETE'
        }
    
    def _execute_drop(self, node: DropTableNode) -> Dict[str, Any]:
        """Execute DROP TABLE"""
        self.database.drop_table(node.table_name)
        return {
            'success': True,
            'message': f"Table '{node.table_name}' dropped successfully",
            'type': 'DROP'
        }

class SQLCompiler:
    """Main SQL Compiler class"""
    
    def __init__(self):
        self.database = Database()
        self.executor = QueryExecutor(self.database)
    
    def compile_and_execute(self, query: str) -> Dict[str, Any]:
        """Complete compilation pipeline"""
        try:
            # Remove trailing semicolon if present
            query = query.strip()
            if query.endswith(';'):
                query = query[:-1]
            
            # Lexical Analysis
            lexer = Lexer(query)
            tokens = lexer.tokenize()
            
            # Syntax Analysis
            parser = Parser(tokens)
            ast = parser.parse()
            
            # Execution
            result = self.executor.execute(ast)
            
            return result
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'type': 'ERROR'
            }
    
    def get_database(self) -> Database:
        """Get database instance"""
        return self.database
