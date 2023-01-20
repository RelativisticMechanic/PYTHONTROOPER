# PYTHONTROOPER
Pythontrooper - A recreation of Paratrooper but in python (pygame).
![The Game](https://github.com/RelativisticMechanic/PYTHONTROOPER/blob/main/screenshot.jpg)

Paratrooper was a DOS game released in 1982 by Orion software. The game came in a DOS .COM exectuable as PARATROOPER.COM and if you were a 2000s kid like me, you'd accidentally stumble upon such goodies on a stray floppy disk or old hard drive. I played this game quite a bit as a child, so it holds a very personal place in my heart. 

Of course, Windows x64 no longer comes with NTVDM (NT Virtual DOS Machine) as Virtual 8086 Mode is only permitted in 32-bit Protected mode on Intel and AMD CPUs. People usually need DOSBox to play a DOS .COM or MZ EXE executable.

Anyways, this is my recreation of it. It's not perfect. The code is not very efficient, of course, it can be improved. One thing I'd like to do is to remove the dependency on data files and generate game data at runtime, as the sprites are not very complicated.

## The Game
You are a artilleryman placed on a faraway base that is about to be ambushed by the bad guys. Your objective? Shoot their helicopters and planes down before they either bomb your base to smithereens or get their paratroopers high enough to snipe down your base!

* Killing a paratrooper - <b>10 points</b>.
* Shooting down a helicopter - <b>30 points</b>
* Shooting down a jet - <b>50 points</b>

Each artillery fire costs <b>5 points</b>, so be careful!

## Losing criteria
* <b>3 hits</b> from an aircraft bomb will destroy your base. You can shoot the falling bombs with your artillery to destroy them before they reach!
* If you allow <b>5 paratroopers to stack themselves on top of each other</b>, they will snipe down your base with a laser guided RPG.

## Controls
Left and Right keys to move your artillery. Space to shoot.


