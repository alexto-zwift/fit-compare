// Check if app element exists before manipulating it
const appElement = document.getElementById("app");
if (appElement) {
  appElement.innerHTML = `
    <div class="container">
      <h1>Fit Compare</h1>
      <div id="user-info"></div>
      <button id="fetch-data">Fetch Strava Data</button>
    </div>
  `;

  const fetchButton = document.getElementById("fetch-data");
  if (fetchButton) {
    fetchButton.addEventListener("click", function() {
      fetch('/api/strava-data')
        .then(response => response.json())
        .then(data => {
          const userInfoDiv = document.getElementById("user-info");
          if (userInfoDiv) {
            userInfoDiv.innerHTML = `
              <h2>User Profile</h2>
              <p>Name: ${data.name}</p>
              <p>Profile Picture: <img src="${data.profile_picture}" alt="Profile Picture"></p>
              <p>Activities: ${data.activities.map(activity => `<li>${activity.name}</li>`).join('')}</p>
            `;
          }
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    });
  }
}