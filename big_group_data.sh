#!/bin/sh

# Crontab usage example
# */5 * * * * telestats/big_group_data.sh tg/bin/telegram-cli capture "Nucleus_Vision_(Official)" "АКТИВИСТ_ДВК" "ICO_HeadStart_-_English" >/dev/null 2>&1

if [ "$#" -lt 3 ]; then
	echo "Usage: $0 path/to/your/telegram-cli path/to/your/capture.file \"printname_of_group_1\" \"printname_of_group_2\" ..." >&2
	exit 1
fi

tg=$1
cap=$2
shift 2

if ! [ -e "$tg" ] || ! [ -f "$tg" ]; then
	echo "Wrong path to telegram-cli: $tg" >&2
	exit 1
fi

for i in "$@"
do
	echo "$i..."
	"$tg" --json -RWe "channel_get_members $i 100000" >> "$cap"
done
echo "Done!"
