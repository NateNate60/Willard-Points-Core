# Thank you for choosing NateNate60's Willard Points Core! If you encounter bugs, please raise an issue on the
# Github repo: https://github.com/NateNate60/Willard-Points-Core. You are free to modify and adapt the program
# to fit your specific needs under the GNU General Public License. This program is provided to you free of
# charge, but tips are very much accepted.
#
# Bitcoin: bc1q4zj35klcnerem0fpzer5usrjpzhcc9xg0e9cwu
# Bitcoin Cash: pt3kuf9ekd47glwgpq87d5ulw945ssfevggafatjr
# Ether and USDC: 0xCFC331eaa62Cd11ef720463C6795cE1636894843
import prawcore.exceptions as e
while True :
    try :
        # NateNate60's Willard Points Bot
        version = "3.1"

        print ("Starting NateNate60 Willard Points Core version", version)

        # Module importation
        print ("Importing modules...", end='')
        import praw
        import config
        import time as t
        import datetime
        import os.path
        print ('done')
        print ("Loading features...", end='')

        # On or Off. You can still run it if off, but nothing will actually happen
        on = True

        # Set the tick
        tick = 0

        # Login function
        def login() :
            print ("Connecting to Reddit")
            print ("Authenticating...", end='')
            r = praw.Reddit(username = config.username,
                            password = config.password,
                            client_id = config.client_id,
                            client_secret = config.client_secret,
                            user_agent = config.username)
            print ('done')
            return r


        """
        Core running functionality
        """


        # Retrieve the queue of transactions to be processed
        def retrieve() :
            with open ("transactions.txt", "r") as queuefile :
                queue = queuefile.read()
                queue = queue.split('\n')
            open('transactions.txt', 'w').close()

            return queue


        #Set the signature
        signature = config.signature
        #signature = "\n \n ^NateNate60's ^Willard ^Points ^Bot ^v" + version + "\n\n" + "Don't be alarmed if the bot replied to you more than once. This is because the bot keeps corrupting its own memory and I can't figure out why."

        # The acutal code
        def run_bot(r, tick, timen, queue, replied_to, time, blacklist) :
            if on == True :
                for trans in queue :
                    trans = str(trans)
                    if "~" in trans and "+" not in trans :
                        trans = trans.split('~')
                        user = trans[0]
                        if os.path.isfile (user + ".txt") :
                            with open (user + ".txt", 'r') as u :
                                balance = u.read()
                            balance = int(balance) - int(trans[1])
                            if balance < 0 :
                                balance = balance + int(trans[1])
                                notify (r, user, balance, trans[1], 0)
                            with open (user + ".txt", 'w') as s :
                                s.write(str(balance))
                            with open ('log.txt', 'a') as log :
                                log.write ("\n" + time + ' ' + user + " paid " + trans[1] + ' ' + unit + ".")
                                print (time + ' ' + user + " paid " + trans[1] + ".")
                            notify(r, user, balance, trans[1], '~')

                    elif "+" in trans and "~" not in trans :
                        trans = trans.split('+')
                        user = trans[0]
                        if os.path.isfile (user + ".txt") :
                            with open (user + ".txt", 'r') as u :
                                balance = u.read()
                            balance = int(balance) + int(trans[1])
                            with open (user + ".txt", 'w') as s :
                                s.write(str(balance))
                            with open ('log.txt', 'a') as log :
                                log.write ("\n" + time + ' ' + user + " gained " + trans[1] + ' ' + unit + ".")
                                print (time + ' ' + user + " gained " + trans[1] + ".")
                            notify(r, user, balance, trans[1], '+')
                if tick%2 == 0 :
                    for message in r.inbox.unread(limit = 5) :
                        if message.author.name not in config.blacklist :
                            #For opening new accounts
                            if "!newacc" in message.body or "!openacc" in message.body or "!createacc" in message.body :
                                accname = str(message.author)
                                if not os.path.isfile(accname + ".txt") and "bot" not in message.body.lower() :
                                    accowner = accname
                                    with open (accname + ".txt", 'w') as newacc :
                                        newacc.write ("0")
                                    message.reply ('Account creation successful. '
                                                   + signature)
                                    with open ('log.txt', 'a') as log :
                                        log.write ("\n" + time + ' ' + accowner + " opened an account.")
                                        print (time + ' ' + accowner + " opened an account.")
                                    
                                else :
                                    if "bot" not in message.body.lower() :
                                        message.reply ('Account creation failed. You already have an account.'
                                                       + signature)


                            #For querying information
                            elif "!inf" in message.body.lower() or "!help" in message.body.lower() :
                                message.reply (config.info + "\n\n Powered by NateNate60's [Willard Points Core](https://github.com/NateNate60/Willard-Points-Core) version " + version)
                            #For moderators adding or removing money from people's accounts administratively.
                            elif "+" in message.body or '~' in message.body :
                                if message.author not in config.approved :
                                    message.reply ('You are not authorised to make that command.' + signature)
                                else :
                                    trans = message.body
                                    if "~" in trans :
                                        trans = trans.split('~')
                                        user = trans[0]
                                        if os.path.isfile(user + ".txt") :
                                            with open (user + ".txt", 'r') as u :
                                                balance = u.read()
                                            balance = int(balance) - int(trans[1])
                                            if balance < 0 :
                                                balance = 0
                                                message.reply ("That user does not have enough " + config.unit + ", so their balance was set to zero." + signature)
                                            else :
                                                message.reply ("The command completed successfully." + signature)
                                            with open (user + ".txt", 'w') as s :
                                                s.write(str(balance))
                                            with open ('log.txt', 'a') as log :
                                                log.write ("\n" + time + ' ' + user + " was docked " + trans[1] + config.unit + " by "  + str(message.author))
                                                print (time + ' ' + user + " was docked " + trans[1] + config.unit + " by "  + str(message.author))
                                            notify(r, user, balance, trans[1], '~~')
                                        else :
                                            message.reply ("That account does not exist." + signature)
                                    elif "+" in trans :
                                        trans = trans.split('+')
                                        user = trans[0]
                                        if os.path.isfile(user + ".txt") :
                                            with open (user + ".txt", 'r') as u :
                                                balance = u.read()
                                            balance = int(balance) + int(trans[1])
                                            message.reply ("The command completed successfully. " + signature)
                                            with open (user + ".txt", 'w') as s :
                                                s.write(str(balance))
                                            with open ('log.txt', 'a') as log :
                                                log.write ("\n" + time + ' ' + user + " was awarded " + trans[1] + config.unit + " by "  + str(message.author))
                                            notify(r, user, balance, trans[1], '++')
                                        else :
                                            message.reply ("That account does not exist." + signature)

                            #Balance checking
                            elif "!bal" in message.body :
                                payload = message.body.split(" ")
                                if len(payload) < 2 :
                                    message.reply ('Invalid syntax. Try !balance [username]')
                                else :
                                    if len(payload) == 1 :
                                        payload.append(message.author.name)
                                    if os.path.isfile(payload[1] + ".txt") :
                                        with open (payload[1] + ".txt") as acc :
                                            bal = acc.read()
                                        message.reply("That account currently has " + bal + ' ' + config.unit + "." + signature)
                                    else :
                                        message.reply ("That account does not exist. Use !newaccount" + signature)

                            # Transferring
                            elif "!trans" in message.body :
                                payload = message.body
                                payload = payload.split(' ')
                                try :
                                    to = payload [2]
                                    amt = int(payload [1])
                                    if amt < 1 :
                                        raise ValueError
                                    fromfile = str(message.author) + ".txt"
                                    if os.path.isfile(fromfile) :
                                        if os.path.isfile(to + ".txt") :
                                            with open (fromfile, 'r') as f :
                                                balance = int(f.read())
                                                balance = balance - amt
                                                if balance < 0 :
                                                    message.reply("Insufficient balance. You don't have enough " + config.unit + ". You have " + str(balance) + " " + config.unit + "." + signature)
                                                else :
                                                    with open ('transactions.txt', 'a') as trans :
                                                        trans.write("\n" + str(message.author) + "~" + str(amt))
                                                        trans.write('\n' + to + "+" + str(amt))
                                                    message.reply ("Successfully sent " + str(amt) + " to " + to + ". You have " + str(balance) + " " + config.unit+ " left." + signature)
                                        else :
                                            message.reply ("Invalid recepient. Make sure you spelled the recepient's username correctly." + signature)
                                    else :
                                        message.reply ("Invalid sender. You do not have an account. Use !newaccount to create a new account." + signature)
                                except ValueError :
                                    message.reply("Invalid amount. Ensure that the amount is a number and that it's greater than zero." + signature)
                            elif "!isup" in message.body.lower() or "!stat" in message.body.lower() :
                                message.reply ("Online." + signature)
                            r.inbox.mark_read([message])
                write_comment_list(replied_to)

        def notify (r, user, balance, amt, sign) :
            if sign == '~' :
                r.redditor(user).message(config.unit + ' were debited from your account', str(amt) + config.unit + ' were deducted from your account. \n \n'
                                         + 'You have ' + str(balance) + config.unit + " left.")
            elif sign == '+' and int(amt) > 1 :
                r.redditor(user).message(config.unit + ' were credited to your account', str(amt) + config.unit + " were added to your account. \n \n"
                                         + 'You have ' + str(balance) + config.unit + " now.")
            elif sign == '~~' :
                r.redditor(user).message(config.unit + ' were debited to your account', str(amt) + config.unit + ' were deducted from your account. \n \n'
                                         + 'You have ' + str(balance) + config.unit + " left.")
            elif sign == '++' :
                r.redditor(user).message(config.unit + ' were credited to your account', str(amt) + config.unit + ' were added to your account. \n \n'
                                         + 'You have ' + str(balance) + config.unit + " now.")
            elif sign == '0' :
                r.redditor(user).message('Attempted overdraw detected', "An attempt was made to overdraw your account. No points were deducted and the transaction has been cancelled. You have " + str(balance) + config.unit)

        def get_comment_list() :
            with open ("comments.txt", "r") as f :
                comments_replied_to = f.read()
                comments_replied_to = comments_replied_to.split("\n")
            return comments_replied_to
        def write_comment_list(replied_to) :
            with open ('comments.txt', 'w') as file :
                for i in replied_to :
                    file.write (i + '\n')
        def write_crp(crp) :
            with open ('crp.txt', 'w') as file :
                for i in crp :
                    file.write (i + '\n')
        def get_crp() :
            with open ("crp.txt", "r") as f :
                crp = f.read()
                crp = crp.split("\n")
            return crp
        print ('done')
        
        
        
        
        
        
        
        
        
        
        replied_to = get_comment_list()
        r = login()
        blacklist = config.blacklist
        time = datetime.datetime.fromtimestamp(t.time()).strftime('%Y-%m-%d %H:%M:%S')
        print ("Right now, it's " + time)
        while True :
            replied_to = get_comment_list()
            tick += 1
            timen = int(t.time())
            time = datetime.datetime.fromtimestamp(t.time()).strftime('%Y-%m-%d %H:%M:%S')
            queue = retrieve()
            run_bot(r, tick, timen, queue, replied_to, time, blacklist)
            if tick == 1 :
                print (time + ": The bot has successfully completed one cycle.")
            elif tick == 5 :
                print (time + ": The bot has successfully completed five cycles.")
            elif tick%10 == 0 and tick < 99 :
                print (time + ": The bot has successfully completed " + str(tick) + " cycles.")
            elif tick%100 == 0 and tick < 999 :
                print (time + ": The bot has successfully completed " + str(tick) + " cycles.")
            elif tick%1000 == 0 and tick > 999:
                print (time + ": The bot has successfully completed " + str(tick) + " cycles.")

            t.sleep(10)
    except e.RequestException :
        print ('The bot crashed with RequestException. Restarting...')
        continue
    except e.ResponseException :
        print ('The bot crashed with Error 503: ResponseException. Restarting...')
        continue
    except ValueError :
        print ('The bot crashed with ValueError. Restarting...')
        continue
    except PermissionError :
        print ('The bot crashed with PermissionError. Restarting...')
        continue
    except e.Forbidden :
        print ('The bot crashed because it recieved a 503 HTTP error. Restarting...')
        continue












