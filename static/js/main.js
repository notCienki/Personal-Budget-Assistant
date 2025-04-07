// Basic JavaScript functionality for Budget Assistant

document.addEventListener('DOMContentLoaded', function() {
    // Format currency amounts
    const formatCurrency = (amount, currency = 'PLN') => {
        return new Intl.NumberFormat('pl-PL', {
            style: 'currency',
            currency: currency
        }).format(amount);
    };

    // Format dates to local format
    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('pl-PL');
    };

    // Apply formatting to currency elements if they exist
    const currencyElements = document.querySelectorAll('.currency');
    if (currencyElements) {
        currencyElements.forEach(element => {
            const amount = parseFloat(element.textContent);
            const currency = element.dataset.currency || 'PLN';
            if (!isNaN(amount)) {
                element.textContent = formatCurrency(amount, currency);
            }
        });
    }

    // Format date elements if they exist
    const dateElements = document.querySelectorAll('.date-format');
    if (dateElements) {
        dateElements.forEach(element => {
            const dateString = element.textContent;
            if (dateString) {
                element.textContent = formatDate(dateString);
            }
        });
    }
});
