window.addEventListener('DOMContentLoaded', async () => {
    const postsChart = document.querySelector('#postsChart');
    const usersChart = document.querySelector('#usersChart');

    const fetchStats = async (apiRoute) => {
        return await fetch(apiRoute, {
            method: 'GET',
            headers: {
                'Authorization': 'Token ' + getCookie('token')
            }
        }).then(response => response.json());
    }

    await fetchStats(`${window.location.origin}/api/stats/posts`).then(data => {
        new Chart(
            postsChart,
            {
                type:'line',
                height: 240, 
                data: {
                    labels: data.map(row => row.date),
                    datasets: [
                        {
                            label: 'Публікації за день',
                            data: data.map(row => row.total)
                        }
                    ]
                },
                options: {
                    maintainAspectRatio: false,
                }
            }
        )
    });

    await fetchStats(`${window.location.origin}/api/stats/users`).then(data => {
        new Chart(
            usersChart,
            {
                type:'line',
                height: 240, 
                data: {
                    labels: data.map(row => row.date),
                    datasets: [
                        {
                            label: 'Реєстрації за день',
                            data: data.map(row => row.total)
                        }
                    ]
                },
                options: {
                    maintainAspectRatio: false,
                }
            }
        )
    });
});