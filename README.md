# Team Signal

A Teamspeak3 Singal integration.

## Why?

Every time when a client joins your Teamspeak channel, a Signal message is sent to the given Signal group.

## Deployment example

### Setup

#### 1 signal-cli: 

The Signal messages are sent via signal-ci: https://github.com/AsamK/signal-cli
You can run the cli via docker container or install it natively on the system

You have to register your account and verfiy your phone number to be capable to send messages via cli.

####  Signal group

Setup a Signal group and get the group id. The id is the receiver for the signal-cli command that sends the message. You can get the group id by enabling the join by link feature in Signal for the corresponding group.

#### 3 Teamspeak server query permissions

You need permissions to use the Teamspeak server queries. Find a short instruction here: https://community.teamspeak.com/t/how-to-use-the-server-query/25386

#### 4 Teamsginal Python service

You can setup the Python daemon with systemctl or run it inside a Docker container. The service will need permission to access the signal-cli binary. Don't forget to open the telnet ports for the ts3 library that is based on the telnet protocol. 
