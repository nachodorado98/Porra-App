const LEFT_16 = ["M74","M77","M73","M75","M83","M84","M81","M82"];
const RIGHT_16 = ["M76","M78","M79","M80","M86","M88","M85","M87"];

const MATCH_TREE = {
    M74:"M89", M77:"M89",
    M73:"M90", M75:"M90",
    M83:"M93", M84:"M93",
    M81:"M94", M82:"M94",

    M76:"M91", M78:"M91",
    M79:"M92", M80:"M92",
    M86:"M95", M88:"M95",
    M85:"M96", M87:"M96",

    M89:"M97", M90:"M97",
    M93:"M98", M94:"M98",

    M91:"M99", M92:"M99",
    M95:"M100", M96:"M100",

    M97:"M101", M98:"M101",
    M99:"M102", M100:"M102",

    M101:"M104",
    M102:"M104"
};

const THIRD_PLACE_TREE = {
    M101:"M103",
    M102:"M103"
};

const ROUNDS = [
    { id:"r16-left", title:"16avos", matches:LEFT_16, side:"left" },
    { id:"r8-left", title:"Octavos", matches:["M89","M90","M93","M94"], side:"left" },
    { id:"r4-left", title:"Cuartos", matches:["M97","M98"], side:"left" },
    { id:"r2-left", title:"Semis", matches:["M101"], side:"left" },

    { id:"final", title:"Final", matches:["M104"], side:"final" },

    { id:"r2-right", title:"Semis", matches:["M102"], side:"right" },
    { id:"r4-right", title:"Cuartos", matches:["M99","M100"], side:"right" },
    { id:"r8-right", title:"Octavos", matches:["M91","M92","M95","M96"], side:"right" },
    { id:"r16-right", title:"16avos", matches:RIGHT_16, side:"right" }
];

const winners = {};
const losers = {};

document.addEventListener("DOMContentLoaded", () => {
    renderBracket();
    renderThirdPlace();
    activarModal();
});

function renderBracket(){
    const bracket = document.getElementById("bracket");

    ROUNDS.forEach(round => {
        const roundDiv = document.createElement("div");
        roundDiv.className = `round ${round.side}`;
        roundDiv.id = round.id;

        roundDiv.innerHTML = `
            <div class="round-title">${round.title}</div>
            <div class="round-matches"></div>
        `;

        const matchesContainer = roundDiv.querySelector(".round-matches");

        round.matches.forEach(matchId => {
            matchesContainer.appendChild(createEmptyMatch(matchId));
        });

        bracket.appendChild(roundDiv);
    });

    fillInitial16avos();
}

function renderThirdPlace(){
    const container = document.getElementById("third-place-container");
    container.appendChild(createEmptyMatch("M103"));
}

function createEmptyMatch(matchId){
    const match = document.createElement("div");
    match.className = "match";
    match.dataset.match = matchId;

    match.innerHTML = `
        <div class="match-label">${matchId}</div>
        <div class="team empty" data-slot="0">Pendiente</div>
        <div class="team empty" data-slot="1">Pendiente</div>
    `;

    return match;
}

function fillInitial16avos(){
    [...LEFT_16, ...RIGHT_16].forEach(matchId => {
        const teams = BRACKET_16AVOS[matchId];
        setMatchTeams(matchId, teams);
    });
}

function setMatchTeams(matchId, teams){
    const match = document.querySelector(`[data-match="${matchId}"]`);

    match.querySelectorAll(".team").forEach((row, index) => {
        const team = teams[index];

        row.className = "team";
        row.dataset.teamId = team[2];
        row.dataset.team = JSON.stringify(team);

        row.innerHTML = `
            <img src="/static/imagenes/escudos/${team[2]}.png">
            <img src="/static/imagenes/banderas/${team[3]}.png">
            <span>${team[1]}</span>
        `;

        row.onclick = () => selectWinner(matchId, team);
    });
}

