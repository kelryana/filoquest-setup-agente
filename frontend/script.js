// URL da API do Agente Filósofo
const API_URL = "http://localhost:8000/perguntar";

/**
 * Envia a pergunta para a API e exibe a resposta
 */
async function enviarPergunta() {
    const perguntaInput = document.getElementById('pergunta');
    const btnPerguntar = document.getElementById('btn-perguntar');
    const loadingDiv = document.getElementById('loading');
    const respostaContainer = document.getElementById('resposta-container');
    const respostaTexto = document.getElementById('resposta-texto');
    const erroContainer = document.getElementById('erro-container');

    // Validação simples
    const pergunta = perguntaInput.value.trim();
    if (!pergunta) {
        mostrarErro("Por favor, digite uma pergunta.");
        return;
    }

    // Resetar estados anteriores
    esconderElementos([respostaContainer, erroContainer]);
    
    // TRUQUE DE ANIMAÇÃO: Força o navegador a reiniciar a animação CSS
    respostaContainer.style.animation = 'none';
    respostaContainer.offsetHeight; /* trigger reflow */
    respostaContainer.style.animation = null; 

    // Mostrar estado de carregamento e desabilitar botão
    mostrarElemento(loadingDiv);
    desabilitarBotao(btnPerguntar, true);

    try {
        // Fazer requisição para a API
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ texto: pergunta })
        });

        if (!response.ok) {
            throw new Error(`Erro na API: ${response.status}`);
        }

        const dados = await response.json();

        // Exibir resposta
        respostaTexto.textContent = dados.resposta;
        mostrarElemento(respostaContainer);

        // Limpar campo de pergunta após sucesso
        perguntaInput.value = '';

    } catch (erro) {
        console.error('Erro ao enviar pergunta:', erro);
        mostrarErro(
            "Não foi possível conectar ao Agente Filósofo. " +
            "Verifique se a API está rodando em localhost:8000"
        );
    } finally {
        esconderElemento(loadingDiv);
        desabilitarBotao(btnPerguntar, false);
    }
}

/**
 * Funções de UI
 */
function mostrarErro(mensagem) {
    const erroContainer = document.getElementById('erro-container');
    const erroMensagem = document.getElementById('erro-mensagem');
    erroMensagem.textContent = mensagem;
    mostrarElemento(erroContainer);
}

function desabilitarBotao(botao, desabilitado) {
    botao.disabled = desabilitado;
    if (desabilitado) {
        botao.innerHTML = '<i class="fas fa-hourglass-half fa-spin"></i> Aguardando...';
    } else {
        botao.innerHTML = '<i class="fas fa-paper-plane"></i> Perguntar ao Filósofo';
    }
}

function mostrarElementos(elementos) { elementos.forEach(el => el.classList.remove('hidden')); }
function esconderElementos(elementos) { elementos.forEach(el => el.classList.add('hidden')); }
function mostrarElemento(elemento) { elemento.classList.remove('hidden'); }
function esconderElemento(elemento) { elemento.classList.add('hidden'); }

/**
 * Event Listeners Iniciais
 */
document.addEventListener('DOMContentLoaded', () => {
    // 1. Enviar pergunta com Enter
    const perguntaInput = document.getElementById('pergunta');
    perguntaInput.addEventListener('keydown', (evento) => {
        if (evento.key === 'Enter' && !evento.shiftKey) {
            evento.preventDefault(); 
            enviarPergunta();
        }
    });

    // 2. Lógica da Aba Lateral Dinâmica (Novo Feature)
    const topicItems = document.querySelectorAll('.topic-item');
    const infoSidebar = document.getElementById('info-sidebar');
    const sidebarTitle = document.getElementById('sidebar-title');
    const sidebarContent = document.getElementById('sidebar-content');
    const closeSidebarBtn = document.getElementById('close-sidebar');

    // Ao clicar num tópico, atualiza o conteúdo e abre a aba
    topicItems.forEach(item => {
        item.addEventListener('click', () => {
            const title = item.getAttribute('data-title');
            const content = item.getAttribute('data-content');
            
            sidebarTitle.textContent = title;
            sidebarContent.textContent = content;
            
            // Adiciona a classe que faz a aba deslizar
            infoSidebar.classList.add('open');
        });
    });

    // Fechar aba pelo botão "X"
    closeSidebarBtn.addEventListener('click', () => {
        infoSidebar.classList.remove('open');
    });

    // Fechar aba ao clicar fora dela
    document.addEventListener('click', (evento) => {
        // Se a aba estiver aberta e o clique não for dentro da aba nem num dos tópicos
        if (infoSidebar.classList.contains('open') && 
            !infoSidebar.contains(evento.target) && 
            !evento.target.closest('.topic-item')) {
            infoSidebar.classList.remove('open');
        }
    });
});