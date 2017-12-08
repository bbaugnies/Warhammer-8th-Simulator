from __future__ import division
import Tkinter as tk

from Tkinter import Tk, W, E, END, IntVar, StringVar, BooleanVar, Toplevel, Canvas, Scrollbar, Frame
from ttk import Frame, Button, Style
from ttk import Entry, Label, OptionMenu, Checkbutton
from tkFileDialog import asksaveasfile, askopenfile
from functools import partial
from re import *
from copy import *
from math import *
from random import randint
import os
import matplotlib.pyplot as plt
import numpy



num = []
turnOrder = []
resultText = ""
itercount = 10000
roundcount = 12
debug = False
if debug:
    itercount = 1
    roundcount = 1


root = tk.Tk()
root.wm_title("Warhammer Sim")
canvas = tk.Canvas(root, borderwidth=0)
frame = tk.Frame(canvas)
vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)

vsb.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((10,10), window=frame, anchor="nw")

frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))


statValues = ["WS", "S", "T", "W", "I", "A", "Ld", "AS", "Wa", "C"]
nstats= len(statValues)
names = [StringVar(frame), StringVar(frame)]
stats=(dict(), dict())
mountFields=["WS", "S", "I", "A"]
mountStats = [dict(), dict()]
#[unit][0=size, 1=rank]
numbers=((IntVar(frame), IntVar(frame)), (IntVar(), IntVar()))
weapChoices=["Hand Weapon", "Hand Weapon and Shield", "Flail", "Great Weapon", "Halberd",
    "Lance", "Morning Star", "Spear (foot)", "Spear (mounted)", "Two Weapons"]
weapons = (StringVar(frame), StringVar(frame))
baseSizeOptions=["20mm", "25mm", "40mm", "50mm"]
baseSizes = (StringVar(frame), StringVar(frame))
rules=(dict(), dict())
ruleOptions=["Always Strikes First", "Always Strikes Last", "Armour Piercing", "BSB",
    "Devastating Charge", "Has Champion", "Has Charged", "Immune Psychology", "Ignore Save",  
    "Monstrous Support", "Mounted", "Stomp", "Stubborn", "Thunderstomp", "Unbreakable", "Unstable"]
ruleOptions=sorted(ruleOptions)
valueRules=["Auto-wound", "Bonus To-Hit", "Bonus To-Wound", "Extra Attack", "Fear", "Fight in Extra Ranks", "Killing Blow",
    "Static CR", "To-Hit Penalty", "To-Wound Penalty"]
