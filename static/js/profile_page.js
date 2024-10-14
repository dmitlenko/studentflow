window.addEventListener('DOMContentLoaded', () => {
    const profile_id = document.querySelector('[data-sf-profile]').dataset.sfProfile;
    const following_button = document.querySelector('[data-sf-following]');

    following_button.addEventListener('click', async () => {
        let is_following = following_button.dataset.sfFollowing == 'true';
        let value = following_button.querySelector('.value');

        await fetch(`/api/follow/${profile_id}/`, {
            method: is_following ? 'DELETE' : 'POST',
            headers: {
                'Authorization': 'Token ' + getCookie('token')
            }
        }).then(
            response => {
                const classToAdd = is_following ?  'btn-outline-secondary': 'btn-secondary';
                const classToRemove = is_following ? 'btn-secondary' : 'btn-outline-secondary';

                following_button.classList.remove(classToRemove);
                following_button.classList.add(classToAdd);

                following_button.setAttribute('data-sf-following', !is_following);

                value.textContent = !is_following ? 'Відписатися' : 'Підписатися';

                const icon = following_button.querySelector('i.bi');
                if (icon) {
                    const personFillDash = 'bi-person-fill-dash';
                    const personFillAdd = 'bi-person-fill-add';
                    icon.classList.add(is_following ? personFillAdd : personFillDash);
                    icon.classList.remove(is_following ? personFillDash : personFillAdd);
                }
            }
        );
    });
});