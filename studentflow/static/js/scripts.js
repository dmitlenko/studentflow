window.addEventListener('DOMContentLoaded', () => {
    const savedTheme = getCookie('theme');
    const themeList = document.querySelector('#themeList');
    const selectThemeButton = document.querySelector('#selectThemeButton');

    let selectedTheme = savedTheme ? savedTheme : 'default';

    if (!savedTheme) setCookie('theme', 'default', 365);

    if (!themeList || !selectThemeButton) return;

    [...themeList.children].forEach(listItem => {
        listItem.addEventListener('click', () => {
            [...themeList.children].forEach(el => 
                el.classList.remove('active')
            )

            listItem.classList.add('active');
            selectedTheme = listItem.dataset.themeName;
        });
    });

    selectThemeButton.addEventListener('click', () => {
        setCookie('theme', selectedTheme, 365);
        document.location.reload();
    });
});
