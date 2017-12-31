# Specification by randium

_**Note**: some subtle details like the actual command words and status messages have been modified from this original specification. Additionally, some extra functionality like the status and stop commands have been added._

When setting up, the bot should have the following steps;
1. The @Game Master role should be found with `!setGM @Game Master`
2. The channel called #tavern should be found with `!setTavern`
3. The channel called #haunted_house should be found with `!setSpookyHouse`

Step 1 can only be done by an administrator, while step 2 and 3 can be done by any @Game Masters.
In #haunted_house, the bot deletes every message that is being sent, except for its own (of course) and messages sent by @Game Masters and administrators. Note my grammar, it deletes messages that are being sent; it does not delete any messages from before `!setSpookyHouse` was typed, nor does it delete any messages that were sent when the bot was offline.
What it also does, is that it has a giant database of words. Every 15 seconds, the bot randomly picks 9 words (strings) out of the giant database (array of strings), and display them like this;
**BOO!** It's time for the **#tavern** to be haunted! Choose a word, and make up sentences! Choose one of the following words!
```
1. <word1>
2. <word2>
3. <word3>
4. <word4>
5. <word5>
6. <word6>
7. <word7>
8. <word8>
9. <word9>
Make a choice by typing the number of your choice in this chat!
```

Obviously, typing 5 will give you `<word5>`, and typing 3 will give you `<word3>`. Each message will be checked before it gets deleted. If it contains only a number from 1 to 9, then it will pick that word. The message will be deleted, and replaced by
``` Ah-ha! @<user> has chosen the word <wordN>! ```

Then, the bot will check if the last character in the chosen string is a `.`, a `!` or a `?` If not, then the bot will add `<wordN>` to its string (which is the sentence), wait 15 seconds, and repeat this process. If the string does end with either of those characters, then the following will happen;
The string `<wordN>` will be added to the long string (the sentence), and the sentence is being displayed in #tavern. Then, all messages sent by the Ghost Bot will be deleted in #haunted_house. The bot will wait 15 seconds, and then start over.
The bot also has a counter for inactivity. If nobody responds to its message after 60 seconds, the bot will delete its message, wait 5 minutes and resend its message with refreshed words.
