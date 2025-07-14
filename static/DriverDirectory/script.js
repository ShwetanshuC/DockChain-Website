document.addEventListener("DOMContentLoaded", function () {
    const dropdown = document.getElementById("navbarDropdown");
    if (dropdown && typeof bootstrap !== 'undefined') {
      const dd = new bootstrap.Dropdown(dropdown);
      dropdown.addEventListener('click', function (event) {
        event.preventDefault();
        dd.toggle();
      });
    }

  const editButtons = document.querySelectorAll(".edit-button");

  editButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const cardBody = button.closest(".card-body");
      const displayMode = cardBody.querySelector(".display-mode");
      const editForm = cardBody.querySelector(".edit-form");

      if (displayMode && editForm) {
        displayMode.classList.add("d-none");
        editForm.classList.remove("d-none");
      }
    });
  });
  });