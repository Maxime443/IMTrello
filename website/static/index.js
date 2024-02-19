function open_Project(projectId) {
    // Redirect the user to the project page with the project ID as part of the URL
    window.location.href = "/project/" + projectId;
}

function delete_Project(projectId) {
  fetch("/delete-project", {
    method: "POST",
    body: JSON.stringify({ projectId: projectId }),
  }).then((_res) => {
    window.location.href = "/";
  });
  }

function rename_Project(projectId) {
  fetch("/delete-project", {
    method: "POST",
    body: JSON.stringify({ projectId: projectId }),
  }).then((_res) => {
    window.location.href = "/";
  });
  }