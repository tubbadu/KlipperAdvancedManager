#!/usr/bin/bash
text="nothing yet"
cnt=0
while [ "$text" != "" ]; do
  text=`qdbus org.kde.klipper /klipper getClipboardHistoryItem $cnt`
  #echo "==== Clipboard content line $cnt:"
  #echo "$text"                      # to terminal output
  echo -n "$text" > /home/tubbadu/.local/share/klipper/history$cnt.cliptxt      # to file (EDIT this)
  cnt=$((cnt + 1))
done
echo "Done."
