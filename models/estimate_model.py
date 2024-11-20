import sqlite3


class EstimateModel:
    def __init__(self):
        self.connection = sqlite3.connect("database.db")

    def save_estimate(self, name, estimate_type, budget):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO Estimates (name, type, budget)
            VALUES (?, ?, ?)
        ''', (name, estimate_type, budget))
        self.connection.commit()
        return cursor.lastrowid  # Возвращаем ID созданной сметы

    def save_materials(self, estimate_id, materials):
        cursor = self.connection.cursor()
        cursor.executemany('''
            INSERT INTO Estimate_Resources (estimate_id, material_id, quantity)
            VALUES (?, ?, ?)
        ''', [(estimate_id, mat['id'], mat['quantity']) for mat in materials])
        self.connection.commit()
