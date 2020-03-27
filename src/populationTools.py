import numpy as np
from src.probData import childsWantedProb, partnerWantedProb

class Person:
    def __init__(self, age: int, iswoman: bool):
        self.__age = age
        self.__single = True
        self.__partner_want = False
        self.__partner = None
        self.__kids_have = 0
        self.__woman = iswoman
        self.__mourning = False
        self.__pregnant = False
        self.__events = []
        prob = np.random.uniform()
        child = 0
        for x in range(5):
            if prob <= childsWantedProb(x):
                child = x+1
                break
        self.__kids_want = child
        

    @property
    def Age(self):
        return self.__age

    @property
    def Partner(self):
        return self.__partner
    
    @property
    def KidsWanted(self):
        return self.__kids_want

    @property
    def CurrentKids(self):
        return self.__kids_have

    
    def IsWoman(self) -> bool:
        return self.__woman

    def IsPregnant(self) -> bool:
        return self.__pregnant

    def IsSingle(self) -> bool:
        return self.__single

    def IsMourning(self) -> bool:
        return self.__mourning

    def CanHaveChildren(self) -> bool:
        return self.__kids_have < self.__kids_want

    def WantsPartner(self) -> bool:
        return self.__partner_want

    def SetSingle(self):
        self.__partner = None
        self.__single = True
        self.__mourning = True

    def SetPartner(self, person):
        self.__partner = person
        self.__single = False
    
    def SetPregnant(self, value: bool):
        self.__pregnant = value
    
    def SetWantedChildren(self, value):
        self.__kids_want = value

    def SetGender(self, value):
        if value < 0.5:
            self.__woman = True
    
    def SetAge(self, value):
        self.__age = value

    def SetMourning(self, value):
        self.__mourning = value

    def SetWantsPartner(self, value: bool):
        self.__partner_want = value

    def AgeUp(self):
        self.__age += 1
    
    def UpdateChildren(self, value: int):
        self.__kids_have += value
    
    @staticmethod
    def SetPerson(person, age: int, iswoman: bool, wantedchildren: int):
        person.__age = age
        person.__woman = iswoman
        person.__kids_want = wantedchildren
        person.__kids_have = 0
        person.__partner = None
        person.__mourning = False
        person.__single = True

class Population:
    def __init__(self):
        self.__people = []
        self.__women = 0
        self.__men = 0
        self.__births = 0
        self.__deaths = 0
        self.__multiple_births = 0
        self._single_women = []
        self._single_men = []
        self.__events = []

    @property
    def TotalWomen(self):
        return self.__women

    @property
    def TotalMen(self):
        return self.__men

    @property
    def TotalBirths(self):
        return self.__births

    @property
    def TotalDeaths(self):
        return self.__deaths

    @property
    def MultipleBirths(self):
        return self.__multiple_births

    def GetSinglePeople(self, women: bool):
        if women:
            return self._single_women
        else:
            return self._single_men

    def AddPerson(self, person: Person):
        self.__people.append(person)   
    
    def AddSingle(self, person, female):
        if female:
            self._single_women.append(person)
        else:
            self._single_men.append(person)
    
    def RemoveSingle(self, person, female):
        if female:
            self._single_women.remove(person)
        else:
            self._single_men.remove(person)
    
    def UpdateBirths(self, multiple: bool):
        if multiple:
            self.__multiple_births += 1
        self.__births += 1

    def RemovePerson(self, person: Person):
        #if person.IsSingle():
        #    if person.IsWoman():
        #        self._single_women.remove(person)
        #    else:
        #        self._single_men.remove(person)
        self.__people.remove(person)
        self.__deaths += 1
    
    def AgeUp(self):
        for person in self.__people:
            person.AgeUp()

    def SetInitialValues(self, populationSize: int, ageAverage: int, ageDeviation: int, womenAmount=0):
        if womenAmount > 0:
            agesw = np.random.normal(ageAverage, ageDeviation, womenAmount)
            agesm = np.random.normal(ageAverage,ageDeviation,populationSize-womenAmount)
            for i in agesw:
                self.__make_woman__(int(i))
            for i in agesm:
                self.__make_man__(int(i))
        else: 
            ages = np.random.normal(ageAverage, ageDeviation, populationSize)
            for i in ages: 
                genderprob = np.random.uniform()
                isFemale = genderprob < 0.5
                if isFemale:
                    self.__make_woman__(int(i))
                else:
                    self.__make_man__(int(i))

    def __make_woman__(self, age: int):
        person = Person(age, True)
        prob = np.random.uniform()
        person.SetWantsPartner(prob < partnerWantedProb(age))
        self.__people.append(person)
        self._single_women.append(person)
        self.__women += 1
    
    def __make_man__(self, age: int):
        person = Person(age, False)
        prob = np.random.uniform()
        person.SetWantsPartner(prob < partnerWantedProb(age))
        self.__people.append(person)
        self._single_men.append(person)
        self.__men += 1

           
    def __iter__(self):
        return self.__people.__iter__()
    
    def AddEvent(self, eventLog):
        self.__events.append(eventLog)
    
    def PrintLog(self):
        for event in self.__events:
            print(event)
        print('------------------------------')
        print(f'Total People in Population: {len(self.__people)}')
        print(f'Total Births: {self.__births}')
        print(f'Multiple Births: {self.__multiple_births}')
        print(f'Total Deaths: {self.__deaths}')
        