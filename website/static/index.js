function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
function gotoRoomPage(roomNumber) {
  console.log("Navigating to Room Page:", roomNumber);
  window.location.href = `/Table?room=${roomNumber}`;
}

function gotoBookingPage(roomNumber) {
  console.log("Navigating to Booking Page:", roomNumber);
  window.location.href = `/booking?room=${roomNumber}`;
}

function deleteClassroom(classroomId) {
  //take noteid that we pass
  fetch("/delete-classroom", {
    //send post request to /delete-note endpoint
    method: "POST",
    body: JSON.stringify({ classroomId: classroomId }),
  }).then((_res) => {
    //if get response
    window.location.href = "/add_classroom"; //reload window
  });
}

function deletebooking(bookingId, roomNumber) {
  //take noteid that we pass
  fetch("/delete-booking", {
    //send post request to /delete-note endpoint
    method: "POST",
    body: JSON.stringify({ bookingId: bookingId }),
  }).then((_res) => {
    //if get response
    window.location.href = `/booking?room=${roomNumber}`; //reload window
    //reload window
  });
}
async function increasedate() {
  console.log("increasedate() triggered");
  await fetch("/increase_monday", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({}),
  });
  location.reload(); // Refresh the page after a successful fetch
}

async function decreasedate() {
  console.log("decreasedate() triggered");
  await fetch("/decrease_monday", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({}),
  });
  location.reload(); // Refresh the page after a successful fetch
}
