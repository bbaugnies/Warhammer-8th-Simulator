from __future__ import division
import Tkinter as tk

from Tkinter import Tk, W, E, END, IntVar, StringVar, BooleanVar, Toplevel, Canvas, Scrollbar, Frame
from ttk import Frame, Button, Style
from ttk import Entry, Label, OptionMenu, Checkbutton, Notebook
from tkFileDialog import asksaveasfile, askopenfile
from functools import partial
from re import *
from copy import *
from math import *
from random import randint
import os
import matplotlib.pyplot as plt
import numpy


'''
Need to test temp rules (set roundcount to 2 in debug mode)
Need to save/load mount rules
Need to update unit files
'''

num = []
turnOrder = []
resultText = ""
itercount = 10000
roundcount = 12
#In debug mode, only do one round and activate console logging
debug = False   
if debug:
    itercount = 1
    roundcount = 1

#Tkinter structures (Frames, notebooks, canvas...)
root = tk.Tk()
title = "Warhammer Sim"
if debug: title = "TEST MODE - " + title + " - TEST MODE"
root.wm_title(title)
canvas = tk.Canvas(root, borderwidth=0)
frame = tk.Frame(canvas)
ruleNotebooks = (Notebook(frame), Notebook(frame))
unitFrames = (tk.Frame(ruleNotebooks[0]), tk.Frame(ruleNotebooks[1]))
mountFrames = (tk.Frame(ruleNotebooks[0]), tk.Frame(ruleNotebooks[1]))
draftFrames = (tk.Frame(ruleNotebooks[0]), tk.Frame(ruleNotebooks[1]))
for i in range(2):
    ruleNotebooks[i].add(unitFrames[i], text = "Unit")    
    ruleNotebooks[i].add(mountFrames[i], text = "Mount")
vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)

vsb.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((10,10), window=frame, anchor="nw")

frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))


# Global variables
statValues = ["WS", "S", "T", "W", "I", "A", "Ld", "AS", "Wa", "C"]
nstats= len(statValues)
names = [StringVar(frame), StringVar(frame)]
stats=(dict(), dict())
mountStatValues = ["WS", "S", "I", "A"]
mountStats = [dict(), dict()]
#numbers format: [unit][0=size, 1=rank]
numbers=((IntVar(frame), IntVar(frame)), (IntVar(), IntVar()))
baseSizeOptions=["20mm", "25mm", "40mm", "50mm"]
baseSizes = (StringVar(frame), StringVar(frame))
mountTypeOptions = ["Foot", "Cavalry", "Monstrous Cavalry", "Chariot", "Monster"]
mountTypes = (StringVar(frame), StringVar(frame))
rules=(dict(), dict())
ruleOptions=["Always Strikes First", "Always Strikes Last", "Armour Piercing", "BSB",
    "Has Champion", "Immune to Psychology", "Ignore Save",  
    "Monstrous Support", "Mounted", "Stomp", "Stubborn", "Thunderstomp", "Unbreakable", "Unstable"]
ruleOptions=sorted(ruleOptions)
valueRules=["Auto-wound", "Bonus To-Hit", "Bonus To-Wound", "Extra Attack", "Fear", "Fight in Extra Ranks", "Killing Blow",
    "Static CR", "To-Hit Penalty", "To-Wound Penalty"]
valueRules=sorted(valueRules)
tempRules = ["1st Turn Attack Bonus", "1st Turn Strength Bonus", "Until-Loss Attack Bonus"]
tempRules = sorted(tempRules)
diceRules=["Multiple Wounds", "Random Attacks"]
diceRules=sorted(diceRules)
rerolls=["To-Hit", "To-Wound", "Save", "Ward"]
rerolls=sorted(rerolls)
rerollOptions=["1s", "6s", "Failures", "Successes"]
armyRules=["Cold-blooded", "Demonic Instability", "Predation", "Strength in Numbers"]
armyRules=sorted(armyRules)

mountRules = (dict(), dict())
mountRuleOptions = deepcopy(ruleOptions)
for i in ["BSB", "Has Champion", "Immune to Psychology", "Monstrous Support", "Mounted", "Stomp", "Stubborn", "Thunderstomp", "Unbreakable", "Unstable"]:
    mountRuleOptions.remove(i)
mountValueRules = deepcopy(valueRules)
for i in ["Fear", "Fight in Extra Ranks", "Static CR"]:
    mountValueRules.remove(i)
mountTempRules = deepcopy(tempRules)
for i in []:
    mountTempRules.remove(i)
mountDiceRules = deepcopy(diceRules)
for i in []:
    mountDiceRules.remove(i)
mountRerolls = deepcopy(rerolls)
for i in ["Save", "Ward"]:
    mountRerolls.remove(i)

