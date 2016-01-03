Examples
========

MUC interaction (MiniBal)
-------------------------

::

   <Hans> plop Minibal
   <Minibal> plop Hans
   [...]
   <Hans> Minibal: -h
   <Minibal> 
   usage: Minibal:  [-h] {say,time} ...
   
   positional arguments:
     {say,time,taunt}
       say             say something
       time
   [...]
   <Hans> Minibal: say -h
   <Minibal> 
   usage: Minibal: say [-h] text [text ...]
   
   positional arguments:
     text
   [...]
   <Hans> Minibal: say hello, world!
   <Minibal> hello, world!

PM interaction (MiniBal)
------------------------

::

   <Hans> -h
   <Minibal> 
   usage: Minibal:  [-h] {say,time,quit,taunt} ...
   
   positional arguments:
     {say,time,quit,taunt}
       say                 say something
       time
       quit                tells the bot to stop
       taunt               manage taunts
   [...]
   <Hans> taunt add programming, do you speak it, mofo?
   <Hans> taunt --list
   <Minibal>
   1 - programming, do you speak it, mofo? (Hans)
