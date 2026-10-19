from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font("msyh", "B", 14)
        self.set_text_color(26, 82, 118)
        self.cell(0, 10, "SQL Database Vocabulary", ln=True, align="C")
        self.set_font("msyh", "", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, "Database Exam Prep  2026-09-23", ln=True, align="C")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("msyh", "", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def section_title(self, title):
        self.set_font("msyh", "B", 12)
        self.set_text_color(30, 132, 73)
        self.cell(0, 10, title, ln=True)
        self.ln(2)

    def table_header(self, cols, widths):
        self.set_font("msyh", "B", 10)
        self.set_fill_color(26, 82, 118)
        self.set_text_color(255, 255, 255)
        for col, w in zip(cols, widths):
            self.cell(w, 8, col, border=1, fill=True, align="C")
        self.ln()

    def table_row(self, cells, widths, fill=False):
        self.set_font("msyh", "", 9)
        self.set_text_color(44, 62, 80)
        if fill:
            self.set_fill_color(235, 245, 251)
        else:
            self.set_fill_color(255, 255, 255)
        max_h = 7
        for i, (cell, w) in enumerate(zip(cells, widths)):
            self.cell(w, max_h, str(cell), border=1, fill=True)
        self.ln()

    def add_table(self, cols, rows, widths):
        self.table_header(cols, widths)
        for i, row in enumerate(rows):
            if self.get_y() > 270:
                self.add_page()
                self.table_header(cols, widths)
            self.table_row(row, widths, fill=(i % 2 == 1))
        self.ln(4)

pdf = PDF()
pdf.add_font("msyh", "", r"C:\Windows\Fonts\msyh.ttc", uni=True)
pdf.add_font("msyh", "B", r"C:\Windows\Fonts\msyhbd.ttc", uni=True)
pdf.add_page()

# Section 1
pdf.section_title("1. Table Creation")
rows1 = [
    ["create", "create", "Create (create table)"],
    ["table", "ta-bu", "Table"],
    ["column", "ko-lam", "Column"],
    ["primary key", "pry-ma-ri ki", "Primary key"],
    ["foreign key", "fo-ran ki", "Foreign key"],
    ["not null", "not nal", "Not null"],
    ["unique", "yu-nik", "Unique"],
    ["default", "di-olt", "Default value"],
    ["check", "chek", "Check constraint"],
    ["identity", "ay-den-ti", "Auto increment"],
    ["drop", "drop", "Drop (table/database)"],
    ["alter", "ol-ter", "Alter (table structure)"],
    ["add", "ad", "Add (column)"],
    ["constraint", "ken-straint", "Constraint"],
]
pdf.add_table(["English", "Pronunciation", "Chinese"], rows1, [45, 50, 95])

# Section 2
pdf.section_title("2. CRUD Operations")
rows2 = [
    ["select", "si-lekt", "Query"],
    ["from", "from", "From (which table)"],
    ["where", "wer", "Where (filter rows)"],
    ["insert", "in-sert", "Insert"],
    ["into", "in-tu", "Into (which table)"],
    ["values", "val-yuz", "Values"],
    ["update", "yu-peyt", "Update"],
    ["set", "set", "Set"],
    ["delete", "di-lit", "Delete (data)"],
]
pdf.add_table(["English", "Pronunciation", "Chinese"], rows2, [45, 50, 95])

# Section 3
pdf.section_title("3. Advanced Query")
rows3 = [
    ["order by", "or-der bai", "Order by (sort)"],
    ["asc", "ask", "Ascending (small to large)"],
    ["desc", "des-k", "Descending (large to small)"],
    ["group by", "grup bai", "Group by"],
    ["having", "ha-ving", "Having (filter groups)"],
    ["top", "top", "Top N rows"],
    ["distinct", "dis-tinkt", "Distinct (deduplicate)"],
    ["like", "lai-k", "Like (fuzzy match)"],
    ["between", "bi-tu-wen", "Between"],
    ["in", "in", "In (within list)"],
    ["and", "and", "And"],
    ["or", "or", "Or"],
    ["not", "not", "Not"],
    ["join", "joyn", "Join (multi-table)"],
    ["as", "as", "As (alias)"],
]
pdf.add_table(["English", "Pronunciation", "Chinese"], rows3, [45, 50, 95])

# Section 4
pdf.section_title("4. Functions")
rows4 = [
    ["count", "kaunt", "Count"],
    ["sum", "sam", "Sum"],
    ["avg", "ay-ji-vi", "Average"],
    ["max", "maks", "Max"],
    ["min", "min", "Min"],
    ["len", "len", "Length"],
    ["year/month/day", "ir / munt / dey", "Year / Month / Day"],
    ["getdate", "get-deyt", "Get current time"],
]
pdf.add_table(["English", "Pronunciation", "Chinese"], rows4, [45, 50, 95])

# Section 5
pdf.section_title("5. Transaction & Security")
rows5 = [
    ["transaction", "tran-zak-shon", "Transaction"],
    ["begin", "bi-gin", "Begin"],
    ["commit", "ko-mit", "Commit (save)"],
    ["rollback", "rol-bak", "Rollback (undo)"],
    ["grant", "grant", "Grant (permission)"],
    ["revoke", "ri-vok", "Revoke permission"],
    ["deny", "di-nai", "Deny"],
]
pdf.add_table(["English", "Pronunciation", "Chinese"], rows5, [45, 50, 95])

# Section 6 - Top 15
pdf.section_title("6. Top 15 Must-Know Words")
rows6 = [
    ["1", "select", "Query"],
    ["2", "from", "From"],
    ["3", "where", "Condition"],
    ["4", "insert", "Insert"],
    ["5", "into", "Into"],
    ["6", "values", "Values"],
    ["7", "update", "Update"],
    ["8", "set", "Set"],
    ["9", "delete", "Delete"],
    ["10", "create", "Create"],
    ["11", "drop", "Drop"],
    ["12", "alter", "Alter"],
    ["13", "table", "Table"],
    ["14", "primary key", "Primary key"],
    ["15", "and", "And"],
]
pdf.add_table(["#", "English", "Chinese"], rows6, [15, 70, 105])

pdf.output(r"D:\Desktop\计算机科学与技术\数据库单词速查表.pdf")
print("PDF generated!")
