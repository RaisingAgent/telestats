# Big-Data collection
In telegram there are so called supergroups with up to 100.000 members.

How about collecting online stats of all the members of some of these supergroups?

## Idea / Approach
Unlike `dialog_list`, `channel_get_members` list only the members without notifying me in the future when they go on- or offline.

Unless I call `channel_get_members` every few seconds.

So I wrote a simple python script to connect to the telegram-cli via tcp and run the `channel_get_members` every second.

### How to find such supergroups
There are serval sites like [this one](https://tgram.io/) where you can find big supergroups.

If you're crazy, you can code a crowler to find all big groups listed on such sites, join automaticly and fetch the members periodically.

(You may need some disk space to log every 5 minutes json objects of all the members in all the goups...)


## How to / Usage
Use tmux to run the cli and scripts at the same time.

### Get the permanent peer id's of the supergroups
1. Join the supergroups
2. Run the telegram-cli with the `--permanent-peer-ids` argument
3. Get the id of each group with the `channel_info` command (`channel_info Ripple_XRP`)
4. Memorize them, write them down, or copy and pate them into a note.

### Run the telegram-cli
Run the telegram-cli with following arguments
```bash
tg/bin/telegram-cli --json -WRdL ~/capturefile01 -P 3731
```

### Run the python script
Run bigdata.py with the peer id's of the supergroups (without the `$`) as arguments
```bash
python bigdata.py 0500000044a6694b41479c673aff81a4 05000000247fa94036920aece5573a0a 050000004316da4304554e7a3b2f1727 05000000f1395647b061e174007154c2 050000006e8e76450464f31a62b1dd24 050000009345f947cc6a9b7fc570d146
```


### Check if it's working
```bash
tail -f ~/capturefile01
```

### Analyze the data
```bash
python telestats/telestats.py capturefile01 -i
```
