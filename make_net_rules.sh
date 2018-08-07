myMac=$(cat /sys/class/net/wlan0/address)
file=/etc/udev/rules.d/70-persistent-net.rules

echo 'SUBSYSTEM=="ieee80211", ACTION=="add|change", ATTR{macaddress}=="'$myMac'", KERNEL=="phy0", \' > $file
echo '  RUN+="/sbin/iw phy phy0 interface add ap0 type __ap", \' >> $file
echo '  RUN+="/bin/ip link set ap0 address '$myMac'"' >> $file

chmod 644 $file


