#!/bin/sh
exec sshpass -p 'xx' ssh -t -o StrictHostKeyChecking=accept-new -o PreferredAuthentications=password -o PubkeyAuthentication=no root@2.28.50.109 'cd /root && /root/.opencode/bin/opencode'
