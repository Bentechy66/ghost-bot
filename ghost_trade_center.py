'''                                                                                         _             
   _____ _               _     _______            _         _____           _              | |             
  / ____| |             | |   |__   __|          | |       / ____|         | |             | |_ _ __ ___  
 | |  __| |__   ___  ___| |_     | |_ __ __ _  __| | ___  | |     ___ _ __ | |_ ___ _ __   | __| '_ ` _ \
 | | |_ | '_ \ / _ \/ __| __|    | | '__/ _` |/ _` |/ _ \ | |    / _ \ '_ \| __/ _ \ '__|  | |_| | | | | |
 | |__| | | | | (_) \__ \ |_     | | | | (_| | (_| |  __/ | |___|  __/ | | | ||  __/ |      \__|_| |_| |_|
  \_____|_| |_|\___/|___/\__|    |_|_|  \__,_|\__,_|\___|  \_____\___|_| |_|\__\___|_| 

Created by BenTechy66 for Randium and co on the Werewolves discord.

'''

M_CHANNEL = "409085003503239169"
BOT_TOKEN = "NDA5MDgzMzAyMTg0NjE1OTM3.DVeCVQ.U2PmYm2yfAXMoBCUGCZnrNxF81E"
MAIN_BOT_ID = "247096918923149313"
global cred_emoji
cred_emoji = ":ghost:" # the emoji used for credits (eg :ghost:)


from discord.ext import commands
import sqlite3
import os 
import re 


bot = commands.Bot(command_prefix='$')

def setup_db():
	# Open and read the file as a single buffer
	fd = open('marketplace_sql_schema.sql', 'r')
	sqlFile = fd.read()
	fd.close()

	# all SQL commands (split on ';')
	sqlCommands = sqlFile.split(';')

	# Execute every command from the input file
	for command in sqlCommands:
		# This will skip and report errors
		# For example, if the tables do not yet exist, this will skip over
		# the DROP TABLE commands
		try:
			c.execute(command)
		except:
			print("Command skipped")





async def get_buy_offers(emoji):
	if emoji == None:
		c.execute("SELECT name,user_id,price FROM buy_offers;")
	else:
		c.execute("SELECT name,user_id,price FROM buy_offers WHERE name = ?;", (emoji,))
	rows = c.fetchall()
	if rows:
		#yay
		offers = "**Buy offers for %s**" % (emoji)
		offers = offers + ""
		await bot.say(str(rows))
	else:
		await bot.say("No buy offers for {0}!".format(emoji))
		return("nope")

async def get_sell_offers(emoji):
	if emoji == None:
		c.execute("SELECT name,user_id,price FROM sell_offers;")
	else:
		c.execute("SELECT name,user_id,price FROM sell_offers WHERE name = ?;", (emoji,))
	rows = c.fetchall()
	if rows:
		#yay
		offers = "**Sell offers for %s**" % (emoji)
		offers = offers + ""
		await bot.say(str(rows))
	else:
		await bot.say("No sell offers for {0}!".format(emoji))
		return("nope")

async def add_buy_offer(user_id, emoji, price):
	c.execute('INSERT INTO buy_offers (name, user_id, price) VALUES (?, ?, ?);', (emoji,user_id,price))
	conn.commit()

async def add_sell_offer(user_id, emoji, price):
	inv = await get_inv_by_id(user_id)
	print("Doin stuff")
	Ting = False
	for e in inv:
		if emoji in e:
			Ting = True
	if Ting:
		print("emoji was in inv")
		c.execute('INSERT INTO sell_offers (name, user_id, price) VALUES (?, ?, ?);', (emoji,user_id,price))
		conn.commit()
		return(True)
	else:
		print("Emoji %s was not in %s" % (emoji, inv))
		return(False)

