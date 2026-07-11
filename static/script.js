document.addEventListener('DOMContentLoaded', async () => {
    const cropSelect = document.getElementById('crop');
    const yearSelect = document.getElementById('year');
    const varietySelect = document.getElementById('variety');
    const stateSelect = document.getElementById('state');
    const seasonSelect = document.getElementById('season');
    const zoneSelect = document.getElementById('zone');
    
    const form = document.getElementById('prediction-form');
    const btnLoader = document.getElementById('btn-loader');
    const predictSpan = form.querySelector('.predict-btn span');
    const resultContainer = document.getElementById('result-container');
    const predictionValue = document.getElementById('prediction-value');
    const aiInsight = document.getElementById('ai-insight');

    // Fetch Metadata
    try {
        const response = await fetch('/api/metadata');
        const data = await response.json();
        
        const populateSelect = (selectElem, optionsList, placeholder) => {
            selectElem.innerHTML = `<option value="" disabled selected>${placeholder}</option>`;
            optionsList.forEach(optVal => {
                const opt = document.createElement('option');
                opt.value = optVal;
                opt.textContent = optVal;
                selectElem.appendChild(opt);
            });
        };

        if (data.crops) populateSelect(cropSelect, data.crops, 'Select Crop');
        if (data.years) populateSelect(yearSelect, data.years, 'Select Year');
        if (data.varieties) populateSelect(varietySelect, data.varieties, 'Select Variety');
        if (data.states) populateSelect(stateSelect, data.states, 'Select State');
        if (data.seasons) populateSelect(seasonSelect, data.seasons, 'Select Season');
        if (data.zones) populateSelect(zoneSelect, data.zones, 'Select Recommended Zone');
        
    } catch (error) {
        console.error("Error fetching metadata:", error);
    }

    // Handle Form Submit
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Show loader
        btnLoader.style.display = 'block';
        predictSpan.textContent = 'Analyzing...';
        resultContainer.classList.remove('show');
        
        const payload = {
            crop: cropSelect.value,
            year: yearSelect.value,
            variety: varietySelect.value,
            state: stateSelect.value,
            season: seasonSelect.value,
            zone: zoneSelect.value,
            cost: document.getElementById('cost').value,
            area: document.getElementById('area').value,
            yield: document.getElementById('yield').value
        };

        try {
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            
            const data = await response.json();
            
            if (response.ok && data.prediction !== undefined) {
                // Formatting number with commas
                const formattedNum = parseFloat(data.prediction).toLocaleString('en-IN', {
                    maximumFractionDigits: 2
                });
                
                predictionValue.textContent = formattedNum;
                
                if (data.insight) {
                    aiInsight.innerHTML = data.insight;
                    aiInsight.style.display = 'block';
                } else {
                    aiInsight.style.display = 'none';
                }

                document.getElementById('default-guide').style.display = 'none';
                resultContainer.classList.add('show');
                
                // Small animation
                predictionValue.style.transform = 'scale(1.2)';
                setTimeout(() => {
                    predictionValue.style.transform = 'scale(1)';
                    predictionValue.style.transition = 'transform 0.3s ease';
                }, 300);
            } else {
                alert(data.error || "An error occurred during prediction.");
            }
        } catch (error) {
            console.error("Error during prediction:", error);
            alert("Failed to connect to the prediction server.");
        } finally {
            // Hide loader
            btnLoader.style.display = 'none';
            predictSpan.textContent = 'Forecast Production';
        }
    });
});
