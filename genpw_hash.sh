#!/bin/bash

genpwd ()
{
        cat /dev/urandom | tr -dc '!-_a-~' | head -c $1
}

echo -n "Enter the universal salt (as defined in config.py, empty for a new salt): "
read SALT_UNI
echo -n "Enter the new password (empty for a random one): "
read PASSWORD

echo "== STARTING GENERATION =="
## SALT_UNI:
if [ -z "$SALT_UNI" ]; then
	SALT_UNI=$(genpwd 10)
	echo "Your new universal salt (write into config.py): $SALT_UNI"
else
	echo "Your universal salt: $SALT_UNI"
fi
## PASSWORD:
if [ -z "$PASSWORD" ]; then
	PASSWORD=$(genpwd 10)
	echo "Your new password (keep in mind): $PASSWORD"
else
	echo "Your password: $PASSWORD"
fi
## SALT:
SALT=$(genpwd 10)
echo "Your new user salt (write into database): $SALT"
## HASH:
HASH=$(echo -n "$PASSWORD$SALT_UNI$SALT" | sha1sum | cut -d ' ' -f 1)
echo "Your password hash (double salted, write into database): $HASH"