function selectWinner(matchId, winnerTeam){
    const match = document.querySelector(`[data-match="${matchId}"]`);
    const teams = [...match.querySelectorAll(".team")]
        .filter(t => !t.classList.contains("empty"))
        .map(t => JSON.parse(t.dataset.team));

    const loserTeam = teams.find(t => t[2] !== winnerTeam[2]);

    winners[matchId] = winnerTeam;

    if(loserTeam){
        losers[matchId] = loserTeam;
    }

    match.querySelectorAll(".team").forEach(row => {
        row.classList.remove("selected");

        if(Number(row.dataset.teamId) === winnerTeam[2]){
            row.classList.add("selected");
        }
    });

    clearNextRounds(matchId);

    sendWinnerForward(matchId, winnerTeam);

    if(THIRD_PLACE_TREE[matchId] && loserTeam){
        sendLoserToThirdPlace(matchId, loserTeam);
    }

    checkCompleted();

    if(matchId === "M104"){
        mostrarCampeon(winnerTeam);
    }
}

function sendWinnerForward(matchId, team){
    const nextMatch = MATCH_TREE[matchId];

    if(!nextMatch) return;

    putTeamInNextMatch(nextMatch, matchId, team);
}

function sendLoserToThirdPlace(matchId, team){
    putTeamInNextMatch("M103", matchId, team);
}

function putTeamInNextMatch(nextMatch, fromMatch, team){
    const match = document.querySelector(`[data-match="${nextMatch}"]`);

    let slot = match.querySelector(`[data-from="${fromMatch}"]`);

    if(!slot){
        slot = [...match.querySelectorAll(".team")]
            .find(row => row.classList.contains("empty"));
    }

    if(!slot) return;

    slot.className = "team";
    slot.dataset.from = fromMatch;
    slot.dataset.teamId = team[2];
    slot.dataset.team = JSON.stringify(team);

    slot.innerHTML = `
        <img src="/static/imagenes/escudos/${team[2]}.png">
        <img src="/static/imagenes/banderas/${team[3]}.png">
        <span>${team[1]}</span>
    `;

    slot.onclick = () => selectWinner(nextMatch, team);
}

function clearNextRounds(matchId){
    const next = MATCH_TREE[matchId];

    if(next){
        clearMatchFrom(next, matchId);
        clearNextRounds(next);
    }

    const third = THIRD_PLACE_TREE[matchId];

    if(third){
        clearMatchFrom(third, matchId);
    }

    if(matchId === "M104"){
        limpiarCampeon();
    }
}

function clearMatchFrom(matchId, fromMatch){
    const match = document.querySelector(`[data-match="${matchId}"]`);
    if(!match) return;

    const slot = match.querySelector(`[data-from="${fromMatch}"]`);

    if(slot){
        slot.className = "team empty";
        slot.removeAttribute("data-from");
        slot.removeAttribute("data-team");
        slot.removeAttribute("data-team-id");
        slot.innerHTML = "Pendiente";
        slot.onclick = null;
    }

    match.querySelectorAll(".team").forEach(row => {
        row.classList.remove("selected");
    });

    delete winners[matchId];
    delete losers[matchId];
}

function checkCompleted(){
    const requiredMatches = [
        "M73","M74","M75","M76","M77","M78","M79","M80",
        "M81","M82","M83","M84","M85","M86","M87","M88",
        "M89","M90","M91","M92","M93","M94","M95","M96",
        "M97","M98","M99","M100",
        "M101","M102",
        "M103",
        "M104"
    ];

    const completed = requiredMatches.every(id => winners[id]);

    const btn = document.getElementById("btnContinuar");

    if(completed){
        btn.disabled = false;
        btn.classList.add("enabled");
    }else{
        btn.disabled = true;
        btn.classList.remove("enabled");
    }
}

