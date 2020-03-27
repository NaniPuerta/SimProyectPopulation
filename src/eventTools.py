import numpy as np
import heapq
from random import sample
from src.populationTools import Person, Population
from src.probData import *
from src.probabilityTools import *


population = Population()

class Event:
    def __init__(self, time, eventQueue: list, person: Person):
        self._time = time
        self._person = person
        self._population = population
        self._eventqueue = eventQueue

    def __lt__(self, anotherEvent):
        return self._time < anotherEvent._time
    
    @property
    def Time(self):
        return self._time
    
    #@property
    #def GetPerson:
    #    return self._person


class Birth(Event):
    def __repr__(self):
        return f'Birth in month {self._time}'
    def __str__(self):
        return self.__repr__()

    def __init__(self, time, eventQueue: list, person: Person, population: Population, father: Person):
        super().__init__(time, eventQueue, person, population)
        self._father = father

    def check(self):
        if self._person.IsPregnant():
            self._execute()
    
    def _execute(self):
        p = np.random.uniform()
        childs = babiesBorn(p)
        for i in range(childs):
            s = np.random.uniform()
            p = Person(0, s <= 0.5)
            self._population.AddPerson(p)
            heapq.heappush(self._eventqueue, PrefixedDeath(self._time, self._eventqueue, p, ))
            heapq.heappush(self._eventqueue, AgeUp(self._time + 12, self._eventqueue, p, self._population))
        self._person.UpdateChildren(childs)
        self._father.UpdateChildren(childs)
        self._person.SetPregnant(False)
        self._population.UpdateBirths(childs > 1)
        self._population.AddEvent(self)       
        heapq.heappush(self._eventqueue, Pregnancy(self._time + 10, self._eventqueue, self._person, self._population))
        heapq.heappush(self._eventqueue, Breakup(self._time + 24, self._eventqueue, self._person, self._population))


class Death(Event):
    def __repr__(self):
        return f'Death in month {self._time}'
    def __str__(self):
        return self.__repr__()

    def check(self):
        #p = np.random.uniform()
        #prob = deathProb(self._person.Age, self._person.iswoman)
        #if p <= prob:
        self.__execute()
            
    def __execute(self):        
        if not self._person.IsSingle():
            lambd = mourningTimeLambda(self._person.Partner.Age)
            etime = int(1/gen_exp(lambd))
            heapq.heappush(self._eventqueue, EndMourning(self._time + etime, self._eventqueue, self._person.Partner, self._population))
            self._person.Partner.SetSingle()
        for event in self._eventqueue:
            if self._person == event._person:
                self._eventqueue.remove(event)
                heapq.heapify(self._eventqueue)
        self._population.RemovePerson(self._person)
        self._population.AddEvent(self) 


class PrefixedDeath(Event):
    def check(self):
        u = np.random.uniform()
        probs = fixedDeathProb(self._person.IsWoman())
        for item in probs:
            agemin, agemax, prob = item
            if u <= prob:
                avage = int(np.random.uniform(agemin,agemax))
                dtime = (avage - self._person.Age)*12
                heapq.heappush(self._eventqueue, Death(self._time + dtime, self._eventqueue, self._person, self._population))

class Pregnancy(Event):
    def __repr__(self):
        return f'Pregnancy in month {self._time}'
    def __str__(self):
        return self.__repr__()

    def check(self):
        if self._person.IsWoman() and not self._person.IsSingle() and self._person.CanHaveChildren() and self._person.Partner.CanHaveChildren():
            p = pregnantProb(self._person.Age)
            u = np.random.uniform()
            if u <= p:
                self._execute()
            else:
                heapq.heappush(self._eventqueue, Pregnancy(self._time + 1, self._eventqueue, self._person, self._population))
        
    def _execute(self):        
        self._person.SetPregnant(True)
        self._population.AddEvent(self)
        heapq.heappush(self._eventqueue, Birth(self._time + 9, self._eventqueue,self._person, self._population, self._person.Partner))


