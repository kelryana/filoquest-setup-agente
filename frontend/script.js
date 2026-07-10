//frontend/script.js
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
    const erroMensagem = document.getElementById('erro-mensagem');

    // Validação simples
    const pergunta = perguntaInput.value.trim();
    if (!pergunta) {
        mostrarErro("Por favor, digite uma pergunta.");
        return;
    }

    // Resetar estados anteriores
    esconderElementos([respostaContainer, erroContainer]);
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

        // Exibir resposta com animação suave
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
 * Mostra mensagem de erro na tela
 */
function mostrarErro(mensagem) {
    const erroContainer = document.getElementById('erro-container');
    const erroMensagem = document.getElementById('erro-mensagem');

    erroMensagem.textContent = mensagem;
    mostrarElemento(erroContainer);
}

/**
 * Habilita ou desabilita o botão de perguntar
 */
function desabilitarBotao(botao, desabilitado) {
    botao.disabled = desabilitado;
    if (desabilitado) {
        botao.innerHTML = '<i class="fas fa-hourglass-half"></i> Aguardando...';
    } else {
        botao.innerHTML = '<i class="fas fa-paper-plane"></i> Perguntar ao Filósofo';
    }
}

/**
 * Utility: Mostra múltiplos elementos
 */
function mostrarElementos(elementos) {
    elementos.forEach(el => el.classList.remove('hidden'));
}

/**
 * Utility: Esconde múltiplos elementos
 */
function esconderElementos(elementos) {
    elementos.forEach(el => el.classList.add('hidden'));
}

/**
 * Utility: Mostra um elemento
 */
function mostrarElemento(elemento) {
    elemento.classList.remove('hidden');
}

/**
 * Utility: Esconde um elemento
 */
function esconderElemento(elemento) {
    elemento.classList.add('hidden');
}

/**
 * Permite enviar pergunta pressionando Enter (sem Shift)
 */
document.addEventListener('DOMContentLoaded', () => {
    const perguntaInput = document.getElementById('pergunta');

    perguntaInput.addEventListener('keydown', (evento) => {
        if (evento.key === 'Enter' && !evento.shiftKey) {
            evento.preventDefault();
            enviarPergunta();
        }
    });
});
