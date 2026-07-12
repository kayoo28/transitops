/* ==========================================
   TransitOps - Main JavaScript
========================================== */

document.addEventListener("DOMContentLoaded", () => {

    initSidebar();

    initAlerts();

    initDeleteConfirmation();

    initTooltips();

    initBackToTop();

});

/* ==========================================
   Sidebar Toggle
========================================== */

function initSidebar() {

    const toggleBtn = document.getElementById("sidebarToggle");

    const sidebar = document.querySelector(".sidebar");

    if (!toggleBtn || !sidebar) return;

    toggleBtn.addEventListener("click", () => {

        sidebar.classList.toggle("collapsed");

    });

}

/* ==========================================
   Auto Hide Alerts
========================================== */

function initAlerts() {

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(alert => {

        setTimeout(() => {

            alert.classList.add("fade");

            setTimeout(() => {

                alert.remove();

            }, 500);

        }, 4000);

    });

}

/* ==========================================
   Delete Confirmation
========================================== */

function initDeleteConfirmation() {

    const deleteButtons = document.querySelectorAll(".btn-delete");

    deleteButtons.forEach(button => {

        button.addEventListener("click", function (event) {

            const confirmed = confirm(
                "Are you sure you want to delete this record?"
            );

            if (!confirmed) {

                event.preventDefault();

            }

        });

    });

}

/* ==========================================
   Bootstrap Tooltips
========================================== */

function initTooltips() {

    if (typeof bootstrap === "undefined") return;

    const tooltipTriggerList = [].slice.call(

        document.querySelectorAll(
            '[data-bs-toggle="tooltip"]'
        )

    );

    tooltipTriggerList.forEach(function (tooltipTriggerEl) {

        new bootstrap.Tooltip(

            tooltipTriggerEl

        );

    });

}

/* ==========================================
   Smooth Scroll
========================================== */

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener("click", function (e) {

        const target = document.querySelector(

            this.getAttribute("href")

        );

        if (!target) return;

        e.preventDefault();

        target.scrollIntoView({

            behavior: "smooth",

            block: "start"

        });

    });

});

/* ==========================================
   Back To Top Button
========================================== */

function initBackToTop() {

    const backToTop = document.getElementById("backToTop");

    if (!backToTop) return;

    window.addEventListener("scroll", () => {

        if (window.scrollY > 300) {

            backToTop.classList.remove("d-none");

        } else {

            backToTop.classList.add("d-none");

        }

    });

    backToTop.addEventListener("click", () => {

        window.scrollTo({

            top: 0,

            behavior: "smooth"

        });

    });

}

/* ==========================================
   Live Table Search Helper
========================================== */

function filterTable(inputId, tableId) {

    const input = document.getElementById(inputId);

    const table = document.getElementById(tableId);

    if (!input || !table) return;

    input.addEventListener("keyup", function () {

        const value = this.value.toLowerCase();

        const rows = table.querySelectorAll("tbody tr");

        rows.forEach(row => {

            row.style.display = row.innerText
                .toLowerCase()
                .includes(value)
                ? ""
                : "none";

        });

    });

}

/* ==========================================
   Table Row Counter
========================================== */

function getVisibleRowCount(tableId) {

    const table = document.getElementById(tableId);

    if (!table) return 0;

    return [...table.querySelectorAll("tbody tr")]

        .filter(row => row.style.display !== "none")

        .length;

}

/* ==========================================
   Dark Mode Toggle
========================================== */

function initDarkMode() {

    const toggle = document.getElementById("darkModeToggle");

    if (!toggle) return;

    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "dark") {

        document.body.classList.add("dark-mode");

        toggle.checked = true;

    }

    toggle.addEventListener("change", function () {

        if (this.checked) {

            document.body.classList.add("dark-mode");

            localStorage.setItem("theme", "dark");

        } else {

            document.body.classList.remove("dark-mode");

            localStorage.setItem("theme", "light");

        }

    });

}

/* ==========================================
   Current Year Auto Update
========================================== */

function updateCurrentYear() {

    const yearElement = document.getElementById("currentYear");

    if (yearElement) {

        yearElement.textContent = new Date().getFullYear();

    }

}

/* ==========================================
   Form Submit Loader
========================================== */

function initFormLoader() {

    const forms = document.querySelectorAll("form");

    forms.forEach(form => {

        form.addEventListener("submit", function () {

            const submitBtn = form.querySelector(

                'button[type="submit"]'

            );

            if (submitBtn) {

                submitBtn.disabled = true;

                submitBtn.innerHTML =

                    '<span class="spinner-border spinner-border-sm me-2"></span>Saving...';

            }

        });

    });

}

/* ==========================================
   Common UI Helpers
========================================== */

function showToast(message) {

    console.log(message);

}

function showSuccess(message) {

    showToast(message);

}

function showError(message) {

    showToast(message);

}

/* ==========================================
   Initialize Additional Features
========================================== */

document.addEventListener("DOMContentLoaded", () => {

    initDarkMode();

    updateCurrentYear();

    initFormLoader();

});

/* ==========================================
   Utility Functions
========================================== */

function formatCurrency(amount) {

    return new Intl.NumberFormat("en-IN", {

        style: "currency",

        currency: "INR",

        maximumFractionDigits: 2

    }).format(amount);

}

function formatNumber(number) {

    return new Intl.NumberFormat("en-IN").format(number);

}

function debounce(callback, delay = 300) {

    let timer;

    return (...args) => {

        clearTimeout(timer);

        timer = setTimeout(() => {

            callback(...args);

        }, delay);

    };

}

/* ==========================================
   End Of File
========================================== */

console.log(

    "TransitOps v1.0 Loaded Successfully"

);