function activarModal(){
    const btn = document.getElementById("btnContinuar");
    const modal = document.getElementById("modalResumen");
    const cancelar = document.getElementById("cancelarModal");
    const resumen = document.getElementById("resumenContenido");
    const input = document.getElementById("inputElecciones");

    cancelar.addEventListener("click", () => {
        modal.classList.remove("active");
    });

    btn.addEventListener("click", () => {
        resumen.innerHTML = "";

        const bracketCompleto = getBracketCompleto();

        bracketCompleto.forEach(partido => {
            const div = document.createElement("div");
            div.className = "resumen-partido";

            div.innerHTML = `
                <strong>${partido.ronda.toUpperCase()} · ${partido.partido}</strong>

                <div class="resumen-equipos">
                    <div class="resumen-equipo">
                        <img src="/static/imagenes/escudos/${partido.equipo_1_escudo}.png">
                        <img src="/static/imagenes/banderas/${partido.equipo_1_bandera}.png">
                        <span>${partido.equipo_1_nombre}</span>
                    </div>

                    <span class="resumen-vs">vs</span>

                    <div class="resumen-equipo">
                        <img src="/static/imagenes/escudos/${partido.equipo_2_escudo}.png">
                        <img src="/static/imagenes/banderas/${partido.equipo_2_bandera}.png">
                        <span>${partido.equipo_2_nombre}</span>
                    </div>
                </div>

                <div class="resumen-ganadores">
                    <div class="resumen-ganador">
                        <span>Ganador:</span>
                        <img src="/static/imagenes/escudos/${partido.ganador_escudo}.png">
                        <img src="/static/imagenes/banderas/${partido.ganador_bandera}.png">
                        <span>${partido.ganador_nombre}</span>
                    </div>
                </div>
            `;

            resumen.appendChild(div);
        });

        input.value = JSON.stringify(getBracketParaGuardar());

        modal.classList.add("active");
    });
}

const ROUND_BY_MATCH = {};

[
    ...LEFT_16,
    ...RIGHT_16
].forEach(id => ROUND_BY_MATCH[id] = "dieciseisavos");

["M89","M90","M91","M92","M93","M94","M95","M96"]
    .forEach(id => ROUND_BY_MATCH[id] = "octavos");

["M97","M98","M99","M100"]
    .forEach(id => ROUND_BY_MATCH[id] = "cuartos");

["M101","M102"]
    .forEach(id => ROUND_BY_MATCH[id] = "semifinales");

ROUND_BY_MATCH["M103"] = "tercer_puesto";
ROUND_BY_MATCH["M104"] = "final";

function getBracketCompleto(){
    const partidos = [];

    Object.keys(ROUND_BY_MATCH)
        .sort((a,b) => Number(a.replace("M","")) - Number(b.replace("M","")))
        .forEach(matchId => {

            const match = document.querySelector(`[data-match="${matchId}"]`);
            const rows = [...match.querySelectorAll(".team")]
                .filter(row => !row.classList.contains("empty"));

            if(rows.length < 2) return;

            const equipo1 = JSON.parse(rows[0].dataset.team);
            const equipo2 = JSON.parse(rows[1].dataset.team);

            const ganador = winners[matchId];

            partidos.push({
                ronda: ROUND_BY_MATCH[matchId],
                partido: matchId,

                equipo_1_id: equipo1[0],
                equipo_1_nombre: equipo1[1],
                equipo_1_escudo: equipo1[2],
                equipo_1_bandera: equipo1[3],

                equipo_2_id: equipo2[0],
                equipo_2_nombre: equipo2[1],
                equipo_2_escudo: equipo2[2],
                equipo_2_bandera: equipo2[3],

                ganador_id: ganador ? ganador[0] : null,
                ganador_nombre: ganador ? ganador[1] : null,
                ganador_escudo: ganador ? ganador[2] : null,
                ganador_bandera: ganador ? ganador[3] : null
            });
        });

    return partidos;
}

function mostrarCampeon(team){
    const modal = document.getElementById("modalCampeon");
    const contenido = document.getElementById("modalCampeonContenido");

    contenido.innerHTML = `
        <img src="/static/imagenes/escudos/${team[2]}.png" class="campeon-escudo">
        <img src="/static/imagenes/banderas/${team[3]}.png" class="campeon-bandera">
        <div class="campeon-nombre">${team[1]}</div>
    `;

    modal.classList.add("active");
}

document.getElementById("cerrarModalCampeon").addEventListener("click", () => {
    document.getElementById("modalCampeon").classList.remove("active");
});

function limpiarCampeon(){
    const box = document.getElementById("campeonBox");
    const contenido = document.getElementById("campeonContenido");

    box.classList.remove("active");
    contenido.innerHTML = "Completa la final para ver tu campeón";
}

function getBracketParaGuardar(){
    return getBracketCompleto().map(partido => ({
        ronda: partido.ronda,
        partido: partido.partido,
        equipo_1_id: partido.equipo_1_id,
        equipo_2_id: partido.equipo_2_id,
        ganador_id: partido.ganador_id
    }));
}