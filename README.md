# Warhammer-8th-Simulator
Battle simulator for Warhammer Fantasy 8th Edition

* avg_sim.py is a warhammer battle simulator that calculates statistical averages for a round of combat.
* sim.py simulates actual dice rolls over 12 rounds of combat and reports statistics regarding the different outcomes.

### Disclaimer
Updates regularly break saved unit files, and the files are not compatible between the two simulators.
### Known Issues:
* Fear and Immune to Psychology only work in sim.py
* Characters on Monsters/Charriots are currently not supported
* Flanking/Rear attacks not supported (can add static CR bonus, but can't cancel support attacks or disrupt)
* Can't have 2 different re-rolls on same stat (e.g. 1s and Successes). They sometimes cancel out but not always.
### Army Rules that can't be emulated:
* Cancel rank bonus (Sisters of Slaughter) (can be emulated with static CR in avg_sim.py, not good enough in sim.py)
* Force Ld test on 3d6 or highest 2 of 3d6 (VC Banner)
* Taking additional hits during combat (Flagellants, Plague censors...)

