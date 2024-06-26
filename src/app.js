// Define the state of parking lots and their respective spots
const parkingLots = [
  { lotId: 'Catalyst Lot', spots: 20 },
  { lotId: 'Downtown Lot', spots: 20 },
  { lotId: 'Cheney Lot', spots: 40 }
];

// State for the individual spots
const allSpots = [];

// Initialize parking spots dynamically for each lot
parkingLots.forEach(lot => {
  for (let i = 1; i <= lot.spots; i++) {
    allSpots.push({
      lotId: lot.lotId,
      spotNumber: i,
      reserved: false,
      selected: false
    });
  }
});

// Function to render all parking lots and their spots
function renderParkingLots(filter = '') {
  const mainContainer = document.querySelector('main');
  mainContainer.innerHTML = ''; // Clear the container first

  const filteredLots = parkingLots.filter(lot => lot.lotId.toLowerCase().includes(filter.toLowerCase()));

  filteredLots.forEach(lot => {
    const section = document.createElement('section');
    section.className = 'lot-section';
    section.id = lot.lotId.replace(' ', '-').toLowerCase();
    section.innerHTML = `<h2>${lot.lotId}</h2><div class="grid"></div>`;
    
    
    const grid = section.querySelector('.grid');

    // section.addEventListener('click', (event) => {
    //   if (event.target === section || event.target.tagName === 'H2') {
    //     grid.style.display = grid.style.display === 'none' ? 'grid' : 'none';
    //   }
    // });

    allSpots.filter(spot => spot.lotId === lot.lotId).forEach((spot, index) => {
      const spotElement = document.createElement('div');
      spotElement.className = 'spot ' + (spot.reserved ? 'reserved' : spot.selected ? 'selected' : 'available');
      spotElement.textContent = `Spot ${spot.spotNumber}`;
      spotElement.addEventListener('click', (event) => {
        toggleSingleSelection(spot, event);
        event.stopPropagation(); // This stops the click event from bubbling up to the section
      });
      grid.appendChild(spotElement);
    });

    mainContainer.appendChild(section);
  });

  // Append reservation section at the end
  const reservationSection = document.createElement('section');
  reservationSection.id = 'reservation-section';
  reservationSection.innerHTML = `<button id="reserve-button">Reserve</button>`;
  mainContainer.appendChild(reservationSection);
  document.getElementById('reserve-button').addEventListener('click', reserveSelected);
}



function toggleSingleSelection(spot, event) {
  if (!spot.reserved) {
    // Deselect all spots before selecting the new one
    allSpots.forEach(s => {
      if (s !== spot) s.selected = false;
    });
    spot.selected = !spot.selected;  // Toggle the selection state of the clicked spot
    renderParkingLots(); // Re-render to reflect the updated selection
  }
  // Prevent the click from bubbling up to the lot header
  event.stopPropagation();
}


// Function to reserve the selected spot
function reserveSelected(event) {
  allSpots.forEach(spot => {
    if (spot.selected) {
      spot.reserved = true;
      spot.selected = false;
    }
  });
  renderParkingLots(); // Re-render to reflect the reservation
  event.stopPropagation(); // Stop propagation here
}


// Search functionality
function setupSearch() {
  const header = document.querySelector('header');
  const searchInput = document.createElement('input');
  searchInput.placeholder = 'Search for a lot...';
  searchInput.oninput = () => renderParkingLots(searchInput.value);

  // Target the first child element of the header
  const firstChild = header.append;
  
  // Insert the search input after the first child
  if (firstChild.nextElementSibling) {
    // If there is a second child, insert before it
    header.insertBefore(searchInput, firstChild.nextElementSibling);
  } else {
    // If there is no second child, append at the end
    header.appendChild(searchInput);
  }
}

function scaleGrid(grid, scale) {
  const currentTransform = grid.style.transform || 'scale(1)';
  const match = /scale\(([^)]+)\)/.exec(currentTransform);
  const currentScale = match ? parseFloat(match[1]) : 1;
  grid.style.transform = `scale(${currentScale * scale})`;
}

document.addEventListener('DOMContentLoaded', function() {
  // Always set up the menu toggle
  const menuToggle = document.querySelector('.menu-toggle');
  const navList = document.querySelector('.nav-list');
  const searchInput = document.querySelector('.search-input');
  if (searchInput) {
    searchInput.oninput = () => renderParkingLots(searchInput.value);
  }

  menuToggle.addEventListener('click', function() {
    // Toggle display based on current state
    if (navList.style.display === 'block') {
      navList.style.display = 'none';
    } else {
      navList.style.display = 'block';
    }
  });

  // Get the current page's URL
  const currentPage = window.location.pathname;

  // Check if the current page is 'availability.html'
  if (currentPage.match(/availability\.html$/) || currentPage.match(/userAvailability\.html$/)) {
    renderParkingLots();
    // setupSearch();
  }
});

const urlParams = new URLSearchParams(window.location.search);
const username = urlParams.get('username');

const userProfileLink = document.getElementById('userProfileLink');
userProfileLink.textContent = "Hello, " + username;

const username_ = document.getElementById('username');
username_.textContent = username;

function userAbout() {
  window.location.href = `userAbout.html?username=${encodeURIComponent(username)}`;
}
function userServices() {
  window.location.href = `userServices.html?username=${encodeURIComponent(username)}`;
}
function userAvailability() {
  window.location.href = `userAvailability.html?username=${encodeURIComponent(username)}`;
}
function userProfile() {
  window.location.href = `userProfile.html?username=${encodeURIComponent(username)}`;
}
function userIndex() {
  window.location.href = `userIndex.html?username=${encodeURIComponent(username)}`;
}