async def buy_emoji(user_id, emoji, price):
	#try:
	c.execute("SELECT name,user_id,price FROM sell_offers WHERE name = ? and price = ?;", (emoji,price))
	rows = c.fetchone()
	print(str(rows))
	if rows:
		cr = "re"
		cr = await get_credits(user_id)
		if int(cr) > rows[2]:
			await add_credits_real(str(rows[1]), str(rows[2]))
			c.execute('DELETE FROM sell_offers WHERE name = ? and price = ?;', (emoji,price))
			conn.commit()
			await remove_item_from_inventory(str(rows[1]), emoji, "1")
			await add_item_to_inventory(user_id, emoji, "1")
			await remove_credits_real(user_id, str(rows[2]))
			await bot.say("Success!")
		else:
			await bot.say("You don't have enough money to buy that! You have %s credits, you need %s more." % (str(cr), str(int(rows[2]) - int(cr))))
	else:
		await bot.say("No offer at that price for that emoji!")
	#except:
	#	await bot.say("No offers for that emoji at that price!")

async def add_user(user_id):
	c.execute("INSERT INTO players (user_id, balance) VALUES (?, 0);", (user_id,))
	conn.commit()
	starterpack(user_id)


async def check_if_investor(user_id):
	c.execute("SELECT balance FROM players WHERE user_id = ?;", (user_id,))
	rows = c.fetchall()
	if rows:
		return(True)
	else:
		return(False)

async def get_inv_by_id(user_id):
	print("Getting inv of " + user_id)
	c.execute("SELECT * FROM inventory_items WHERE user_id = ?;", (user_id,))
	print("Fetched from db")
	rows = c.fetchall()
	print(rows)
	print("Returning...")
	return(rows)

async def get_credits(user_id):
	try:
		print("Getting credits of " + str(user_id))
		c.execute("SELECT balance FROM players WHERE user_id = ?;", (user_id,))
		rows = c.fetchone()
		bal = rows[0]
		bal = str(bal)
		b = re.findall(r'\d+', str(bal))
		b = str(b[0])
		return(str(b))
	except:
		return("0")

async def add_item_to_inventory(user_id, item, quantity):
	try:
		e = await get_inv_by_id(user_id)
		Temp = False
		for i in e:
			if item in i:
				Temp = True
			else:
				pass

		if Temp:
			r = c.execute("UPDATE inventory_items SET quantity = quantity + ? WHERE user_id = ? AND item = ?;", (quantity, user_id, item))
			print(r)
			conn.commit()
		else:
			r = c.execute("INSERT INTO inventory_items (user_id, item, quantity) VALUES (?, ?, ?);", (user_id, item, quantity))
			print(r)
			conn.commit()

	except:
		try:
			print("UPDATE not INSERT")
			r = c.execute("UPDATE inventory_items SET quantity = ? WHERE user_id = ? AND item = ?;", (quantity, user_id, item))
			print(r)
			conn.commit()
		except:
			await bot.say("Something went wrong! Try again, or contact a bot dev.")
			return("broken")

async def remove_item_from_inventory(user_id, item, quantity):
	try:
		e = await get_inv_by_id(user_id)
		Temp = False
		Tmp = False
		for i in e:
			if item in i:
				p = i[2]
				if int(p) > int(quantity):
					Temp = True
				elif p == quantity:
					Tmp = True
				else:
					pass

		if Temp:
			r = c.execute("UPDATE inventory_items SET quantity = quantity - ? WHERE user_id = ? AND item = ?;", (quantity, user_id, item))
			print(r)
			conn.commit()
		elif Tmp:
			r = c.execute("DELETE FROM inventory_items WHERE user_id = ? and item = ? and quantity = ?;", (user_id, item, quantity))
			print(r)
			conn.commit()

		else:
			await bot.say("There's none of that item in the inventory!")
			return("broken")
	except:
			await bot.say("Something went wrong when `Removing item from inventory`! Try again, or contact a bot dev.")
			return("broken")

async def starterpack(user_id):
	if starterpack:
		c.execute("INSERT INTO players (user_id, balance) VALUES (?, 10);", (user_id,))
		#c.execute("INSERT INTO inventory_items (user_id, item, quantity) VALUES (?, ?, ?);", (user_id, emoji, quantity) #test code; ignore
		#Starter pack code goes here

		conn.commit()


setup = os.path.isfile('./marketplace.db')
conn = sqlite3.connect('marketplace.db')
c = conn.cursor()
if setup == False:
	print("setting up DB")
	setup_db()
else:
	print("Already set up DB")




async def username(user_id):
	print("Getting username of " + user_id)
	mem = await bot.get_user_info(user_id)
	return mem.name

