// https://stackoverflow.com/questions/10420352/converting-file-size-in-bytes-to-human-readable-string
const humanFileSize = (size) => {
    var i = size == 0 ? 0 : Math.floor(Math.log(size) / Math.log(1024));
    return (size / Math.pow(1024, i)).toFixed(2) * 1 + ' ' + ['B', 'kB', 'MB', 'GB', 'TB'][i];
}

const showFilesInfo = (data, downloadPrefix) => {
    const modal = document.querySelector('#fileDataModal');
    const modalInstance = new bootstrap.Modal(modal);

    const modalTitle = modal.querySelector('.modal-title');
    const modalBody = modal.querySelector('.modal-body');

    const fileName = modalBody.querySelector('#fileName');
    const fileSize = modalBody.querySelector('#fileSize');
    const fileDate = modalBody.querySelector('#fileDate');
    const uploader = modalBody.querySelector('#author');

    const downloadButton = modal.querySelector('#downloadButton');
    downloadButton.href = downloadPrefix + data.file_path;
    downloadButton.addEventListener('click', () => setTimeout(() => modalInstance.hide(), 250));
    downloadButton.download = data.file_name;

    modalTitle.textContent = data.file_name;
    fileName.textContent = data.file_name;
    fileSize.textContent = humanFileSize(data.file_size);
    fileDate.textContent = new Date(data.date_created).toLocaleDateString();

    uploader.href = '/profile/detail/' + data.uploader.id;
    uploader.textContent = data.uploader.username;

    modalInstance.show();
}

const generateListItem = (data, files_list) => {
    const li = document.createElement('li');
    li.classList.add('list-group-item', 'd-flex');

    const icon = document.createElement('i');
    icon.classList.add('bi', 'bi-paperclip', 'flex-grow-1');

    const link = document.createElement('a');
    link.textContent = data.file_name;
    link.href = '#';
    link.addEventListener('click', () => showFilesInfo(data, files_list.dataset.sfFiles));

    icon.appendChild(link);
    li.appendChild(icon);

    const span = document.createElement('span');
    span.classList.add('flex-shrink-0');

    const eyeLink = document.createElement('a');
    eyeLink.href = '#';
    eyeLink.addEventListener('click', () => showFilesInfo(data, files_list.dataset.sfFiles));

    const eyeIcon = document.createElement('i');
    eyeIcon.classList.add('bi', 'bi-eye', 'me-2');
    eyeLink.appendChild(eyeIcon);

    const downloadLink = document.createElement('a');
    downloadLink.href = files_list.dataset.sfFiles + data.file_path;
    downloadLink.download = data.file_name;

    const downloadIcon = document.createElement('i');
    downloadIcon.classList.add('bi', 'bi-download');
    downloadLink.appendChild(downloadIcon);

    span.appendChild(eyeLink);
    span.appendChild(downloadLink);

    li.appendChild(span);

    files_list.appendChild(li);
}

window.addEventListener('DOMContentLoaded', async () => {
    const card = document.querySelector('[data-sf-post]');
    const files_list = document.querySelector('[data-sf-files]');
    const post_id = card.dataset.sfPost;

    await fetch(`/api/post/${post_id}/files`, {
        method: 'GET',
        headers: {
            'Authorization': 'Token ' + getCookie('token')
        }
    }).then(
        response => response.json()
    ).then(data => {
        files_list.innerHTML = "";
        data.forEach(file => 
            generateListItem(file, files_list)
        );
    });
});