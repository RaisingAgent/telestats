# Telestats

Analyze the telegram usage behavior of your contacts and members of public groups to sell the information to Google. Or Cambridge Analytica.

## Usage and how it works

1. First, make the [telegram-cli](https://github.com/vysheng/tg) running on your system.
2. If you wanna capture usage data of more than a few hours, it'd be the best using a server. (or a raspberrypi)
3. Run `telegram-cli` with the following parameters as background process (`&`).
   ```sh
   path/to/your/telegram-cli --json -WRdL capture01 &
   ```
   - The `--json` parameter tells the telegram-cli the we want the output to be in the json format.
   - The `-W` parameter makes the telegram-cli to send a `dialog_list` query.
     - This is necessary because we get the online status update only from the users we have interacted with.
     - So we get only the status update from users we have chatted with.
     - If you want to capture the status update of all your contacts you have to find a way to send a `contact_list` query.
       - One way would be using the `-P` parameter to make the telegram-cli listen on a tcp port and send the query with netcat.
       - If you find a better way (e.g. with pipes) you can write a comment or edit the run.sh and make a pull request.
   - The `-R` parameter is necessary because it causes a linebreak between the stringified json objects.
     - You can see the difference using cat -n path/to/your/capture.file
   - The `-d` parameter activates the daemon mode and is needed to use the log functionality.
   - The `-L` parameter defined that and where (`capture01` in the above shown case) the output should be logged.
   - The `&` makes the process running in the background.
     - If you use this and wanna close the terminal window or the ssh session, you should disown this job before.
     - Alternatively you can use tmux or screen for the process.
4. Check wether the recording is working.
   - You can use tail (`tail -f path/to/your/capture.file`) to watch it and send a telegram message to yourself ("Saved Messages") to see if it's working.
5. Wait some time.
6. Run the python scrip.
   ```sh
   python telestats.py path/to/your/capture.file
   python telestats.py path/to/your/capture.file -d Marcel #shows hourly stats
   ```
   - You don't have to stop the telegram-cli daemon.
   - Check the help (`-h` or `--help`) for some usefull features.
   ```sh
   python telestats.py -h
   ```
   - Check the [output examples](output-examples.md) for some usage examples.

## Big data
Take a look at the [bigdata.md](bigdata.md)

## Examples
Take a look at the [output-examples.md](output-examples.md)

## Why?
I like terminals.

Telegram is a lot better than Whatsapp. (serverside, bots, open source, custom styles,  ...)

I have a little netbook with 2 gigs of RAM (this one on my profile pic).

That's why I've tried the telegram-cli and I love it. It's not as comfortable as the graphical client, but it is in a terminal. And it needs no RAM. Terminals are so productive!

Anyway, using this cli I noticed that I get whenever somebody is now online or offline a message. Of course I get - because on my phone I see if somebody is online and somehow my phone has to get these information.

Since than I thought it would be very interesting to record these information and analyze them.

I thinks the fewest telegram users know that everyone who has their number [(or if they are in a big public group)](bigdata.md) could create statistics about their telegram usage behavior.


## Credits
This project is based on the [telegram-cli](https://github.com/vysheng/tg) of [vysheng](https://github.com/vysheng)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
