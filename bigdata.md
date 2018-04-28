# Big-Data collection
In telegram there are so called supergroups with up to 100.000 members.

How about collecting online stats of all the members of some of these supergroups?

## Idea / Approach
With `channel_get_members` you get a list of all members and a `when` property.

This is the `last online` information. If it is in the future, the user is online.

Doing this every 5 minutes will cover the whole online activity of all members.

### Why not load the members list and listen for online status updates?
I tried this and got only notified if someone is offline now (the `when` property of the `channel_get_members` result is not in the future anymore).

### How to find such supergroups
There are serval sites like [this one](https://tgram.io/) where you can find big supergroups.

If you're crazy, you can code a crowler to find all big groups listed on such sites, join automaticly and fetch the members periodically.

(You may need some disk space to log every 5 minutes json objects of all the members in all the goups...)
