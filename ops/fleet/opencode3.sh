#!/bin/sh
exec ssh -t -i /home/box/.ssh/vps_ed25519 -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new ubuntu@51.222.81.2 "cd ~ && ~/.opencode/bin/opencode"
