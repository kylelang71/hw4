# AI Prompts

## Problem 1: Vibe Coder Prompts

1. Create AI_prompts.md and create subheadings for 12 questions in the format "## Problem X". As I progress through questions I will tell you which I am on and you need to insert each of my prompts under that heading. Number the prompts as well. Include this prompt under Problem 1 to show you understand.

## Problem 2: Analyze the Database

1. what are the fields in the databse
2. Yes, log everything in AI_prompts.md under the problem I tell you. Do not ask again
3. In harness.md we are going to record the following information for the sake of a future chatbot build. "The following description covers the structure and used of the campus_customs.db. There are four tables: Catalogue, Inventory, users, and chat_messages. Catalogue contains information about each of the product types these are product_id, common name, type of garment, a text description, colors, search tags, the file path for an image of the product, and the price. The Inventory table has the same product_id, product size (like clothing size), and quantity (the amount in stock). the Users table saves information about the accounts that have been made ot access the site...name, first_name, last_name, email, password hash, and time of creation. Finally chat_messages had a user_id (what user), role, content, products_json, and created_at (time of creation).

## Problem 3: Build the Campus Customs Website

1. Moving on to problem 3. We are going to build a website. The frontend will be made with React + Vite + Typescript. Across the top there needs to be a navigation bar that includes: Home, Products, About Us, Log In, and Create Account
2. Review the stylistic cues in this website:[yalebulldogblue.com](https://yalebulldogblue.com/). Summarize them in the frontend folder in a markdown. Use this as a guide to style the website throughout this project.
3. On the 'about us' page say: We are the home of letting everyone else know that you chose your school for it's likelihood of turning you into another coastal elite. The best thing about a ball cap with a Y on it is that people will immediately think you're much smart than them, or so you think, and that's why you buy them.
4. re-review the website and make sure the style guide takes into account the information that's provided alongside each product's thumbnail on the products page.
5. On the products page, show product image thumbnails. Use the image paths in the db, with basic product info. Name, price, short description. Make each product open a single item page that has a large image on the left side, full product text on the other, description, price, sizes, and stock when they are available. Clicking on the thumbnail on the products page should take the user to the full screen single item page.
6. There is going to be a chat interface on the bottom right of the site. Make it float. It does not need to talk to an agent yet. I just create a stub that we will call in the back end later.
7. we're going to need to find a way to connect to the database that sits in the back end. We can use a API to read it. Let's start with a fast API app in the backend folder under main.py. We will use this just to serve products and images and then grow it later to serve the needs of an agent.

## Problem 4: Create account and login

1. We are now moving on to problem four. We will need to create the functionality for logging into an existing account and also creating a new account. New accounts will go into the users table in the database. We need to use hashing in order for the stored passwords to be secure. The create account Survey should include first name, last name, email, password, and confirm password with check that the password and confirm password are aligned. For login, the user should only have to give email and password.
2. The database's user table already contains a test account under test@campuscustoms.yale.edu with a password as password. Try to use this to log in and confirm that it works. Also update the harness.md file with a description of how this create a new account and login system works, including how passwords are protected using hash.

## Problem 5: PydanticAI agent Backend

1. Moving on to problem five. We're going to use Fast API to create the chat bot as a pedantic AI agent to use in that chat widget that we made a shell for earlier that will sit on the bottom right of the website. In the backend folder, the agent will be constructed using four files. agent.py, tools.py, models.py, and in a prompts folder, which rests inside the same backend folder, a prompt.md file. The prompt.md file is a symptom prompt that we will improve on later. The agent file is an agent entry and wiring file. The tools file is something to describe all the tools the agent can call, and the models.py file provides all the structure types for the Pydantic AI. Oh, and the API app is going to sit in the backend/main.py file that will be run with Uvicorn. And main.py, make sure there's the functionality so that a message from the website returns a reply from the agent in the chat. Consider whatever else might be needed for that functionality as well. Tell me where I should put my API key in this build. Make a VENV if you haven't already.
2. in the prompt.md file, give a description of how the campus customs chat bot interacts with others. Specifically, it should always be polite and apologetic if there are mistakes. It should welcome people to the store It should always ask if it can help with anything else. Generally, it should have the disposition of a butler.
3. Update the types in models.py for chat replies and product cards as needed. without my permission. In harness.md, create a summary of how the front end talks to Fast API and how the agent is loaded that a beginner could understand.
4. ensure that the backend runs from the backend/ folder with the following terminal command: uvicorn main:app --reload --port 8000
5. If a grade were to review this project and attempt to use "uvicorn main:app --reload --port 8000" would it still work?

## Problem 6: Tools: Product info and stock

1. Yes, add the readme
2. The agent is going to have to use the database. It should never invent prices or quantities. So it should read directly from it. If a size is out of stock, for example, it should say so clearly and never be sycophantic. Because of this, it, we need to give it tools that look up information from the campus customs database. Specifically, so it can retrieve product description, price, and Inventory by size. Edit the prompts.md file so that the agent knows it has these tools to call for price and stock questions. Add or update return types in models.py.
3. create tools so that the agent can look up each of the tables in the database. Those are catalog, inventory, users, and chat messages. Specifically under users, the price. will be very important and under inventory, the quantity, size, and product ID will be very important. add to the prompt file that the agent should never discuss the information in the users table, whether or not it is for the logged in user's account or for anyone else's account.
4. Under harness.md, add a subheading for problem six. Under that subheading, list very briefly by name only each tool that was given to the agent for parsing the database. With regards to the price and inventory fields, add a justification that these are the most likely user requests, which is why they were included. Product ID was excluded for the same reason. Users will not know that, but they will be able to interact with the other information.
5. to that same section in the harness.md, add that get chat history was provided so that the agent could be more effective at problem solving for a given customer.
6. get user account was also added so that the user could not ask for other users' information, even though the agent had access to that table in the database. Add this detail to harness.md in the same section.
7. Reduce the wordiness of the harness.md file. So that it's a bit smaller.

## Problem 7: Chat search that updates the page

1. Moving on to problem seven, period. We're going to add a feature to the chat agent that is similar to search, specifically when a customer asks something along the lines of, what hoodies do you have? The agent should search the catalog and the website should dynamically show those matching items as product cards. Product cards contain image, name, price, and short info. To be clear, this should be dynamic. So cards not matching that product type should disappear or get shuffled below the others that do match. The architecture should rely on an API. to the database. Essentially, the agent returns the product matches, and then the front end renders them on the website. Before you attempt to do this, add an additional tool for the agent that pulls product type. Add an description to the problem six subheading in the harness.md file explaining that this was added in problem seven in order to get this function to work well.
2. Check that once the new product cards are dynamically loaded under this new feature, that the product page operates the same way as described in problem three, both for the multiple product page and the single item page that you can click into. to get more detail. Each card that's being dynamically shown should still open that detail view with a large image on the left and full info on the right when clicked. Check this and confirm that it's the case.
3. Try the same functionality with the prompt. What t-shirts do you have in the chatbot?
4. Now that this is working, update the prompt.md file and the harness.md file with a brief description of how search results reach the page.

## Problem 8: Customer Memory

1. Confirm that in this current build that when a shopper is logged in, the agent knows who is chatting by name and email.
2. Rewrite prompt MD. The original t- intent was that the chatbot never discusses other users or their credentials. The chatbot can have access to the current user's credentials so that it is aware of who it is chatting with. record the last prompt, this one and all the following under problem nine, until prompted otherwise. When a shopper is logged in, their chat history should be saved in the database. and trackable to their credentials. When they log back in in the future, it should be reloaded so that the agent has that as context. make this change.
3. make sure that there is still functionality for guests to the page, guests being people that are on the website but not logged in, to use the chat bot. However, guest messages should never be saved.
4. I also want the agent to have context for the page that is being looked at. Is there a way that you can do this by passing HTML or screenshots into the agent whenever a question is asked? I would prefer HTML over screenshots. For example, I want the agent to be able to answer the question, do you have this in a different color? In order to answer that question, it needs to understand what is being shown on the page.
5. reiterate in harness.md how the user chat history is stored, including in models.py, what customer fields the agent sees, and how page context is passed. Put this under a subheading problem eight.

## Problem 9: Usability Improvements

1. Starting with this user prompt, start recording under problem nine. We're going to make some improvements to the pages on this website. First, I've added a .gif file to the data folder, and I want this to play at the top of the About Us page. Next, the text that's in the About Us page should use the word art file found in the data folder as a template and should be illustrated in that style, specifically the blue wording in that file.
2. Next, make sure that the page title on the top left says Yale Campus Customs, not just Campus Customs. Rebuild the home page so it has section summaries. such as our best hoodies, or our hottest long sleeves. And include some product images from those categories. There. That can be clicked into. Finally, the chat bot should proactively welcome people to the chat by sending a welcome to Yale Campus Customs, how can I help you message when they enter the website. This should occur regardless of whether or not they're a guest or signed in.
3. make the blue text on the About Us page three times the size and the .gif large enough to span the window.
4. Make the agent chat button on the bottom right blink with a gold outline before the user clicks in to view the welcome message.
5. Also make the 'products page' in the navigation bar 'all products.'
6. I added a photo of the Yale Bulldog to the data folder. Add this to the top of the home page. Without any caption.
7. Create a new file under the output folder called usability.md. In this file, write the following structured bullet points with the change and then colon why the change was made."Front end improvements included actual sections on the home page, to give users suggestions before viewing all products, a message was also added to the agent to proactively welcome people to the page. The agent chat button also flashes with a gold outline to draw the user's eye to it. Earlier in the project, I made sure to add controls so that the agent did not share information about other users, their IDs, their emails, or passwords with anybody that was using the chatbot. Finally, I also added images to the About Us and home page to make it more eye-catching."
8. Make these changes and add them to the usability.md file in the same structure...Cut tool-call round trips — each tool call is a full extra model round trip (the biggest cost by far, bigger than DB/network overhead). Two easy wins: bake `list_product_types()`'s output directly into the static prompt/instructions at agent build time instead of making it a callable tool (the catalog's categories barely change — eliminates a whole round trip on most product questions), and tell the agent in `prompt.md` not to call `get_product_details` when `search_products` already returned the price/description it needs.

    1. Stream the reply instead of `run_sync` — switch to `agent.run_stream()` and stream tokens to the frontend. Doesn't reduce total time, but the user sees the first words almost immediately instead of waiting for the full reply, which is what actually feels slow right now.
    2. Reuse one DB connection per request instead of opening/closing a fresh `sqlite3.connect()` for every tool call, user lookup, history load, and save (a single chat turn can open 5+ connections). Minor on SQLite, but free to fix.
