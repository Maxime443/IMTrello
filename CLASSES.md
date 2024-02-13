# Réflexion pour la database

## Task
- [ ] task_id  <span style="color:cyan">**< primary key >**</span> 
- [ ] name
- [ ] section
- [ ] description
- [ ] priority(1 to 5)
- [ ] start_date
- [ ] end_date
- [ ] state(“On Going” “Done” “Stop”)
- [ ] developers
- [ ] comments

## Section
- [ ] section_id  <span style="color:cyan">**< primary key >**</span> 
- [ ] name
- [ ] project
- [ ] tasks

## Project
- [ ] project_id  <span style="color:cyan">**< primary key >**</span> 
- [ ] nom
- [ ] description
- [ ] start_date
- [ ] end_date
- [ ] sections
- [ ] completion
- [ ] admin

## User
- [ ] user_id  <span style="color:cyan">**< primary key >**</span> 
- [ ] surname
- [ ] name
- [ ] user_type

## Project Manager 
- [ ] <span style="color:green">**extends User**</span> 
- [ ] my_projects 

## Developer
- [ ] <span style="color:green">**extends User**</span>
- [ ] tasks
- [ ] skills

## Comment
- [ ] comment_id  <span style="color:cyan">**< primary key >**</span> 
- [ ] creation_date
- [ ] user
- [ ] content



