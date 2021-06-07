# ejabberd-firebase-auth
A python script for authenticating ejabberd users with Firebase Authentication



https://www.ejabberd.im/files/doc/dev.html#htoc9


4.0.1  External

The external authentication script follows the erlang port driver API.

That script is supposed to do theses actions, in an infinite loop:

read from stdin: AABBBBBBBBB.....
A: 2 bytes of length data (a short in network byte order)
B: a string of length found in A that contains operation in plain text operation are as follows:
auth:User:Server:Password (check if a username/password pair is correct)
isuser:User:Server (check if it’s a valid user)
setpass:User:Server:Password (set user’s password)
tryregister:User:Server:Password (try to register an account)
removeuser:User:Server (remove this account)
removeuser3:User:Server:Password (remove this account if the password is correct)
write to stdout: AABB
A: the number 2 (coded as a short, which is bytes length of following result)
B: the result code (coded as a short), should be 1 for success/valid, or 0 for failure/invalid
