from src.eventTools import *
from src.populationTools import *

class Simulation:
    def __init__(self, simTime: int, populationSize: int, ageAverage: int, ageDeviation: int, womenAmount=0):
        self._simTime = simTime*12
        self._currentTime = 0
        self._eventsQueue = []
        self._population = Population()
        self._psize = populationSize
        self._age = ageAverage
        self._agedev = ageDeviation
        self._women = womenAmount

    def __set_initial_sate__(self, populationSize: int, ageAverage: int, ageDeviation: int, womenAmount):
        self._population.SetInitialValues(populationSize, ageAverage, ageDeviation, womenAmount)
        for person in self._population:
            heapq.heappush(self._eventsQueue, AgeUp(self._currentTime + 12, self._eventsQueue, person, self._population))
            heapq.heappush(self._eventsQueue, GetPartner(self._currentTime, self._eventsQueue,person,self._population))

    def __run__(self):
        while(len(self._eventsQueue) != 0 and self._currentTime < self._simTime):
            event = heapq.heappop(self._eventsQueue)
            self._currentTime += (event.Time - self._currentTime)
            event.check()
        self._population.PrintLog()

    def Start(self):
        self.__set_initial_sate__(self._psize, self._age, self._agedev, self._women)        
        self.__run__()

