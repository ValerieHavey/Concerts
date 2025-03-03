![Screenshot of gigLog](/backend/static/images/Screenshot%20of%20gigLog.png)

# gigLog

## An App for Tracking the Live Shows You've Attended

### Objective of the app

    *   Sign in and input the concerts you've attended with fields for Headliners, Openers, Date, Location & Notes.

    *   Create, Read, Update, and Delete live shows in your collection.

### Description

I was asked to build a full stack application:

- The back-end application was built with Flask

- The front-end application was built with React

- PostgreSQL is the database management system

- The back-end and front-end applications implement JWT token-based authentication to sign up, sign in, and sign out users.

- The application must have two data entities, one of which is the User model, and the 2nd data entity must interact with the User model.

### Timeframe:

I built the app in one week. 

### Technologies Used:

    Front End:
    HTML
    CSS
    Javascript
    React
    Python

    Back End:
    Flask
    JWT Auth
    PostgreSQL

### MVP:

    - The back-end application is built with Flask.
    - The front-end application is built with React, Python, and JavaScript.
    - PostgreSQL is used as the database management system.
    - The back-end and front-end applications implement JWT token-based authentication to sign up, sign in, and sign out users.
    - Authorization is implemented across the front-end and back-end. Guest users (those not signed in) should not be able to create, update, or delete data in the application or access functionality allowing those actions.
    - The project has one data entity, and a User model which must interact with one another. 
    - The project has full CRUD functionality on both the back-end and front-end.
    - The front-end application does not hold any secret keys. Public APIs that require secret keys must be accessed from the back-end application.
    - The project is deployed online so that the rest of the world can use it.

### Code Convention:

- The files in the back-end and front-end applications are organized following the conventions demonstrated in lectures.
- The code in the back-end and front-end applications adheres to the coding conventions demonstrated in lectures, like using plural names for arrays.
- The back-end and front-end applications do not contain dead code, commented-out sections, or console logs.
- The back-end application can be used without encountering errors in the terminal. The front-end application can be used without encountering errors in the browser’s console.
- The back-end application follows RESTful routing conventions for routes.
- The back-end and front-end applications are coded using proper indentation.

### UI/UX:

- The app exhibits a visual theme, like a consistent color palette and cohesive layout across pages.
- The app is easily navigable by a first-time user. For example, navigation should be done through links instead of having to type in a URL to navigate around the app.
- The app utilizes CSS Flexbox and/or Grid for page layout design.
- Colors used in the app have appropriate contrast that meet the WCAG 2.0 level AA standard.
- When editing an item, the form is pre-filled with that item’s details.
- Only the user who created a piece of data can see and interact with the UI for editing or deleting that data.
- All images have alt text.
- No text is placed on top of an image in a way that makes the text inaccessible.
- All buttons are styled.

### Planning:

Trello was used to complete a list of AAU, Wireframes, ERD, and Stretch Goals

![Screenshot of gigLog Trello Planning Board](/backend/static/images/gigLog%20Trello%20Planning%20Board.png) 

### User Stories:

- I want to securely signup and login to gigLog.
- I want to view my index of shows in my dashboard
- I want to add, edit, or delete any shows from my index.
- Fields that are important to me are: Headliners, Openers, Date of Show, Location of Show, and an optional Notes field.


### Pseudocode

1. Welcome to Your gigLog!
2. An App for listing concerts, live shows, and gigs you've attended.
3. Securely log-in with a hashed password.
4. View your log of gigs when you're logged in. 
5. Button to add a show.
6. Ability to click on any show to edit or delete.
7. No other user is able to add, edit, or delete my shows.
8. Securely logout.

### Build/ Code Process:

1. Read and complete labs for Flask.
2. Read through additional Flask knowledge bases:
    - flask.palletsprojects.com
    - mdn webdocs
    - pyjwt.readthedocs.io
3. Setup and begin project.
4. First I completed the backend, then I completed the front-end. 
5. At a point, I needed to research how to get the whole app going, which is discussed in challenges next. 


### Challenges:

- As a class, we dove right into Django, not learning Flask in a formal setting. I requested to complete the Flask project to extend my skills and continue practicing learning on my own and my research skills.

- From a development standpoint, my biggest challenge was connecting my frontend with my backend. I compiled an index bundle that I added to my backend which was read and applied. I'm still not sure if there was an easier way, but I did get this way to work. 


### Wins:

- Finishing!

### Key Learnings/ Takeaways:

- Key Learning: Flask
- This project really helped hone my SQL skills
- I really enjoyed learning how React/Python/ JS interact with one another.


### Bugs:

- Notes isn't working correctly.

### Future Improvements:

- Stretch Goals:
    Add a community aspect, so users can see a list of other usernames who have attended the same shows, and allowing for comments/discussion.