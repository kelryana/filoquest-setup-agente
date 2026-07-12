const API_URL = "http://localhost:8000/perguntar";

async function enviarPergunta() {
    const perguntaInput = document.getElementById('pergunta');
    const btnPerguntar = document.getElementById('btn-perguntar');
    const loadingDiv = document.getElementById('loading');
    const respostaContainer = document.getElementById('resposta-container');
    const respostaTexto = document.getElementById('resposta-texto');
    const erroContainer = document.getElementById('erro-container');
    const erroMensagem = document.getElementById('erro-mensagem');

    const pergunta = perguntaInput.value.trim();
    if (!pergunta) {
        erroMensagem.textContent = "Por favor, digite uma pergunta.";
        mostrarElemento(erroContainer);
        return;
    }

    esconderElementos([respostaContainer, erroContainer]);
    
    respostaContainer.style.animation = 'none';
    respostaContainer.offsetHeight; 
    respostaContainer.style.animation = null; 

    mostrarElemento(loadingDiv);
    desabilitarBotao(btnPerguntar, true);

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ texto: pergunta })
        });

        if (!response.ok) throw new Error(`Erro na API: ${response.status}`);

        const dados = await response.json();
        respostaTexto.textContent = dados.resposta;
        mostrarElemento(respostaContainer);
        perguntaInput.value = '';

    } catch (erro) {
        console.error('Erro ao enviar pergunta:', erro);
        erroMensagem.textContent = "Não foi possível conectar ao Agente Filósofo. Verifique se a API está rodando em localhost:8000";
        mostrarElemento(erroContainer);
    } finally {
        esconderElemento(loadingDiv);
        desabilitarBotao(btnPerguntar, false);
    }
}

function desabilitarBotao(botao, desabilitado) {
    botao.disabled = desabilitado;
    botao.innerHTML = desabilitado 
        ? '<i class="fas fa-hourglass-half fa-spin"></i> Aguardando...' 
        : '<i class="fas fa-paper-plane"></i> Perguntar ao Filósofo';
}

function mostrarElementos(elementos) { elementos.forEach(el => el.classList.remove('hidden')); }
function esconderElementos(elementos) { elementos.forEach(el => el.classList.add('hidden')); }
function mostrarElemento(elemento) { elemento.classList.remove('hidden'); }
function esconderElemento(elemento) { elemento.classList.add('hidden'); }

document.addEventListener('DOMContentLoaded', () => {
    
    // Lógica da Pergunta
    const perguntaInput = document.getElementById('pergunta');
    const btnPerguntar = document.getElementById('btn-perguntar');

    perguntaInput.addEventListener('keydown', (evento) => {
        if (evento.key === 'Enter' && !evento.shiftKey) {
            evento.preventDefault(); 
            enviarPergunta();
        }
    });
    btnPerguntar.addEventListener('click', enviarPergunta);

    // --- Lógica do MODAL FLASHCARD ---
    const topicItems = document.querySelectorAll('.topic-item');
    const modalOverlay = document.getElementById('modal-overlay');
    const modalTitle = document.getElementById('modal-title');
    const modalContent = document.getElementById('modal-content');
    const closeModalBtn = document.getElementById('close-modal');

    function abrirModal(title, content) {
        modalTitle.textContent = title;
        modalContent.textContent = content;
        modalOverlay.classList.add('open');
        // NÃO TRAVAMOS MAIS O SCROLL DO BODY. O usuário pode ler e rolar o fundo.
    }

    function fecharModal() {
        modalOverlay.classList.remove('open');
    }

    topicItems.forEach(item => {
        item.addEventListener('click', () => {
            const title = item.getAttribute('data-title');
            const content = item.getAttribute('data-content');
            abrirModal(title, content);
        });
    });

    closeModalBtn.addEventListener('click', fecharModal);
    modalOverlay.addEventListener('click', fecharModal);

    document.addEventListener('keydown', (evento) => {
        if (evento.key === 'Escape' && modalOverlay.classList.contains('open')) {
            fecharModal();
        }
    });
});