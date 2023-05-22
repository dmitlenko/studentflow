window.addEventListener('DOMContentLoaded', () => {
    const form = document.forms['userform'];
    const topicsSelect = form.elements['review_topics'];
    const errorMessage = topicsSelect.parentElement.querySelector('.invalid-feedback')

    form.addEventListener('submit', (e) => {
        [...topicsSelect.options].forEach((option) => {
            if (!option.selected && option.dataset.sfReviewers == 0) {
                errorMessage.style.display = 'block';
                topicsSelect.classList.add('is-invalid');
                topicsSelect.focus();
                e.preventDefault();
            }
        });
    });
});