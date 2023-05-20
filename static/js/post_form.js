window.addEventListener('DOMContentLoaded', () => {
    const publishCheck = document.querySelector('input[name="published"]');
    const publishDate = document.querySelector('input[name="date_published"]');
    const archivedCheck = document.querySelector('input[name="archived"]');
    const archivedDate = document.querySelector('input[name="date_archive"]');

    const publishDateDisable = e => publishDate.disabled = e.checked;
    const arhivedDateDisable = e => archivedDate.disabled = e.checked;

    arhivedDateDisable(archivedCheck);
    publishDateDisable(publishCheck);

    archivedCheck.addEventListener('change', event => arhivedDateDisable(event.currentTarget));
    publishCheck.addEventListener('change', event => publishDateDisable(event.currentTarget));
});