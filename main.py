# Variables you might need to change

#replace with the token of your bot
BOT_TOKEN = "INSERT BOT TOKEN HERE!"

#replace with the id of your server
SERVER_ID = "INSERT SERVER ID HERE"

#don't edit stuff below here unless you know what you're doing
import discord
import asyncio
import pickle
import sys
import random

client = discord.Client()

T_CHANNEL = H_CHANNEL = GM_ROLE = "" # fill these in later in the code

def already_set_up(): # figures out whether the bot has already been set up
    print("checking already set up")
    try:
        with open("data.dat", "rb") as f:
            return pickle.load(f)["set_up"]
    except FileNotFoundError:
        return False
    except KeyError:
        return False

@client.event
async def on_ready(): # here be dragons

    global H_CHANNEL # we need to be able to modify these
    global T_CHANNEL
    global GM_ROLE


    print("bot online")
    print("logged in as " + client.user.name + "\n")

    # first a few sanity checks
    #check we're in SERVER_ID
    if not client.get_server(SERVER_ID) in client.servers :
        print("we don't appear to be in the right server... -_-")
        sys.exit(1)

    WW_SERVER = client.get_server(SERVER_ID)

    if already_set_up():
        print("already been set up, retrieving values")
        with open("data.dat", "rb") as datafile:
            obj = pickle.load(datafile)

            H_CHANNEL = obj["h_channel"]
            T_CHANNEL = obj["t_channel"]
            GM_ROLE   = obj["gm_role"]

    else:
        # time to do setup!
        print("\n")
        print("doing setup. awaiting message saying '!ghost_setup' from server admin in the correct channel")

        msg = await client.wait_for_message(author=WW_SERVER.owner, content='!ghost_setup')
        setup_channel = msg.channel
        await client.send_message(setup_channel, "Hi, time to do setup. First please give me the game master role by saying, '!ghost_gmrole @role'")

        msg = await client.wait_for_message(author=WW_SERVER.owner, check=lambda msg : msg.content.startswith("!ghost_gmrole"))
        #global GM_ROLE
        GM_ROLE = msg.role_mentions[0] # due to a limitation with discord, specifying multiple roles will lead to undefined behaviour at this point.
        await client.send_message(setup_channel, "Game master role set to '"+GM_ROLE.name+"'!\nOk, now go to the tavern channel and type '!ghost_tavern'")

        msg = await client.wait_for_message(author=WW_SERVER.owner, content="!ghost_tavern")
        #global T_CHANNEL
        T_CHANNEL = msg.channel
        await client.delete_message(msg)
        await client.send_message(setup_channel, "Tavern channel set to " + T_CHANNEL.mention)

        await client.send_message(setup_channel, "Ok now finally go to the spooky house and type '!ghost_spooky'")
        msg = await client.wait_for_message(author=WW_SERVER.owner, content="!ghost_spooky")
        #global H_CHANNEL
        H_CHANNEL = msg.channel
        await client.delete_message(msg)
        await client.send_message(setup_channel, "Spooky channel set to " + H_CHANNEL.mention)

        with open("data.dat", "wb") as datafile:
            obj = {
                "set_up": True,
                "h_channel": H_CHANNEL,
                "t_channel": T_CHANNEL,
                "gm_role": GM_ROLE
            }
            pickle.dump(obj, datafile) # save for later

        await client.send_message(setup_channel, "Setup complete! I will now delete messages in " + H_CHANNEL.mention + " that aren't sent by game masters.")
    client.loop.create_task(ghost_loop())

@client.event
async def on_message(msg):
    if GM_ROLE != "" and GM_ROLE in msg.author.roles:
        if msg.content == "!ghost_debug_reveal":
            print(globals())
        elif msg.content == "!ghost_stop":
            await client.send_message(msg.channel, "Bot shutting down")
            await client.logout()
        elif msg.content == "!ghost_status":
            e = discord.Embed(title="Ghostbot status", colour=0x449944)
            e.add_field(name="Tavern channel", value=T_CHANNEL.mention)
            e.add_field(name="Haunted House channel", value=H_CHANNEL.mention)
            e.add_field(name="Game master role", value=GM_ROLE.mention)
            await client.send_message(msg.channel, embed=e)

    if H_CHANNEL != "" and msg.channel == H_CHANNEL:
        if not (msg.author == msg.server.me or GM_ROLE in msg.author.roles) :
            await client.delete_message(msg)


async def make_wordlist(fhandle, num=10):
    fhandle.seek(0)
    lines = fhandle.readlines()
    words = random.sample(lines, num)
    emb = discord.Embed(title="Choose some words!", description="*Type a number to choose a word! The first number that gets typed will be chosen.*", colour=0x449944)
    lu = dict()
    for n, v in enumerate(words):
        emb.add_field(name="Word #"+str(n), value=v.rstrip())
        lu[n] = v.rstrip()
    return emb, lu

# word list loop
async def ghost_loop(): # here be more dragons
    await client.wait_until_ready()
    convo = []
    sentence_convo = []
    while not client.is_closed:
        if H_CHANNEL == "":
            continue
        sentence_done = False
        sentence_convo = []
        sentence = ""
        tomsg = ""
        while not sentence_done:
            if tomsg != "":
                await client.delete_message(tomsg)
                tomsg = ""

            wordlist_sent = False
            while not wordlist_sent:
                try:
                    with open("words.txt") as wh:
                        wordlist, lookup = await make_wordlist(wh)
                    startmsg = await client.send_message(H_CHANNEL, embed=wordlist)
                    wordlist_sent = True
                except discord.errors.HTTPException:
                    print("failed to send wordlist, trying again")
                    wordlist_sent = False # just to make sure -_-


            #get number
            respmsg = await client.wait_for_message(timeout=60, channel=H_CHANNEL, check=lambda msg: msg.content.isdigit() and 0 <= int(msg.content) <= 9)
            if respmsg is None: # timed out
                await client.delete_message(startmsg)
                tomsg = await client.send_message(H_CHANNEL, "I gave you 60 seconds but no one said anything! You will get another opportunity in 5 minutes.")
                sentence = ""
                sentence_done = True
                await asyncio.sleep(60*5)
            else:
                await client.delete_message(startmsg)
                try:
                    await client.delete_message(respmsg)
                except discord.errors.NotFound:
                    pass # the other bit already deleted it hopefully

                sentence_convo.append(await client.send_message(H_CHANNEL, respmsg.author.mention+" says "+lookup[int(respmsg.content)]))
                sentence += lookup[int(respmsg.content)]+" "
                print("sentence is '"+sentence+"'")
                if sentence[-2] in [".", "?", "!"]:
                    sentence_done=True
                await asyncio.sleep(15)

        if sentence != "":
            await client.send_message(T_CHANNEL, "**Boo!** The ghosts want to say something! They say \""+sentence[:-1]+"\"!")

        if sentence_convo:
            if len(sentence_convo) == 1:
                await client.delete_message(sentence_convo[0])
            else:
                await client.delete_messages(sentence_convo)
client.run(BOT_TOKEN)
