# boxD

##  Define "boxD"
What is bo**xD**?  Well, I'm glad you asked.  Bo**xD**, or Boxed, is (going to be) a multiplayer [Dots and Boxes](https://en.wikipedia.org/wiki/Dots_and_Boxes) with a few other twists.

Bo**xD** is a realtime variant of the typical turn-based Dots and Boxes game that supports far more than two players.
Instead of each user taking a turn to draw a line, lines can be placed at any time by any user.  After a user places a line, he or she enters a brief "cool-down" state, where lines can no longer be placed by that user.  If adding a line results in the creation of a box, the user by-passes the cool-down state and is free to place another line immediately.

If you are reading this and you aren't taking se329 at Iowa State or personally know any of the developers, kudos to you.  We're always looking for new way to improve the game, so maybe shoot us an idea if you have one.

## Getting local development up and running

**Get the code**

```
$ git clone https://github.com/jonnykry/boxD.git
$ cd boxD
$ pip install -r requirements.txt
```


**Start the server**

```
$ cd ./server       # from boxD directory
$ python server.py
```

**Load the app in your [browser of choice](https://www.google.com/chrome/)**

Open up your favorite web browser and navigate to `http://localhost:5000?local=true`

note:  notice the **?local=true**.  This is **required** for running locally.  If this is ommitted, your websocket connection will open agains the real websocket server (which is no bueno; `//TODO:  FIX`).
