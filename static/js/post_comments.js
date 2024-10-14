async function deleteComment(comment_id, element) {
    const response = await fetch(`/api/comment/${comment_id}`, {
        method: 'DELETE',
        headers: {
            'Authorization': 'Token ' + getCookie('token')
        }
    });

    if (response.status == 200) {
        element.remove();
    }
}

async function postComment(body, container){
    const response = await fetch(`/api/comment/${body.post_id}/`, {
        method: 'POST',
        headers: {
            'Authorization': 'Token ' + getCookie('token'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(body)
    });

    if (response.status == 201) {
        const comment = await response.json();
        const comment_container = document.querySelector(`#comments_${comment.post_id}`);
        const comment_div = createComment(comment, body.author_id, body.user_id);
        container.appendChild(comment_div);
    }
}

function createComment(comment, author_id, user_id) {
    const div = document.createElement('div');
    div.className = 'list-group-item';
    div.id = `comment_${comment.id}`;

    const innerDiv = document.createElement('div');
    innerDiv.className = 'd-flex w-100 justify-content-between';

    const h5 = document.createElement('h5');
    h5.className = 'mb-1';
    h5.textContent = comment.body;

    if (author_id == user_id || comment.author.id == user_id) {
        const deleteLink = document.createElement('a');
        deleteLink.href = '#';
        deleteLink.onclick = () => deleteComment(comment.id, div);
        deleteLink.className = 'fs-6 text fst-light ms-1';
        const trashIcon = document.createElement('i');
        trashIcon.className = 'bi bi-trash-fill';
        deleteLink.appendChild(trashIcon);
        deleteLink.appendChild(document.createTextNode('Видалити'));
        h5.appendChild(deleteLink);
    }

    const small = document.createElement('small');
    small.textContent = new Date(comment.date_created).toLocaleDateString();

    const authorLink = document.createElement('a');
    authorLink.href = `/profile/detail/${comment.author.id}`;
    authorLink.textContent = `@${comment.author.username}`;

    div.appendChild(innerDiv);
    innerDiv.appendChild(h5);
    innerDiv.appendChild(small);
    div.appendChild(document.createElement('small').appendChild(authorLink));

    return div;
}

window.addEventListener('DOMContentLoaded', async () => {
    const card = document.querySelector('[data-sf-post]');
    const post_id = card.dataset.sfPost;
    const author_id = card.dataset.sfAuthor;
    const user_id = getCookie('user_id');
    const comments_container = card.querySelector('#comments');
    const comment_form = card.querySelector('#commentForm');

    await fetch(`/api/post/${post_id}/comments`, {
        method: 'GET',
        headers: {
            'Authorization': 'Token ' + getCookie('token')
        }
    }).then(
        response => {
            comments_container.innerHTML = "";
            return response.json();
        }
    ).then(
        data => data.forEach(element =>
            comments_container.appendChild(createComment(element, author_id, user_id))
        )
    );

    if (!comment_form) return;

    comment_form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const body = {
            post_id: post_id,
            body: event.target.body.value,
        };

        await postComment(body, comments_container);
        event.target.reset();
    });
});