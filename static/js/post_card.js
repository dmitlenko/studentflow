document.addEventListener('DOMContentLoaded', function() {
    [...document.getElementsByClassName('post-card')].forEach(card => {
        const post_id = card.dataset.sfPost;
        const like_button = card.querySelector('[data-sf-likes]');
        const view_button = card.querySelector('[data-sf-views]');
        const read_button = card.querySelector(`[href="/post/detail/${post_id}"]`);

        like_button.addEventListener('click', async () => {
            let is_liked = like_button.dataset.sfLiked == 'true';
            let value = like_button.querySelector('.value');

            await fetch(`/api/like/${post_id}/`, {
                method: is_liked ? 'DELETE' : 'POST',
                headers: {
                    'Authorization': 'Token ' + getCookie('token')
                }
            }).then(
                response => {
                    const classToAdd = is_liked ? 'btn-danger' : 'btn-outline-danger';
                    const classToRemove = is_liked ? 'btn-outline-danger' : 'btn-danger';

                    like_button.classList.remove(classToRemove);
                    like_button.classList.add(classToAdd);

                    const currentLikes = parseInt(like_button.dataset.sfLikes);
                    const updatedLikes = currentLikes + (is_liked ? -1 : 1);

                    like_button.setAttribute('data-sf-likes', updatedLikes);
                    like_button.setAttribute('data-sf-liked', !is_liked);

                    value.textContent = updatedLikes == 0 ? '' : updatedLikes;

                    const heartIcon = like_button.querySelector('i.bi');
                    if (heartIcon) {
                        const filledHeartClass = 'bi-heart-fill';
                        const emptyHeartClass = 'bi-heart';
                        heartIcon.classList.add(is_liked ? emptyHeartClass : filledHeartClass);
                        heartIcon.classList.remove(is_liked ? filledHeartClass : emptyHeartClass);
                    }
                }
            );
        });

        read_button.addEventListener('click', () => {
            const views_value = view_button.querySelector('.value');

            if (!view_button.dataset.sfViewed == 'true'){
                views_value.textContent = parseInt(view_button.dataset.sfViews) + 1;
            }
        });
    });
});