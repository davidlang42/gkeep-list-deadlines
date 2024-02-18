#!/usr/bin/bash
set -eu

# set user's password from environment variables
if [ -z "${PLAYER_PASSWORD}" ]; then
    echo "Must set environment variable PLAYER_PASSWORD"
    exit 1 # failed
fi
echo "$PLAYER_USERNAME:$PLAYER_PASSWORD" | chpasswd

set -x

# install additional packages
if ! [ -f install_packages ]
then
    echo "Creating default install_packages"
    echo "# These packages are installed by apt-get on container start" > install_packages
    chown ${PLAYER_USERNAME}:${PLAYER_USERNAME} install_packages
    chmod 660 install_packages
fi
apt-get update
for package in $(cat install_packages | grep -v '^ *#' | sed 's/#.*$//')
do
    apt-get install -y $package
done

# run startup script
if ! [ -f run_on_startup.sh ]
then
    echo "Creating default run_on_startup.sh"
    echo "#!/usr/bin/bash" > run_on_startup.sh
    echo "# This script is run (as root) on container start" >> run_on_startup.sh
    chown ${PLAYER_USERNAME}:${PLAYER_USERNAME} run_on_startup.sh
    chmod 770 run_on_startup.sh
fi
./run_on_startup.sh

# start the ssh server
/usr/sbin/sshd -D