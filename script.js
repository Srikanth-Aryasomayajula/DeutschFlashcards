window.addEventListener('DOMContentLoaded', () => {
  // Load navbar
  fetch('navbar.html')
    .then(response => response.text())
    .then(data => {
      document.getElementById('navbar-placeholder').innerHTML = data;

      const toggleBtn = document.getElementById("menuToggleBtn");
      const menu = document.getElementById("menuContainer");

      // Toggle menu when clicking the button
      if (toggleBtn && menu) {
        toggleBtn.addEventListener("click", () => {
          menu.classList.toggle("show-menu");
        });

        // Close menu when clicking outside
        document.addEventListener('click', (event) => {
          if (
            menu.classList.contains('show-menu') &&
            !menu.contains(event.target) &&
            !toggleBtn.contains(event.target)
          ) {
            menu.classList.remove('show-menu');
          }
        });
      }
    });

  // Load footer
  fetch('footer.html')
    .then(response => response.text())
    .then(data => {
      document.getElementById('footer-placeholder').innerHTML = data;
    });
});
