from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Banco de Dados
DB_FILE = "tasks.db"

def init_db():
    """Cria a tabela do banco de dados, se não existir."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Inicializa o banco de dados
init_db()

@app.route("/")
def index():
    """Exibe todas as tarefas."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    """Adiciona uma nova tarefa."""
    title = request.form.get("title")
    description = request.form.get("description")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)", (title, description, "Pending"))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/update/<int:task_id>", methods=["POST"])
def update_task(task_id):
    """Atualiza o status de uma tarefa."""
    status = request.form.get("status")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    """Remove uma tarefa."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