valueRules=sorted(valueRules)
diceRules=["Multiple Wounds", "Random Attacks"]
diceRules=sorted(diceRules)
rerolls=["To-Hit", "To-Wound", "Save", "Ward"]
rerolls=sorted(rerolls)
rerollOptions=["1s", "6s", "Failures", "Successes"]
armyRules=["Cold-blooded", "Demonic Instability", "Predation", "Strength in Numbers"]
armyRules=sorted(armyRules)
combatStatList=["To-Hit", "To-Wound", "Save", "Ward", "Priority"]
resBox = StringVar(frame, "")
    
    

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
            if statValues[j] in mountFields:
                mountStats[i][statValues[j]] = IntVar(frame)
                Entry(frame, textvariable=mountStats[i][statValues[j]], width=2).grid(row=nextRow, column=j+i*nstats, padx=2)
    nextRow+=1
            
    
    
    
    #Unit numbers
    
    
    Label(frame, text="Unit size:").grid(row=nextRow, sticky=W, columnspan=nstats//2)
    size1 = Entry(frame, textvariable=numbers[0][0], width= 10)
    size1.grid(row=nextRow, column=nstats//2, columnspan=nstats//2)        
    Label(frame, text="Unit size:").grid(row=nextRow, column=nstats, sticky=W, columnspan=nstats//2)
    size2 = Entry(frame, textvariable=numbers[1][0], width= 10)
    size2.grid(row=nextRow, column=nstats+nstats//2, columnspan=nstats//2)
    nextRow+=1
    
    Label(frame, text="Rank size:").grid(row=nextRow, sticky=W, columnspan=nstats//2)
    rank1 = Entry(frame, textvariable=numbers[0][1], width= 10)
    rank1.grid(row=nextRow, column=nstats//2, columnspan=nstats//2)
    Label(frame, text="Rank size:").grid(row=nextRow, column=nstats, sticky=W, columnspan=nstats//2)
    rank2 = Entry(frame, textvariable=numbers[1][1], width= 10)
    rank2.grid(row=nextRow, column=nstats+nstats//2, columnspan=nstats//2)
    nextRow+=1
	
	
	#Weapons & base width
    Label(frame, text="Weapons:").grid(row=nextRow, sticky=W, columnspan=nstats)        
    #weapChoices = sorted(weapChoices)       
    for w in weapons:
        w.set(weapChoices[0])
    Label(frame,text="Base Width:").grid(row=nextRow, column=nstats, sticky=W, columnspan=nstats)
    for b in baseSizes:
        b.set(baseSizeOptions[0])
    nextRow+=1
        
    for i in range(2):  
        apply(OptionMenu, (frame, weapons[i]) + tuple([weapChoices[0]]+weapChoices)).grid(row=nextRow, column=i*nstats, sticky = W, columnspan=nstats//2)
        apply(OptionMenu, (frame, baseSizes[i]) + tuple([baseSizeOptions[0]]+baseSizeOptions)).grid(row=nextRow, column=nstats//2+i*nstats, sticky=W, columnspan=nstats//2)
    nextRow+=1
    
    
    #Rules        
    
    
    
    Label(frame, text="Special Rules:").grid(row=nextRow, sticky=W, columnspan=nstats*2)
    
    for i in range(len(ruleOptions)):
        Label(frame, text=ruleOptions[i]).grid(row=nextRow+1+i, column=0, columnspan=nstats//3, sticky=W)
        Label(frame, text=ruleOptions[i]).grid(row=nextRow+1+i, column=nstats, columnspan=nstats//3, sticky=W)
        rules[0][ruleOptions[i]]=BooleanVar(frame)
        rules[1][ruleOptions[i]]=BooleanVar(frame)
        Checkbutton(frame, variable=rules[0][ruleOptions[i]]).grid(row=nextRow+1+i, column=nstats//3+1)
        Checkbutton(frame, variable=rules[1][ruleOptions[i]]).grid(row=nextRow+1+i, column=nstats+nstats//3+1)
        
    nextRow+=len(ruleOptions)+1  
    Label(frame, text="Special Rules with flat values:").grid(row=nextRow, sticky=W, columnspan=nstats*2)
    
    for i in range(len(valueRules)):
        Label(frame, text=valueRules[i]).grid(row=nextRow+1+i, column=0, columnspan=nstats//3, sticky=W)
        Label(frame, text=valueRules[i]).grid(row=nextRow+1+i, column=nstats, columnspan=nstats//3, sticky=W)
        rules[0][valueRules[i]]=(BooleanVar(frame),IntVar(frame))
        rules[1][valueRules[i]]=(BooleanVar(frame),IntVar(frame))
        Checkbutton(frame, variable=rules[0][valueRules[i]][0]).grid(row=nextRow+1+i, column=nstats//3+1)
        Checkbutton(frame, variable=rules[1][valueRules[i]][0]).grid(row=nextRow+1+i, column=nstats+nstats//3+1)
        Entry(frame, textvariable=rules[0][valueRules[i]][1], width=2).grid(row=nextRow+1+i, column=nstats//3+2)
        Entry(frame, textvariable=rules[1][valueRules[i]][1], width=2).grid(row=nextRow+1+i, column=nstats+nstats//3+2)
        
    nextRow+=len(valueRules)+1  
    Label(frame, text="Special Rules with random values:").grid(row=nextRow, sticky=W, columnspan=nstats*2)
    for i in range(len(diceRules)):
        Label(frame, text=diceRules[i]).grid(row=nextRow+1+i, column=0, columnspan=nstats//3, sticky=W)
        Label(frame, text=diceRules[i]).grid(row=nextRow+1+i, column=nstats, columnspan=nstats//3, sticky=W)
        rules[0][diceRules[i]]=(BooleanVar(frame),IntVar(frame), IntVar(frame))
        rules[1][diceRules[i]]=(BooleanVar(frame),IntVar(frame), IntVar(frame))
        Checkbutton(frame, variable=rules[0][diceRules[i]][0]).grid(row=nextRow+1+i, column=nstats//3+1)
        Checkbutton(frame, variable=rules[1][diceRules[i]][0]).grid(row=nextRow+1+i, column=nstats+nstats//3+1)
        Entry(frame, textvariable=rules[0][diceRules[i]][1], width=2).grid(row=nextRow+1+i, column=nstats//3+2)
        Entry(frame, textvariable=rules[1][diceRules[i]][1], width=2).grid(row=nextRow+1+i, column=nstats+nstats//3+2)
        Label(frame, text="d").grid(row=nextRow+1+i, column=nstats//3+3)
        Label(frame, text="d").grid(row=nextRow+1+i, column=nstats+nstats//3+3)
        OptionMenu(frame, rules[0][diceRules[i]][2], 1, 1, 3, 6).grid(row=nextRow+1+i, column=nstats//3+4)
        OptionMenu(frame, rules[1][diceRules[i]][2], 1, 1, 3, 6).grid(row=nextRow+1+i, column=nstats+nstats//3+4)
        
    nextRow+=len(diceRules)+1
    Label(frame, text="Reroll rules:").grid(row=nextRow, sticky=W, columnspan=nstats*2)
    for i in range(len(rerolls)):
        Label(frame, text=rerolls[i]).grid(row=nextRow+1+i, column=0, columnspan=nstats//3, sticky=W)
        Label(frame, text=rerolls[i]).grid(row=nextRow+1+i, column=nstats, columnspan=nstats//3, sticky=W)
        rules[0][rerolls[i]]=(BooleanVar(frame), StringVar(frame))
        rules[1][rerolls[i]]=(BooleanVar(frame), StringVar(frame))
        Checkbutton(frame, variable=rules[0][rerolls[i]][0]).grid(row=nextRow+1+i, column=nstats//3+1)
        Checkbutton(frame, variable=rules[1][rerolls[i]][0]).grid(row=nextRow+1+i, column=nstats+nstats//3+1)
        apply(OptionMenu, (frame, rules[0][rerolls[i]][1]) + tuple([rerollOptions[0]]+rerollOptions)).grid(row=nextRow+1+i, column=nstats//3+2, sticky = W, columnspan=nstats//3)
        apply(OptionMenu, (frame, rules[1][rerolls[i]][1]) + tuple([rerollOptions[0]]+rerollOptions)).grid(row=nextRow+1+i, column=nstats+nstats//3+2, sticky = W, columnspan=nstats//3)
    
    
    nextRow+=len(rerolls)+1
    Label(frame, text="Army Specific Rules:").grid(row=nextRow, sticky=W, columnspan=nstats*2)
    for i in range(len(armyRules)):
        Label(frame, text=armyRules[i]).grid(row=nextRow+1+i, column=0, columnspan=nstats//3, sticky=W)
        Label(frame, text=armyRules[i]).grid(row=nextRow+1+i, column=nstats, columnspan=nstats//3, sticky=W)
        rules[0][armyRules[i]]=BooleanVar(frame)
        rules[1][armyRules[i]]=BooleanVar(frame)
        Checkbutton(frame, variable=rules[0][armyRules[i]]).grid(row=nextRow+1+i, column=nstats//3+1)
        Checkbutton(frame, variable=rules[1][armyRules[i]]).grid(row=nextRow+1+i, column=nstats+nstats//3+1)
        
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
    return total <= target
    
    

#Return the combatStats of both units
#These are the target rolls for hitting, wounding, saving, and wards
#as well as the order of attack (1 for first, -1 for second, 0 for simultaneous)
#turn: the number of the turn
def getStats(turn):
    s = (dict(), dict())
    ws = [stats[0]["WS"].get(), stats[1]["WS"].get()]
    strength = [stats[0]["S"].get(), stats[1]["S"].get()]
    toughness = (stats[0]["T"].get(), stats[1]["T"].get())
    ini = (stats[0]["I"].get(), stats[1]["I"].get())
    armor = (stats[0]["AS"].get(), stats[1]["AS"].get())
    ward = (stats[0]["Wa"].get(), stats[1]["Wa"].get())
    thb= (rules[0]["Bonus To-Hit"], rules[1]["Bonus To-Hit"])
    thp= (rules[0]["To-Hit Penalty"], rules[1]["To-Hit Penalty"])
    twb= (rules[0]["Bonus To-Wound"], rules[1]["Bonus To-Wound"])
    twp= (rules[0]["To-Wound Penalty"], rules[1]["To-Wound Penalty"])
    weap = (weapons[0].get(), weapons[1].get())
    
    for i in range(2):    
        if weap[i]== "Great Weapon":
            strength[i]+=2
            rules[i]["Always Strikes Last"].set(True)
        if weap[i]== "Halberd":         strength[i]+=1
        if turn == 0:
            if  weap[i] == "Morning Star" or (weap[i] == "Spear (mounted)" and rules[i]["Has Charged"].get()):
                strength[i]+=1
            elif weap[i] == "Flail" or (weap[i] == "Lance" and rules[i]["Has Charged"].get()):
                strength[i]+=2
                
                
    # Done after weapons, because STR bonus affects armor
    for i in range(2):
        if rules[not i]["Fear"][0].get() and not rules[i]["Immune Psychology"].get():
            if not fearTest(rules[not i]["Fear"][1].get(), i):
                ws[i] = 1
        
        if ws[i]>ws[not i]:
            s[i]["To-Hit"]=3
        elif ws[i]*2<ws[not i]: s[i]["To-Hit"]=5
        else:   s[i]["To-Hit"]=4
        if thb[i][0].get(): s[i]["To-Hit"]-= thb[i][1].get()
        if thp[not i][0].get(): s[i]["To-Hit"]+= thp[not i][1].get()
        
        s[i]["To-Wound"] = 4+toughness[not i]-strength[i]
        if twb[i][0].get(): s[i]["To-Wound"]-= twb[i][1].get()
        if twp[not i][0].get(): s[i]["To-Wound"]+= twp[not i][1].get()
        s[i]["To-Wound"] = min(6, s[i]["To-Wound"])
        s[i]["To-Wound"] = max(2, s[i]["To-Wound"])
        
        if rules[not i]["Ignore Save"].get(): s[i]["Save"] = 7
        else:
            s[i]["Save"] = armor[i]
            if rules[not i]["Armour Piercing"].get():    s[i]["Save"] += 1
            if strength[not i]>3 :  s[i]["Save"] += strength[not i]-3
        s[i]["Save"]= min(7, s[i]["Save"])
        s[i]["Save"] = max(2, s[i]["Save"])
        
        s[i]["Ward"] = ward[i]
        
        #This part is only usefull for rerolls, rest is taken care of by setTurnOrder
        s[i]["Priority"] = rules[i]["Always Strikes First"].get() - rules[i]["Always Strikes Last"].get()
    
    for i in range(1):
        if s[i]["Priority"]==s[not i]["Priority"]:
            if s[i]["Priority"]!=0 or ini[i]==ini[not i]:
                s[i]["Priority"]=0  
                s[not i]["Priority"]=0
            else:
                s[i]["Priority"]=int(ini[i]>ini[not i])*2-1
                s[not i]["Priority"]=s[i]["Priority"]*-1
        elif s[i]["Priority"]==1 and ini[i]>ini[not i]:
            rules[i]["To-Hit"][0].set(True)
            rules[i]["To-Hit"][1].set("Failures")
            s[not i]["Priority"]=-1
        elif s[not i]["Priority"]==1 and ini[not i]>ini[i]:
            rules[not i]["To-Hit"][0].set(True)
            rules[not i]["To-Hit"][1].set("Failures")
            s[i]["Priority"]=-1
        else:
            s[i]["Priority"]=int(s[i]["Priority"]>s[not i]["Priority"])*2-1
            s[not i]["Priority"] = s[i]["Priority"]*-1
    return s
    
    
def getMountStats(turn):
    s = (dict(), dict())
    
    ws = (stats[0]["WS"].get(), stats[1]["WS"].get())
    mws = (mountStats[0]["WS"].get(), mountStats[1]["WS"].get())
    strength = [mountStats[0]["S"].get(), mountStats[1]["S"].get()]
    toughness = (stats[0]["T"].get(), stats[1]["T"].get())
    ini = (mountStats[0]["I"].get(), mountStats[1]["I"].get())
    armor = (stats[0]["AS"].get(), stats[1]["AS"].get())
    ward = (stats[0]["Wa"].get(), stats[1]["Wa"].get())
    thp= (rules[0]["To-Hit Penalty"], rules[1]["To-Hit Penalty"])
    twp= (rules[0]["To-Wound Penalty"], rules[1]["To-Wound Penalty"])
    weap = (weapons[0].get(), weapons[1].get())
    
    for i in range(2):            
        
        
        if mws[i]>ws[not i]:
            s[i]["To-Hit"]=3
        elif mws[i]*2<ws[not i]: s[i]["To-Hit"]=5
        else:   s[i]["To-Hit"]=4
        if thp[not i][0].get(): s[i]["To-Hit"]+= thp[not i][1].get()
        
        s[i]["To-Wound"] = 4+toughness[not i]-strength[i]
        if twp[not i][0].get(): s[i]["To-Wound"]+= twp[not i][1].get()
        s[i]["To-Wound"] = min(6, s[i]["To-Wound"])
        s[i]["To-Wound"] = max(2, s[i]["To-Wound"])
        
        if rules[i]["Ignore Save"].get(): s[i]["Save"] = 7
        else:
            s[i]["Save"] = armor[not i]
            if rules[i]["Armour Piercing"].get():    s[i]["Save"] += 1
            if strength[i]>3 :  s[i]["Save"] += strength[i]-3
        s[i]["Save"]= min(7, s[i]["Save"])
        s[i]["Save"] = max(2, s[i]["Save"])
        
        s[i]["Ward"] = ward[not i]
        
        #pretty sure everything concerning priority here is replace by
        # setTurnOrder
        s[i]["Priority"] = rules[i]["Always Strikes First"].get() - rules[i]["Always Strikes Last"].get()
    
    for i in range(1):
        if s[i]["Priority"]==s[not i]["Priority"]:
            if s[i]["Priority"]!=0 or ini[i]==ini[not i]:
                s[i]["Priority"]=0  
                s[not i]["Priority"]=0
            else:
                s[i]["Priority"]=int(ini[i]>ini[not i])*2-1
                s[not i]["Priority"]=s[i]["Priority"]*-1
        elif s[i]["Priority"]==1 and ini[i]>ini[not i]:
            rules[i]["To-Hit"][0].set(True)
            rules[i]["To-Hit"][1].set("Failures")
            s[not i]["Priority"]=-1
        elif s[not i]["Priority"]==1 and ini[not i]>ini[i]:
            rules[not i]["To-Hit"][0].set(True)
            rules[not i]["To-Hit"][1].set("Failures")
            s[i]["Priority"]=-1
        else:
            s[i]["Priority"]=int(s[i]["Priority"]>s[not i]["Priority"])*2-1
            s[not i]["Priority"] = s[i]["Priority"]*-1
    return s
    
    
    
#Sets the global var turnOrder to contain the ordered list of attackers
#Each entry is the index of the unit, a boolean indicating if it is a mount, and a boolean indicating if it is a (Thunder)Stomp    
def setTurnOrder():
    global turnOrder
    global resultText
    turnOrder= []
    tempOrder = []
    for i in range(2):
        ini = stats[i]["I"].get()
        mod = (rules[i]["Always Strikes First"].get() - rules[i]["Always Strikes Last"].get()) * 100
        if mod != 0:    tempOrder.append((mod, i, False, False))
        else:           tempOrder.append((ini, i, False, False))
            
        if rules[i]["Mounted"].get():
            tempOrder.append((mountStats[i]["I"].get(), i, True, False))
        
        if rules[i]["Stomp"].get() or rules[i]["Thunderstomp"].get():
            tempOrder.append((-100, i, False, True))
    tempOrder = sorted(tempOrder, key=lambda unit: unit[0], reverse=True)
    #turnOrder contains lists of units that attack at the same time, drop the mod/ini value
    turnOrder.append([(tempOrder[0][1], tempOrder[0][2], tempOrder[0][3])])
    for i in range(1, len(tempOrder)):
        if tempOrder[i][0] == tempOrder[i-1][0]:
            turnOrder[-1].append((tempOrder[i][1], tempOrder[i][2], tempOrder[i][3]))
        else:
            turnOrder.append([(tempOrder[i][1], tempOrder[i][2], tempOrder[i][3])])
    resultText += "Turn Order:\n"
    for i in range(len(turnOrder)):
        s = str(i+1) + " : "
        for u in turnOrder[i]:
            if u[1]: s+= "Mount of "
            if u[2]: s+= "(Thunder)Stomp of "
            s+= names[u[0]].get() +"; "
        resultText += s[:-2] + "\n"
    resultText+= "\n"
            
            
    
    

#Get the number of attacks a unit will do and
#   the number of models in base contact in the first rank
#unit: the identifier of the attacking unit (0 or 1)
#losses: the amount of models the unit lost before attacking
#        (only non-0 if the unit attacks second)    
def getAttacks(unit, losses):
    if num[unit][0] == 0 or num[unit][1] == 0:
        return(0,0)
            
    apm = stats[unit]["A"].get()
    randApm = 0
    if weapons[unit].get()=="Two Weapons":      apm+=1
    if rules[unit]["Extra Attack"][0].get():    apm+=rules[unit]["Extra Attack"][1].get()
    if rules[unit]["Devastating Charge"].get() and rules[unit]["Has Charged"].get():    apm+=1
        
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
    
    firstRank=min(available, int(num[unit][1]), widthConstraint)
    attacks = firstRank*(apm)
    if rules[unit]["Random Attacks"][0].get():
        for i in range(firstRank):
            for j in range(rules[unit]["Random Attacks"][1].get()):
                attacks += randint(1, rules[unit]["Random Attacks"][2].get())
    available-=int(num[unit][1])
    supportRanks = 1
    if int(num[unit][1])>=10 and not rules[unit]["Monstrous Support"].get(): supportRanks+=1
    if int(num[unit][1])>=6 and rules[unit]["Monstrous Support"].get(): supportRanks+=1
    if weapons[unit].get()=="Spear (foot)": supportRanks+=1
    if rules[unit]["Fight in Extra Ranks"][0].get():
        supportRanks += rules[unit]["Fight in Extra Ranks"][1].get()
    while supportRanks > 0 and available > 0:
        rankAttacks = min(available, int(num[unit][1]), widthConstraint)
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
    #predation handled during attack
    #if rules[unit]["Predation"].get():    attacks = attacks * (1+1/6)
    #shortenable?
    return (int((max(0, attacks)+ (1 if attacks >=0 else 0)) if rules[unit]["Has Champion"].get() else max(0, attacks)), int(max(0, firstRank)))
   
    
def calcRerolls(attacker, cstats, stat):
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
        r = calcRerolls(attacker, cstats, "To-Hit")
        if rules[attacker]["Predation"].get() and r == 6:
            pred += 1
        if r < cstats[attacker]["To-Hit"]:
            continue
        
        if r > auto_w:
            r = 0
        else:
            r = calcRerolls(attacker, cstats, "To-Wound")
            if r < cstats[attacker]["To-Wound"]:
                continue
        
        if r > kb:
            r = 0
        else:
            r = calcRerolls(not attacker, cstats, "Save")
            if r >= cstats[not attacker]["Save"]:
                continue
         
        r = calcRerolls(not attacker, cstats, "Ward")
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
        r = calcRerolls(attacker, cstats, "To-Hit")
        if r < cstats[attacker]["To-Hit"]:
            continue
        
        if r > auto_w:
            r = 0
        else:
            r = calcRerolls(attacker, cstats, "To-Wound")
            if r < cstats[attacker]["To-Wound"]:
                continue
        
        if r > kb:
            r = 0
        else:
            r = calcRerolls(not attacker, cstats, "Save")
            if r >= cstats[not attacker]["Save"]:
                continue
         
        r = calcRerolls(not attacker, cstats, "Ward")
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


    
    
    
    
        
      
#Resolves Stomp and Thunderstomp hits
#unit: the id of the unit hitting
#stats: combat stats of the units
def stomp(unit, models, stats, rules):
    temp = (rules[unit]["Auto-wound"][0].get(), stats[unit]["To-Hit"])
    stats[unit]["To-Hit"]=1
    rules[unit]["Auto-wound"][0].set(False)
    if rules[unit]["Stomp"].get():
        res = [attack(unit, models, stats, rules), models]
    if rules[unit]["Thunderstomp"].get():
        a = 0
        for i in range(models):
            a += randint(1, 6)
        res = [attack(unit, a, stats, rules), models*3.5]
    rules[unit]["Auto-wound"][0].set(temp[0])
    stats[unit]["To-Hit"] = temp[1]
    return res
        
dummyrules = dict()
for i in ruleOptions+armyRules:
    dummyrules[i] = BooleanVar(frame)
for i in valueRules + diceRules + rerolls:
    dummyrules[i] = [BooleanVar(frame)]
       
        
#Resolves one round of combat
#roundn: the number of the round
#stats: the ordered combatStats of both units
#mstats: combatStats of both units' mounts
def fightRound(roundn, stats, mstats):
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
            att = getAttacks(unit[0], kills[not unit[0]])
            r= [dict(), dict()]
            r[unit[0]] = dummyrules
            r[unit[0]]["Stomp"] = rules[unit[0]]["Stomp"]
            r[unit[0]]["Thunderstomp"] = rules[unit[0]]["Thunderstomp"]
            r[not unit[0]] = rules[not unit[0]]
            s = [dict(), dict()]
            s[unit[0]] = mstats[unit[0]]
            s[not unit[0]] = stats[not unit[0]]
            
            #if mount
            if unit[1]:
                #number of models * mount attacks
                #TODO include mount specials rules (uses dummy ad interim)
                a = att[1]*mountStats[unit[0]]["A"].get()
                orderAttacks[unit[0]] += a
                k = attack(unit[0], att[1]*mountStats[unit[0]]["A"].get(), s, r)
                orderKills[unit[0]] += k
                resultText += "Mount of " + names[unit[0]].get() + " does " + str(round(a, 2)) + " attacks, for "+ str(round(k, 2)) + " wounds\n"
            #if Stomp
            elif unit[2]:
                #uses mount stats if mounted
                #uses dummy rules (don't affect stomp)
                stompRes = stomp(unit[0], att[1], s if unit[1] else stats, r)
                orderAttacks[unit[0]] += stompRes[1]
                orderKills[unit[0]] += stompRes[0]
                resultText += "(Thunder)Stomp of " + names[unit[0]].get() + " does " + str(round(stompRes[1], 2)) + " attacks, for "+ str(round(stompRes[0], 2)) + " wounds\n"
            else:
                orderAttacks[unit[0]] += att[0]
                k = attack(unit[0], att[0], stats, rules)
                orderKills[unit[0]] += k
                resultText += names[unit[0]].get() + " does " + str(round(att[0], 2)) + " attacks, for "+ str(round(k, 2)) + " wounds\n"
                
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
        #this will represent numbers of wounds left, not models
        for i in range(2):
            num[i][0]=num[i][0] * int(stats[i]["W"].get())
        for i in range(roundcount):
            roundReached[i] += 1
            combatStats=getStats(i)
            mountCombatStats=getMountStats(i)
            setTurnOrder()
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
    for i in mountFields:
        txt += str(mountStats[n][i].get()) + ","
    #weapon and base size
    txt += "\n" + weapons[n].get() + "\n" + baseSizes[n].get() + "\n"
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
    #dicerules
    for i in diceRules:
        if rules[n][i][0].get():
            txt +=i +"("+str(rules[n][i][1].get())+";"+ str(rules[n][i][2].get()) +"),"
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
    f.write(txt)
    f.close()


def loadUnit(n):
    #reset rules
    for i in rules[n]:
        if isinstance(rules[n][i], tuple):
            rules[n][i][0].set(False)
        else: rules[n][i].set(False)
        
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
        for i in range(len(mountFields)):
            mountStats[n][mountFields[i]].set(s[i])
    #weapon
    l = f.readline()[:-1]
    if l != "":
        weapons[n].set(l)
    #base size
    l = f.readline()[:-1]
    if l!= "":
        baseSizes[n].set(l)
    #rules
    l = f.readline()[:-2]
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
    #diceRules
    l = f.readline()[:-1]
    if l != "":
        matches = findall("(.*?)\(([\d;]*)\),", l)
        for m in matches:
            rules[n][m[0]][0].set(True)
            v = m[1].split(";")
            rules[n][m[0]][1].set(v[0])
            rules[n][m[0]][2].set(v[1])
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
                    
                    

populate(frame)

root.mainloop()
