import ui
from operator import itemgetter  # used to sort list of lists
from datetime import datetime, date, time
from collections import deque
import os, glob


# Open and read drinks from file into list
# iterate through list convert string to date and discard all but date and alcohol value
# store values in new list
# sort list by date descending
# print list and what it will look like in 7 days if no drinking

# added how many days till 30days average < 60


def calcweeks(shift):  # lists alcohol units per week for 30 days and average over the weeks
    thisweek = 0
    lastweek = 0
    twoweeks = 0
    threeweeks = 0
    threemonths = 0
    sixmonths = 0
    twelvemonths = 0
    for drink in drinks:
        days = today - drink[0]  # calculate number of days from today
        if days.days < shift: thisweek = thisweek + float(drink[1])
        if (shift + 7) > days.days >= (shift): lastweek = lastweek + float(drink[1])
        if (shift + 14) > days.days >= (shift + 7): twoweeks = twoweeks + float(drink[1])
        if (shift + 23) > days.days >= (shift + 14): threeweeks = threeweeks + float(drink[1])
        if (shift + 84) > days.days >= (shift + 23): threemonths = threemonths + float(drink[1])
        if (shift + 175) > days.days >= (shift + 84): sixmonths = sixmonths + float(drink[1])
        if (shift + 357) > days.days >= (shift + 175): twelvemonths = twelvemonths + float(drink[1])
    print('  This week: ' + str(int(thisweek / 8)) + ' units')
    print('  Last week: ' + str(int(lastweek / 8)) + '  ' + str(int((lastweek + thisweek) / 8 / 2)) + ' units')
    print(
        'Three weeks: ' + str(int(twoweeks / 8)) + '  ' + str(int((lastweek + thisweek + twoweeks) / 8 / 3)) + ' units')
    thirtydays = round((lastweek + thisweek + twoweeks + threeweeks) / 8, 1)
    twelvemonths = round((lastweek + thisweek + twoweeks + threeweeks + threemonths + sixmonths + twelvemonths) / 8, 1)
    sixmonths = round((lastweek + thisweek + twoweeks + threeweeks + threemonths + sixmonths) / 8, 1)
    threemonths = round((lastweek + thisweek + twoweeks + threeweeks + threemonths) / 8, 1)
    print('    30 days: ' + str(int(threeweeks / 8)) + '  ' + str(
        int((lastweek + thisweek + twoweeks + threeweeks) / 8 / 4.29)) + ' units')
    print()
    print('   30 day total:  ' + str(int(thirtydays)) + '  of 60 units' + '   ' + str(
        round(thirtydays / 4.29, 1)))  # 30days = 4.29 weeks
    print(' 3 months total: ' + str(int(threemonths)) + ' of 182 units' + '   ' + str(round(threemonths / 13, 1)))
    print(' 6 months total: ' + str(int(sixmonths)) + ' of 364 units' + '   ' + str(round(sixmonths / 26, 1)))
    print('12 months total: ' + str(int(twelvemonths)) + ' of 728 units' + '   ' + str(round(twelvemonths / 52, 1)))
    print()
    if shift == 7:
        v0['labelAverage'].text = str(round(thirtydays / 4.29, 1))  # 30days = 4.29 weeks
        v1['labelAverage'].text = str(round(threemonths / 13, 1))  # 30days = 4.29 weeks
        v2['labelAverage'].text = str(round(sixmonths / 26, 1))  # 30days = 4.29 weeks
        v3['labelAverage'].text = str(round(twelvemonths / 52, 1))  # 30days = 4.29 weeks

    return (int(thisweek), int(thirtydays), int(threemonths), int(sixmonths), int(twelvemonths))


