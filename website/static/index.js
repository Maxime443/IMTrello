function deleteNote(noteId) {
  console.log("Delete button is clicked for note ID: " + noteId);
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/home2";
  });
}

function changeNote(button, noteId) {
  // Add a CSS class to change the color of the button
  button.classList.add("clicked");
  console.log("Change button clicked for note ID: " + noteId);
  // Here you can perform other actions, such as showing a new button
  // or performing any other logic related to the note ID
}

