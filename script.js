// selecionando a API(canvas) da biblioteca JS
const canvas = document.querySelector('canvas');
//gráfico 2d
const dimension = canvas.getContext('2d');

//tamanho dos quadrados
const res = 10;
// Altura e largura do grafico canvas
canvas.width = 500;
canvas.height = 500;

//define numero de linhas e colunas, é uma razao entre o tamanho do graf e dos quadrados
const coluna = canvas.width / res;
const linha  = canvas.height / res;

// cria o array e os preenche com 0, e após randomiza entre  1 e 0
function quadro() {
return new Array(coluna).fill(null).map(() => new Array(linha).fill(null).map(() => Math.floor(Math.random() * (Math.PI/2))));
}

//condição principal do jogo
let running = true;

//para inciar o jogo quando se clica o botao
function run() {
running = true;
}
// para parar o jogo quando se clica o botao
function stop() {
running = false;
}
// para reiniciar o jogo quando se clica o botao
function startag() {
graf = quadro();
}

// graf sera o grafico do jogo, que é retorno da funcao quadro
let graf = quadro();

// mudança ininterrupta das mudanças
requestAnimationFrame(change);

//função recursiva principal pra atualização dos frames
function change() {
if (running) {
//se estiver rodando, atualiza constantemente o canvas
graf = newGen(graf);
}
render(graf); //visualização
requestAnimationFrame(change);
quadro();  
}

//aplica as regras do jogo
function newGen(graf) {
//cria um novo objeto graf
const newGraf = graf.map(arr => [...arr]);

//
for (let c = 0; c < graf.length; c++) {
for (let l = 0; l < graf[c].length; l++) {
//posição determinada pelo for
let celula = graf[c][l];
let viziqtd = 0;
for (let i = -1; i < 2; i++) {
for (let j = -1; j < 2; j++) {
if ( i == 0 && j == 0 ) {
continue;
}
const x_celula = c + i;
          const y_celula = l + j;

        //serve pra analisar se o vizinho esta morto ou vivo, adicionando seu valor absoluto (0 ou 1)
       if (x_celula >= 0 && y_celula >= 0 && x_celula < coluna && y_celula < linha) {
          const newVizinho = graf[c + i][l + j]; //analisa o "valor" do vizinho (0 ou 1)
           viziqtd += newVizinho; // e o adiciona nessa variavel, para ser comparado apos
}
        }
      }

// Leis

if (celula == 1 && viziqtd < 2) { //regra 1, morrerá por solidão
newGraf[c][l] = 0

} else if (celula == 1 && viziqtd > 3) { //regra 2, morrerá por aglomeração
newGraf[c][l] = 0;

} else if (celula == 0 && viziqtd == 3) { //tiver tres vizinhos, viverá
newGraf[c][l] = 1;
}    
}
}
return newGraf; //retorna o novo graf
}


var firstime = true;

//render == manifestação grafica
function render(graf) {
for (var c = 0; c < graf.length; c++) { //percorre a matriz
for (var l = 0; l < graf.length; l++) {
const celula = graf[c][l];
//Ccomeça a desenhar os quadrados
dimension.beginPath();
//traça e colore os quadrados, do comprimento da linha, para o da colun. res e res sao largura e altura
dimension.rect(c * res, l * res, res, res);
//variação na cor. ? = if. se for true(1) sera #40D7D3, se nao purple
dimension.fillStyle = celula ? '#40D7D3' : 'purple';
//função da API
dimension.fill();
}
}

//para o jogo nao inicializar assim que se abre
if (firstime == true) {
running = false;
firstime = false;
}
}
