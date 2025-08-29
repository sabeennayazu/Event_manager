// Main JavaScript for Event Manager

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.classList.contains('show')) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('[href*="delete"], [action*="delete"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            if (!confirm('Are you sure you want to delete this item?')) {
                event.preventDefault();
            }
        });
    });

    // Calendar navigation
    const calendarNavButtons = document.querySelectorAll('.calendar-nav');
    calendarNavButtons.forEach(button => {
        button.addEventListener('click', function() {
            document.body.classList.add('loading');
        });
    });

    // Event card animations
    const eventCards = document.querySelectorAll('.event-card');
    eventCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // AJAX for marking attendance
    const markAttendedButtons = document.querySelectorAll('.mark-attended');
    markAttendedButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            const eventId = this.dataset.eventId;
            const button = this;
            
            // Add loading state
            button.disabled = true;
            const originalContent = button.innerHTML;
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            
            // Create form data with CSRF token
            const formData = new FormData();
            const csrfToken = getCsrfToken();
            
            fetch(`/event/${eventId}/mark-attended/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // Update button appearance
                    const icon = data.is_attended ? 'times' : 'check';
                    const color = data.is_attended ? 'warning' : 'success';
                    const text = data.is_attended ? 'Mark Not Attended' : 'Mark Attended';
                    
                    button.className = button.className.replace(/btn-outline-(success|warning)/, `btn-outline-${color}`);
                    button.innerHTML = `<i class="fas fa-${icon}"></i>`;
                    button.title = text;
                    
                    // Show success message
                    showAlert(data.message, 'success');
                    
                    // Update card appearance if it's in a card
                    const card = button.closest('.event-card');
                    if (card) {
                        if (data.is_attended) {
                            card.classList.add('attended');
                        } else {
                            card.classList.remove('attended');
                        }
                    }
                } else {
                    showAlert('Error updating attendance status', 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('Error updating attendance status. Please try again.', 'danger');
            })
            .finally(() => {
                button.disabled = false;
                if (button.innerHTML.includes('spinner')) {
                    button.innerHTML = originalContent;
                }
            });
        });
    });

    // Date input default to today for new events
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        if (!input.value && input.closest('form').querySelector('h3').textContent.includes('Add')) {
            const today = new Date().toISOString().split('T')[0];
            input.value = today;
        }
    });
});

// Utility functions
function getCsrfToken() {
    // Try multiple methods to get CSRF token
    let token = document.querySelector('[name=csrfmiddlewaretoken]');
    if (token) return token.value;
    
    // Try from cookie
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    
    // Try from meta tag
    const metaToken = document.querySelector('meta[name="csrf-token"]');
    if (metaToken) return metaToken.getAttribute('content');
    
    return '';
}

function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert after navbar
    const existingAlerts = alertContainer.querySelector('.alert');
    if (existingAlerts) {
        alertContainer.insertBefore(alert, existingAlerts);
    } else {
        alertContainer.insertBefore(alert, alertContainer.firstChild);
    }
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        if (alert.classList.contains('show')) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 5000);
}

// Calendar helper functions
function navigateCalendar(year, month) {
    const url = new URL(window.location);
    url.searchParams.set('view', 'month');
    url.searchParams.set('year', year);
    url.searchParams.set('month', month);
    window.location.href = url.toString();
}

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + N for new event
    if ((event.ctrlKey || event.metaKey) && event.key === 'n') {
        event.preventDefault();
        window.location.href = '/add/';
    }
    
    // Escape to go back
    if (event.key === 'Escape') {
        const backButton = document.querySelector('a[href*="event_list"], .btn-secondary');
        if (backButton) {
            backButton.click();
        }
    }
});

// Removed ServiceWorker registration to prevent console errors
