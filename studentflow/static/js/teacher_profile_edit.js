window.addEventListener('DOMContentLoaded', () => {
    const form = document.forms['userform'];
    const list = form.querySelector('#review_topics');
    const topicList = form.querySelectorAll('li[data-sf-topic]');
    const topicsSelect = form.elements['review_topics'];
    const errorMessage = topicsSelect.parentElement.querySelector('.invalid-feedback');

    [...topicList].forEach((topic) => {
        const countSpan = topic.querySelector('span');
        const checkBox = topic.querySelector('input[type=checkbox]');

        checkBox.setAttribute('data-sf-initial-checked', checkBox.checked);

        checkBox.addEventListener('change', (e) => {
            const option = [...topicsSelect.options].find((option) => option.value == checkBox.value);
            const initialValue = checkBox.dataset.sfInitialChecked == 'true' ? 1 : -1;
            const increment = e.target.checked ? initialValue : -initialValue;
            const updatedValue = parseInt(countSpan.textContent) + increment;

            option.selected = e.target.checked;

            countSpan.textContent = updatedValue;
            option.setAttribute('data-sf-reviewers', updatedValue);
            
            if (updatedValue == 0) {
                countSpan.classList.remove('bg-primary');
                countSpan.classList.add('bg-danger');
            } else {
                countSpan.classList.remove('bg-danger');
                countSpan.classList.add('bg-primary');
            }
        });
    });

    form.addEventListener('submit', (e) => {
        [...topicsSelect.options].forEach((option) => {
            if (!option.selected && option.dataset.sfReviewers == 0) {
                errorMessage.style.display = 'block';
                list.classList.add('is-invalid');
                list.focus();
                e.preventDefault();
            }
        });
    });
});