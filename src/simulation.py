from src.eventTools import *
from src.populationTools import *


class Simulation:
    def __init__(self, simTime: int, populationSize: int, ageAverage: int, ageDeviation: int, womenAmount=0):
        self._simTime = simTime*12
        self._currentTime = 0
        self._eventsQueue = []
        self._psize = populationSize
        self._age = ageAverage
        self._agedev = ageDeviation
        self._women = womenAmount
    
    @property
    def CurrentTime(self):
        return self._currentTime

    @property
    def EndTime(self):
        return self._simTime

    def __set_initial_sate__(self, populationSize: int, ageAverage: int, ageDeviation: int, womenAmount):
        population.SetInitialValues(populationSize, ageAverage, ageDeviation, womenAmount)
        for person in population.People:
            heapq.heappush(eventQueue, AgeUp(self.CurrentTime + 12, person))
            heapq.heappush(eventQueue, GetPartner(self.CurrentTime, person))

    def __run__(self):
        while(len(eventQueue) != 0 and self.CurrentTime < self.EndTime):
            event = heapq.heappop(eventQueue)
            oldtime = self.CurrentTime
            self._currentTime += (event.Time - oldtime)
            event.check()
        population.PrintLog()

    def Start(self):
        self.__set_initial_sate__(self._psize, self._age, self._agedev, self._women)   
        self.__run__()