9. Add the functionality that if you click on the top left corner Yale campus customs text, that it will take you back to the homepage.
10. Do not make it stand out as a link, it can look like normal text.
11. You never made the changes to the usability.md file for the backend improvements that you suggested, and I accepted. Make those changes now.

## Problem 10: Style the website

1. We're now moving on to problem 10. Create a design.md file under the output folder. Any of the changes in the usability.md folder that are really more design oriented (the look of the site) should be removed from there and added to design.md
2. Add the Yale students .jpg image in the place of the bulldog on the home page. Put the bulldog lower on the page and put text in the bottom right saying, Dan's favorites. Above one of the product categories. your choice of which
3. add the image file named Yale in the data folder to the background of the home page and the all products page as a pattern with high opacity in the background. Once complete provide a link so i can see the page
4. update the design.md with the most recent requests. include a very brief sentence about why these changes will improve the customer experience and keep them on the page. keep it very concrete and very short.
5. Zoom out on the photo of the Yale students at the top of the Yale Campus Customs homepage so that I can see the banner. Also make the text bolded for the shop all products and your home for Yale themed collegiate apparel and product short descriptions. Do this on the all products page as well. Again, on the home page, make sure you are centering the Dan's favorites in larger text, in white text, over the bulldog image.
6. The zoom out of the hero image was too far. Make sure that it reaches all the way across the screen without any padding. Just move the center up so that it includes the Welcome to Yale Class of 2030 banner and the faces of the students.
7. RE-write the design.md say this exactly "Added a blinking gold outline to the chat button: to draw the user's eye to it, increasing the odds that they use it and shop more quickly

