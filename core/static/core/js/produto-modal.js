function abrirModal(nome, preco, img, desc) {
    const modal = document.getElementById('modal');
    const modalImg = document.getElementById('modal-img');

    modal.classList.add('is-open');
    document.getElementById('modal-nome').innerText = nome;
    document.getElementById('modal-preco').innerText = `R$ ${preco}`;
    document.getElementById('modal-desc').innerText = desc;

    if (img) {
        modalImg.src = img;
        modalImg.style.display = 'block';
    } else {
        modalImg.removeAttribute('src');
        modalImg.style.display = 'none';
    }
}

function fecharModal() {
    document.getElementById('modal').classList.remove('is-open');
}

document.querySelectorAll('[data-product-modal]').forEach(function (button) {
    button.addEventListener('click', function () {
        abrirModal(
            button.dataset.productName,
            button.dataset.productPrice,
            button.dataset.productImg,
            button.dataset.productDesc
        );
    });
});

document.querySelectorAll('[data-modal-close]').forEach(function (button) {
    button.addEventListener('click', fecharModal);
});

window.addEventListener('click', function (event) {
    const modal = document.getElementById('modal');
    if (event.target === modal) {
        fecharModal();
    }
});

window.addEventListener('keydown', function (event) {
    if (event.key === 'Escape') {
        fecharModal();
    }
});
