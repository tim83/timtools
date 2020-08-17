#! /bin/bash

bash ~/Programs/python/tools/install.sh

ssync
sshin serverpi -c "ssync"
for dev in laptop serverpi camerapi desktop toshiba ; do
	sshin $dev -s -c "bash ~/Programs/python/tools/install.sh"
done
