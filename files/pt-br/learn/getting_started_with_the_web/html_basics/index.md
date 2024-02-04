<!DOCTYPE html>
<html>
<head>
  <title>Botão Dia/Noite</title>
  <style>
    body {
      margin: 0;
      padding: 0;
      overflow: hidden;
      font-family: Arial, sans-serif;
      background-color: #3498db; /* Cor padrão de fundo (dia) */
      background-image: url('https://images.unsplash.com/photo-1551620947-ff6d0d64e8f9'); /* Imagem de fundo do dia */
      background-size: cover;
      background-position: center;
      transition: background-color 0.5s, background-image 0.5s;
    }

    #botao {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background-color: #3498db; /* Cor do botão (dia) */
      color: white;
      padding: 15px 25px;
      font-size: 16px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      text-align: center;
      transition: background-color 0.3s;
      z-index: 2;
    }

    #botao:hover {
      background-color: #2980b9; /* Cor do botão ao passar o mouse (dia) */
    }

    .noite #botao {
      background-color: #2c3e50; /* Cor do botão (noite) */
    }

    .noite #botao:hover {
      background-color: #34495e; /* Cor do botão ao passar o mouse (noite) */
    }

    .sol {
      position: absolute;
      top: 10%;
      left: 50%;
      transform: translateX(-50%);
      width: 100px;
      height: 100px;
      background-image: url('https://i.imgur.com/7DE0PnH.png'); /* Imagem do sol */
      background-size: cover;
      z-index: 1;
      transition: opacity 0.5s;
    }

    .lua {
      position: absolute;
      top: 10%;
      left: 50%;
      transform: translateX(-50%);
      width: 100px;
      height: 100px;
      background-image: url('https://i.imgur.com/tTM8VW2.png'); /* Imagem da lua */
      background-size: cover;
      z-index: 1;
      opacity: 0;
      transition: opacity 0.5s;
    }
  </style>
</head>
<body class="dia">

<div id="botao" draggable="true" ondragstart="drag(event)" ondragend="drop(event)">Arraste-me</div>
<div class="sol"></div>
<div class="lua"></div>

<script>
  function drag(event) {
    event.dataTransfer.setData("text", event.target.id);
  }

  function drop(event) {
    event.preventDefault();
    var data = event.dataTransfer.getData("text");
    var elemento = document.getElementById(data);
    var body = document.body;
    
    if (body.classList.contains("dia")) {
      body.classList.remove("dia");
      body.classList.add("noite");
      elemento.style.top = "90%";
    } else {
      body.classList.remove("noite");
      body.classList.add("dia");
      elemento.style.top = "10%";
    }
  }

  function allowDrop(event) {
    event.preventDefault();
  }
</script>

</body>
</html>