def daystill(poss,
             alc_units, offset):  # calculates how many days working back from today that I consumed 60 units - used to calculate number of days till I am within the healthy 60 units over the last 30 days. (182 units for 3 months 364 units for 6 months)
    totalalcohol = 0 + poss
    lastentries = deque(maxlen=5)
    alclimitflag = 0
    daysreachedflag = 0
    daydrink = [0, 0]
    FourWeeks = [0,0,0,0]
    for drink in drinks:
        days = today - drink[0]
        if days.days < alc_units / 2:
            if daydrink[0] == drink[0]:
                daydrink[1] = float(daydrink[1]) + float(drink[1])
            else:
                lastentries.append(daydrink)
                daydrink = []
                daydrink.append(drink[0])
                daydrink.append(drink[1])
            if offset < days.days <= offset + 7:
            	FourWeeks[0] = float(FourWeeks[0])+float(drink[1])
            if offset + 7 < days.days <= offset + 14:
            	FourWeeks[1] = float(FourWeeks[1])+float(drink[1])
            if offset + 14 < days.days <= offset + 21:
            	FourWeeks[2] = float(FourWeeks[2])+float(drink[1])
            if offset + 21 < days.days <= offset + 28:
            	FourWeeks[3] = float(FourWeeks[3])+float(drink[1])

        else:
            daysreachedflag = 1
        if totalalcohol < alc_units:
            totalalcohol += float(drink[1]) / 8
            dayresult = days.days
        else:
            alclimitflag = 1
        if alclimitflag and daysreachedflag:
            lastentries.append(daydrink)
            return (dayresult, lastentries, FourWeeks)



class TabbedView(ui.View):
    def __init__(self,tablist=[], frame=(0,0)+ui.get_screen_size()):
        '''takes an iterable of Views, using the view name as the tab selector.  
        empty views sre just given generic names'''
        self.tabcounter=0    #unique counter, for name disambiguation
        self.buttonheight=30 #height of buttonbar
        #setup button bar
        self.tabbuttons=ui.SegmentedControl(frame=(0,-5,self.width, self.buttonheight+5),bg_color='white')
        self.tabbuttons.action=self.tab_action
        self.tabbuttons.flex='W'
        self.tabbuttons.segments=[]
        self.add_subview(self.tabbuttons)

        for tab in tablist:
            self.addtab(tab)
    def tab_action(self,sender):
        if sender.selected_index >= 0:
            tabname=sender.segments[sender.selected_index]
            self[tabname].bring_to_front()
    def focus_tab_by_index(self,index):
        self.tabbuttons.selected_index=index
        self.tab_action(self.tabbuttons)
    
    def focus_tab_by_name(self,tabname):
        self.tabbuttons.selected_index=self.tabbuttons.segments.index(tabname)
        self.tab_action(self.tabbuttons)

    def addtab(self,tab):
            if not tab.name:
                tab.name='tab{}'.format(self.tabcounter)
            if tab.name in self.tabbuttons.segments:
                #append unique counter to name
                tab.name+=str(self.tabcounter)
            self.tabcounter+=1
            self.tabbuttons.segments+=(tab.name,) 
            tab.frame=(0,self.buttonheight,self.width,self.height-self.buttonheight)
            tab.flex='WH'
            self.add_subview(tab)
            self.focus_tab_by_name(tab.name)

    def removetab(self,tabname):
        self.tabbuttons.segments=[x for x in self.tabbuttons.segments if x != tabname]
        self.remove_subview(tabname)
        # if tab was top tab, think about updating selected tab to whatever is on top 
    def get_tab_contents_by_index(self,index):
        tabname=self.tabbuttons.segments[index]
        return self[tabname]
    def layout(self):
        pass   # maybe set tabbuttons size
        
