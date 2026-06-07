const MI_LEFT_16 = ["M74","M77","M73","M75","M83","M84","M81","M82"];
const MI_RIGHT_16 = ["M76","M78","M79","M80","M86","M88","M85","M87"];

const MI_ROUNDS = [
    { id:"mi-r16-left", title:"16avos", matches:MI_LEFT_16, side:"left" },
    { id:"mi-r8-left", title:"Octavos", matches:["M89","M90","M93","M94"], side:"left" },
    { id:"mi-r4-left", title:"Cuartos", matches:["M97","M98"], side:"left" },
    { id:"mi-r2-left", title:"Semis", matches:["M101"], side:"left" },

    { id:"mi-final", title:"Final", matches:["M104"], side:"final" },

    { id:"mi-r2-right", title:"Semis", matches:["M102"], side:"right" },
    { id:"mi-r4-right", title:"Cuartos", matches:["M99","M100"], side:"right" },
    { id:"mi-r8-right", title:"Octavos", matches:["M91","M92","M95","M96"], side:"right" },
    { id:"mi-r16-right", title:"16avos", matches:MI_RIGHT_16, side:"right" }
];

document.addEventListener("DOMContentLoaded", () => {
    renderMiBracket();
    renderMiThirdPlace();
    renderMiCampeon();
});

function renderMiBracket(){

    const bracket = document.getElementById("miBracket");

    if(!bracket) return;

    MI_ROUNDS.forEach(round => {

        const roundDiv = document.createElement("div");
        roundDiv.className = `mi-round ${round.side}`;
        roundDiv.id = round.id;

        roundDiv.innerHTML = `
            <div class="mi-round-title">${round.title}</div>
            <div class="mi-round-matches"></div>
        `;

        const matchesContainer = roundDiv.querySelector(".mi-round-matches");

        round.matches.forEach(matchId => {
            matchesContainer.appendChild(createMiMatch(matchId));
        });

        bracket.appendChild(roundDiv);
    });
}

function renderMiThirdPlace(){

    const container = document.getElementById("miThirdPlace");

    if(!container) return;

    container.appendChild(createMiMatch("M103"));
}

function createMiMatch(matchId){

    const partido = ELIMINATORIAS_PORRA[matchId];

    const match = document.createElement("div");
    match.className = "mi-match";
    match.dataset.match = matchId;

    if(!partido){

        match.innerHTML = `
            <div class="mi-match-label">${matchId}</div>
            <div class="mi-team empty">Pendiente</div>
            <div class="mi-team empty">Pendiente</div>
        `;

        return match;
    }

    match.innerHTML = `
        <div class="mi-match-label">${matchId}</div>
        ${crearFilaEquipo(partido.equipo_1, partido.ganador)}
        ${crearFilaEquipo(partido.equipo_2, partido.ganador)}
    `;

    return match;
}

function crearFilaEquipo(equipo, ganador){

    const esGanador = ganador && equipo.equipo_id === ganador.equipo_id;

    return `
        <div class="mi-team ${esGanador ? 'selected' : ''}">
            <img src="/static/imagenes/escudos/${equipo.escudo}.png">
            <img src="/static/imagenes/banderas/${equipo.bandera}.png">
            <span>${equipo.nombre}</span>
        </div>
    `;
}

function renderMiCampeon(){

    const contenido = document.getElementById("miCampeonContenido");

    if(!contenido) return;

    const final = ELIMINATORIAS_PORRA["M104"];

    if(!final || !final.ganador){

        contenido.innerHTML = "Todavía no hay campeón";
        return;
    }

    const campeon = final.ganador;

    contenido.innerHTML = `
        <div class="mi-campeon-card">
            <img src="/static/imagenes/escudos/${campeon.escudo}.png" class="mi-campeon-escudo">
            <img src="/static/imagenes/banderas/${campeon.bandera}.png" class="mi-campeon-bandera">
            <div class="mi-campeon-nombre">${campeon.nombre}</div>
        </div>
    `;
}