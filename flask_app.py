from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # valores iniciais (vazios ou None)
    name = ''
    errors = {}


    if request.method == 'POST':
        # 1) captura dos dados de formulário
        name        = request.form.get('name', '').strip()

        # 2) validação de campos
        if not name:
            errors['name'] = 'Preencha esse campo'


    return render_template(
        'index.html',
        name=name,
        errors=errors,
    )

if __name__ == '__main__':
    app.run()