async def add_credits_real(user_id, amount):
	print("Adding credits to " + user_id + "with $" + amount + " being added")
	#try:
	cr = await get_credits(user_id)
	if str(cr) == "0":
		c.execute("INSERT INTO players (user_id, balance) VALUES (?, ?)", (user_id, amount))
		print("Had to insert; not update")
	else:
		c.execute("UPDATE players SET balance = balance + ? WHERE user_id = ?", (amount, user_id))
		print("Had to update; not insert")
	conn.commit()

async def remove_credits_real(user_id, amount):
	print("Removing credits from " + user_id + "with $" + amount + " being removed")
	#try:
	cr = await get_credits(user_id)
	if str(cr) == "0":
		c.execute("INSERT INTO players (user_id, balance) VALUES (?, ?)", (user_id, 0 - int(amount)))
		print("Had to insert; not update")
	else:
		c.execute("UPDATE players SET balance = balance - ? WHERE user_id = ?", (amount, user_id))
		print("Had to update; not insert")
	conn.commit()
	
	#except:
	#	await bot.say("Errored; check your command")


#Player commands

@bot.command(pass_context=True,aliases=["inventory","balance","credits","bal"])
async def inv(ctx, user_id=None):
	"""Show your inventory: !inv [player]"""
	if user_id == None:
		print("Setting UID")
		user_id = ctx.message.author.id

	if user_id.isdigit() == False:
		user_id = re.findall('\d+', user_id)[0]
	rows = await get_inv_by_id(user_id)
	credits = await get_credits(user_id)
	credits = str(credits)
	global cred_emoji	
	cred_emoji_temp = cred_emoji
	if user_id == "247096918923149313":
		
		cred_emoji = ":yen:"

	
	if not rows:
		await bot.say("I am sorry, but " + await username(user_id) + " has no items in their inventory!\n**Their Ectoplasm balance is " + cred_emoji + " " + credits + ".**")
	else:
		#await bot.say("**__This is the inventory of" + username(user_id) + "__**:")
		inventory = "**" + await username(user_id) + "**:\n"
		for row in rows:
			inventory+=str(row[1]) + " x " + str(row[2]) + "\n"
			#await bot.say(" - " + str(row[1]) + " x " + str(row[2]))
		inventory+="\n**Ectoplasm balance: " + cred_emoji + " " + credits + ".**"
		await bot.say(inventory)
	cred_emoji = cred_emoji_temp

@bot.command(pass_context=True)
async def market(ctx, emoji=None):
	await get_sell_offers(emoji)

@bot.command(pass_context=True)
async def sell(ctx, emoji, price):
	if not await add_sell_offer(ctx.message.author.id, emoji, price):
		await bot.say("You don't have that item in your inventory to sell!")
	else:
		await bot.say("Item added to the market!")

@bot.command(pass_context=True)
async def buy(ctx, emoji, price=None):
	await buy_emoji(ctx.message.author.id, emoji, price)
	#await bot.say("Done hopefully")




#GM Commands
#TODO: Actually check if user is GM




@bot.command(pass_context=True)
async def add_item(ctx, user_id, item, quantity):
	if user_id.isdigit() == False:
		user_id = re.findall('\d+', user_id)[0]
	await add_item_to_inventory(user_id, item, quantity)
	await bot.say("Copy that! *(I hope)*")

@bot.command(pass_context=True)
async def remove_item(ctx, user_id, item, quantity):
	if user_id.isdigit() == False:
		user_id = re.findall('\d+', user_id)[0]
	await remove_item_from_inventory(user_id, item, quantity)
	await bot.say("Copy that! *(I hope)*")


@bot.command(pass_context=True)
async def add_credits(ctx, user_id, amount):
	if user_id.isdigit() == False:
		user_id = re.findall('\d+', user_id)[0]
	await add_credits_real(user_id, amount)
	await bot.say("Copy that! *(I hope)*")


@bot.command(pass_context=True)
async def interface(ctx, action, *, request):
	if action == "die" and ctx.message.author.id == MAIN_BOT_ID:
		try:
			await add_user(request)
			await bot.say("Done: " + request)
		except:
			await bot.say("Some error occured with request " + request)





@bot.command(pass_context=True,aliases=["test"])
async def ping(ctx):
	await bot.say("Hello! I am alive!")



print("running bot")
bot.run(BOT_TOKEN)
