document.addEventListener('DOMContentLoaded', function () {
  // Handle inline edit toggles
  document.querySelectorAll('.edit-button').forEach(button => {
    button.addEventListener('click', function () {
      const cardBody = this.closest('.card-body');
      cardBody.querySelector('.display-mode').classList.add('d-none');
      cardBody.querySelector('.edit-form').classList.remove('d-none');
    });
  });

  // Handle live search filter from navbar
const searchBox = document.querySelector('input[name="q"]');
const cardsContainer = document.getElementById("trucker-cards");

if (searchBox && cardsContainer) {
  searchBox.addEventListener("input", function () {
    const term = this.value.toLowerCase();
    const cards = cardsContainer.querySelectorAll(".card");

    cards.forEach(card => {
      const text = card.textContent.toLowerCase();
      card.closest(".col-12").style.display = text.includes(term) ? "" : "none";
    });
  });
}
});