document.addEventListener("DOMContentLoaded", function () {
  const dropdown = document.getElementById("navbarDropdown");
  if (dropdown && typeof bootstrap !== 'undefined') {
    const dd = new bootstrap.Dropdown(dropdown);
    dropdown.addEventListener('click', function (event) {
      event.preventDefault();
      dd.toggle();
    });
  }
  const startJobDropdown = document.getElementById("startJobDropdown");
  if (startJobDropdown && typeof bootstrap !== 'undefined') {
    const startJobMenu = new bootstrap.Dropdown(startJobDropdown);
    startJobDropdown.addEventListener('click', function (event) {
      event.preventDefault();
      startJobMenu.toggle();
    });
  }
  const moreOptionsDropdown = document.getElementById("moreOptionsDropdown");
  if (moreOptionsDropdown && typeof bootstrap !== 'undefined') {
    const moreOptionsMenu = new bootstrap.Dropdown(moreOptionsDropdown);
    moreOptionsDropdown.addEventListener('click', function (event) {
      event.preventDefault();
      moreOptionsMenu.toggle();
    });
  }
});