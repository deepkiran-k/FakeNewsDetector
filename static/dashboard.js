$(document).ready(function () {
    // Fetch data from the backend
    fetch('/dashboard-data')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
                $('#total-articles').text('Error loading data');
                return;
            }

            // Display Total Articles
            $('#total-articles').text(data.total_articles);

            // Render Verdict Distribution Chart
            const verdictCtx = document.getElementById('verdictChart').getContext('2d');
            const verdictLabels = data.verdict_data.map(item => item.verdict);
            const verdictPercentages = data.verdict_data.map(item => item.percentage);

            new Chart(verdictCtx, {
                type: 'pie',
                data: {
                    labels: verdictLabels,
                    datasets: [{
                        label: 'Verdict Distribution',
                        data: verdictPercentages,
                        backgroundColor: ['#f44336','#4caf50', '#ffeb3b'], // Red, Green, Yellow
                    }]
                }
            });

            // Render Trends Chart
            const trendsCtx = document.getElementById('trendsChart').getContext('2d');
            const trendsLabels = data.trends_data.map(item => item.search_query);
            const trendsFrequencies = data.trends_data.map(item => item.frequency);

            new Chart(trendsCtx, {
                type: 'bar',
                data: {
                    labels: trendsLabels,
                    datasets: [{
                        label: 'Common False Claims',
                        data: trendsFrequencies,
                        backgroundColor: '#2196f3' // Blue
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Search Queries'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Frequency'
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching dashboard data:', error));
});