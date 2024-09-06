const expand_btn = document.querySelector(".expand-btn");

function setSidebarCollapsedCookie() {
    days = 15
    time = 3600 * 24 * days
    document.cookie = `sidebarCollapsed=true; path=/; max-age=${time}`;
}

function flushSidebarCollapsedCookie() {
    document.cookie = "sidebarCollapsed=; path=/; max-age=0";
}


expand_btn.addEventListener("click", () => {
    document.body.classList.toggle("collapsed");
    if (document.body.classList.contains('collapsed')) {
        setSidebarCollapsedCookie();
    } 
    if (!document.body.classList.contains('collapsed')) {
        flushSidebarCollapsedCookie();
    }
});


function handleResize() {
    const body = document.body;

    if (window.innerWidth < 640) {
        // Se a tela for menor que 640px, adiciona a classe 'collapsed'
        body.classList.add('collapsed');
        setSidebarCollapsedCookie();
    } else {
        // Se a tela for maior que 640px, remove a classe 'collapsed'
        body.classList.remove('collapsed');
        flushSidebarCollapsedCookie();
    }
}


window.addEventListener('resize', handleResize);