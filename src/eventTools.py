import numpy as np
import heapq
from random import sample
from src.populationTools import Person, Population
from src.probData import *
from src.probabilityTools import *


population = Population()
eventQueue = []

class Event:
    def __init__(self, time, person: Person):
        self._time = time
        self._person = person

    def __lt__(self, anotherEvent):
        return self.Time < anotherEvent.Time
    
    @property
    def Time(self):
        return self._time
    
    @property
    def Person(self):
        return self._person


class Birth(Event):
    def __repr__(self):
        return f'Birth in month {self.Time}'
    def __str__(self):
        return self.__repr__()

    def __init__(self, time, person: Person, father: Person):
        super().__init__(time, person)
        self._father = father

    @property
    def Father(self):
        return self._father

    def check(self):
        self._execute()
    
    def _execute(self):
        p = np.random.uniform()
        childs = babiesBorn(p)
        for i in range(childs):
            s = np.random.uniform()
            pers = population.NewPerson(0, s <= 0.5)
            heapq.heappush(eventQueue, AgeUp(self.Time + 12, pers))
        self.Person.UpdateChildren(childs)
        self.Father.UpdateChildren(childs)
        self.Person.SetPregnant(False)
        population.UpdateBirths(childs > 1)
        population.AddEvent(self)       
        print(f'{self}')
        heapq.heappush(eventQueue, Pregnancy(self.Time + 10, self.Person))
        heapq.heappush(eventQueue, Breakup(self.Time + 24, self.Person))


class Death(Event):
    def __repr__(self):
        return f'Death in month {self.Time}'
    def __str__(self):
        return self.__repr__()

    def check(self):
        self.__execute()
            
    def __execute(self):  
        single = self.Person.IsSingle()      
        if not single:
            partner = Population.GetPartner(population, self.Person)
            lambd = mourningTimeLambda(partner.Age)
            etime = int(1/gen_exp(lambd))
            partner.SetSingle()
            partner.SetMourning(True)
            heapq.heappush(eventQueue, EndMourning(self.Time + etime, partner))
        for event in eventQueue:
            if self.Person == event.Person:
                eventQueue.remove(event)     
        heapq.heapify(eventQueue)        
        population.RemovePerson(self.Person)
        population.AddEvent(self) 
        print(f'{self}')


class PrefixedDeath(Event):
    def check(self):
        u = np.random.uniform()
        probs = fixedDeathProb(self.Person.IsWoman())
        for item in probs:
            agemin, agemax, prob = item
            if u <= prob:
                avage = int(np.random.uniform(agemin,agemax))
                dtime = (avage - self.Person.Age)*12
                heapq.heappush(eventQueue, Death(self.Time + dtime, self.Person))

class Pregnancy(Event):
    def __repr__(self):
        return f'Pregnancy in month {self.Time}'
    def __str__(self):
        return self.__repr__()

    def check(self):
        if self.Person.IsWoman() and not self.Person.IsSingle() and self.Person.CanHaveChildren() and self.Person.Partner.CanHaveChildren():
            p = pregnantProb(self.Person.Age)
            u = np.random.uniform()
            if u <= p:
                self._execute()
            else:
                heapq.heappush(eventQueue, Pregnancy(self.Time + 1, self.Person))
        
    def _execute(self):        
        self.Person.SetPregnant(True)
        population.AddEvent(self)
        print(f'{self}')
        father = Population.GetPartner(population, self.Person)
        heapq.heappush(eventQueue, Birth(self.Time + 9, self.Person, father))


class Breakup(Event):
    def __repr__(self):
        return f'Breakup in month {self.Time}'
    def __str__(self):
        return self.__repr__()

    def check(self):
        single = self.Person.IsSingle()
        mourn = self.Person.IsMourning()
        if single or mourn:
            return
        p = np.random.uniform()
        if p <= 0.2:
            self._execute()
        else:
            heapq.heappush(eventQueue, Breakup(self.Time + 6, self.Person))

    def _execute(self): 
        partner = Population.GetPartner(population, self.Person)
        lamd1 = mourningTimeLambda(self.Person.Age)
        lamd2 = mourningTimeLambda(partner.Age)
        etime1 = int(1/gen_exp(lamd1))
        etime2 = int(1/gen_exp(lamd2))
        population.AddEvent(self)
        print(f'{self}')
        partner.SetSingle() 
        partner.SetMourning(True)
        self.Person.SetSingle()
        self.Person.SetMourning(True)
        heapq.heappush(eventQueue,EndMourning(self.Time + etime1, self.Person))
        heapq.heappush(eventQueue,EndMourning(self.Time + etime2, partner))


class EndMourning(Event):
    def __repr__(self):
        return f'End Mourning in month {self.Time}'
    def __str__(self):
        return self.__repr__()
    
    def check(self):
        self._execute()
    
    def _execute(self):
        self.Person.SetMourning(False)
        female = self.Person.IsWoman()
        heapq.heappush(eventQueue, GetPartner(self.Time + 1, self.Person))


class GetPartner(Event):
    def __repr__(self):
        return f'Couple created in month {self.Time}'
    def __str__(self):
        return self.__repr__()

    def check(self):
        if self._person.Age < 12:
            return
        single = self.Person.IsSingle()
        mour = self.Person.IsMourning()
        if not single:
            return
        if mour:
            return
        if self.Person.IsWoman():
            if population.SingleMen == 0:
                heapq.heappush(eventQueue, GetPartner(self.Time + 3, self.Person)) 
                return   
        else:
            if population.SingleWomen == 0:
                heapq.heappush(eventQueue, GetPartner(self.Time + 3, self.Person))
                return 
        p = partnerWantedProb(self.Person.Age)
        u1 = np.random.uniform()
        if u1 <= p:
            self._execute()
        else:
            heapq.heappush(eventQueue, GetPartner(self.Time + 5, self.Person)) 
    
    def _execute(self):
        female = self.Person.IsWoman()  
        guy = population.GetSinglePerson(female)
        age_difference = abs(self.Person.Age - guy.Age)
        p = bePartnersProb(age_difference)
        u1 = np.random.uniform()
        if u1 <= p:
            self.Person.SetPartner(guy)
            part = Population.GetPartner(population, self.Person)
            part.SetPartner(self.Person)
            population.AddEvent(self)            
            print(f'{self}')
            heapq.heappush(eventQueue, Breakup(self.Time + 12, self.Person))
            heapq.heappush(eventQueue, Pregnancy(self.Time + 2, self.Person))
        else:
            heapq.heappush(eventQueue, GetPartner(self.Time + 3, self.Person))  
                     


class AgeUp(Event):
    def __repr__(self):
        return f'Person aged up in month {self.Time}'
    def __str__(self):
        return self.__repr__()
    

    def check(self):
        self.Person.AgeUp()
        population.AddEvent(self)
        print(f'{self}')
        if self.Person.Age == self.Person.DiesAge:
            heapq.heappush(eventQueue, Death(self.Time, self.Person))
            return
        heapq.heappush(eventQueue, AgeUp(self.Time + 12, self.Person))
        if self.Person.Age > 12:
            female = self.Person.IsWoman()
            heapq.heappush(eventQueue, GetPartner(self.Time + 2, self.Person))
        