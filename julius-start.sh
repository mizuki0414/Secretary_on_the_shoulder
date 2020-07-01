#! /bin/sh
julius -C main.jconf -C am-gmm.jconf -module > /dev/null &
echo $!
sleep 2
