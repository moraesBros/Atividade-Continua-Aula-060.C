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

def categorize_entries(entries):
    usuarios = []
    moderadores = []
    administradores = []
    for e in entries:
        role = (e.get("role") or "").strip()
        name = e.get("name", "").strip()
        if role.lower() == "administrador":
            administradores.append(name)
        elif role.lower() == "moderador":
            moderadores.append(name)
        else:
            # inclui role == "" e role == "Usuário" e qualquer outro valor que não seja moderador/administrador
            usuarios.append(name)
    return {
        "Usuário": usuarios,
        "Moderador": moderadores,
        "Administrador": administradores
    }

def generate_lista_template(entries):
    count = len(entries)
    groups = categorize_entries(entries)
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
    .group { margin-top: 18px; }
    .group p.title { font-weight: 700; margin: 6px 0; }
    .group ul { margin: 6px 0 0 18px; padding: 0; }
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
""")
        # adicionar seções agrupadas abaixo
        for group_name in ["Usuário", "Moderador", "Administrador"]:
            names = groups.get(group_name, [])
            f.write(f'  <div class="group"><p class="title">{group_name}</p>\n')
            if names:
                f.write("    <ul>\n")
                for n in names:
                    safe = n.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    f.write(f"      <li>{safe}</li>\n")
                f.write("    </ul>\n")
            else:
                f.write("    <p>Nenhum registro</p>\n")
            f.write("  </div>\n")
        f.write("</body>\n</html>")

@app.route("/", methods=["GET", "POST"])
def index():
    errors = {}
    name = ""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        role = request.form.get("role", "").strip()
        # validação: name obrigatório; role pode ser vazio (será tratado como Usuário)
        if not name:
            errors["name"] = "Nome é obrigatório."
        # não tornar role obrigatório para permitir gravação sem função
        if not errors:
            append_entry(name, role)
            flash("Dados enviados com sucesso!")
            return redirect(url_for("index"))
    entries = read_entries()
    groups = categorize_entries(entries)
    # gerar lista.html atualizada
    generate_lista_template(entries)
    return render_template(
        "index.html",
        name=name,
        errors=errors,
        entries=entries,
        count=len(entries),
        groups=groups
    )

@app.route("/lista")
def lista():
    entries = read_entries()
    generate_lista_template(entries)
    return render_template("lista.html")

if __name__ == "__main__":
    app.run(debug=True)
