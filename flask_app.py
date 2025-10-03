from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = "troque-essa-chave-para-uma-segura"

DATA_DIR = os.path.join(app.root_path, "data")
NAMES_FILE = os.path.join(DATA_DIR, "names.txt")
GENERATED_TEMPLATE = os.path.join(app.root_path, "templates", "lista.html")

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(NAMES_FILE):
        open(NAMES_FILE, "a", encoding="utf-8").close()

def read_entries():
    ensure_data_dir()
    entries = []
    with open(NAMES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # formato armazenado: nome|role
            parts = line.split("|", 1)
            if len(parts) == 2:
                name, role = parts[0].strip(), parts[1].strip()
            else:
                name, role = parts[0].strip(), ""
            entries.append({"name": name, "role": role})
    return entries

def append_entry(name, role):
    ensure_data_dir()
    safe_name = name.strip()
    safe_role = role.strip()
    with open(NAMES_FILE, "a", encoding="utf-8") as f:
        f.write(f"{safe_name}|{safe_role}\n")

def generate_lista_template(entries):
    count = len(entries)
    os.makedirs(os.path.dirname(GENERATED_TEMPLATE), exist_ok=True)
    with open(GENERATED_TEMPLATE, "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Lista de Nomes</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <style>
    body { font-family: Arial, sans-serif; margin: 24px; color:#111; background:#fff; }
    h1 { font-size: 20px; margin-bottom: 12px; }
    table { border-collapse: collapse; width: 100%; max-width: 720px; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    th { background: #f5f5f5; }
    .count { margin-top: 12px; font-weight: 600; }
  </style>
</head>
<body>
  <h1>Lista de nomes recebidos</h1>
  <table>
    <thead>
      <tr><th>Nome</th><th>Função</th></tr>
    </thead>
    <tbody>
""")
        for e in entries:
            name = e["name"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            role = e["role"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            f.write(f"      <tr><td>{name}</td><td>{role}</td></tr>\n")
        f.write(f"""    </tbody>
  </table>
  <p class="count">Quantidade: {count}</p>
</body>
</html>""")

@app.route("/", methods=["GET", "POST"])
def index():
    errors = {}
    form_name = ""
    form_role = ""
    if request.method == "POST":
        form_name = request.form.get("name", "").strip()
        form_role = request.form.get("role", "").strip()

        if form_name:
            if len(form_name) < 2:
                errors["name"] = "Nome muito curto."
            else:
                append_entry(form_name, form_role)
                entries = read_entries()
                generate_lista_template(entries)
                flash("Nome gravado com sucesso.", "success")
                form_name = ""
                # manter role selecionado vazio após envio
                form_role = ""
        else:
            # manter comportamento anterior: não exigir nome
            pass

    entries = read_entries()
    count = len(entries)

    return render_template("index.html",
                           name="",
                           role="",
                           errors=errors,
                           count=count,
                           entries=entries)

if __name__ == "__main__":
    app.run(debug=True)
