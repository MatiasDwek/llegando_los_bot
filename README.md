# llegando_los_bot

Bot for the Telegram app. It uses the [telepot](https://github.com/nickoala/telepot) library. It send citations from a list that is hardcoded in the project. It was made for personal uses. The instructions coded are:

+ **set_schedule_time** - Schedule the time when the bot sends the citations. It should be called with one argument, which is the time, e.g.: /set_schedule_time 14:30. Format of the time should be HOUR:MINUTE, with 0 <= HOUR < 24 and 0 <= MINUTE < 60 (no a.m./p.m. format supported). By default the schedule's time is 12:00.


+ **set_schedule** - Toggle on/off the schedule option. It should be called with one argument, which is either 'on' or 'off', e.g.: /set_schedule on. By default, it is on.


+ **set_schedule_period** - Period by which the scheduler sends citations, in days. The days where DAY_NUMBER % PERIOD equals 0 are the days when the bot will send the citations. So, if the period is 1, the bot will send citations every day. If period is 2, every other day. It should be called with one argument, which is an integer between 1 and 31, e.g.: /set_schedule_period 2. By default, the period is 1.


+ **oh_si** - Manually sends a citation.