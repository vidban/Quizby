# Quizby App

## Details:

Click [here](https://docs.google.com/document/d/1UX03vmtLDEaC_aLBhUG15_K6iTjF3O1jh8ZUhMs7dlQ/edit)

## Tech Stack:

- Python-Flask
- Postgres
- Javascript

## Environment Variables:

- CURR_USER_KEY - **string name to hold current user info**
- SECRET_KEY - **any string**

## API used:

[Unsplash API](https://unsplash.com/documentation#getting-started)


## Routes

#### login routes
  - *GET '/'*  
	  - Render Homepage based on user status
  - *GET '/login'*  
 	  - Render login form
  - *POST '/login'*  
 	  - Validate login info and reroute to '/'
  - *GET '/signup'*
    - Render Signup form  
  - *POST '/signup'*
    - Validate Signup and reroute to '/'
  - *GET '/logout'*
    - Reroute to '/' 
#### User routes
  - *GET '/users/profile'*
    - Display info about user
  - *GET '/users/profile/edit'*
    - Display form to edit user's profile
  - *POST '/users/profile/edit'*
    - Verify password on form submit and reroute to '/users/profile'
  - *GET '/users/<int:user_id>/quizzes'*
    - Display all quizzes created by the user
  - *GET '/users/<int:user_id>/questions'*
    - Display all questions added by the user
#### Quizzes routes
  - *GET '/create'*
    - Display create a quiz form
  - *POST '/create'*
    - Reroute to Adding questions page '/questions'
  - *GET '/quizzes/<int:quiz_id>/delete'
	- Delete quiz with the provided id
  - *GET '/search'*
    - Render search modal for image
  - *POST '/search'*
    - Get selected image and return to create quiz page
  - *GET '/search/unsplash'*
    - Search the unsplash API for images based on term entered
#### Questions routes
  - *GET '/questions'*
    - Display list of questions
  - *GET '/questions/add'*
    - Display form to add questions
  - *POST '/questions/add'*
    - Add question to database and reroute to '/questions'
  - *POST '/questions/<int:question_id>/delete'*
    - Delete a user's question
	




## Theme

[#24 - Clean and Modern](https://visme.co/blog/website-color-schemes/)
