fetch('disease_risk_sensors.json')
  .then(response => response.json())
  .then(sensorData => {
    const resultsDiv = document.getElementById('results');
    if (sensorData.length === 0) {
      resultsDiv.innerHTML = '<p>No sensors with disease risk detected.</p>';
    } else {
      sensorData.forEach(sensor => {
        const sensorDiv = document.createElement('div');
        sensorDiv.className = 'sensor';
        sensorDiv.innerHTML = `<strong>Sensor ${sensor.id}</strong>: pH=${sensor.pH}, turbidity=${sensor.turbidity}, microorganisms_count=${sensor.microorganisms_count}, rainfall=${sensor.rainfall}`;
        resultsDiv.appendChild(sensorDiv);
      });
    }
  });
