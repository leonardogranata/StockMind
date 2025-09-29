document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("toggle-btn");
    const sidebar = document.getElementById("sidebar");
    const mainContent = document.querySelector(".main-content");

    // Recupera o estado da sidebar
    if (localStorage.getItem("sidebar-collapsed") === "true") {
        sidebar.classList.add("collapsed");
        mainContent.style.marginLeft = "70px";
    }

    toggleBtn.addEventListener("click", function () {
        sidebar.classList.toggle("collapsed");

        if (sidebar.classList.contains("collapsed")) {
            mainContent.style.marginLeft = "70px";
            localStorage.setItem("sidebar-collapsed", "true");
        } else {
            mainContent.style.marginLeft = "250px";
            localStorage.setItem("sidebar-collapsed", "false");
        }
    });
});
