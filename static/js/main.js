// AF IMPERIYA - Professional JavaScript Functions

// Real-time yangilanishlar
let updateInterval;

function updateTaskStatus() {
    // Real-time task status yangilanishi
    console.log('Topshiriqlar yangilanmoqda...');
    
    // Fetch yangi ma'lumotlar (agar kerak bo'lsa)
    // fetch('/api/tasks/status')
    //     .then(response => response.json())
    //     .then(data => {
    //         // Ma'lumotlarni yangilash
    //     });
}

// Dashboard grafiklar
function initDashboard() {
    console.log('Dashboard ishga tushdi');
    
    // Animatsiyalarni ishga tushirish
    animateCards();
    
    // Real-time yangilanishni boshlash (har 30 sekundda)
    updateInterval = setInterval(updateTaskStatus, 30000);
}

// Kartochkalarni animatsiya qilish
function animateCards() {
    const cards = document.querySelectorAll('.stat-card, .module-card, .chart-container');
    
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.style.animation = 'fadeIn 0.5s ease-in';
        }, index * 100);
    });
}

// Notification ko'rsatish
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed top-0 end-0 m-3`;
    alertDiv.style.zIndex = '9999';
    alertDiv.style.minWidth = '300px';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    const inputs = form.querySelectorAll('[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        }
    });
    
    return isValid;
}

// Loading state
function setLoading(button, loading = true) {
    if (loading) {
        button.disabled = true;
        button.innerHTML = '<span class="loading"></span> Yuklanmoqda...';
    } else {
        button.disabled = false;
        button.innerHTML = button.dataset.originalText || 'Saqlash';
    }
}

// Smooth scroll
function smoothScrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Confirm dialog
function confirmAction(message) {
    return confirm(message);
}

// Format date
function formatDate(date) {
    const d = new Date(date);
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    return `${day}.${month}.${year}`;
}

// Get days remaining color
function getDaysRemainingColor(days) {
    if (days <= 3) return 'danger';
    if (days <= 5) return 'warning';
    if (days <= 7) return 'info';
    return 'success';
}

// Initialize tooltips
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize popovers
function initPopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Auto-hide alerts
function autoHideAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.remove('show');
            setTimeout(() => alert.remove(), 150);
        }, 5000);
    });
}

// Counter animation
function animateCounter(element, target, duration = 1000) {
    let current = 0;
    const increment = target / (duration / 16);
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = Math.round(target);
            clearInterval(timer);
        } else {
            element.textContent = Math.round(current);
        }
    }, 16);
}

// Initialize counters
function initCounters() {
    const counters = document.querySelectorAll('.stat-value');
    counters.forEach(counter => {
        const target = parseInt(counter.textContent);
        if (!isNaN(target)) {
            counter.textContent = '0';
            setTimeout(() => {
                animateCounter(counter, target);
            }, 500);
        }
    });
}

// Search functionality
function setupSearch(inputId, targetClass) {
    const searchInput = document.getElementById(inputId);
    if (!searchInput) return;
    
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase();
        const items = document.querySelectorAll(targetClass);
        
        items.forEach(item => {
            const text = item.textContent.toLowerCase();
            if (text.includes(searchTerm)) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });
    });
}

// Dark mode toggle (future feature)
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

// Export to Excel (placeholder)
function exportToExcel(tableId, filename) {
    showNotification('Excel export funksiyasi tez orada qo\'shiladi', 'info');
}

// Print functionality
function printPage() {
    window.print();
}

// Document ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('AF IMPERIYA tizimi yuklandi ✅');
    
    // Initialize everything
    initDashboard();
    initTooltips();
    initPopovers();
    autoHideAlerts();
    
    // Animate counters on dashboard
    if (document.querySelector('.stat-value')) {
        initCounters();
    }
    
    // Form validations
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.dataset.originalText = submitBtn.innerHTML;
                setLoading(submitBtn, true);
            }
        });
    });
    
    // Add fade-in animation to all cards
    document.querySelectorAll('.card').forEach(card => {
        card.classList.add('fade-in');
    });
});

// Cleanup on page unload
window.addEventListener('beforeunload', function() {
    if (updateInterval) {
        clearInterval(updateInterval);
    }
});

// Expose functions globally
window.AF = {
    showNotification,
    validateForm,
    setLoading,
    smoothScrollTo,
    confirmAction,
    formatDate,
    exportToExcel,
    printPage,
    toggleDarkMode
};

