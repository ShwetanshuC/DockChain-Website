  document.addEventListener("DOMContentLoaded", function () {
    const dropdown = document.getElementById("navbarDropdown");
    if (dropdown && typeof bootstrap !== 'undefined') {
      const dd = new bootstrap.Dropdown(dropdown);
      dropdown.addEventListener('click', function (event) {
        event.preventDefault();
        dd.toggle();
      });
    }
  });