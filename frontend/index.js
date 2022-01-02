const button = document.getElementsByTagName("button")[0];
const input = document.getElementsByTagName("input")[0];
const divSearch = document.getElementById("search");
const divInfo = document.getElementById("info");
const SEARCH_GAME = "https://twitch-game-app.herokuapp.com/games?name=";
const GAME_INFO = "https://twitch-game-app.herokuapp.com/gameinfo?id=";

button.addEventListener("click", () => {
  inicia();
});

input.onkeydown = (event) => {
  if (event.keyCode === 13) inicia();
};

function inicia() {
  divSearch.innerHTML = divInfo.innerHTML = "";
  divSearch.innerHTML = `<p>Carregando....</p><img src="loading.gif">`;
  if (input.value != "") {
    if (localStorage.getItem(SEARCH_GAME + input.value) != null)
      resultSearch(JSON.parse(localStorage.getItem(SEARCH_GAME + input.value)));
    else acessaApi(SEARCH_GAME + input.value);
  } else alert("Preencha os dados corretamente.");
}

function resultSearch(json) {
  let temp = "";
  const games = json.response;
  for (let i in games) {
    temp += `
      <span onclick="infoGame(${games[i].id},0)">
        <img src="https:${games[i].cover}">
        <p>${games[i].name}</p>
      </span>
    `;
  }
  divSearch.innerHTML = temp;
}

function infoGame(json, id) {
  divSearch.innerHTML = divInfo.innerHTML = "";
  divSearch.innerHTML = `<p>Carregando....</p><img src="loading.gif" width="100px">`;
  if (id == 0) {
    acessaApi(GAME_INFO + json);
  } else {
    const result = json.response[0];
    console.log(result);
    
    let resultStream = `<div class="stream">`;
    
    if (result.streams != 400) {
      for (let i in result.streams) {
        resultStream += `
        <a href="${result.streams[i].user}">
        <img src="${result.streams[i].imagem}">
        <p>${result.streams[i].titulo}</p>
        <p><b>Inicio:</b>${date2(result.streams[i].inicio)}</p>
        </a>
        `;
      }
    } else resultStream += `<h2>Nenhuma stream para esse jogo!</h2></div>`;
    
    let response = `
    <img class="rifth" src="https:${result.cover}">
    <div class="game-info">
    <h2>${result.name}</h2>
    <p>${result.descricao}</p>
    <p><b>Gêneros:</b> ${result.generos.join(", ")}</p>
    <p><b>Plataformas:</b> ${result.plataformas.join(", ")}</p>
    <p><b>Data lançamento:</b> ${date(result.data_criacao)}</p>
    <a href="${result.url}" target="_blank">Acessar página original</a>
    </div>
    <div class="video-container">
    <iframe src="${result.youtube_id}" 
    frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>
    ${resultStream}
    `;
    
    divInfo.innerHTML = response;
  }
}

const date = (timestamp) => {
  const now = new Date();
  let date = new Date(parseInt(timestamp * 1000));
  let dateSplit = date.toString().split(" ");
  const diff = Math.abs(now.getTime() - date.getTime());
  const days = Math.ceil(diff / 31557600000);
  return `${dateSplit[1]} ${dateSplit[2]}, ${dateSplit[3]} (${days} year)`;
};

const date2 = (data) => {
  let date = new Date(data);
  return `${date.toLocaleDateString("pt-BR")} ${date.toLocaleTimeString(
    "pt-BR"
  )}`;
};

function acessaApi(url) {
  let xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4) {
      if (this.status == 200) {
        if (url.includes(SEARCH_GAME)) {
          localStorage.setItem(url, this.responseText);
          resultSearch(JSON.parse(this.responseText));
        } else {
          infoGame(JSON.parse(this.responseText), 1);
        }
      } else if (this.status == 404)
        divSearch.innerHTML = "<h1>Jogo não encontrado!</h1>";
    }
  };
  xhttp.open("GET", url, true);
  xhttp.send();
}
