import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, create_table_sql):
        try:
            self.cursor.execute(create_table_sql)
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def insert_data(self, insert_sql, data):
        try:
            self.cursor.executemany(insert_sql, data)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error inserting data: {e}")

    def close(self):
        self.conn.close()

class CustomerDB(Database):
    def __init__(self, db_name='customer_info.db'):
        super().__init__(db_name)
        self.create_tables()

    def create_tables(self):
        customers_table_sql = '''
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT
            )
        '''
        self.create_table(customers_table_sql)

        orders_table_sql = '''
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                order_date TEXT NOT NULL,
                total_amount REAL NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            )
        '''
        self.create_table(orders_table_sql)

        products_table_sql = '''
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER NOT NULL
            )
        '''
        self.create_table(products_table_sql)

    def populate_tables(self):
        customers_data = [
            ('John', 'Doe', 'john.doe@example.com', '123-456-7890'),
            ('Jane', 'Smith', 'jane.smith@example.com', '098-765-4321')
        ]
        self.insert_data('INSERT INTO customers (first_name, last_name, email, phone) VALUES (?, ?, ?, ?)', customers_data)

        products_data = [
            ('Laptop', 999.99, 10),
            ('Smartphone', 499.99, 20),
            ('Tablet', 299.99, 15)
        ]
        self.insert_data('INSERT INTO products (product_name, price, stock) VALUES (?, ?, ?)', products_data)

        orders_data = [
            (1, '2023-10-01', 1499.98),
            (2, '2023-10-02', 299.99)
        ]
        self.insert_data('INSERT INTO orders (customer_id, order_date, total_amount) VALUES (?, ?, ?)', orders_data)

if __name__ == '__main__':
    customer_db = CustomerDB()
    customer_db.populate_tables()
    customer_db.close()
    print("Database and tables created successfully with sample data.")

# TEstTest