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



  document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("live-search-input");
    const resultsBox = document.getElementById("live-search-results");
    let timeout = null;

    input.addEventListener("input", function () {
      clearTimeout(timeout);
      const query = this.value;

      if (!query.trim()) {
        resultsBox.style.display = "none";
        resultsBox.innerHTML = "";
        return;
      }

      timeout = setTimeout(() => {
        fetch(`/accounts/search_all/?q=${encodeURIComponent(query)}`)
          .then(response => response.json())
          .then(data => {
            let html = "";

            if (data.jobs.length) {
              html += `<h6 class="dropdown-header">Jobs</h6>`;
              data.jobs.forEach(job => {
                html += `<a class="dropdown-item" href="#">${job.description} — ${job.driver}</a>`;
              });
            }

            if (data.truckers.length) {
              html += `<h6 class="dropdown-header">Drivers</h6>`;
              data.truckers.forEach(driver => {
                html += `<a class="dropdown-item" href="#">${driver.firstname} ${driver.lastname} — ${driver.role}</a>`;
              });
            }

            if (data.plates.length) {
              html += `<h6 class="dropdown-header">License Plates</h6>`;
              data.plates.forEach(plate => {
                html += `<a class="dropdown-item" href="#">${plate.state} - ${plate.plate_number}</a>`;
              });
            }

            resultsBox.innerHTML = html || `<span class="dropdown-item text-muted">No results</span>`;
            resultsBox.style.display = "block";
          });
      }, 300); // Debounce delay
    });

    document.addEventListener("click", function (e) {
      if (!resultsBox.contains(e.target) && e.target !== input) {
        resultsBox.style.display = "none";
      }
    });
  });