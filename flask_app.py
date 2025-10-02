<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Flasky Moraes</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
  <style>
    /* Estilos adicionais para garantir o alinhamento */
    .container {
      padding-left: 20px; /* Ajuste este valor conforme necessário para alinhar com a navbar */
    }

    /* Se precisar de mais controle, você pode usar isso: */
    .content-wrapper {
      margin-left: 0; /* Ajuste para igualar a margem da navbar */
      max-width: 100%;
    }
  </style>
</head>
<body>
  <nav class="navbar">
      <a href="{{ url_for('index') }}" class="brand">
    Avaliação contínua: <b>Aula 060.C</b>
  </a>
    <a href="#" class="nav-link">Home</a>
  </nav>

  <div class="container">
    <div class="content-wrapper">
      <!-- Mensagens acima do separador -->
      <h1 class="greeting">
        {% if name %}
          Ola, {{ name }}!
        {% else %}
          Ola, Estranho!
        {% endif %}
      </h1>



      <!-- separador -->
      <div class="separator"></div>

      <!-- Formulário único -->
      <form method="post" novalidate>
        <p class="prompt">Qual o seu nome?</p>
        <input
          type="text"
          name="name"
          placeholder="Digite seu nome"
          class="input-name"
          value="{{ name }}"
        >
        {% if errors.name %}
          <div class="error">{{ errors.name }}</div>
        {% endif %}


        <button type="submit" class="btn-submit">Enviar tudo</button>
      </form>

  </script>
</body>
</html>
