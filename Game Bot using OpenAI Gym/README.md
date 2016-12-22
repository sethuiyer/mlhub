#Game Bot using OpenAI Gym

Trying to implement simple game bot using OpenAI's gym

####Steps

Install Gym, universe and Docker.

Run`docker run -p 5900:5900 -p 15900:15900 --cap-add SYS_ADMIN --ipc
 host --privileged quay.io/openai/universe.flashgames:0.20.8\n`

Run `python bot.py`