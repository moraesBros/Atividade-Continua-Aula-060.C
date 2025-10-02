from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # valores iniciais (vazios ou None)
    name = ''
    institution = ''
    discipline = ''
    errors = {}

    # variáveis novas para IP e host
    remote_ip = None
    host_name = None

    if request.method == 'POST':
        # 1) captura dos dados de formulário
        name        = request.form.get('name', '').strip()
        institution = request.form.get('institution', '').strip()
        discipline  = request.form.get('discipline', '').strip()

        # 2) validação de campos
        if not name:
            errors['name'] = 'Preencha esse campo'
        if not institution:
            errors['institution'] = 'Preencha esse campo'
        if not discipline:
            errors['discipline'] = 'Preencha esse campo'

        # 3) atribuir IP e host somente após o POST
        remote_ip = request.remote_addr
        # request.host traz host:porta; se quiser só o host sem porta:
        host_name = request.host.split(':')[0]

    return render_template(
        'index.html',
        name=name,
        institution=institution,
        discipline=discipline,
        errors=errors,
        remote_ip=remote_ip,
        host_name=host_name
    )

if __name__ == '__main__':
    app.run()
