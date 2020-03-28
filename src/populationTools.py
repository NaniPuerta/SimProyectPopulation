import numpy as np
from random import sample
from src.probData import childsWantedProb, partnerWantedProb, fixedDeathProb
from src.probabilityTools import gen_normal

class Person:
    def __init__(self,person_id: int, age: int, iswoman: bool):
        self.__person_id = person_id
        self.__age = age
        self.__single = True
        self.__partner_want = False
        self.__partner = None
        self.__kids_have = 0
        self.__woman = iswoman
        self.__mourning = False
        self.__pregnant = False
        self.__events = []
        self.__deadAge = 0
        prob = np.random.uniform()
        child = 0
        for x in range(5):
            if prob <= childsWantedProb(x):
                child = x+1
                break
        self.__kids_want = child
        
        u = np.random.uniform()
        probs = fixedDeathProb(self.__woman)
        for item in probs:
            agemin, agemax, prob = item
            if u <= prob:
                avage = int(np.random.uniform(agemin,agemax))
                self.__deadAge = avage
        
    def __eq__(self, anotherPerson):
        return self.Id == anotherPerson.Id
    
    def __hash__(self):
        return self.Id

    @property
    def Age(self):
        return self.__age

    @property
    def DiesAge(self):
        return self.__deadAge

    @property
    def Id(self):
        return self.__person_id

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
    
    

class Population:
    def __init__(self):
        self.__people = []
        self.__peopleDict = {}
        self.__number_of_people = 0
        self.__women = 0
        self.__men = 0
        self.__births = 0
        self.__deaths = 0
        self.__multiple_births = 0
        self.__events = []
        self.removed = []

    @property
    def People(self):
        return self.__people

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

    @property
    def SingleMen(self):
        return len(self.__GetSinglePeople(True))

    @property
    def SingleWomen(self):
        return len(self.__GetSinglePeople(False))

    def GetSinglePerson(self, women):
        singles = self.__GetSinglePeople(not women)
        guy = sample(singles, 1)[0]
        pers = self.__Find_Person(guy.Id)
        return pers

    def __GetSinglePeople(self, women: bool) -> list:
        singles = []
        if women:            
            for i in self.__people:
                if i.IsSingle() and not i.IsMourning() and not i.IsWoman():
                    singles.append(i)
        else:
            for i in self.__people:
                if i.IsSingle() and not i.IsMourning() and i.IsWoman():
                    singles.append(i)
        return singles

    def AddSingle(self, person, female):
        pers = self.__Find_Person(person.Id) 
        if not pers or person.Age < 12:
            return
        pers.SetSingle()                
        

    def GetNextId(self):
        self.__number_of_people += 1
        return self.__number_of_people
    
    def RemoveSingle(self, person, female):
        try:
            if female:
                pers = self.__Find_Person(person.Id, self._single_women)
                self._single_women.remove(pers)
                return True
            else:
                pers = self.__Find_Person(person.Id, self._single_men)
                self._single_men.remove(pers)
                return True
        except KeyError:
            return False
    
    def UpdateBirths(self, multiple: bool):
        if multiple:
            self.__multiple_births += 1
        self.__births += 1

    def RemovePerson(self, person: Person):
        female = person.IsWoman()
        pers = self.__Find_Person(person.Id)
        persid = pers.Id
        self.__people.remove(pers)
        self.__peopleDict.pop(persid)
        self.__deaths += 1
        self.removed.append(persid)
    
    def NewPerson(self, age, female):
        pid = self.GetNextId()
        per = Person(pid, age, female)
        self.__people.append(per)
        self.__peopleDict[pid] = per 
        return per

    def __Find_Person(self, personId: int):
        return self.__peopleDict[personId]
        
    @staticmethod
    def GetPartner(self, person: Person):
        guy = person.Partner.Id
        return self.__Find_Person(guy)
        
    def SetInitialValues(self, populationSize: int, ageAverage: int, ageDeviation: int, womenAmount=0):
        if womenAmount > 0:
            count = 0
            for i in range(womenAmount):
                u = np.random.uniform()
                age = gen_normal(35, 100)
                print(age)
                pers1 = self.NewPerson(age, True)
            for i in range(populationSize-womenAmount):
                u = np.random.uniform()
                age = gen_normal(35, 100)
                print(age)
                pers1 = self.NewPerson(age, False)
            #agesw = np.random.normal(ageAverage, ageDeviation, womenAmount)
            #agesm = np.random.normal(ageAverage, ageDeviation, populationSize-womenAmount)
            #for i in agesw:
            #    pers1 = self.NewPerson(i, True)
            #for i in agesm:
            #    pers2 = self.NewPerson(i, False)                
        else:
            for i in range(populationSize):
                u = np.random.uniform() 
                age = gen_normal(35, 100)
                genderprob = np.random.uniform()
                female = genderprob < 0.5
                pers1 = self.NewPerson(age, female)
            #ages = np.random.normal(ageAverage, ageDeviation, populationSize)
            #for i in ages: 
            #    genderprob = np.random.uniform()
            #    female = genderprob < 0.5
            #    pers = self.NewPerson(i, female)

           
    def __iter__(self):
        return self.__people.__iter__()
    
    def AddEvent(self, eventLog):
        self.__events.append(eventLog)
    
    def PrintLog(self):
        print('------------------------------')
        print(f'Total People in Population: {len(self.__people)}')
        print(f'Total Births: {self.__births}')
        print(f'Multiple Births: {self.__multiple_births}')
        print(f'Total Deaths: {self.__deaths}')

    def Log(self):
        st = f'Total People in Population: {len(self.__people)}\nTotal Births: {self.__births}\nMultiple Births: {self.__multiple_births}\nTotal Deaths: {self.__deaths}\n'
        return st