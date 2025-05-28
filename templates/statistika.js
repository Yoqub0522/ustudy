<canvas id="userChart"></canvas>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
fetch('/api/user-stats/')
  .then(response => response.json())
  .then(data => {
    const ctx = document.getElementById('userChart').getContext('2d');

    const labels = data.last_7_days.map(item => item.date);
    const counts = data.last_7_days.map(item => item.count);

    new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Ro‘yxatdan o‘tgan foydalanuvchilar (so‘nggi 7 kun)',
          data: counts,
          borderColor: 'blue',
          backgroundColor: 'lightblue',
          fill: true,
        }]
      }
    });
  });
</script>
