# GROCERATE
#### Video Demo: https://youtu.be/Fcqh5X4IuRk
#### Description:
 My project's name is Grocerate.It is a web application created with Python on the backend with Flask framework and HTML and CSS on the frontend with Bootstrap library. SQL is used to interact with the database.
 The idea of this website is for people who are stuck in home quarantine to utilise this platform to post their daily supply needs as they
 are unable to go out and buy supplies on their own. Delivery agents around their vicinity can purchase the items and leave it at their doorstep
 upon confirming the items with their customer. Payment can then be done through digital payment transactions.

 The first folder contains all static files which consists of styles.css and an icon. In styles.css , I used bootstrap to aid with the colors
 ,navigation bar and form design choices as they are easy to implement and straight forward for the user. This file also contains the necessary code
 to centralise my content and increase font size to extra large, making it easier for the viewer to read. Small screen optimization has also been done here.

 The second folder contains all the html templates. add.html comprises of a form for users to furnish the relevant details needed for delivery agents to
 fulfill the user's requirements. apology.html is used to deliver an apology message with the relevant error code and error message for users to ammend their
 errors. A link is also provided for them to return to the main page and redo their form for convenience. The error code is color coded to catch the users
 attention. index.html displays all the current posts in a table format to whoever has logged in. info.html is for delivery agents who is interested to know
 more about a particular post to visit and learn about the contact details and other important information about the post.
 Layout.html comprises of the general outlook of the website, importing the css and bootstrap files along with the icon, containing navigation bar layout,
 footer to give credit to the author of the icon , and flask message for new registered users and posts. login.html is for users to log in by furnishing their username
 and password, also giving them an option at the bottom to register as new user if they do not hold an account.mine.html is the page where logged in users can add new posts,
 view their current posts, and delete them if the order has already been fulfilled. add and delete functions are color coded and done with buttons for user's simplicity.
 register.html is the site for users to furnish their particulars to sign up for a new account.

 Application.py imports the relevant libraries needed for the web application to work and configures the session. Most of the backend programming
 is done here - /add, /register, /delete, /info, /logout , /login, /mine , including the various failsafes to ensure false entries in forms are not allowed .

 helpers.py helps to render apology message and ensures that certain routes require login