if __name__=='__main__':
    v=TabbedView()
    v.addtab(ui.View(name='30 Days',bg_color=(1.00, 0.8, 0.8)))
    v.addtab(ui.View(name='3 Months',bg_color=(1.00, 1.00, 0.80)))
    v.addtab(ui.View(name='6 Months',bg_color=(0.9,1.0,0.9)))
    v.addtab(ui.View(name='12 Months',bg_color='white'))
    v.focus_tab_by_name('30 Days')
    v0 = ui.load_view('tabbedSubview')
    v1 = ui.load_view('tabbedSubview')
    v2 = ui.load_view('tabbedSubview')
    v3 = ui.load_view('tabbedSubview')

    # clean up old and surplus files
    for fn in glob.glob('text*'):
        os.remove(fn)
    qty = len(glob.glob('*.csv'))
    if qty > 1:
        filename = 'drinkcontrol ' + str(qty) + '.csv'
        os.rename(filename, 'drinkcontrol.csv')
    for fn in glob.glob('drinkcontrol *'):
        os.remove(fn)

    today = datetime.now()
    # today = datetime(2019, 12, 1, 12, 43, 22, 181463) #use to set manual date for 'today' for calculations
    previous = deque(maxlen=5) #used for displayimg the last five days with drinks - non-drinking days are skipped
    prevWeeks = [0,0,0,0]
    f = open("drinkcontrol.csv")  # Open file for reading drinks
    lines = f.read().splitlines()  # read file into list
    del lines[0]  # delete title row
    drinks = []
    for line in lines:  # extract list items from list one by one
        drink = line.split(';')
        drink[0] = drink[0][0:10]  # strip time from date time
        drink[0] = datetime.strptime(drink[0], '%Y-%m-%d')  # convert date string to datetime
        drink = [drink[0], drink[9]]  # throw away all data except date and alcohol value
        drinks.append(drink)  # add this drink to list of all drinks
        drinks = sorted(drinks, key=itemgetter(0), reverse=True)  # sort list

    print()
    print('Current status:')
    currweek, units30, units3months, units6months, units12months = calcweeks(7)
    print('30 days')
    drinkingday, previous, prevWeeks = daystill(0, 60, 1)
    v0['labelLimit'].text = str(units30) + '/60'
    v1['labelLimit'].text = str(units3months) + '/182'
    v2['labelLimit'].text = str(units6months) + '/364'
    v3['labelLimit'].text = str(units12months) + '/728'
    v0['labelD0'].text = str(30 - (today - previous[4][0]).days)
    v0['labelD1'].text = str(30 - (today - previous[3][0]).days)
    v0['labelD2'].text = str(30 - (today - previous[2][0]).days)
    v0['labelD3'].text = str(30 - (today - previous[1][0]).days)
    v0['labelD4'].text = str(30 - (today - previous[0][0]).days)
    v0['labelD5'].text = str(round(float(previous[4][1]) / 8, 1))
    v0['labelD6'].text = str(round(float(previous[3][1]) / 8, 1))
    v0['labelD7'].text = str(round(float(previous[2][1]) / 8, 1))
    v0['labelD8'].text = str(round(float(previous[1][1]) / 8, 1))
    v0['labelD9'].text = str(round(float(previous[0][1]) / 8, 1))
    v0['labelD10'].text = str(round(float(prevWeeks[3]) / 8, 1))
    v0['labelD11'].text = str(round(float(prevWeeks[2]) / 8, 1))
    v0['labelD12'].text = str(round(float(prevWeeks[1]) / 8, 1))
    v0['labelD13'].text = str(round(float(prevWeeks[0]) / 8, 1))
    
    if 30- drinkingday > 0:
        v0['labelDelta'].text_color = 'red'
        v0['labelDelta'].text = str(int(units30 - 60))
        v0['labelTill'].text = str(30 - drinkingday)
    else:
        v0['labelDelta'].text_color = 'green'
        v0['labelDelta'].text = str(int(60 - units30))
    Buff1=float(60-units30 -14)+float(v0['labelD10'].text)
    Buff2 = Buff1 - 14 +float(v0['labelD11'].text)
    Buff3 = Buff2 -14+float(v0['labelD12'].text)
    Buff4 = Buff3 -14 +float(v0['labelD13'].text)
    v0['label13'].text = str(round((Buff1),1))
    v0['label14'].text = str(round((Buff2),1))
    v0['label15'].text = str(round((Buff3),1))
    v0['label16'].text = str(round((Buff4),1))
    v0['label18'].text=str(round((currweek/8),1))
    for prev in previous:
        print(30 - (today - prev[0]).days, round(float(prev[1]) / 8, 1))
    if 30 - drinkingday > 0:
        print('You can have a drink in ' + str(30 - drinkingday) + ' days time and you have a deficit of ' + str(
            int(units30 - 60)) + ' units')
    else:
        print('Congratulations, you have a 30 day buffer of ' + str(int(60 - units30)) + ' units')
    print()
    print('3 months')
    drinkingday, previous, prevWeeks = daystill(0, 182, 62)
    v1['labelD0'].text = str(91 - (today - previous[4][0]).days)
    v1['labelD1'].text = str(91 - (today - previous[3][0]).days)
    v1['labelD2'].text = str(91 - (today - previous[2][0]).days)
    v1['labelD3'].text = str(91 - (today - previous[1][0]).days)
    v1['labelD4'].text = str(91 - (today - previous[0][0]).days)
    v1['labelD5'].text = str(round(float(previous[4][1]) / 8, 1))
    v1['labelD6'].text = str(round(float(previous[3][1]) / 8, 1))
    v1['labelD7'].text = str(round(float(previous[2][1]) / 8, 1))
    v1['labelD8'].text = str(round(float(previous[1][1]) / 8, 1))
    v1['labelD9'].text = str(round(float(previous[0][1]) / 8, 1))
    v1['labelD10'].text = str(round(float(prevWeeks[3]) / 8, 1))
    v1['labelD11'].text = str(round(float(prevWeeks[2]) / 8, 1))
    v1['labelD12'].text = str(round(float(prevWeeks[1]) / 8, 1))
    v1['labelD13'].text = str(round(float(prevWeeks[0]) / 8, 1))
    if 91- drinkingday > 0:
        v1['labelDelta'].text_color = 'red'
        v1['labelDelta'].text = str(int(units3months - 182))
        v1['labelTill'].text = str(91 - drinkingday)
    else:
        v1['labelDelta'].text_color = 'green'
        v1['labelDelta'].text = str(int(182 - units3months))
    Buff1=float(182 - units3months-14)+float(v1['labelD10'].text)
    Buff2 = Buff1 - 14 +float(v1['labelD11'].text)
    Buff3 = Buff2 -14+float(v1['labelD12'].text)
    Buff4 = Buff3 -14 +float(v1['labelD13'].text)
    v1['label13'].text = str(round((Buff1),1))
    v1['label14'].text = str(round((Buff2),1))
    v1['label15'].text = str(round((Buff3),1))
    v1['label16'].text = str(round((Buff4),1))
    v1['label18'].text=str(round((currweek/8),1))
    for prev in previous:
        print(91 - (today - prev[0]).days, round(float(prev[1]) / 8, 1))
    if 91 - drinkingday > 0:
        print('You can have a drink in ' + str(91 - drinkingday) + ' days time and you have a deficit of ' + str(
            int(units3months - 182)) + ' units')
    else:
        print('Congratulations, you have a 90 day buffer of ' + str(int(182 - units3months)) + ' units')
        # print 'Congratulations, you have a 90 day buffer of '+str(int(182 - returnedalcohol)) +' units'
    drinkingday, previous, prevWeeks = daystill(0, 364, 153)
    # drinkingday, previous, returnedalcohol = daystill(0,364)
    print()
    print('6 months')
    v2['labelD0'].text = str(182 - (today - previous[4][0]).days)
    v2['labelD1'].text = str(182 - (today - previous[3][0]).days)
    v2['labelD2'].text = str(182 - (today - previous[2][0]).days)
    v2['labelD3'].text = str(182 - (today - previous[1][0]).days)
    v2['labelD4'].text = str(182 - (today - previous[0][0]).days)
    v2['labelD5'].text = str(round(float(previous[4][1]) / 8, 1))
    v2['labelD6'].text = str(round(float(previous[3][1]) / 8, 1))
    v2['labelD7'].text = str(round(float(previous[2][1]) / 8, 1))
    v2['labelD8'].text = str(round(float(previous[1][1]) / 8, 1))
    v2['labelD9'].text = str(round(float(previous[0][1]) / 8, 1))
    v2['labelD10'].text = str(round(float(prevWeeks[3]) / 8, 1))
    v2['labelD11'].text = str(round(float(prevWeeks[2]) / 8, 1))
    v2['labelD12'].text = str(round(float(prevWeeks[1]) / 8, 1))
    v2['labelD13'].text = str(round(float(prevWeeks[0]) / 8, 1))
    if 182 - drinkingday > 0:
        v2['labelDelta'].text_color = 'red'
        v2['labelDelta'].text = str(int(units6months - 364))
        v2['labelTill'].text = str(182 - drinkingday)
    else:
        v2['labelDelta'].text_color = 'green'
        v2['labelDelta'].text = str(int(364 - units6months))
    Buff1=float(364 - units6months-14)+float(v2['labelD10'].text)
    Buff2 = Buff1 - 14 +float(v2['labelD11'].text)
    Buff3 = Buff2 -14+float(v2['labelD12'].text)
    Buff4 = Buff3 -14 +float(v2['labelD13'].text)
    v2['label13'].text = str(round((Buff1),1))
    v2['label14'].text = str(round((Buff2),1))
    v2['label15'].text = str(round((Buff3),1))
    v2['label16'].text = str(round((Buff4),1))
    v2['label18'].text=str(round((currweek/8),1))
    for prev in previous:
        print(182 - (today - prev[0]).days, round(float(prev[1]) / 8, 1))
    if 182 - drinkingday > 0:
        print('You can have a drink in ' + str(182 - drinkingday) + ' days time and you have a deficit of ' + str(
            int(units6months - 364)) + ' units')
    else:
        print('Congratulations, you have a 180 day buffer of ' + str(int(364 - units6months)) + ' units')

    drinkingday, previous, prevWeeks = daystill(0, 728, 335)
    # drinkingday, previous, returnedalcohol = daystill(0,364)
    print()
    print('12 months')
    v3['labelD0'].text = str(364 - (today - previous[4][0]).days)
    v3['labelD1'].text = str(364 - (today - previous[3][0]).days)
    v3['labelD2'].text = str(364 - (today - previous[2][0]).days)
    v3['labelD3'].text = str(364 - (today - previous[1][0]).days)
    v3['labelD4'].text = str(364 - (today - previous[0][0]).days)
    v3['labelD5'].text = str(round(float(previous[4][1]) / 8, 1))
    v3['labelD6'].text = str(round(float(previous[3][1]) / 8, 1))
    v3['labelD7'].text = str(round(float(previous[2][1]) / 8, 1))
    v3['labelD8'].text = str(round(float(previous[1][1]) / 8, 1))
    v3['labelD9'].text = str(round(float(previous[0][1]) / 8, 1))
    v3['labelD10'].text = str(round(float(prevWeeks[3]) / 8, 1))
    v3['labelD11'].text = str(round(float(prevWeeks[2]) / 8, 1))
    v3['labelD12'].text = str(round(float(prevWeeks[1]) / 8, 1))
    v3['labelD13'].text = str(round(float(prevWeeks[0]) / 8, 1))
    if 364- drinkingday > 0:
        v3['labelDelta'].text_color = 'red'
        v3['labelDelta'].text = str(int(units12months - 728))
        v3['labelTill'].text = str(364 - drinkingday)
    else:
        v3['labelDelta'].text_color = 'green'
        v3['labelDelta'].text = str(int(728 - units12months))
    Buff1=float(728 - units12months-14)+float(v3['labelD10'].text)
    Buff2 = Buff1 - 14 +float(v3['labelD11'].text)
    Buff3 = Buff2 -14+float(v3['labelD12'].text)
    Buff4 = Buff3 -14 +float(v3['labelD13'].text)
    v3['label13'].text = str(round((Buff1),1))
    v3['label14'].text = str(round((Buff2),1))
    v3['label15'].text = str(round((Buff3),1))
    v3['label16'].text = str(round((Buff4),1))
    v3['label18'].text=str(round((currweek/8),1))

    for prev in previous:
        print(364 - (today - prev[0]).days, round(float(prev[1]) / 8, 1))
    if 364 - drinkingday > 0:
        print('You can have a drink in ' + str(364 - drinkingday) + ' days time and you have a deficit of ' + str(
            int(units12months - 728)) + ' units')
    else:
        print('Congratulations, you have a year buffer of ' + str(int(728 - units12months)) + ' units')

    print()
    print('Status in one week if no drinking:')
    calcweeks(0)

    f.close()  # close file

    v.get_tab_contents_by_index(0).add_subview(v0)
    v.get_tab_contents_by_index(1).add_subview(v1)
    v.get_tab_contents_by_index(2).add_subview(v2)
    v.get_tab_contents_by_index(3).add_subview(v3)
    v.present()
