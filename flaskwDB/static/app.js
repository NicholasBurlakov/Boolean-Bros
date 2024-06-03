document.addEventListener('DOMContentLoaded', function() {
        const parkingGrid = document.getElementById('parking-grid');
        const reserveButton = document.getElementById('reserve-button');
        let selectedSpot = null;

        // Generate parking spots
        for (let i = 1; i <= 50; i++) {
            const spot = document.createElement('div');
            spot.classList.add('spot', 'available');
            spot.textContent = `Spot ${i}`;
            spot.dataset.spotId = i;
            spot.addEventListener('click', function() {
                if (spot.classList.contains('reserved')) return;
                if (selectedSpot) {
                    selectedSpot.classList.remove('selected');
                }
                selectedSpot = spot;
                spot.classList.add('selected');
            });
            parkingGrid.appendChild(spot);
        }

        reserveButton.addEventListener('click', function() {
            if (!selectedSpot) {
                alert('Please select a spot to reserve.');
                return;
            }
            const spotId = selectedSpot.dataset.spotId;
            const parkingLotId = 1;  // Default parking lot ID
            const vehicleId = 1;  // Default vehicle ID

            const now = new Date();
            const endT = new Date(now.getTime() + 4 * 60 * 60 * 1000);  // + 4 hours from now

            const startTime = now.toISOString().slice(0, 19).replace('T', ' ');
            const endTime = endT.toISOString().slice(0, 19).replace('T', ' ');

            //Send the json for the database to read
            fetch('/reserve', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    spot_id: spotId,
                    parking_lot_id: parkingLotId,
                    vehicle_id: vehicleId,
                    start_time: startTime,
                    end_time: endTime
                }),
            })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    selectedSpot.classList.remove('selected');
                    selectedSpot.classList.add('reserved');
                    selectedSpot = null;
                });
        });
    });