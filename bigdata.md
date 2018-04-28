# Big-Data collection

In telegram there are so called supergroups with up to 100.000 members.

How about collecting online stats of all the members of some of these supergroups?

## Idea / Approach

With `channel_get_members` you get a list of all members and a `when` property.

This is the `last online` information. If it is in the future, the user is online.
