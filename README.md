# Warhammer-8th-Simulator
Battle simulator for Warhammer Fantasy 8th Edition

* sim.py is a warhammer battle simulator that calculates statistical averages for a round of combat.
* sim2.py is similar, but will perform a discreet simulation over 12 rounds of combat and report statistics regarding the different outcomes.
### Known Issues:
* Fear and Immune to Psychology only work in sim2.py
* Mount special rules are currently not supported
* Ridden Monsters/Charriots are currently not supported
* Flanking/Rear attacks not supported (can add static CR bonus, but can't cancel support attacks or disrupt)
* Impact hits not supported
* Can't have 2 different re-rolls on same stat (e.g. 1s and Successes). They sometimes cancel out but not always.
### Army Rules that can't be emulated:
* Nurgle poison generates hit
* Cancel rank bonus (Sisters of Slaughter) (can be emulated with static CR in sim.py, not good enough in sim2.py)
* Force Ld test on 3d6 or highest 2 of 3d6 (VC Banner)
* Taking additional hits during combat (Flagellants, Plague censors...)

