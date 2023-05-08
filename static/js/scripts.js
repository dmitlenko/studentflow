function getCookie(name) {
    const cookieArr = document.cookie.split(';');
    for (let i = 0; i < cookieArr.length; i++) {
        const cookiePair = cookieArr[i].split('=');
        if (name === cookiePair[0].trim()) {
            return decodeURIComponent(cookiePair[1]);
        }
    }
    return null;
}

function setCookie(name, value, days) {
    let expires = '';
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = `; expires=${date.toUTCString()}`;
    }
    document.cookie = `${name}=${encodeURIComponent(value)}${expires}; path=/`;
}

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
