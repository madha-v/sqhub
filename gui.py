"""
Mini SQL Compiler GUI
A graphical user interface for the SQL compiler
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
from sql_compiler import SQLCompiler
import datetime

class SQLCompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini SQL Compiler - Compiler Design Project")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e1e')
        
        # Initialize compiler
        self.compiler = SQLCompiler()
        self.query_history = []
        
        # Configure styles
        self.setup_styles()
        
        # Create GUI components
        self.create_header()
        self.create_main_content()
        self.create_footer()
        
        # Load sample queries
        self.load_sample_queries()
    
    def setup_styles(self):
        """Setup custom styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        bg_dark = '#1e1e1e'
        bg_medium = '#2d2d2d'
        bg_light = '#3e3e3e'
        fg_light = '#ffffff'
        fg_accent = '#00d4ff'
        
        # Button style
        style.configure('Custom.TButton',
                       background=bg_light,
                       foreground=fg_light,
                       borderwidth=1,
                       focuscolor='none',
                       padding=10,
                       font=('Arial', 10, 'bold'))
        style.map('Custom.TButton',
                 background=[('active', fg_accent)])
        
        # Frame style
        style.configure('Custom.TFrame', background=bg_dark)
        style.configure('Card.TFrame', background=bg_medium, relief='raised', borderwidth=2)
        
        # Label style
        style.configure('Header.TLabel',
                       background=bg_dark,
                       foreground=fg_accent,
                       font=('Arial', 24, 'bold'))
        style.configure('Subheader.TLabel',
                       background=bg_medium,
                       foreground=fg_light,
                       font=('Arial', 11, 'bold'))
        style.configure('Normal.TLabel',
                       background=bg_medium,
                       foreground=fg_light,
                       font=('Arial', 10))
    
    def create_header(self):
        """Create header section"""
        header_frame = ttk.Frame(self.root, style='Custom.TFrame')
        header_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        title_label = ttk.Label(header_frame,
                               text="⚡ Mini SQL Compiler",
                               style='Header.TLabel')
        title_label.pack(side='left')
        
        subtitle_label = ttk.Label(header_frame,
                                  text="Compiler Design Project - 6th Semester",
                                  style='Normal.TLabel')
        subtitle_label.pack(side='left', padx=20)
        
        # Database info
        info_frame = ttk.Frame(header_frame, style='Custom.TFrame')
        info_frame.pack(side='right')
        
        self.db_info_label = ttk.Label(info_frame,
                                       text="Tables: 0 | Ready",
                                       style='Normal.TLabel')
        self.db_info_label.pack()
    
    def create_main_content(self):
        """Create main content area"""
        main_frame = ttk.Frame(self.root, style='Custom.TFrame')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel - Query editor and examples
        left_panel = ttk.Frame(main_frame, style='Custom.TFrame')
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Query editor
        editor_frame = ttk.Frame(left_panel, style='Card.TFrame')
        editor_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        editor_label = ttk.Label(editor_frame,
                                text="📝 SQL Query Editor",
                                style='Subheader.TLabel')
        editor_label.pack(anchor='w', padx=10, pady=(10, 5))
        
        # Text editor with line numbers
        editor_container = ttk.Frame(editor_frame, style='Card.TFrame')
        editor_container.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        self.query_text = scrolledtext.ScrolledText(
            editor_container,
            wrap=tk.WORD,
            width=60,
            height=12,
            font=('Consolas', 11),
            bg='#0d1117',
            fg='#c9d1d9',
            insertbackground='#00d4ff',
            selectbackground='#264f78',
            relief='flat',
            padx=10,
            pady=10
        )
        self.query_text.pack(fill='both', expand=True)
        
        # Button frame
        button_frame = ttk.Frame(editor_frame, style='Card.TFrame')
        button_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        execute_btn = ttk.Button(button_frame,
                                text="▶ Execute Query",
                                command=self.execute_query,
                                style='Custom.TButton')
        execute_btn.pack(side='left', padx=5)
        
        clear_btn = ttk.Button(button_frame,
                              text="🗑 Clear",
                              command=self.clear_query,
                              style='Custom.TButton')
        clear_btn.pack(side='left', padx=5)
        
        tables_btn = ttk.Button(button_frame,
                               text="📊 Show Tables",
                               command=self.show_tables,
                               style='Custom.TButton')
        tables_btn.pack(side='left', padx=5)
        
        # Sample queries
        samples_frame = ttk.Frame(left_panel, style='Card.TFrame')
        samples_frame.pack(fill='both', expand=True)
        
        samples_label = ttk.Label(samples_frame,
                                 text="📚 Sample Queries",
                                 style='Subheader.TLabel')
        samples_label.pack(anchor='w', padx=10, pady=(10, 5))
        
        self.samples_listbox = tk.Listbox(
            samples_frame,
            font=('Arial', 10),
            bg='#0d1117',
            fg='#c9d1d9',
            selectbackground='#00d4ff',
            selectforeground='#000000',
            relief='flat',
            height=8
        )
        self.samples_listbox.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        self.samples_listbox.bind('<<ListboxSelect>>', self.load_sample)
        
        # Right panel - Output and results
        right_panel = ttk.Frame(main_frame, style='Custom.TFrame')
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Output console
        output_frame = ttk.Frame(right_panel, style='Card.TFrame')
        output_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        output_label = ttk.Label(output_frame,
                                text="📤 Output Console",
                                style='Subheader.TLabel')
        output_label.pack(anchor='w', padx=10, pady=(10, 5))
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            width=60,
            height=12,
            font=('Consolas', 10),
            bg='#0d1117',
            fg='#00ff00',
            relief='flat',
            padx=10,
            pady=10,
            state='disabled'
        )
        self.output_text.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Results table
        results_frame = ttk.Frame(right_panel, style='Card.TFrame')
        results_frame.pack(fill='both', expand=True)
        
        results_label = ttk.Label(results_frame,
                                 text="📋 Query Results",
                                 style='Subheader.TLabel')
        results_label.pack(anchor='w', padx=10, pady=(10, 5))
        
        # Create Treeview for results
        table_container = ttk.Frame(results_frame, style='Card.TFrame')
        table_container.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_container, orient='vertical')
        h_scrollbar = ttk.Scrollbar(table_container, orient='horizontal')
        
        self.results_table = ttk.Treeview(
            table_container,
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set,
            selectmode='browse',
            height=8
        )
        
        v_scrollbar.config(command=self.results_table.yview)
        h_scrollbar.config(command=self.results_table.xview)
        
        # Pack scrollbars and treeview
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        self.results_table.pack(fill='both', expand=True)
        
        # Style the treeview
        style = ttk.Style()
        style.configure("Treeview",
                       background="#0d1117",
                       foreground="#c9d1d9",
                       fieldbackground="#0d1117",
                       borderwidth=0,
                       font=('Arial', 10))
        style.configure("Treeview.Heading",
                       background="#1f6feb",
                       foreground="white",
                       font=('Arial', 10, 'bold'))
        style.map('Treeview',
                 background=[('selected', '#264f78')])
    
    def create_footer(self):
        """Create footer section"""
        footer_frame = ttk.Frame(self.root, style='Custom.TFrame')
        footer_frame.pack(fill='x', padx=20, pady=(10, 20))
        
        info_text = "Supports: CREATE TABLE, INSERT, SELECT, UPDATE, DELETE, DROP TABLE | WHERE clauses with AND/OR"
        info_label = ttk.Label(footer_frame,
                              text=info_text,
                              style='Normal.TLabel')
        info_label.pack(side='left')
        
        self.status_label = ttk.Label(footer_frame,
                                     text="Status: Ready",
                                     style='Normal.TLabel')
        self.status_label.pack(side='right')
    
    def load_sample_queries(self):
        """Load sample queries into listbox"""
        samples = [
            "CREATE TABLE students (id INT, name VARCHAR(50), age INT, grade VARCHAR(2))",
            "INSERT INTO students VALUES (1, 'Alice', 20, 'A')",
            "INSERT INTO students VALUES (2, 'Bob', 21, 'B')",
            "INSERT INTO students VALUES (3, 'Charlie', 19, 'A')",
            "SELECT * FROM students",
            "SELECT name, grade FROM students WHERE age > 19",
            "UPDATE students SET grade = 'A+' WHERE name = 'Alice'",
            "DELETE FROM students WHERE age < 20",
            "DROP TABLE students",
            "CREATE TABLE employees (emp_id INT, name VARCHAR(50), salary INT, dept VARCHAR(30))",
            "INSERT INTO employees VALUES (101, 'John Doe', 50000, 'IT')",
            "SELECT name, salary FROM employees WHERE salary > 40000",
            "UPDATE employees SET salary = 55000 WHERE emp_id = 101",
        ]
        
        for sample in samples:
            self.samples_listbox.insert(tk.END, sample)
    
    def load_sample(self, event):
        """Load selected sample query"""
        selection = self.samples_listbox.curselection()
        if selection:
            query = self.samples_listbox.get(selection[0])
            self.query_text.delete('1.0', tk.END)
            self.query_text.insert('1.0', query)
    
    def execute_query(self):
        """Execute the SQL query"""
        query = self.query_text.get('1.0', tk.END).strip()
        
        if not query:
            messagebox.showwarning("Empty Query", "Please enter a SQL query.")
            return
        
        self.update_status("Executing...")
        
        # Compile and execute
        result = self.compiler.compile_and_execute(query)
        
        # Display result
        self.display_result(result, query)
        
        # Update database info
        self.update_db_info()
        
        # Add to history
        self.query_history.append({
            'query': query,
            'result': result,
            'timestamp': datetime.datetime.now()
        })
        
        self.update_status("Ready")
    
    def display_result(self, result, query):
        """Display query result"""
        # Clear previous output
        self.output_text.config(state='normal')
        self.output_text.delete('1.0', tk.END)
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.output_text.insert(tk.END, f"[{timestamp}] Executed Query:\n", 'timestamp')
        self.output_text.insert(tk.END, f"{query}\n\n", 'query')
        
        if result['success']:
            self.output_text.insert(tk.END, "✓ SUCCESS\n", 'success')
            
            if result['type'] == 'SELECT':
                self.output_text.insert(tk.END, f"Retrieved {result['row_count']} row(s)\n", 'info')
                self.display_table(result['data'])
            else:
                self.output_text.insert(tk.END, f"{result['message']}\n", 'info')
                # Clear table for non-SELECT queries
                self.results_table.delete(*self.results_table.get_children())
                self.results_table['columns'] = ()
        else:
            self.output_text.insert(tk.END, "✗ ERROR\n", 'error')
            self.output_text.insert(tk.END, f"{result['error']}\n", 'error_detail')
            # Clear table on error
            self.results_table.delete(*self.results_table.get_children())
            self.results_table['columns'] = ()
        
        self.output_text.insert(tk.END, "\n" + "="*60 + "\n\n")
        
        # Configure tags
        self.output_text.tag_config('timestamp', foreground='#8b949e')
        self.output_text.tag_config('query', foreground='#00d4ff')
        self.output_text.tag_config('success', foreground='#00ff00', font=('Consolas', 10, 'bold'))
        self.output_text.tag_config('error', foreground='#ff0000', font=('Consolas', 10, 'bold'))
        self.output_text.tag_config('error_detail', foreground='#ff6b6b')
        self.output_text.tag_config('info', foreground='#ffffff')
        
        self.output_text.config(state='disabled')
        self.output_text.see(tk.END)
    
    def display_table(self, data):
        """Display SELECT query results in table"""
        # Clear previous data
        self.results_table.delete(*self.results_table.get_children())
        
        if not data:
            self.results_table['columns'] = ()
            return
        
        # Get columns
        columns = list(data[0].keys())
        self.results_table['columns'] = columns
        
        # Configure columns
        self.results_table.column('#0', width=0, stretch=False)
        for col in columns:
            self.results_table.column(col, anchor='center', width=150)
            self.results_table.heading(col, text=col, anchor='center')
        
        # Insert data
        for row in data:
            values = [row[col] for col in columns]
            self.results_table.insert('', tk.END, values=values)
    
    def clear_query(self):
        """Clear query editor"""
        self.query_text.delete('1.0', tk.END)
    
    def show_tables(self):
        """Show all tables in database"""
        tables = self.compiler.get_database().list_tables()
        
        if not tables:
            messagebox.showinfo("Database Tables", "No tables exist in the database.")
            return
        
        # Create a window to show tables
        table_window = tk.Toplevel(self.root)
        table_window.title("Database Tables")
        table_window.geometry("600x400")
        table_window.configure(bg='#1e1e1e')
        
        # Header
        header = ttk.Label(table_window,
                          text="📊 Database Tables",
                          style='Subheader.TLabel')
        header.pack(pady=10)
        
        # Table list
        for table_name in tables:
            table_info = self.compiler.get_database().get_table_info(table_name)
            
            frame = ttk.Frame(table_window, style='Card.TFrame')
            frame.pack(fill='x', padx=20, pady=5)
            
            name_label = ttk.Label(frame,
                                  text=f"Table: {table_name}",
                                  style='Subheader.TLabel')
            name_label.pack(anchor='w', padx=10, pady=5)
            
            info_label = ttk.Label(frame,
                                  text=f"Columns: {len(table_info['columns'])} | Rows: {table_info['row_count']}",
                                  style='Normal.TLabel')
            info_label.pack(anchor='w', padx=10, pady=5)
            
            cols_text = ", ".join([f"{col[0]} ({col[1]})" for col in table_info['columns']])
            cols_label = ttk.Label(frame,
                                  text=f"Structure: {cols_text}",
                                  style='Normal.TLabel')
            cols_label.pack(anchor='w', padx=10, pady=(0, 5))
    
    def update_db_info(self):
        """Update database info in header"""
        tables = self.compiler.get_database().list_tables()
        self.db_info_label.config(text=f"Tables: {len(tables)} | Ready")
    
    def update_status(self, status):
        """Update status label"""
        self.status_label.config(text=f"Status: {status}")
        self.root.update()

def main():
    root = tk.Tk()
    app = SQLCompilerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
