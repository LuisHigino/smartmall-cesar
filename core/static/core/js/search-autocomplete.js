const searchInput = document.getElementById('search-input');
const suggestionsBox = document.getElementById('search-suggestions');
let debounceTimer;

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function displaySuggestions(results) {
    if (results.length === 0) {
        suggestionsBox.innerHTML = `
            <div class="suggestion-group">Nenhum resultado</div>
            <div class="suggestion-item">
                <span class="item-name">Tente buscar por outro termo</span>
            </div>
        `;
        return;
    }

    let html = '';
    const lojas = results.filter((result) => result.type === 'loja');
    const produtos = results.filter((result) => result.type === 'produto');

    if (lojas.length > 0) {
        html += '<div class="suggestion-group">Lojas</div>';
        lojas.forEach((loja) => {
            html += `
                <a href="${loja.url}" class="suggestion-item">
                    <div>
                        <span class="item-name">${escapeHtml(loja.name)}</span>
                        ${loja.category ? `<span class="item-meta"> - ${escapeHtml(loja.category)}</span>` : ''}
                    </div>
                    <span class="item-type loja">Loja</span>
                </a>
            `;
        });
    }

    if (produtos.length > 0) {
        html += '<div class="suggestion-group">Produtos</div>';
        produtos.forEach((produto) => {
            html += `
                <a href="${produto.url}" class="suggestion-item">
                    <div>
                        <span class="item-name">${escapeHtml(produto.name)}</span>
                        ${produto.loja ? `<span class="item-meta"> - ${escapeHtml(produto.loja)}</span>` : ''}
                        ${produto.preco ? `<span class="item-meta"> - R$ ${escapeHtml(produto.preco)}</span>` : ''}
                    </div>
                    <span class="item-type produto">Produto</span>
                </a>
            `;
        });
    }

    suggestionsBox.innerHTML = html;
}

function fetchSuggestions(query) {
    suggestionsBox.innerHTML = '<div class="suggestion-loading">Buscando...</div>';
    suggestionsBox.classList.add('active');

    fetch(`/busca/autocomplete/?q=${encodeURIComponent(query)}`)
        .then((response) => response.json())
        .then((data) => displaySuggestions(data.results))
        .catch(() => {
            suggestionsBox.innerHTML = '';
            suggestionsBox.classList.remove('active');
        });
}

if (searchInput && suggestionsBox) {
    searchInput.addEventListener('input', function () {
        const query = this.value.trim();
        clearTimeout(debounceTimer);

        if (query.length < 2) {
            suggestionsBox.classList.remove('active');
            suggestionsBox.innerHTML = '';
            return;
        }

        debounceTimer = setTimeout(() => {
            fetchSuggestions(query);
        }, 300);
    });

    searchInput.addEventListener('focus', function () {
        const query = this.value.trim();
        if (query.length >= 2) {
            fetchSuggestions(query);
        }
    });

    document.addEventListener('click', function (event) {
        if (!searchInput.contains(event.target) && !suggestionsBox.contains(event.target)) {
            suggestionsBox.classList.remove('active');
        }
    });
}
