window.addEventListener('DOMContentLoaded', () => {
    const approveButton = document.querySelector('#approveButton');
    let selectedPost = 0, 
        selectedRow = null;

    document.querySelectorAll('[data-sf-post]').forEach(val => {
        val.querySelector('.publish-button').addEventListener('click', e => {
            selectedPost = val.dataset.sfPost;
            selectedRow = val;
        });
    });

    approveButton.addEventListener('click', async () => {
        if (!selectedPost) return;

        await fetch(`/api/post/${selectedPost}/approve`, {
            method: 'POST',
            headers: {
                'Authorization': 'Token ' + getCookie('token')
            }
        }).then(
            response => {
                if (response.status == 200) {
                    selectedRow.remove();
                    alert('Оголошення було опубліковане');
                }
            }
        ).then(() => {
            [...document.querySelectorAll('tr[data-sf-post]')].forEach((val, i) => {
                val.querySelector('td[scope="row"]').textContent = i + 1;
            });
        });
    });
});
