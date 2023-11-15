document.addEventListener("DOMContentLoaded", function () {
  var currentDateElement = document.getElementById("dateDisplay");
  var nextWeekButton = document.getElementById("nextWeekButton");
  var previousWeekButton = document.getElementById("previousWeekButton");

  function updateDateDisplay(currentDate) {
    // Get the current day of the week (0 = Sunday, 1 = Monday, ..., 6 = Saturday)
    var currentDay = currentDate.getDay();

    // Calculate the difference between the current day and Monday (assuming Monday is 1)
    var daysUntilMonday = currentDay === 0 ? 6 : 1 - currentDay;

    // Calculate the difference between the current day and Friday (assuming Friday is 5)
    var daysUntilFriday = currentDay <= 5 ? 5 - currentDay : 5 + 7 - currentDay;

    // Calculate the dates of Monday and Friday in the current week
    var mondayDate = new Date(currentDate);
    mondayDate.setDate(currentDate.getDate() + daysUntilMonday);

    var fridayDate = new Date(currentDate);
    fridayDate.setDate(currentDate.getDate() + daysUntilFriday);

    // Format the dates
    var options = {
      day: "numeric",
      year: "numeric",
      month: "long",
    };
    mon = mondayDate.toLocaleDateString("th-TH", options);
    var fri = fridayDate.toLocaleDateString("th-TH", options);

    currentDateElement.innerText = ` ${mon} - ${fri}`;

    fetch("/Table", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        monday: mondayDate.toISOString(),
        friday: fridayDate.toISOString(),
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          // Update the UI or perform other actions if needed
        }
      });
  }

  // Initial date display
  var currentDate = new Date();
  updateDateDisplay(currentDate);

  // Button click event
  nextWeekButton.addEventListener("click", function () {
    // Update the date to the next week
    currentDate.setDate(currentDate.getDate() + 7);

    // Update the display
    updateDateDisplay(currentDate);
  });
  previousWeekButton.addEventListener("click", function () {
    // Update the date to the previous week
    currentDate.setDate(currentDate.getDate() - 7);

    // Update the display
    updateDateDisplay(currentDate);
  });
});
