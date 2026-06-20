// Seat Selection Map Logic

document.addEventListener('DOMContentLoaded', function() {
    const seatContainer = document.getElementById('seatMapContainer');
    if (!seatContainer) return;

    const selectedSeatInput = document.getElementById('selectedSeatInput');
    const displaySelectedSeat = document.getElementById('displaySelectedSeat');
    const submitBookingBtn = document.getElementById('submitBookingBtn');
    
    // Parse occupied seats from data attribute (injected by backend)
    const occupiedSeats = JSON.parse(seatContainer.dataset.occupied || '[]');
    const totalSeats = parseInt(seatContainer.dataset.capacity || '60');
    
    // Number of rows (assume 6 seats per row: A, B, C, D, E, F)
    const seatsPerRow = 6;
    const numRows = Math.ceil(totalSeats / seatsPerRow);
    const seatLetters = ['A', 'B', 'C', 'D', 'E', 'F'];
    
    let selectedSeat = null;

    // Draw the seat map
    for (let r = 1; r <= numRows; r++) {
        const rowDiv = document.createElement('div');
        rowDiv.className = 'seat-row';
        
        // Row label
        const rowNumLabel = document.createElement('div');
        rowNumLabel.className = 'row-number';
        rowNumLabel.textContent = r;
        rowDiv.appendChild(rowNumLabel);
        
        // Seat buttons
        for (let s = 0; s < seatsPerRow; s++) {
            // Add aisle space after index 2 (between C and D)
            if (s === 3) {
                const aisle = document.createElement('div');
                aisle.className = 'aisle';
                rowDiv.appendChild(aisle);
            }
            
            const seatIndex = (r - 1) * seatsPerRow + s;
            if (seatIndex >= totalSeats) break; // Don't exceed total capacity
            
            const seatNumber = `${r}${seatLetters[s]}`;
            const seatButton = document.createElement('div');
            seatButton.className = 'seat';
            seatButton.textContent = seatLetters[s];
            seatButton.dataset.seat = seatNumber;
            
            // Check if seat is booked/occupied
            if (occupiedSeats.includes(seatNumber)) {
                seatButton.classList.add('occupied');
                seatButton.title = `Seat ${seatNumber} - Occupied`;
            } else {
                seatButton.title = `Seat ${seatNumber} - Available`;
                
                // Click handler for selection
                seatButton.addEventListener('click', function() {
                    // Remove selection from previous seat
                    const previousSelected = seatContainer.querySelector('.seat.selected');
                    if (previousSelected) {
                        previousSelected.classList.remove('selected');
                    }
                    
                    if (selectedSeat === seatNumber) {
                        // Toggle off
                        selectedSeat = null;
                        this.classList.remove('selected');
                        displaySelectedSeat.textContent = 'None';
                        selectedSeatInput.value = '';
                        submitBookingBtn.disabled = true;
                    } else {
                        // Select new
                        selectedSeat = seatNumber;
                        this.classList.add('selected');
                        displaySelectedSeat.textContent = seatNumber;
                        selectedSeatInput.value = seatNumber;
                        submitBookingBtn.disabled = false;
                    }
                });
            }
            
            rowDiv.appendChild(seatButton);
        }
        
        seatContainer.appendChild(rowDiv);
    }
});
