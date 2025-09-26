


function getRandomValue(min, max) {
  return (Math.random() * (max - min) + min).toFixed(2);
}


function sendMultipleRandomPredictions() {
  const placeNames = [
    "Ziro Valley, Arunachal Pradesh",
    "Khonoma Village, Nagaland",
    "Wokha, Nagaland",
    "Mawlynnong, Meghalaya",
    "Dampa Hills, Mizoram"
  ];
  const numSensors = placeNames.length;
  const sensors = [];
  // Randomly select one sensor to be the guaranteed 'No Disease Risk' sensor
  const noRiskIndex = Math.floor(Math.random() * numSensors);
  for (let i = 0; i < numSensors; i++) {
    if (i === noRiskIndex) {
      // Guaranteed no risk values (all set to lowest risk)
      sensors.push({
        name: placeNames[i],
        sensor1: 7.0, // pH (neutral)
        sensor2: 0,   // turbidity (lowest)
        sensor3: 0,   // microorganisms_count (lowest)
        sensor4: 0,   // rainfall (lowest)
        chlorine: 2.0 // chlorine content (highest, safest)
      });
    } else {
      sensors.push({
        name: placeNames[i],
        sensor1: getRandomValue(6.0, 9.0), // pH
        sensor2: getRandomValue(0, 100),   // turbidity
        sensor3: Math.floor(getRandomValue(0, 100)), // microorganisms_count
        sensor4: getRandomValue(0, 200),   // rainfall
        chlorine: getRandomValue(0.1, 2.0) // chlorine content (random)
      });
    }
  }
  // Predict for all sensors in parallel
  Promise.all(sensors.map(sensor =>
    fetch('/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
  sensor1: sensor.sensor1,
  sensor2: sensor.sensor2,
  sensor3: sensor.sensor3,
  sensor4: sensor.sensor4,
  chlorine: sensor.chlorine
      })
    })
    .then(response => response.json())
    .then(data => ({...sensor, result: data.result}))
    .catch(() => ({...sensor, result: 'Error'}))
  ))
  .then(results => {
    const resultsDiv = document.getElementById('results');
    const now = new Date();
    const timestamp = now.toLocaleTimeString();
    let html = `<p>Latest Sensor Predictions: <br><small>Timestamp: ${timestamp}</small></p><ul>`;
    results.forEach(sensor => {
      html += `<li><strong>${sensor.name}</strong>: <span style=\"color:${sensor.result==='Disease Risk'?'red':'green'}\">${sensor.result}</span><br>
      <small>pH: ${sensor.sensor1}, Turbidity: ${sensor.sensor2}, Microorganisms: ${sensor.sensor3}, Rainfall: ${sensor.sensor4}, Chlorine: ${sensor.chlorine}</small></li>`;
    });
    html += '</ul>';
    resultsDiv.innerHTML = html;
  });
}

// Run every 5 seconds
sendMultipleRandomPredictions(); // Initial call
setInterval(sendMultipleRandomPredictions, 5000);
