$(document).ready(function () {
    $('#optionChronological').on('click', function () {
        $('#chronological-section').show();
        $('#stats-section').hide();
    });

    $('#optionScore').on('click', function () {
        $('#chronological-section').hide();
        $('#stats-section').show();

        // Fetch and render stats data if not already loaded
        if (!$('#total-articles').text().trim().toLowerCase().includes('loading')) return;
        fetch('/dashboard-data')
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error(data.error);
                    return;
                }

                // Display Total Articles
                $('#total-articles').text(data.total_articles);

                // Render Verdict Chart (Pie Chart)
                const verdictCtx = document.getElementById('verdictChart').getContext('2d');
                const verdictLabels = data.verdict_data.map(item => item.verdict);
                const verdictPercentages = data.verdict_data.map(item => item.percentage);

                new Chart(verdictCtx, {
                    type: 'pie',
                    data: {
                        labels: verdictLabels,
                        datasets: [{
                            label: '% of Verdicts',
                            data: verdictPercentages,
                            backgroundColor: ['#f44336','#4caf50', '#ffeb3b'], // Green, Red, Yellow
                        }]
                    },
                    options: {
                        responsive: false, // Disable responsiveness to respect fixed dimensions
                    }
                });

                // Render Trends Chart (Bar Chart)
                const trendsCtx = document.getElementById('trendsChart').getContext('2d');
                const trendsLabels = data.trends_data.map(item => item.search_query);
                const trendsFrequencies = data.trends_data.map(item => item.frequency);

                new Chart(trendsCtx, {
                    type: 'bar',
                    data: {
                        labels: trendsLabels,
                        datasets: [{
                            label: 'Frequency of False Claims',
                            data: trendsFrequencies,
                            backgroundColor: '#2196f3' // Blue
                        }]
                    },
                    options: {
                        responsive: false, // Disable responsiveness to respect fixed dimensions
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
});