class Breakup(Event):
    def __repr__(self):
        return f'Breakup in month {self._time}'
    def __str__(self):
        return self.__repr__()

    def check(self):
        if not self._person.IsSingle():
            p = np.random.uniform()
            if p <= 0.2:
                self._execute()
            else:
                heapq.heappush(self._eventqueue, Breakup(self._time + 6, self._eventqueue, self._person, self._population))

    def _execute(self):        
        lamd1 = mourningTimeLambda(self._person.Age)
        lamd2 = mourningTimeLambda(self._person.Partner.Age)
        self._person.Partner.SetSingle()        
        etime1 = int(1/gen_exp(lamd1))
        etime2 = int(1/gen_exp(lamd2))
        self._population.AddEvent(self)
        heapq.heappush(self._eventqueue,EndMourning(self._time + etime1, self._eventqueue, self._person, self._population))
        heapq.heappush(self._eventqueue,EndMourning(self._time + etime2, self._eventqueue, self._person.Partner, self._population))
        self._person.SetSingle()

class EndMourning(Event):
    
    def check(self):
        self._execute()
    
    def _execute(self):
        self._person.SetMourning(False)
        if self._person.IsWoman:
            self._population.AddSingle(self._person, True)
        else:
            self._population.AddSingle(self._person, False)
        heapq.heappush(self._eventqueue,GetPartner(self._time + 1, self._eventqueue, self._person, self._population))


class GetPartner(Event):
    def __repr__(self):
        return f'Couple created in month {self._time}'
    def __str__(self):
        return self.__repr__()

    def check(self):
        if self._person.Age < 12:
            return
        if not self._person.IsSingle():
            print(f'single: {self._person.IsSingle()}')
            return
        if self._person.IsMourning():
            print(f'mourning: {self._person.IsMourning()}')
            return
        if self._person.IsWoman():
            if len(self._population._single_men) == 0:
                heapq.heappush(self._eventqueue, GetPartner(self._time + 3, self._eventqueue, self._person, self._population))            
                return   
        else:
            if len(self._population._single_women) == 0:
                heapq.heappush(self._eventqueue, GetPartner(self._time + 3, self._eventqueue, self._person, self._population))            
                return 
        p = partnerWantedProb(self._person.Age)
        u1 = np.random.uniform()
        if u1 <= p:
            self._execute()
        else:
            heapq.heappush(self._eventqueue, GetPartner(self._time + 5, self._eventqueue, self._person, self._population))            

    def _execute(self):        
        if self._person.IsWoman():
            #if len(self._population._single_men) == 0:
             #   heapq.heappush(self._eventqueue, GetPartner(self._time + 3, self._eventqueue, self._person, self._population))            
              #  return
            guy = sample(self._population.GetSinglePeople(False), 1)
        else:
           # if len(self._population._single_women) == 0:
            #    heapq.heappush(self._eventqueue, GetPartner(self._time + 3, self._eventqueue, self._person, self._population))            
             #   return
            guy = sample(self._population.GetSinglePeople(True), 1)
        age_difference = abs(self._person.Age - guy[0].Age)
        p = bePartnersProb(age_difference)
        u1 = np.random.uniform()
        if u1 <= p:
            self._person.SetPartner(guy[0])
            guy[0].SetPartner(self._person)
            print(self._person)
            print(guy[0])
            if self._person.IsWoman():
                self._population.RemoveSingle(self._person, True)
                self._population.RemoveSingle(guy[0], False)
                print('1---------------')
            else:
                self._population.RemoveSingle(guy[0], True)
                self._population.RemoveSingle(self._person, False)
                print('2---------------')
            self._population.AddEvent(self)            
            heapq.heappush(self._eventqueue, Breakup(self._time + 12, self._eventqueue, self._person, self._population))
            heapq.heappush(self._eventqueue, Pregnancy(self._time + 2, self._eventqueue, self._person, self._population))
        else:
            heapq.heappush(self._eventqueue, GetPartner(self._time + 3, self._eventqueue, self._person, self._population))  
            print('3-----------------------')          


class AgeUp(Event):
    def __repr__(self):
        return f'Person aged up in month {self._time}'
    def __str__(self):
        return self.__repr__()
    

    def check(self):
        self._person.AgeUp()
        self._population.AddEvent(self)
        heapq.heappush(self._eventqueue, AgeUp(self._time + 12, self._eventqueue, self._person, self._population))
        if self._person.Age > 12:
            self._population.AddSingle(self._person, self._person.IsWoman())
            heapq.heappush(self._eventqueue, GetPartner(self._time + 1, self._eventqueue, self._person, self._population))
        