* Added images to the About Us and Home pages, Added a tiled Yale "Y" logo watermark pattern to the Home and Products page: to make the site more eye-catching and reinforces the Yale brand throughout browsing, making the site feel more polished and trustworthy.
8. The cards under the product thumbnails should not be see-through to the yale logo background, update that and add it to design.md as a readability improvement

## Problem 11: Site Testing (app check)

1. Create the file app_check.html in the output folder. This should be a page that can be double-clicked open. The page should include screenshots and short captions for one. Showing that a chat with the chat bot accurately checked the inventory level of an item. Comma, if this can also take a screenshot of the data in the database in some form, that would be helpful. Period. Two. The dynamic search result cards appearing after a category question, for example, hoodies, and then hoodies are outlined in gold at the top of the page. And it's clear that this was requested in the chat, in the screenshot. Period. Three. A screenshot of the chat bot button being outlined in gold at the opening of the page in order to draw the user's attention. The goal is to make this easy to grade so that HTML file should have a heading for each one of those checks. The one or two screenshots. And then one brief sentence on what the screenshot proves. Put those screenshot image files in the output folder under another folder called app_check_images and link those suckers from  app_check.html with relative paths. Freaking awesome. Thank you so much. Please do this quickly.
2. There should be a single screenshot for section two. The image should show the open chat button asking for hoodies, in front of hoodies with gold border on the all products page, not the home page

## Problem 12: Audit trail, safety, finish harness

1. Moving on to problem 12. Under the output folder, make a JSON file named audit_trail.JSON. This will serve as an append only. Journal of agent loop activity. Specifically, it should include time of activity, tool name used, very short arguments and results, and stop reason. Never wipe it between runs.
2. Simulate the app check checks again and see if the activity is appended to that JSON once you're done.
3. Add the following safety rules to prompt.md. The agent can only use 20 loops. There can only be 50 results for any one search. The model must be ChatGPT Luna.
4. Also add that the agent cannot use anything on the open internet. It can only access the database. it also cannot edit the audit log.
5. add reasoning for each of these. Limitations on loops and results. Into harness.md under a new section called Problem 12 Audit Trail & Safety. Also explain why we do not need controls for limiting the agent's ability to access the internet or to edit the audit log. these should be very brief explanations. There is discussion elsewhere in this project of why um, the model fields in models.py were chosen, and that should be included in this discussion as well. The backend model config for my port key API key needs to change to GPT-5.6-Luna, make that change
6. remove the model config comment from the problem 12 section in the harness.md.
