const expand_btn = document.querySelector(".expand-btn");

expand_btn.addEventListener("click", () => {
    document.body.classList.toggle("collapsed");
    if (document.body.classList.contains('collapsed')) {
        localStorage.setItem('sidebarCollapsed', 'true');
    } else {
        localStorage.setItem('sidebarCollapsed', 'false');
    }
});

// Verifica o localStorage para aplicar a classe 'collapsed' antes do carregamento


// Função para aplicar o estado do localStorage ao carregar a página
function applyCollapsedState() {
    const isCollapsed = localStorage.getItem('sidebarCollapsed');
    const body = document.body;

    // Se o valor for 'true', adiciona a classe 'collapsed'
    if (isCollapsed === 'true') {
        body.classList.add('collapsed');
    } else {
        body.classList.remove('collapsed');
    }
}

// Função para verificar o tamanho da janela e ajustar o estado
function handleResize() {
    const body = document.body;

    if (window.innerWidth < 640) {
        // Se a tela for menor que 640px, adiciona a classe 'collapsed'
        body.classList.add('collapsed');
        localStorage.setItem('sidebarCollapsed', 'true'); // Salva o estado no localStorage
    } else {
        // Se a tela for maior que 640px, remove a classe 'collapsed'
        body.classList.remove('collapsed');
        localStorage.setItem('sidebarCollapsed', 'false'); // Salva o estado no localStorage
    }
}

// Recupera o estado do localStorage quando a página carrega
window.addEventListener('load', () => {
    applyCollapsedState(); // Aplica o estado salvo no localStorage
});

// Atualiza o estado ao redimensionar a janela
// window.addEventListener('resize', handleResize);