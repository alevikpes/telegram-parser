[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner2-direct.svg)](https://stand-with-ukraine.pp.ua)


# telegram-bot

This script logs in as a user and can perform actions on behalf of
the currently logged in user.

At the moment it can get all the groups, where the user is subscribed and get
a list of users of some of those groups. This script cannot get the users
of any group due to some kind of restrictions, which the group admins
place for in the groups.

Get the [**source code**](https://github.com/alevikpes/telegram-parser.git)
from github.


### Initialisation

##### User application
In order to start using this bot, it is necessary to obtain **API ID** and
**API HASH** for your user account.

It can be done via https://my.telegram.org/.
Enter your phone number, verify with the sent code and go to the
**API Development Tools** page. There create an app and copy API ID
and API HASH.

##### Bot
If there is a plan to use a bot, then the bot must be created via the
**BotFather** in any Telegram application. See
[**Telegram instructions**](https://core.telegram.org/bots#3-how-do-i-create-a-bot).
Such bot will have a name and a token, which also must be stored.

**NOTE** Bots cannot perform all the actions, so the creation of the
user application, as desribed above, may be necessary for certain tasks.

**WARNING** Never give anyone the credentials of neither your
user application nor your bot. Also add to the ignore list of your VCS,
the files, which have the credentials stored.


### Setup

##### Environment variables
Create a file `.env` and save there the **API ID**, the **API HASH**,
the **bot name**, the **bot token**, a **database name** (can be any),
a **session name** (can be any) and, possibly, other required data in
the following format (see `env.example`):
```
APP_API_HASH=<your api hash>
APP_API_ID=<your api id>
DB_NAME=<your database name>
SESSION_NAME=<your session name>
TG_BOT_NAME=<bot name>
TG_BOT_TOKEN=<bot token>
...
```

**NOTE** Do not use spaces or other special characters in your custom names.

**WARNING** Never give anyone the credentials of neither your
user application nor your bot. Also add to the ignore list of your VCS,
the files, which have the credentials stored.


##### Initialisation
Make sure you are in the root of your project's directory, since the following steps will
create necessary directories and files. Make file `init-project.bash` an
executable:
```bash
sudo chmod +x init-project,bash  # needs to be done once
```
The above setup only needs to be done once.

##### Starting the project
Every time you want to start your project just run the file:
```bash
./init-project.bash
```
This will populate the environment variables from the `.env` file and
create an sqlite database file with two tables `group` and `user`, if it
doesn't exist yet. The name of the file will be read from the environment
variable **DB_NAME**. See `init.py` for more details.


### Parsing

After the initialisation it is all ready for parsing channels and users.

**NOTE** Always start your virtual environment before executing the sripts:
```bash
source /path/to/virtual-environment/bin/activate
```

Run `main.py` to start the parsing:
```bash
python main.py
```
The script will parse the channels
and save their info and the data of the participants of those channels into
the database.

In order to parse only one channel, use -g optional argument with the cahnnel
`username` (the name which starts with `@` symbol and can be found in the
channel info page, specifying `@` is not necessary):
```bash
python main.py -g <channel username>
```
