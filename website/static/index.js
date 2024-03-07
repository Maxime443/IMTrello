function open_Project(projectId) {
  // Redirect the user to the project page with the project ID as part of the URL
  window.location.href = "/project/" + projectId;
}

function delete_Project(projectId) {
  fetch("/delete-project", {
    method: "POST",
    body: JSON.stringify({projectId: projectId}),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function deleteAllNotifications(user_id){
  console.log("caca")
  console.log(user_id==="1") 
  user_id=parseInt(user_id) 
  console.log(user_id===1) 
  fetch("/delete-all-notifications", {
    method: "POST",
    body: JSON.stringify({user_id: user_id}),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function rename_Project(projectId) {
  fetch("/delete-project", {
    method: "POST",
    body: JSON.stringify({projectId: projectId}),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function deleteSection(sectionId,projectId) {
  fetch("/delete-section", {
    method: "POST",
    body: JSON.stringify({ sectionId: sectionId }),
  }).then((_res) => {
    window.location.href = "/project/" + projectId;
  });
  }

function deleteTask(taskId,sectionId,projectId) {
  fetch("/delete-task", {
    method: "POST",
    body: JSON.stringify( { taskId: taskId })
  }).then((_res) => {
    window.location.href = "/project/" + projectId;
  });
  }

function showModalforNewTask(sectionId) {
            // Set the value of the hidden input field with the project ID
            document.getElementById('task_section_id').value = sectionId;
            $('#modal_new_task').modal('show');
        }

document.querySelectorAll('.editableContent').forEach(function(element) {
    element.addEventListener('click', function() {
        // Créer un formulaire
        var form = document.createElement('form');
        form.method="post";
        var sectionId = this.getAttribute('data-section-id');
        form.addEventListener('submit', function(event) {
            event.preventDefault(); // Empêcher l'envoi du formulaire par défaut
            var newText = input.value.trim();
            this.parentNode.textContent = newText; // Remplacer l'input par le nouveau texte
        });

        // Créer un input de type texte à l'intérieur du formulaire
        var input = document.createElement('input');
        input.type = 'text';
        input.name = 'new_name';
        input.value = this.textContent.trim(); // Utiliser le texte actuel comme valeur par défaut
	    input.classList.add('section_input');
        input.select();
        input.addEventListener('blur', function() {
            form.submit(); // Soumettre le formulaire lorsque l'input perd le focus
        });

        var input_id = document.createElement('input');
        input_id.name = 'id';
        input_id.value = sectionId;
        input_id.type = 'hidden';

        // Créer un champ de formulaire caché pour l'action
        var hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'action';
        hiddenInput.value = 'rename_section';

        // Ajouter les éléments au formulaire
        form.appendChild(input);
        form.appendChild(hiddenInput);
        form.appendChild(input_id);
        // Remplacer le contenu du div par le formulaire
        this.textContent = '';
        this.appendChild(form);

        // Mettre le focus sur l'input
        input.focus();
    });
});

const draggables = document.querySelectorAll('.li_task');
const droppables = document.querySelectorAll(".task-list");
draggables.forEach((task) => {
  task.addEventListener("dragstart", () => {
    task.classList.add("is-dragging");
  });
  task.addEventListener("dragend", () => {
    task.classList.remove("is-dragging");
});
});

droppables.forEach((zone) => {
  zone.addEventListener("dragover", (e) => {
    e.preventDefault();

    const bottomTask = insertAboveTask(zone, e.clientY);
    const curTask = document.querySelector(".is-dragging");
    var bottomtaskId=""
    if (!bottomTask) {
      zone.appendChild(curTask);
      bottomtaskId=null
    } else {
      zone.insertBefore(curTask, bottomTask);
      bottomtaskId = bottomTask.getAttribute('data-task-id');
    }
    const taskId = curTask.getAttribute('data-task-id');
    const newSectionId = zone.getAttribute('data-section-id'); // Ajouter un attribut data-section-id dans votre HTML
    updateTaskSection(taskId, newSectionId,bottomtaskId);
  });
});

const insertAboveTask = (zone, mouseY) => {
  const els = zone.querySelectorAll(".li_task:not(.is-dragging)");

  let closestTask = null;
  let closestOffset = Number.NEGATIVE_INFINITY;

  els.forEach((task) => {
  const {top} = task.getBoundingClientRect();

  const offset = mouseY - top;

  if (offset < 0 && offset > closestOffset) {
  closestOffset = offset;
  closestTask = task;
}
});

  return closestTask;
};

const updateTaskSection = (taskId, newSectionId,bottomtaskId) => {
    const data = {
        task_id: taskId,
        new_section_id: newSectionId,
        bottom_task_id: bottomtaskId
    };

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/update_task_section", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Traitement à effectuer après la réception de la réponse
        }
    };
    xhr.send(JSON.stringify(data));
};

function createSectionForm() {
    // Créer le formulaire en utilisant jQuery
    var form = $('<form>').attr({
        method: 'POST',
        class: 'section-form'
    });
    var input = $('<input>').attr({
        type: 'text',
        name: 'section_name',
        placeholder: 'Enter section name',
        class: 'section_input'
    });
    var input_hidden=$('<input>').attr({
        type:"hidden" ,
        name:"action" ,
        value:"add_section"
    })
    var button = $('<button>').attr({
        type: 'submit',
        class: 'btn btn-primary'
    }).text('Create Section');

    // Créer les divs pour la carte
    var cardHeader = $('<div>').addClass('card_header');
    var cardFooter = $('<div>').addClass('card_footer');
    var card = $('<div>').addClass('carte');

    // Placer l'input dans le div de l'en-tête de la carte
    cardHeader.append(input);

    // Placer le bouton dans le div du pied de la carte
    cardFooter.append(button);

    // Placer le div de l'en-tête et le div du pied dans la carte
    card.append(cardHeader, cardFooter);

    // Placer la carte dans le formulaire
    form.append(card);
    form.append(input_hidden)
    // Remplacer le bouton par le formulaire
    $('.btn_section').replaceWith(form);

    // Ajouter un gestionnaire d'événements pour fermer le formulaire si l'utilisateur clique ailleurs dans la page
    $(document).on('click', function(event) {
        if (!$(event.target).closest('.section-form').length && !$(event.target).closest('.btn_section').length) {
            closeSectionForm();
        }
    });
    $('.add_section').on('click', '.btn_section', createSectionForm);
}

// Ajouter un gestionnaire d'événements pour le clic sur le bouton "New Section"


function closeSectionForm() {
    // Supprimer le formulaire et remettre le bouton "New Section"
    $('.section-form').remove();
    if ($('.add_section').find('.btn_section').length === 0) {
        // Remettre le bouton "New Section" seulement s'il n'existe pas déjà
        $('.add_section').append('<button type="button" class="btn_section btn btn-dark"><i class="fas fa-plus"></i>New Section</button>');
}}

function updateTaskStatus (task_id, value, projectId) {

      fetch ( '/update_task_status/' + task_id , {
          method : "POST" ,
          headers : {
              'Content-Type' : 'application/json'
          } ,
          body : JSON.stringify ( { status : value } ) ,
      } ).then ( response => {
          if ( ! response.ok ) {
              throw new Error ( 'Failed to update task status' );
          }
          console.log ( 'Task status updated successfully.' );
          window.location.href = "/project/" + projectId;
          // You can add additional handling here if needed
      } )
          .catch ( error => {
              console.error ( 'Error:' , error );
          } );

}

function updateTaskPriority (task_id, value, projectId) {

      fetch ( '/update_task_priority/' + task_id , {
          method : "POST" ,
          headers : {
              'Content-Type' : 'application/json'
          } ,
          body : JSON.stringify ( { priority : value } ) ,
      } ).then ( response => {
          if ( ! response.ok ) {
              throw new Error ( 'Failed to update task priority' );
          }
          console.log ( 'Task priority updated successfully.' );
          window.location.href = "/project/" + projectId;
          // You can add additional handling here if needed
      } )
          .catch ( error => {
              console.error ( 'Error:' , error );
          } );

}

document.addEventListener('DOMContentLoaded', function () {
  const searchInput = document.getElementById('search-input');
  const tasks = document.querySelectorAll('.task-card');
  searchInput.addEventListener('input', function () {
    const searchTerm = searchInput.value.trim().toLowerCase();

    tasks.forEach(function (task) {
      const taskName = task.querySelector('.card-title a').textContent.toLowerCase();
      const taskPriority = task.querySelector('.priority span').textContent.toLowerCase();
      const taskStatus = task.querySelector('.status span').textContent.toLowerCase();
      console.log(taskStatus);

      if (taskName.includes(searchTerm) || taskPriority === searchTerm || taskStatus.includes(searchTerm)) {
        task.style.display = 'block';
      } else {
        task.style.display = 'none';
      }
    });
  });
});




function remove_dev_from_task(user_id, task_id, project_id) {
  fetch("/remove-dev", {
    method: "POST",
    body: JSON.stringify({ user_id : user_id ,task_id : task_id}),
  }).then((_res) => {
    window.location.href = "/project/" + project_id;
  });
  }

  function remove_dev_from_project(user_id, project_id) {
  fetch("/remove-dev-from-project", {
    method: "POST",
    body: JSON.stringify({ user_id : user_id ,project_id : project_id }),
  }).then((_res) => {
    window.location.href = "/project/" + project_id;
  });
  }

  $(document).ready(function(){      
    var down = false;
    
    $('#bell').click(function(e){
      
        var color = $(this).text();
        if(down){
            
            $('#box').css('height','0px');
            $('#box').css('opacity','0');
            down = false;
        }else{
            
            $('#box').css('height','auto');
            $('#box').css('opacity','1');
            down = true;
            
        }
        
    });
        
        });


        $(function(){
          $("[data-toggle=popover]").popover({
              html : true,
              content: function() {
                var content = $(this).attr("data-popover-content");
                return $(content).children(".popover-body").html();
              },
              title: function() {
                var title = $(this).attr("data-popover-content");
                return $(title).children(".popover-heading").html();
              }
          });
          $(document).on("click", ".popover .btn" , function(){
            var id = $(this).attr("id");
            deleteAllNotifications(id);
        });
      });