resBox = StringVar(frame, "")
    
    
# Fills all the frames
def populate(frame):
    nextRow=0

    # Unit Names
    unitLabel1 = Label(frame, text="Unit 1:")
    unitLabel1.grid(row=nextRow, columnspan=nstats, sticky=W)    
    unitLabel2 = Label(frame, text="Unit 2:")
    unitLabel2.grid(row=nextRow, column=nstats, columnspan=nstats, sticky=W)  
    nextRow+=1 
    unitName1 = Entry(frame, width= 30, textvariable=names[0])
    unitName1.grid(row=nextRow, columnspan=nstats, sticky=W)
    unitName2 = Entry(frame, width= 30, textvariable=names[1])
    unitName2.grid(row=nextRow, column=nstats, columnspan=nstats, sticky=W)
    nextRow+=1
    
    # Stats
    for i in range(nstats):
        Label(frame, text=statValues[i]).grid(row=nextRow, column=i, padx=5)
        Label(frame, text=statValues[i]).grid(row=nextRow, column=i+nstats, padx=5)
        stats[0][statValues[i]] = IntVar(frame)
        stats[1][statValues[i]] = IntVar(frame)
        Entry(frame, textvariable=stats[0][statValues[i]], width=2).grid(row=nextRow+1, column=i, padx=2)
        
    for i in range(nstats):
        Entry(frame, textvariable=stats[1][statValues[i]], width=2).grid(row=nextRow+1, column=i+nstats, padx=2)
        
    nextRow+=2
    for i in range(2):
        for j in range(nstats):
            if statValues[j] in mountStatValues:
                mountStats[i][statValues[j]] = IntVar(frame)
                Entry(frame, textvariable=mountStats[i][statValues[j]], width=2).grid(row=nextRow, column=j+i*nstats, padx=2)
    nextRow+=1
            
    
    
    
    #Unit numbers
    Label(frame, text="Unit size:").grid(row=nextRow, sticky=W, columnspan=nstats//2)
    size1 = Entry(frame, textvariable=numbers[0][0], width= 10)
    size1.grid(row=nextRow, column=nstats//2, columnspan=nstats//2, sticky=W)
    size1.insert(END, "1")
    size1.delete(0)
    Label(frame, text="Unit size:").grid(row=nextRow, column=nstats, sticky=W, columnspan=nstats//2)
    size2 = Entry(frame, textvariable=numbers[1][0], width= 10)
    size2.grid(row=nextRow, column=nstats+nstats//2, columnspan=nstats//2, sticky=W)
    size2.insert(END, "1")
    size2.delete(0)
    nextRow+=1
    
    Label(frame, text="Rank size:").grid(row=nextRow, sticky=W, columnspan=nstats//2)
    rank1 = Entry(frame, textvariable=numbers[0][1], width= 10)
    rank1.grid(row=nextRow, column=nstats//2, columnspan=nstats//2, sticky=W)
    rank1.insert(END, "1")
    rank1.delete(0)
    Label(frame, text="Rank size:").grid(row=nextRow, column=nstats, sticky=W, columnspan=nstats//2)
    rank2 = Entry(frame, textvariable=numbers[1][1], width= 10)
    rank2.grid(row=nextRow, column=nstats+nstats//2, columnspan=nstats//2, sticky=W)
    rank2.insert(END, "1")
    rank2.delete(0)
    nextRow+=1
	
	
	#Weapons, Base width, and mount type
    #for w in weapons:
    #    w.set(weapChoices[0])
    for b in baseSizes:
        b.set(baseSizeOptions[0])
    for m in mountTypes:
        m.set(mountTypeOptions[0])
    mopt = tuple([mountTypeOptions[0]]+mountTypeOptions)   
    
    for i in range(2):
        Label(frame,text="Base Width:").grid(row=nextRow+1, column= i*nstats, sticky=W, columnspan=nstats//2)
        apply(OptionMenu, (frame, baseSizes[i]) + tuple([baseSizeOptions[0]]+baseSizeOptions)).grid(row=nextRow+1, column=nstats//2+i*nstats, sticky=W, columnspan=nstats//2)
    nextRow+=3
    
    
    #Rules        
    ruleNotebooks[0].grid(row = nextRow, sticky=W, columnspan = nstats)
    ruleNotebooks[1].grid(row = nextRow, column = nstats, sticky = W, columnspan = nstats)
    nextRow += 1
    mountTabRow = nextRow
    
    
    for j in range(2):
        ruleNotebooks[j].tab(1, state = "disabled")
        Label(unitFrames[j], text="Special Rules:").grid(row=nextRow, sticky=W, columnspan=nstats*2)
        Label(mountFrames[j], text="Special Rules:").grid(row=nextRow, sticky=W, columnspan=nstats*2)
        
        for i in range(len(ruleOptions)):
            Label(unitFrames[j], text=ruleOptions[i]).grid(row=nextRow+1+i, column=0, columnspan=nstats//3, sticky=W)
            rules[j][ruleOptions[i]]=BooleanVar(unitFrames[j])
            Checkbutton(unitFrames[j], variable=rules[j][ruleOptions[i]], command = partial(checkMount, j, ruleOptions[i])).grid(row=nextRow+1+i, column=nstats//3+1)
            
        for i in range(len(mountRuleOptions)):
            Label(mountFrames[j], text=mountRuleOptions[i]).grid(row=nextRow+1+i, column=0, columnspan=nstats//3, sticky=W)
            mountRules[j][mountRuleOptions[i]]=BooleanVar(mountFrames[j])
            Checkbutton(mountFrames[j], variable=mountRules[j][mountRuleOptions[i]]).grid(row=nextRow+1+i, column=nstats//3+1)

        nextRow+=len(ruleOptions)+1 
        mountTabRow+=len(mountRuleOptions)+1 
        Label(unitFrames[j], text="Special Rules with flat values:").grid(row=nextRow, sticky=W, columnspan=nstats*2)
        Label(mountFrames[j], text="Special Rules with flat values:").grid(row=nextRow, sticky=W, columnspan=nstats*2)
        
        for i in range(len(valueRules)):
            Label(unitFrames[j], text=valueRules[i]).grid(row=nextRow+1+i, column=0, columnspan=nstats//3, sticky=W)
            rules[j][valueRules[i]]=(BooleanVar(unitFrames[j]),IntVar(unitFrames[j]))
            Checkbutton(unitFrames[j], variable=rules[j][valueRules[i]][0]).grid(row=nextRow+1+i, column=nstats//3+1)
            Entry(unitFrames[j], textvariable=rules[j][valueRules[i]][1], width=2).grid(row=nextRow+1+i, column=nstats//3+2)            
        
        for i in range(len(mountValueRules)):
            Label(mountFrames[j], text=mountValueRules[i]).grid(row=nextRow+1+i, column=0, columnspan=nstats//3, sticky=W)
            mountRules[j][mountValueRules[i]]=(BooleanVar(mountFrames[j]),IntVar(mountFrames[j]))
            Checkbutton(mountFrames[j], variable=mountRules[j][mountValueRules[i]][0]).grid(row=nextRow+1+i, column=nstats//3+1)
            Entry(mountFrames[j], textvariable=mountRules[j][mountValueRules[i]][1], width=2).grid(row=nextRow+1+i, column=nstats//3+2)
            
            
        nextRow+=len(valueRules)+1 
        mountTabRow+=len(mountValueRules)+1 
        Label(unitFrames[j], text="Temporary Rules:").grid(row=nextRow, sticky=W, columnspan=nstats*2)
        Label(mountFrames[j], text="Temporary Rules:").grid(row=nextRow, sticky=W, columnspan=nstats*2)
        
        for i in range(len(tempRules)):
            Label(unitFrames[j], text=tempRules[i]).grid(row=nextRow+1+i, column=0, columnspan=nstats//3, sticky=W)
            rules[j][tempRules[i]]=(BooleanVar(unitFrames[j]),IntVar(unitFrames[j]), True)
            Checkbutton(unitFrames[j], variable=rules[j][tempRules[i]][0]).grid(row=nextRow+1+i, column=nstats//3+1)
            Entry(unitFrames[j], textvariable=rules[j][tempRules[i]][1], width=2).grid(row=nextRow+1+i, column=nstats//3+2)            
        
        for i in range(len(mountTempRules)):
            Label(mountFrames[j], text=mountTempRules[i]).grid(row=nextRow+1+i, column=0, columnspan=nstats//3, sticky=W)
            mountRules[j][mountTempRules[i]]=(BooleanVar(mountFrames[j]),IntVar(mountFrames[j]), True)
            Checkbutton(mountFrames[j], variable=mountRules[j][mountTempRules[i]][0]).grid(row=nextRow+1+i, column=nstats//3+1)
            Entry(mountFrames[j], textvariable=mountRules[j][mountTempRules[i]][1], width=2).grid(row=nextRow+1+i, column=nstats//3+2)
            
        nextRow+=len(tempRules)+1  
        mountTabRow+=len(mountTempRules)+1 
        Label(unitFrames[j], text="Special Rules with random values:").grid(row=nextRow, sticky=W, columnspan=nstats*2)
        Label(mountFrames[j], text="Special Rules with random values:").grid(row=nextRow, sticky=W, columnspan=nstats*2)
        
        for i in range(len(diceRules)):
            Label(unitFrames[j], text=diceRules[i]).grid(row=nextRow+1+i, column=0, columnspan=nstats//3, sticky=W)
            rules[j][diceRules[i]]=(BooleanVar(unitFrames[j]),IntVar(unitFrames[j]), IntVar(unitFrames[j]))
            Checkbutton(unitFrames[j], variable=rules[j][diceRules[i]][0]).grid(row=nextRow+1+i, column=nstats//3+1)
            Entry(unitFrames[j], textvariable=rules[j][diceRules[i]][1], width=2).grid(row=nextRow+1+i, column=nstats//3+2)
            Label(unitFrames[j], text="d").grid(row=nextRow+1+i, column=nstats//3+3)
            OptionMenu(unitFrames[j], rules[j][diceRules[i]][2], 1, 1, 3, 6).grid(row=nextRow+1+i, column=nstats//3+4)
            
        for i in range(len(mountDiceRules)):
            Label(mountFrames[j], text=mountDiceRules[i]).grid(row=nextRow+1+i, column=0, columnspan=nstats//3, sticky=W)
            mountRules[j][mountDiceRules[i]]=(BooleanVar(mountFrames[j]),IntVar(mountFrames[j]), IntVar(mountFrames[j]))
            Checkbutton(mountFrames[j], variable=mountRules[j][mountDiceRules[i]][0]).grid(row=nextRow+1+i, column=nstats//3+1)
            Entry(mountFrames[j], textvariable=mountRules[j][mountDiceRules[i]][1], width=2).grid(row=nextRow+1+i, column=nstats//3+2)
            Label(mountFrames[j], text="d").grid(row=nextRow+1+i, column=nstats//3+3)
            OptionMenu(mountFrames[j], mountRules[j][mountDiceRules[i]][2], 1, 1, 3, 6).grid(row=nextRow+1+i, column=nstats//3+4)
            
            
        nextRow+=len(diceRules)+1
        
        #Impact hits get their own thing
        Label(unitFrames[j], text="Impact Hits").grid(row=nextRow , column=0, columnspan=nstats//3, sticky=W)
        rules[j]["Impact Hits"]={
            "active": BooleanVar(unitFrames[j]),
            "dAmount": IntVar(unitFrames[j]),
            "dSize": IntVar(unitFrames[j]),
            "staticHits": IntVar(unitFrames[j]),
            "strength": IntVar(unitFrames[j])
        }
        Checkbutton(unitFrames[j], variable=rules[j]["Impact Hits"]["active"]).grid(row=nextRow, column=nstats//3+1)
        Entry(unitFrames[j], textvariable=rules[j]["Impact Hits"]["dAmount"], width=2).grid(row=nextRow, column=nstats//3+2)
        Label(unitFrames[j], text="d").grid(row=nextRow, column=nstats//3+3)
        OptionMenu(unitFrames[j], rules[j]["Impact Hits"]["dSize"], 1, 1, 3, 6).grid(row=nextRow, column=nstats//3+4)        
        Label(unitFrames[j], text="+").grid(row=nextRow, column=nstats//3+5)
        Entry(unitFrames[j], textvariable=rules[j]["Impact Hits"]["staticHits"], width=2).grid(row=nextRow, column=nstats//3+6)
        Label(unitFrames[j], text="S").grid(row=nextRow, column=nstats//3+7)
        Entry(unitFrames[j], textvariable=rules[j]["Impact Hits"]["strength"], width=2).grid(row=nextRow, column=nstats//3+8)
        
        nextRow += 1
        mountTabRow+=len(mountDiceRules)+1 
        Label(unitFrames[j], text="Reroll rules:").grid(row=nextRow, sticky=W, columnspan=nstats*2)
        Label(mountFrames[j], text="Reroll rules:").grid(row=nextRow, sticky=W, columnspan=nstats*2)
        
        for i in range(len(rerolls)):
            Label(unitFrames[j], text=rerolls[i]).grid(row=nextRow+1+i, column=0, columnspan=nstats//3, sticky=W)
            rules[j][rerolls[i]]=(BooleanVar(unitFrames[j]), StringVar(unitFrames[j]))
            Checkbutton(unitFrames[j], variable=rules[j][rerolls[i]][0]).grid(row=nextRow+1+i, column=nstats//3+1)
            apply(OptionMenu, (unitFrames[j], rules[j][rerolls[i]][1]) + tuple([rerollOptions[0]]+rerollOptions)).grid(row=nextRow+1+i, column=nstats//3+2, sticky = W, columnspan=nstats//3)
        
        for i in range(len(mountRerolls)):
            Label(mountFrames[j], text=mountRerolls[i]).grid(row=nextRow+1+i, column=0, columnspan=nstats//3, sticky=W)
            mountRules[j][mountRerolls[i]]=(BooleanVar(mountFrames[j]), StringVar(mountFrames[j]))
            Checkbutton(mountFrames[j], variable=mountRules[j][mountRerolls[i]][0]).grid(row=nextRow+1+i, column=nstats//3+1)
            apply(OptionMenu, (mountFrames[j], mountRules[j][mountRerolls[i]][1]) + tuple([rerollOptions[0]]+rerollOptions)).grid(row=nextRow+1+i, column=nstats//3+2, sticky = W, columnspan=nstats//3)
        
        
        nextRow+=len(rerolls)+1
        mountTabRow+=len(mountRerolls)+1 
        Label(unitFrames[j], text="Army Specific Rules:").grid(row=nextRow, sticky=W, columnspan=nstats*2)
        
        for i in range(len(armyRules)):
            Label(unitFrames[j], text=armyRules[i]).grid(row=nextRow+1+i, column=0, columnspan=nstats//3, sticky=W)
            rules[j][armyRules[i]]=BooleanVar(unitFrames[j])
            Checkbutton(unitFrames[j], variable=rules[j][armyRules[i]]).grid(row=nextRow+1+i, column=nstats//3+1)
        
    Label(frame, textvariable = resBox).grid(row=1, column = 2*nstats +1, columnspan=nstats, rowspan= 2* nstats)
        
    
    for i in range(2):
        Button(frame, text="Save", command=partial(saveUnit, i)).grid(row=99, column=i*nstats, columnspan=nstats//2)
        Button(frame, text="Load", command=partial(loadUnit, i)).grid(row=99, column=i*nstats+nstats//2, columnspan=nstats//2)
    
    Button(frame, text="Sim", command = sim).grid(row=100, columnspan=10)

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))
    
    
    

#----------------------------------------------------------
#Functions

#Called for all flat rules
#enables or disables the mount tab if it was the "Mounted" rule
def checkMount(unit, rule):
    if rule == "Mounted":
        if rules[unit]["Mounted"].get():
            ruleNotebooks[unit].tab(1, state = "normal")
        else:
            ruleNotebooks[unit].tab(1, state = "disabled")

#
def fearTest(penalty, unit):    
    target = stats[unit]["Ld"].get()-penalty
    dice = [randint(1,6), randint(1,6), randint(1,6)]
    if rules[unit]["Cold-blooded"].get():
        total = sum(dice) - max(dice)
    else:
        total = dice[0] + dice[1]
        
    if total > target and rules[unit]["BSB"].get():
        dice = [randint(1,6), randint(1,6), randint(1,6)]
        if rules[unit]["Cold-blooded"].get():
            total = sum(dice) - max(dice)
        else:
            total = dice[0] + dice[1]
    if debug: print "Fear rolled {}, target {}".format(total, target)
    return total <= target
    
    
# Calculate To-Hit target
# i:        ID of attacker
# wsA:      Weapon skill of attacker
# wsD:      Weapon skill of defender
# rulesA:   rules to use for attacker (defender always uses unit rules)
def toHit(i, wsA, wsD, rulesA):
    if wsA>wsD:
        res = 3
    elif wsA*2<wsD: res=5
    else:   res = 4
    if rulesA[i]["Bonus To-Hit"][0].get(): res-= rulesA[i]["Bonus To-Hit"][1].get()
    if rules[not i]["To-Hit Penalty"][0].get(): res += rules[not i]["To-Hit Penalty"][1].get()
    res = min(6, res)
    res = max(2, res)
    return res

# Calculate To-Wound target
# i:        ID of attacker
# sA:       Strength of attacker
# tD:       Toughness of defender
# rulesA:   rules to use for attacker (defender always uses unit rules)
def toWound(i, sA, tD, rulesA):
    res = 4+tD-sA
    res = max(2, res)
    if rulesA[i]["Bonus To-Wound"][0].get(): res-= rulesA[i]["Bonus To-Wound"][0].get()
    if rules[not i]["To-Wound Penalty"][0].get(): res+= rules[not i]["To-Wound Penalty"][0].get()
    res = min(6, res)
    res = max(1, res)
    return res

# Calculate Armor save target
# Note that here, attacker and defender are reversed
# i:        ID of attacker
# aA:       Armor of attacker
# sD:       Strength of defender
# rulesD:   rules to use for defender (attacker always uses unit rules)
def saveTarget(i, aA, sD, rulesD):
    if rulesD[not i]["Ignore Save"].get(): res = 7
    else:
        res = aA if aA != 0 else 7
        if rulesD[not i]["Armour Piercing"].get():    res += 1
        if sD>3 :  res += sD-3
    res = min(7, res)
    res = max(2, res)
    return res
        

#Return the combatStats of both units
#These are the target rolls for hitting, wounding, saving, and wards
#as well as the order of attack (1 for first, -1 for second, 0 for simultaneous)
#turn: the number of the turn
def getStats(turn):
    s = (dict(), dict())
    ms = (dict(), dict())
    #copy ws, mount ws, and strength because they get modified
    ws = [stats[0]["WS"].get(), stats[1]["WS"].get()]
    mws = [mountStats[0]["WS"].get(), mountStats[1]["WS"].get()]
    strength = [stats[0]["S"].get(), stats[1]["S"].get()]
    ini = (stats[0]["I"].get(), stats[1]["I"].get())
    mIni = (mountStats[0]["I"].get(), mountStats[1]["I"].get())
    weap = (weapons[0].get(), weapons[1].get())
    
    #First loop, things where the other's stats influence targets
    for i in range(2):    
        if turn == 0:
            if rules[i]["1st Turn Strength Bonus"][0].get():
                strength[i] += rules[i]["1st Turn Strength Bonus"][1].get()
        if rules[not i]["Fear"][0].get() and not rules[i]["Immune to Psychology"].get():
            if not fearTest(rules[not i]["Fear"][1].get(), i):
                ws[i] = 1
                mws[i] = 1                
                
    #Second loop, determine target rolls
    for i in range(2):
        #To Hit
        s[i]["To-Hit"] = toHit(i, ws[i], ws[not i], rules)
        ms[i]["To-Hit"] = toHit(i, mws[i], ws[not i], mountRules)
        
        #To Wound
        s[i]["To-Wound"] = toWound(i, strength[i], stats[not i]["T"].get(), rules)
        ms[i]["To-Wound"] = toWound(i, mountStats[i]["S"].get(), stats[not i]["T"].get(), mountRules)
        
        #Armor Save
        s[i]["Save"] = saveTarget(i, stats[i]["AS"].get(), stats[i]["S"].get(), rules)
        ms[i]["Save"] = saveTarget(i, stats[i]["AS"].get(), mountStats[i]["S"].get(), mountRules)        
        
        #Ward Save
        s[i]["Ward"] = stats[i]["Wa"].get() if stats[i]["Wa"].get() != 0 else 7
        ms[i]["Ward"] = stats[i]["Wa"].get() if stats[i]["Wa"].get() != 0 else 7
        
    #This part is only usefull for rerolls, rest is taken care of by setTurnOrder
        s[i]["Priority"] = rules[i]["Always Strikes First"].get() - rules[i]["Always Strikes Last"].get()
        ms[i]["Priority"] = mountRules[i]["Always Strikes First"].get() - mountRules[i]["Always Strikes Last"].get()
    
    if s[i]["Priority"]==1 and ini[i]>=ini[not i] and s[not i]["Priority"]<1:
        rules[i]["To-Hit"][0].set(True)
        rules[i]["To-Hit"][1].set("Failures")
    if s[not i]["Priority"]==1 and ini[not i]>=ini[i] and s[i]["Priority"]<1:
        rules[not i]["To-Hit"][0].set(True)
        rules[not i]["To-Hit"][1].set("Failures")
        
    if ms[i]["Priority"]==1 and mIni[i]>=ini[not i] and s[not i]["Priority"]<1:
        mountRules[i]["To-Hit"][0].set(True)
        mountRules[i]["To-Hit"][1].set("Failures")
    if ms[not i]["Priority"]==1 and mIni[not i]>=ini[i] and s[i]["Priority"]<1:
        mountRules[not i]["To-Hit"][0].set(True)
        mountRules[not i]["To-Hit"][1].set("Failures")
        
    return (s, ms)


    
    
    
#Sets the global var turnOrder to contain the ordered list of attackers
#Order is a nested list. Each top-level entry is a list of units attacking at the same time
#Each inner entry contains the ID and attack type
#(Unit, Mount, Stomp, Thunderstomp, Impact Hits)
def setTurnOrder(turn):
    global turnOrder
    global resultText
    turnOrder= []
    tempOrder = []
    
    #Create Temp list, which has ini/mod in addition to other fields.
    #mod = 200 for impact, 100 for ASF, -100 for ASL
    for i in range(2):
        ini = stats[i]["I"].get()
        mod = (rules[i]["Always Strikes First"].get() - rules[i]["Always Strikes Last"].get()) * 100
        if mod != 0:    tempOrder.append((mod, i, "Unit"))
        else:           tempOrder.append((ini, i, "Unit"))
            
        if rules[i]["Mounted"].get():
            ini = mountStats[i]["I"].get()
            mod = (mountRules[i]["Always Strikes First"].get() - mountRules[i]["Always Strikes Last"].get()) * 100
            if mod != 0:    tempOrder.append((mod, i, "Mount"))
            else:           tempOrder.append((mountStats[i]["I"].get(), i, "Mount"))
        
        if rules[i]["Stomp"].get():
            tempOrder.append((-100, i, "Stomp"))
        
        if rules[i]["Thunderstomp"].get():
            tempOrder.append((-100, i, "Thunderstomp"))
            
        if rules[i]["Impact Hits"]["active"].get() and turn == 0 and rules[i]["Has Charged"].get():
            tempOrder.append((200, i, "Impact Hits"))
            
    #Sort on ini/mod, group by equal value, and drop ini/mod
    tempOrder = sorted(tempOrder, key=lambda unit: unit[0], reverse=True)
    turnOrder.append([(tempOrder[0][1], tempOrder[0][2])])
    for i in range(1, len(tempOrder)):
        if tempOrder[i][0] == tempOrder[i-1][0]:
            turnOrder[-1].append((tempOrder[i][1], tempOrder[i][2]))
        else:
            turnOrder.append([(tempOrder[i][1], tempOrder[i][2])])
    resultText += "Turn Order:\n"
    for i in range(len(turnOrder)):
        s = str(i+1) + " : "
        for u in turnOrder[i]:
            if u[1] != "Unit": s+= u[1] + " of "
            s+= names[u[0]].get() +"; "
        resultText += s[:-2] + "\n"
    resultText+= "\n"
            
            
    
    

#Get the number of attacks a unit will do and
#   the number of models in base contact in the first rank
#unit: the identifier of the attacking unit (0 or 1)
#losses: the amount of models the unit lost before attacking
#        (only non-0 if the unit attacks second)    
def getAttacks(unit, losses, attackType, turn):
    if num[unit][0] == 0 or num[unit][1] == 0:
        return 0
    if debug: print attackType
            
    if attackType == "Unit":
        apm = stats[unit]["A"].get()
        if weapons[unit].get()=="Two Weapons":      apm+=1
        if rules[unit]["Extra Attack"][0].get():    apm+=rules[unit]["Extra Attack"][1].get()
        if rules[unit]["1st Turn Attack Bonus"][0].get() and turn == 0:
            rules[unit]["1st Turn Attack Bonus"][1].get()
        if rules[unit]["Until-Loss Attack Bonus"][0].get() and rules[unit]["Until-Loss Attack Bonus"][2]:
            rules[unit]["Until-Loss Attack Bonus"][1].get()
    elif attackType == "Mount":
        apm = mountStats[unit]["A"].get()
        if mountRules[unit]["Extra Attack"][0].get():    apm+=mountRules[unit]["Extra Attack"][1].get()
        if mountRules[unit]["1st Turn Attack Bonus"][0].get() and turn == 0:
            mountRules[unit]["1st Turn Attack Bonus"][1].get()
        if mountRules[unit]["Until-Loss Attack Bonus"][0].get() and mountRules[unit]["Until-Loss Attack Bonus"][2]:
            mountRules[unit]["Until-Loss Attack Bonus"][1].get()
    elif attackType == "Impact Hits":
        apm = rules[unit]["Impact Hits"]["staticHits"].get()
    elif attackType == "Thunderstomp":
        apm = 0
    else: apm = 1
        
    available = int(num[unit][0]) - losses
    available = int(ceil(available/stats[unit]["W"].get()))
    av_enemy = int(ceil(num[not unit][0] / stats[not unit]["W"].get()))
    
    #current fronts of both units
    r = [min(available, int(num[unit][1])), min(av_enemy, int(num[not unit][1]))]
    width = [int(baseSizes[unit].get()[:-2]), int(baseSizes[not unit].get()[:-2])]
    #front in mm
    r= [r[0]*width[0], r[1]*width[1]]
    availableWidth = min(r)
    #maximum models in attacking unit that are in contact
    widthConstraint = ceil(availableWidth/width[0]) + (2 if availableWidth%width[0] == 0 else 1)
    
    #Handle all randomly rolled attacks
    firstRank=int(min(available, int(num[unit][1]), widthConstraint))
    attacks = firstRank*(apm)
    if attackType == "Unit" and rules[unit]["Random Attacks"][0].get():
        for i in range(firstRank):
            for j in range(rules[unit]["Random Attacks"][1].get()):
                attacks += randint(1, rules[unit]["Random Attacks"][2].get())
    if attackType == "Mount" and mountRules[unit]["Random Attacks"][0].get():
        for i in range(firstRank):
            for j in range(mountRules[unit]["Random Attacks"][1].get()):
                attacks += randint(1, mountRules[unit]["Random Attacks"][2].get())
    if attackType == "Impact Hits":
        for i in range(firstRank):
            for j in range(rules[unit]["Impact Hits"]["dAmount"].get()):
                attacks += randint(1, rules[unit]["Impact Hits"]["dSize"].get())
    if attackType == "Thunderstomp":
        for i in range(firstRank):
            attacks += randint(1, 6)
    
    #Support attacks, unit only
    available-=int(num[unit][1])
    if attackType == "Unit":
        supportRanks = 1
        if int(num[unit][1])>=10 and not rules[unit]["Monstrous Support"].get(): supportRanks+=1
        if int(num[unit][1])>=6 and rules[unit]["Monstrous Support"].get(): supportRanks+=1
        if weapons[unit].get()=="Spear (foot)": supportRanks+=1
        if rules[unit]["Fight in Extra Ranks"][0].get():
            supportRanks += rules[unit]["Fight in Extra Ranks"][1].get()
        while supportRanks > 0 and available > 0:
            rankAttacks = int(min(available, int(num[unit][1]), widthConstraint)) * min(1, stats[unit]["A"].get())
            if rules[unit]["Monstrous Support"].get():            
                attacks += min(rankAttacks * apm, rankAttacks * 3)
                if rules[unit]["Random Attacks"][0].get():
                    for i in range(rankAttacks):
                        for j in range(rules[unit]["Random Attacks"][1].get()):
                            attacks += min(3-apm, randint(1, rules[unit]["Random Attacks"][2].get()))                
            else:
                attacks += rankAttacks
            available -= int(num[unit][1])
            supportRanks-=1
            
    attacks = max(0, attacks)
    if attackType == "Unit" and rules[unit]["Has Champion"].get() and attacks != 0: attacks += 1
    return attacks
   
    
def calcRerolls(attacker, cstats, stat, rules):
    r = randint(1, 6)
    if rules[attacker][stat][0].get():
        reroll = rules[attacker][stat][1].get()
        if reroll=="1s" and r == 1:
            if debug:
                print "rolled {} to {}, rerolling".format(r, stat)
            r=randint(1,6)
        if reroll=="Failures" and r < cstats[attacker][stat]:
            if debug:
                print "rolled {} to {}, rerolling".format(r, stat)
            r=randint(1,6)
        if reroll=="6s" and r == 6:
            if debug:
                print "rolled {} to {}, rerolling".format(r, stat)
            r=randint(1,6)
        if reroll=="Successes" and r >= cstats[attacker][stat]:
            if debug:
                print "rolled {} to {}, rerolling".format(r, stat)
            r=randint(1,6)
    if debug:
        print "rolled {} to {}, target : {}".format(r, stat, cstats[attacker][stat])
    return r
     
    
#Resolves the attacks of one side, calculating the amount of kills
#attacker: the identifier of the attacking side (0 or 1)
#attacks: the number of attacks carried out
#cstats: the ordered combatStats of both units
def attack(attacker, attacks, cstats, rules):
    if debug:
        print "{} attacks by {}: {}".format(attacks, attacker, cstats)
    wounds = 0
    auto_w = 7
    if rules[attacker]["Auto-wound"][0].get():
        auto_w = rules[attacker]["Auto-wound"][1].get()
    kb = 7
    if rules[attacker]["Killing Blow"][0].get():
        kb = rules[attacker]["Killing Blow"][1].get()
    pred = 0
    for i in range(attacks):
        r = calcRerolls(attacker, cstats, "To-Hit", rules)
        if "Predation" in rules[attacker]:
            if rules[attacker]["Predation"].get() and r == 6:
                pred += 1
        if r < cstats[attacker]["To-Hit"]:
            continue
        
        if r > auto_w:
            r = 0
        else:
            r = calcRerolls(attacker, cstats, "To-Wound", rules)
            if r < cstats[attacker]["To-Wound"]:
                continue
        
        if r > kb:
            r = 0
        else:
            r = calcRerolls(not attacker, cstats, "Save", rules)
            if r >= cstats[not attacker]["Save"]:
                continue
         
        r = calcRerolls(not attacker, cstats, "Ward", rules)
        if r < cstats[not attacker]["Ward"]:
            if debug:
                print "WOUND"
            if rules[attacker]["Multiple Wounds"][0].get():
                dmg = 0
                for i in range(rules[attacker]["Multiple Wounds"][1].get()):
                    dmg += randint(1, rules[attacker]["Multiple Wounds"][2].get())
                wounds += min(dmg, stats[not attacker]["W"].get())
            else:
                wounds += 1
            if debug:
                print wounds
    #TODO make predation more elegant?
    #-----------------PREDATION--------------------------
    for i in range(pred):
        r = calcRerolls(attacker, cstats, "To-Hit", rules)
        if r < cstats[attacker]["To-Hit"]:
            continue
        
        if r > auto_w:
            r = 0
        else:
            r = calcRerolls(attacker, cstats, "To-Wound", rules)
            if r < cstats[attacker]["To-Wound"]:
                continue
        
        if r > kb:
            r = 0
        else:
            r = calcRerolls(not attacker, cstats, "Save", rules)
            if r >= cstats[not attacker]["Save"]:
                continue
         
        r = calcRerolls(not attacker, cstats, "Ward", rules)
        if r < cstats[not attacker]["Ward"]:
            if debug:
                print "WOUND"
            if rules[attacker]["Multiple Wounds"][0].get():
                dmg = 0
                for i in range(rules[attacker]["Multiple Wounds"][1].get()):
                    dmg += randint(1, rules[attacker]["Multiple Wounds"][2].get())
                wounds += min(dmg, stats[not attacker]["W"].get())
            else:
                wounds += 1
            if debug:
                print wounds
    #-----------------PREDATION--------------------------
    
        
    return wounds
    
    
#Calculates the combat resolution
#kills: the number of kills done during the round
#return ([id of the looser], [amount lost by], [if looser is steadfast], [rank bonus of the looser])
def combatResolution(kills):
    global resultText
    result = [kills[0], kills[1]]
    for i in range(2):
        if rules[i]["Static CR"][0].get():
            result[i] += rules[i]["Static CR"][1].get()
    rank=[0, 0]
    for i in range(2):
        left = num[i][0]
        left = int(ceil(left/stats[i]["W"].get()))
        if rules[i]["Has Charged"].get(): result[i]+=1
        if num[i][1] >= 5:
            rank[i] = left//num[i][1] - 1 + (left%num[i][1] >= 5)
        result[i] += min(3, rank[i])
    res = result[0] - result[1]
    steadfast = False
    if res > 0:
        looser = 1
        resultText += names[1].get() + " looses combat by "+ str(round(res,2)) + "\n"
        if rank[1] > rank[0]:
            resultText += names[1].get()+ " is steadfast\n"
            steadfast = True
    elif res < 0:               
        looser = 0 
        resultText += names[0].get() + " looses combat by " + str(round(-res,2)) + "\n"
        if rank[0] > rank[1]:
            resultText += names[0].get() + " is steadfast\n"
            steadfast = True
    else:
        resultText += "combat is tied"
        return 0
    return (looser, res, steadfast, rank[looser])
    
    
# Returns true if break test passed, false otherwise
def breakTest(cr):
    global resultText
    if num[cr[0]][0] <= 0: return False
    if rules[cr[0]]["Unbreakable"].get():
        resultText += "Break test passed, Unbreakable"
        return True
    
    target = stats[cr[0]]["Ld"].get()
    if not cr[2] and not rules[cr[0]]["Stubborn"].get():
        target -= abs(cr[1])
    if rules[cr[0]]["Strength in Numbers"].get():
        target += cr[3]
    dice = [randint(1,6), randint(1,6), randint(1,6)]
    if rules[cr[0]]["Cold-blooded"].get():
        total = sum(dice) - max(dice)
    else:
        total = dice[0] + dice[1]
        
    if total > target and rules[cr[0]]["BSB"].get():
        dice = [randint(1,6), randint(1,6), randint(1,6)]
        if rules[cr[0]]["Cold-blooded"].get():
            total = sum(dice) - max(dice)
        else:
            total = dice[0] + dice[1]
    if total <= target:
        resultText += "Break test passed. Rolled {}, needed {}".format(total, target)
    else:
        resultText += "Break test failed. Rolled {}, needed {}".format(total, target)
    return total <= target
    
        
def demonBreak(cr, losses):
    if num[cr[0]][0] <= 0: return False
    target = max(0, stats[cr[0]]["Ld"].get() - abs(cr[1]))
    total = randint(1, 6) + randint(1, 6)
    if total > 8 and rules[cr[0]]["BSB"].get():
        total = randint(1,6) + randint(1, 6)
    if total == 2:
        num[cr[0]][0] += losses
    elif total <= target:
        pass
    elif total == 12:
        num[cr[0]][0] = 0
    else:
        num[cr[0]][0] -= total - target
    return total <= target


        
#Rules dictionary where all rules are off.
#Used for Impact Hits and (Thunder)Stomp
dummyrules = dict()
for i in ruleOptions+armyRules:
    dummyrules[i] = BooleanVar(frame)
for i in valueRules + diceRules + rerolls:
    dummyrules[i] = [BooleanVar(frame)]
       

#Resolves one round of combat
#roundn: the number of the round
#stats: the ordered combatStats of both units
#mstats: combatStats of both units' mounts
def fightRound(roundn, cstats, mstats):
    global resultText
    global num
    kills =[0, 0]
    attacks = [0, 0]
    first = turnOrder[0][0][0] # =ID of first unit in first turn
    for order in turnOrder:
        orderKills = [0, 0]
        orderAttacks = [0, 0]
        resultText += "---------\n"
        for unit in order:
            att = getAttacks(unit[0], kills[not unit[0]], unit[1], roundn)
            #r = rule dictionary for dummy vs. unit (Impact hits and [thunder]Stomp)
            #mRules = rule dictionary for mount vs. unit
            r= [dict(), dict()]
            r[unit[0]] = dummyrules
            r[not unit[0]] = rules[not unit[0]]
            
            orderAttacks[unit[0]] += att
            k = 0
            if unit[1] == "Unit":
                k = attack(unit[0], att, cstats, rules)
            elif unit[1] == "Mount":
                mRules = [dict(), dict()]
                mRules[unit[0]] = mountRules[unit[0]]
                mRules[not unit[0]] = rules[not unit[0]]
                k = attack(unit[0], att, mstats, mRules)
                
            #TODO refactor this to have getStats used here
            elif unit[1] == "Impact Hits":
                #Re-evaluate combat stats
                #set auto-hit (to-hit = 1), new to-wound, and adapt ennemy's save
                s = deepcopy(cstats)
                s[unit[0]]["To-Hit"] = 1
                s[unit[0]]["To-Wound"] = toWound(unit[0], rules[unit[0]]["Impact Hits"]["strength"].get(), stats[not unit[0]]["T"].get(), r)
                #for save, unit[0] is considered "defender" => use r so no armor piercing/ignore save
                s[not unit[0]]["Save"] = saveTarget(not unit[0], stats[not unit[0]]["AS"].get(), rules[unit[0]]["Impact Hits"]["strength"].get(), r)
                k = attack(unit[0], att, s, r)
            #Stomp and Thunderstomp
            else:
                #same as impact hits, but using S (unit or mound) instead of special strength
                #still has to be done since thb,twb, armor piercing... shouldn't be used.
                strength = mountStats[unit[0]]["S"].get() if rules[unit[0]]["Mounted"].get() else stats[unit[0]]["S"].get()
                s = deepcopy(cstats)
                s[unit[0]]["To-Hit"] = 1
                s[unit[0]]["To-Wound"] = toWound(unit[0], strength, stats[not unit[0]]["T"].get(), r)
                #for save, unit[0] is considered "defender" => use r so no armor piercing/ignore save
                s[not unit[0]]["Save"] = saveTarget(not unit[0], stats[not unit[0]]["AS"].get(), strength, r)
                k = attack(unit[0], att, s, r)
                
            orderKills[unit[0]] += k
            resultText +=   ((unit[1]+ " of ") if unit[1] != "Unit" else "")
            resultText +=   names[unit[0]].get() + " does " + str(round(att, 2))
            resultText +=   " attacks, for " + str(round(k, 2)) + " wounds\n"
                
        for i in range(2):
            kills[i]+=orderKills[i]
            attacks[i]+=orderAttacks[i]
        
        
    resultText += "____________________________________________\n"    
    resultText += names[first].get()+ " does "+ str(round(attacks[first], 2))+ " attacks, for "+ str(round(kills[first], 2)) + " wounds\n"
    resultText += names[not first].get()+ " does "+ str(round(attacks[not first],2))+ " attacks, for "+ str(round(kills[not first],2)) + " wounds\n"
    
    for i in range(0, 2):
        cur = num[i][0]
        cur = cur - kills[not i]
        num[i][0]= cur
    resultText += str(num) + "\n"
    cr = combatResolution(kills)
    # cr[0] = id of looser
    #Looser looses frenzy-type bonuses
    rules[cr[0]]["Until-Loss Attack Bonus"][2] = False
    mountRules[cr[0]]["Until-Loss Attack Bonus"][2] = False
    if cr != 0:
        if rules[cr[0]]["Unstable"].get():
            num[cr[0]][0] = num[cr[0]][0] - abs(cr[1])
        if rules[cr[0]]["Demonic Instability"].get():
            demonBreak(cr, kills[not cr[0]])
        return (breakTest(cr), cr[0])
    else: return (True, "tie")
    
    
class wincounter:
    wins = 0
    rounds = 0
    u_left = 0
    e_left = 0
    
    def __str__(self):
        return "occurence: {}%\naverage rounds: {}\naverage left:{}\naverage enemy left: {}\n-------------------\n".format(self.wins/itercount*100, 0 if self.wins == 0 else self.rounds/self.wins, 0 if self.wins == 0 else self.u_left/self.wins, 0 if self.wins == 0 else self.e_left/self.wins)

def sim():
    global resultText
    global num
    plt.figure(1)
    plt.clf()
    roundReached = numpy.zeros(roundcount)
    alivePerRound = numpy.zeros((roundcount+1)*2).reshape(2, roundcount+1)
    woundsPerRound = numpy.zeros(roundcount*2).reshape(2, roundcount)
    resultPerRound = numpy.zeros(roundcount*3).reshape(3, roundcount)
    resultPerRound_individual = numpy.zeros(roundcount*3).reshape(3, roundcount)
    survivalChance = numpy.zeros(roundcount*2).reshape(2, roundcount)
    
    results = [wincounter(), wincounter(), wincounter()]
    alivePerRound[0][0] = numbers[0][0].get() * stats[0]["W"].get()
    alivePerRound[1][0] = numbers[1][0].get() * stats[1]["W"].get()
    for j in range(itercount):
        #copy number of units for running counts
        num=[[numbers[0][0].get(), numbers[0][1].get()], [numbers[1][0].get(), numbers[1][1].get()]]
        for i in range(2):
            #this will represent numbers of wounds left, not models
            num[i][0]=num[i][0] * int(stats[i]["W"].get())
            #reset frenzy-type bonus
            rules[i]["Until-Loss Attack Bonus"][2] = True
            mountRules[i]["Until-Loss Attack Bonus"][2] = True
        for i in range(roundcount):
            roundReached[i] += 1
            s = getStats(i)
            combatStats = s[0]
            mountCombatStats = s[1]
            setTurnOrder(i)
            curNum = [num[0][0], num[1][0]]
            outcome = fightRound(i, combatStats, mountCombatStats)
            if debug:    
                print resultText
            resultText = ""
            for u in range(2):
                woundsPerRound[u][i] += curNum[u] - num[u][0]
                alivePerRound[u][i+1] += num[u][0]
            if debug:
                print outcome
            if not outcome[0]:
                a = (0 if outcome[1] else 1)
                for r in range(i, roundcount):
                    resultPerRound[a][r] += 1
                    survivalChance[a][r] += 1
                resultPerRound_individual[a][i] += 1
                results[not outcome[1]].wins += 1
                results[not outcome[1]].rounds += i+1
                results[not outcome[1]].u_left += num[not outcome[1]][0]
                results[not outcome[1]].e_left += num[outcome[1]][0]                
                break
            else:
                resultPerRound[2][i] += 1
                resultPerRound_individual[2][i] += 1
                survivalChance[0][i] += 1
                survivalChance[1][i] += 1
        if outcome[0]:
            results[2].wins += 1
            results[2].rounds += i+1
            results[2].u_left += num[0][0]
            results[2].e_left += num[1][0]  
            
            
    #set output string
    resultText += "{} Wins:\n".format(names[0].get())
    resultText += str(results[0])
    resultText += "{} Wins:\n".format(names[1].get())
    resultText += str(results[1])
    resultText += "Draws:\n"
    resultText += str(results[2])
    resultText += "\n"
    resBox.set(resultText)
    #print resultText
    
    
    #plot results
    axis = range(1,roundcount+1)
    axis0 = range(roundcount+1)
    wax1 = []
    wax2 = []
    for i in axis:
        wax1.append(i-0.2)
        wax2.append(i+0.2)
    for u in range(2):
        for i in range(roundcount):
            alivePerRound[u][i+1] = 0 if roundReached[i] == 0 else alivePerRound[u][i+1]/roundReached[i]
            woundsPerRound[u][i] = woundsPerRound[u][i]/itercount
            survivalChance[u][i] = survivalChance[u][i]/itercount*100
    for u in range(3):
        for i in range(roundcount):
            resultPerRound[u][i] = resultPerRound[u][i]/itercount*100
            resultPerRound_individual[u][i] = 0 if roundReached[i] == 0 else resultPerRound_individual[u][i]/roundReached[i]*100
    for i in range(roundcount):
        roundReached[i] = roundReached[i]/itercount*100
    plt.subplot(321)
    plt.plot(axis0, alivePerRound[0], "b-", label = names[0])
    plt.plot(axis0, alivePerRound[1], "r-", label = names[1])
    plt.ylabel("Wounds remaining")
    plt.subplot(322)
    plt.bar(wax1, woundsPerRound[1], 0.40, color="b")
    plt.bar(wax2, woundsPerRound[0], 0.40, color="r")
    plt.ylabel("Wounds done in round")
    plt.subplot(323)
    plt.bar(axis, resultPerRound[0], 0.40, color="b", label = "{} wins".format(names[0]))
    plt.bar(axis, resultPerRound[2], 0.40, color="g", bottom=resultPerRound[0], label = "draws")
    plt.bar(axis, resultPerRound[1], 0.40, color="r", bottom=resultPerRound[2]+resultPerRound[0], label = "{} wins".format(names[1]))
    plt.ylabel("% of occurence (cumulative)")
    plt.subplot(324)
    plt.bar(axis, resultPerRound_individual[0], 0.40, color="b", label = "{} wins".format(names[0]))
    plt.bar(axis, resultPerRound_individual[2], 0.40, color="g", bottom=resultPerRound_individual[0], label = "draws")
    plt.bar(axis, resultPerRound_individual[1], 0.40, color="r", bottom=resultPerRound_individual[2]+resultPerRound_individual[0], label = "{} wins".format(names[1]))
    plt.plot(axis, roundReached, "b-")
    plt.ylabel("% of occurence (per round)")
    plt.subplot(325)
    plt.plot(axis, survivalChance[0], "b-")
    plt.plot(axis, survivalChance[1], "r-")
    plt.ylabel("Change of surviving to this round")
    plt.ion()
    plt.show()
            
    
def saveUnit(n):
    f = asksaveasfile(mode='w', defaultextension=".whs", initialfile=names[n].get())
    #name
    txt = names[n].get()+"\n"
    #stats
    for i in statValues:
        txt += str(stats[n][i].get()) + ","
    txt += "\n"
    #mountstats
    for i in mountStatValues:
        txt += str(mountStats[n][i].get()) + ","
    #base size
    txt +="\n" + baseSizes[n].get() + "\n"
    #rules
    for i in ruleOptions:
        if rules[n][i].get():
            txt += i + ","
    txt += "\n"
    #valuerules
    for i in valueRules:
        if rules[n][i][0].get():
            txt += i +"("+str(rules[n][i][1].get())+"),"
    txt += "\n"
    #temprules
    for i in tempRules:
        if rules[n][i][0].get():
            txt += i +"("+str(rules[n][i][1].get())+"),"
    txt += "\n"            
    #dicerules
    for i in diceRules:
        if rules[n][i][0].get():
            txt +=i +"("+str(rules[n][i][1].get())+";"+ str(rules[n][i][2].get()) +"),"
    txt += "\n"
    #impact hits
    for i in ["Impact Hits"]:
        if rules[n][i]["active"].get():
            txt += i+"("+str(rules[n][i]["dAmount"].get())+";"+str(rules[n][i]["dSize"].get())+";"+str(rules[n][i]["staticHits"].get())+";"+str(rules[n][i]["strength"].get())+")"
    txt += "\n"
    #rerolls
    for i in rerolls:
        if rules[n][i][0].get():
            txt += i +"("+str(rules[n][i][1].get())+"),"
    txt += "\n"
    #armyrules
    for i in armyRules:
        if rules[n][i].get():
            txt += i + ","
    txt += "\n"
    #mountrules
    for i in mounRuleOptions:
        if mountRules[n][i].get():
            txt += i + ","
    txt += "\n"
    #mountValueRules
    for i in MountValueRules:
        if mountRules[n][i][0].get():
            txt += i +"("+str(mountRules[n][i][1].get())+"),"
    txt += "\n"
    #mounttemprules
    for i in mountTempRules:
        if mountRules[n][i][0].get():
            txt += i +"("+str(mountRules[n][i][1].get())+"),"
    txt += "\n"            
    #mountdicerules
    for i in mountDiceRules:
        if mountRules[n][i][0].get():
            txt +=i +"("+str(mountRules[n][i][1].get())+";"+ str(mountRules[n][i][2].get()) +"),"
    txt += "\n"
    #mountrerolls
    for i in mountRerolls:
        if mountRules[n][i][0].get():
            txt += i +"("+str(mountRules[n][i][1].get())+"),"
    txt += "\n"
    
    f.write(txt)
    f.close()
    '''
mountRules = (dict(), dict())
mountRuleOptions = deepcopy(ruleOptions)
for i in ["BSB", "Has Champion", "Immune to Psychology", "Monstrous Support", "Mounted", "Stomp", "Stubborn", "Thunderstomp", "Unbreakable", "Unstable"]:
    mountRuleOptions.remove(i)
mountValueRules = deepcopy(valueRules)
for i in ["Fear", "Fight in Extra Ranks", "Static CR"]:
    mountValueRules.remove(i)
mountTempRules = deepcopy(tempRules)
for i in []:
    mountTempRules.remove(i)
mountDiceRules = deepcopy(diceRules)
for i in []:
    mountDiceRules.remove(i)
mountRerolls = deepcopy(rerolls)
for i in ["Save", "Ward"]:
    mountRerolls.remove(i)
'''
def loadUnit(n):
    #reset rules
    for i in rules[n]:
        if isinstance(rules[n][i], tuple):
            rules[n][i][0].set(False)
        elif isinstance(rules[n][i], dict):
            rules[n][i]["active"].set(False)
        else: rules[n][i].set(False)
    for i in mountRules[n]:
        if isinstance(mountRules[n][i], tuple):
            mountRules[n][i][0].set(False)
        elif isinstance(mountRules[n][i], dict):
            mountRules[n][i]["active"].set(False)
        else: mountRules[n][i].set(False)
        
    f = askopenfile(mode='r', initialdir=os.getcwd()+"../../")
    #name
    l = f.readline()[:-1]
    if l != "":
        names[n].set(l)
    #stats
    l = f.readline()[:-2]
    if l != "":
        s = l.split(",")
        for i in range(nstats):
            stats[n][statValues[i]].set(s[i])
    #mount stats
    l = f.readline()[:-2]
    if l != "":
        s = l.split(",")
        for i in range(len(mountStatValues)):
            mountStats[n][mountStatValues[i]].set(s[i])
    #base size
    l = f.readline()[:-1]
    if l!= "":
        baseSizes[n].set(l)
    #rules
    l = f.readline()[:-2]
    print l
    if l != "":
        s = l.split(",")
        for r in s:
            rules[n][r].set(True)
    #valueRules
    l = f.readline()[:-1]
    if l != "":
        matches = findall("(.*?)\((\d*)\),", l)
        for m in matches:
            rules[n][m[0]][0].set(True)
            rules[n][m[0]][1].set(m[1])
    #temprules
    l = f.readline()[:-1]
    if l != "":
        matches = findall("(.*?)\((\d*)\),", l)
        for m in matches:
            rules[n][m[0]][0].set(True)
            rules[n][m[0]][1].set(m[1])
    #diceRules
    l = f.readline()[:-1]
    if l != "":
        matches = findall("(.*?)\(([\d;]*)\),", l)
        for m in matches:
            rules[n][m[0]][0].set(True)
            v = m[1].split(";")
            rules[n][m[0]][1].set(v[0])
            rules[n][m[0]][2].set(v[1])
    #impact hits
    l = f.readline()[:-1]
    print l
    if l!= "":
        matches = findall("(.*?)\(([\d;]+)\)", l)
        for m in matches:
            rules[n][m[0]]["active"].set(True)
            v = m[1].split(";")
            rules[n][m[0]]["dAmount"].set(v[0])
            rules[n][m[0]]["dSize"].set(v[1])
            rules[n][m[0]]["staticHits"].set(v[2])
            rules[n][m[0]]["strength"].set(v[3])
            
    #rerolls
    l = f.readline()[:-1]
    if l != "":
        matches = findall("(.*?)\((.*?)\),", l)
        for m in matches:
            rules[n][m[0]][0].set(True)
            rules[n][m[0]][1].set(m[1])
    #armyrules
    l = f.readline()[:-2]
    if l != "":
        s = l.split(",")
        for r in s:
            rules[n][r].set(True)
    #toggle mount tab
    checkMount(n, "Mounted")
        
                    
                    

populate(frame)

root.mainloop()