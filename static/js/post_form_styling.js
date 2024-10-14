window.addEventListener('DOMContentLoaded', () => {
    const bodyField = document.querySelector('textarea[name="body"]');

    const wrapCursor = (textarea, before, after) => {
        let startPos = textarea.selectionStart;
        let endPos = textarea.selectionEnd;
        let textBeforeCursor = textarea.value.substring(0, startPos);
        let textAfterCursor = textarea.value.substring(endPos, textarea.value.length);
        let wrappedText = before + textarea.value.substring(startPos, endPos) + after;
        textarea.value = textBeforeCursor + wrappedText + textAfterCursor;
        let newCursorPos = startPos + before.length;
        textarea.setSelectionRange(newCursorPos, newCursorPos);
    }

    [...document.querySelectorAll('[data-sf-styling-pattern')].forEach(val => {
        const pattern = val.dataset.sfStylingPattern;
        const [before, after] = pattern.split('||');
        
        val.addEventListener('click', () => {
            wrapCursor(bodyField, before, after);
            bodyField.focus();
        });
    });
});