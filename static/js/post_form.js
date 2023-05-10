window.addEventListener('DOMContentLoaded', () => {
    const publishCheck = document.querySelector('input[name="published"]');
    const publishDate = document.querySelector('input[name="date_published"]');
    const archivedCheck = document.querySelector('input[name="archived"]');
    const archivedDate = document.querySelector('input[name="date_archive"]');
    const bodyField = document.querySelector('textarea[name="body"]');

    const buttonTextBold = document.querySelector('button#buttonTextBold');
    const buttonTextItalic = document.querySelector('button#buttonTextItalic');
    //const buttonTextUnderline = document.querySelector('button#buttonTextUnderline');
    const buttonTextImage = document.querySelector('button#buttonTextImage');
    const buttonTextHyperlink = document.querySelector('button#buttonTextHyperlink');

    const insertAtCursor = (myField, myValue) => {
        if (document.selection) {
            myField.focus();
            sel = document.selection.createRange();
            sel.text = myValue;
        }
        else if (myField.selectionStart || myField.selectionStart == '0') {
            var startPos = myField.selectionStart;
            var endPos = myField.selectionEnd;
            myField.value = myField.value.substring(0, startPos)
                + myValue
                + myField.value.substring(endPos, myField.value.length);
        } else {
            myField.value += myValue;
        }

        myField.focus();
    }

    buttonTextBold.onclick = () => insertAtCursor(bodyField, '**текст**');
    buttonTextItalic.onclick = () => insertAtCursor(bodyField, '*текст*');
    //buttonTextUnderline.onclick = () => insertText('**текст**');
    buttonTextImage.onclick = () => insertAtCursor(bodyField, '![опис фото](посилання на фото)');
    buttonTextHyperlink.onclick = () => insertAtCursor(bodyField, '[текст посилання](посилання)');


    const publishDateDisable = e => publishDate.disabled = e.checked;
    const arhivedDateDisable = e => archivedDate.disabled = e.checked;

    arhivedDateDisable(archivedCheck);
    publishDateDisable(publishCheck);

    archivedCheck.addEventListener('change', event => arhivedDateDisable(event.currentTarget));
    publishCheck.addEventListener('change', event => publishDateDisable(event.currentTarget));

    bodyField.focus();
});