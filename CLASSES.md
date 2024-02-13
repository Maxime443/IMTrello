# Réflexion pour la database

## Task
- [ ] task_id  <span style="color:cyan">**< primary key >**</span> 
- [ ] name
- [ ] project
- [ ] description
- [ ] priority(1 to 5)
- [ ] delay
- [ ] state(“On Going” “Done” “Stop”)
- [ ] users
- [ ] comments

## Project
- [ ] project_id  <span style="color:cyan">**< primary key >**</span> 
- [ ] nom
- [ ] description
- [ ] delay
- [ ] completion
- [ ] admin_user

## User
- [ ] user_id  <span style="color:cyan">**< primary key >**</span> 
- [ ] surname
- [ ] name
- [ ] user_type

## Project Manager 
- [ ] <span style="color:green">**extends User**</span> 
- [ ] my_projects 

## Developper
- [ ] <span style="color:green">**extends User**</span>
- [ ] tasks
- [ ] skills

## Comment
- [ ] comment_id  <span style="color:cyan">**< primary key >**</span> 
- [ ] creation_date
- [ ] user
- [ ] content



