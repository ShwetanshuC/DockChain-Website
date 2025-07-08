document.addEventListener("DOMContentLoaded", function () {
  const dropdown = document.getElementById("navbarDropdown");
  if (dropdown && typeof bootstrap !== 'undefined') {
    const dd = new bootstrap.Dropdown(dropdown);
    dropdown.addEventListener('click', function (event) {
      event.preventDefault();
      dd.toggle();
    });
  }

  const searchInput = document.querySelector('input[type="search"]');
  const cardsContainer = document.getElementById('trucker-cards') || document.getElementById('license-plate-cards');

  if (searchInput && cardsContainer) {
    searchInput.addEventListener('input', function () {
      const query = this.value.toLowerCase();
      const cards = cardsContainer.querySelectorAll('.card');

      cards.forEach(card => {
        const cardText = card.innerText.toLowerCase();
        if (cardText.includes(query)) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });
    });
  }
});