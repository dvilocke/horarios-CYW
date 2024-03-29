from typing import List, Dict
import random
import pandas as pd

class Almanac:
    def __init__(self, days:List, persons:List, starCriteria:str, smallAlmanac: Dict, listOfPeopleWhoDoesNotRest: List, hoursPerWorker = 48) -> None:
        self.days = days
        self.persons = persons
        self.available = []
        self.copy = []
        self.weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        self.starCriteria = starCriteria
        self.hoursPerWorker = hoursPerWorker
        self.smallAlmanac = smallAlmanac
        self.listOfPeopleWhoDoesNotRest = listOfPeopleWhoDoesNotRest

    #funcion mas dificil
    def generateScheduleWithPeople(self):
        counterWeekdays = self.weekdays.index(self.starCriteria)
        resetDay = self.days[0].getDay

        for day in self.days:

            if counterWeekdays == len(self.weekdays):
                counterWeekdays = 0

            #cada vez que se complete un ciclo de la semana debo reiniciar los datos, datos de las personas disponibles !!!! ---> nada
            if self.weekdays[counterWeekdays] == resetDay:
                for person in self.persons:
                    person.resetData()

            #cada dia se debe actualizar los datos para estar revisnando ----> nada
            self.getAvailable(day=day.getNumberDay, nameDay=day.getDay)


            #si ya no existe nadie que no pueda mas debo romper todo esto, porque entraria en un ciclo infinito ---> listo
            if len(self.available) == 0:
                counterWeekdays += 1
                continue

            #Existe la posibilidad de que en available quede solo una persona, entonces se debe controlar eso --> listo
            if len(self.available) == 1:
                aPerson = random.choice(self.available)
                whatSchedule = random.choice(['day','afternoon'])
                if self.weekdays[counterWeekdays] == 'sunday' and aPerson not in self.listOfPeopleWhoDoesNotRest:
                    aPerson.setMustRestOneDay = True
                    #aqui es para en que parte de la semana debe descansar
                    #dayYouHaveToRest = random.choice(self.smallAlmanac[day.getNumberDay])
                    #aPerson.daysOff.append({day.getDay:dayYouHaveToRest})
                    #aPerson.setRestDay = dayYouHaveToRest
                    aPerson.setRestDay = day.getNumberDay + 1

                aPerson.hoursWorked  = int(aPerson.getHoursWorked) - int(self.hoursPerWorker / 7)

                aPerson.workedDays += 1

                if whatSchedule == 'day':
                    day.getPointerToPersonsDay.append(aPerson)
                else:
                    day.getPointerToPersonsAfternoon.append(aPerson)
            
                del self.available[self.available.index(aPerson)]


            #Aqui se controla cuando en la lista de disponibles existen mas de dos personas --> listo
            else:
                counter = 0
                while True:
                    if counter == day.getNumberPeople:
                        #debo revisar si el horario de la mañana esta lleno y el de la tarde, reiniciar los horarios y los datos del usuario ---> Listo
                        if len(day.getPointerToPersonsDay) > 0 and len(day. getPointerToPersonsAfternoon) > 0:
                            self.copy = []
                            break

                        else:
                            #bedo reiniciar los valores tanto el horario de la mañana y el horario de la tarde, tambien la clase persona que actulizo sus valores  -> listo
                            self.__resetValues(day=day)
                            counter = 0
                            self.available += self.copy
                            self.copy = []

                    else:
                        aPerson = random.choice(self.available)
                        whatSchedule = random.choice(['day','afternoon'])
                        if whatSchedule == 'day':
                            if aPerson not in day.getPointerToPersonsDay:
                                counter += 1
                                if self.weekdays[counterWeekdays] == 'sunday' and aPerson not in self.listOfPeopleWhoDoesNotRest:
                                    aPerson.setMustRestOneDay = True
                                    #dayYouHaveToRest = random.choice(self.smallAlmanac[day.getNumberDay])
                                    #aPerson.daysOff.append({day.getDay:dayYouHaveToRest})
                                    #aPerson.setRestDay = dayYouHaveToRest
                                    aPerson.setRestDay = day.getNumberDay + 1

                                aPerson.hoursWorked  = int(aPerson.getHoursWorked) + int(self.hoursPerWorker / 7)

                                aPerson.workedDays += 1

                                day.getPointerToPersonsDay.append(aPerson)

                                self.copy.append(aPerson)

                                del self.available[self.available.index(aPerson)]

                            else:
                                del self.available[self.available.index(aPerson)] 
                        else:
                            if aPerson not in day.getPointerToPersonsAfternoon:
                                counter += 1

                                if self.weekdays[counterWeekdays] == 'sunday' and aPerson not in self.listOfPeopleWhoDoesNotRest:
                                    aPerson.setMustRestOneDay = True
                                    #dayYouHaveToRest = random.choice(self.smallAlmanac[day.getNumberDay])
                                    #aPerson.daysOff.append({day.getDay:dayYouHaveToRest})
                                    #aPerson.setRestDay = dayYouHaveToRest
                                    aPerson.setRestDay = day.getNumberDay + 1

                                aPerson.hoursWorked  = int(aPerson.getHoursWorked) + int(self.hoursPerWorker / 7)

                                aPerson.workedDays += 1

                                day.getPointerToPersonsAfternoon.append(aPerson)

                                self.copy.append(aPerson)

                                del self.available[self.available.index(aPerson)]

                            else:
                                del self.available[self.available.index(aPerson)]
            
            counterWeekdays += 1
            self.available = []

        return {
            self.__totalWeightOnlyNumber():self.days
        }

    def getAvailable(self, day, nameDay):
        #fucnion que debo revisar bien
        self.__sundaySystem(day=day)
        for person in self.persons:
            #como los domingos se modifican, siempre quedarian con un valur True, entonces debemos hacer que un dia true y el otro no --> Nada
            if self.__deserveADayOff(person):
                if self.__reviewHours(person):
                    #como esto se actualiza cada dia, van a ver personas que no quedaron en ese dia y van a cumplir con las condiciones y se vuelve agregar, controlar eso -->listo
                    if self.__systemOfDaysNotToWork(person, nameDay):
                        if self.__systemDayExcluderSystem(person):
                            if person not in self.available:
                                self.available.append(person)
                else:
                    if person in self.available:
                        del self.available[self.available.index[person]]
                    
            else:
                if person in self.available:
                    del self.available[self.available.index[person]]


    def printSchedule(self):
        for day in self.days:
            msg = f"day:{day.getDay}, weight:{day.getWeight}, weightUpdate:{day.getWeightUpdated}, weight_M({day.getWeightMorning})_A({day.getWeightAfternoon})-------->{[f'{person.getName}({person.getWeight})' for person in day.getPointerToPersonsDay]}, {[f'{person.getName}({person.getWeight})' for person in day.getPointerToPersonsAfternoon]}"
            print(msg)

        print(self.__countWeightScheduleWithPeople())

    def __systemDayExcluderSystem(self, person):
        #este sistema fue creado porque Franciso, Jhoana y Cris son de apoyo, es decir maximo dos dias
        if person.workedDays > person.daysAllowedToWork and person.activateExclusiveSystem:
            return False
        return True
    

    def __systemOfDaysNotToWork(self, person, day):
        #este sistema fue creado porque Julian no puede trabajar algunos dias  jueves, sabado, domingo-> Julian
        if day not in person.getNonwWorkingDays:
            return True
        return False

    def __sundaySystem(self, day):
        #que pasa si todos dos caen un domingo y no pueden trabajar al otro dia
        for person in self.persons:
            if day > person.getRestDay:
                person.setMustRestOneDay = False

    def __deserveADayOff(self, person):
        if not person.getMustRestOneDay:
            return True
        return False

    def __reviewHours(self, person):
        #function to evaluate the hours of a person
        if person.getHoursWorked != self.hoursPerWorker:
            return True
        return False

    def __resetValues(self, day):
        for person in day.getPointerToPersonsDay:
            if person.getHoursWorked == 0:
                person.setHoursWorked = 0
            else:
                person.hoursWorked  = int(person.getHoursWorked) - int(self.hoursPerWorker / 7)

            if person.workedDays == 0:
                person.workedDays = 0
            else:
                person.workedDays = person.workedDays - 1

            person.setMustRestOneDay = False
            person.setRestDay = 0

        for person in day.getPointerToPersonsAfternoon:
            if person.getHoursWorked == 0:
                person.setHoursWorked = 0

            else:
                person.hoursWorked  = int(person.getHoursWorked) - int(self.hoursPerWorker / 7)

            if person.workedDays == 0:
                person.workedDays = 0
            else:
                person.workedDays = person.workedDays - 1
            
            person.setMustRestOneDay = False
            person.setRestDay = 0

        day.stockReset()

    def seeDaysWithoutThePeople(self) -> str:
        #function that shows the days with less information, that's why the components were created -- it works
        index = [day.getNumberDay for day in self.days]
        readyToShow = []
        for day in self.days:
            component = f'day:{day.getDay}, weight:{day.getWeightUpdated},weight_M({day.getWeightMorning})_A({day.getWeightAfternoon})'
            readyToShow.append(component)

        return pd.Series(data=readyToShow, index=index)

    def __totalWeightOnlyNumber(self) -> int:
        component = 0
        for day in self.days:
            component += day.getWeightUpdated + (day.getWeightMorning * sum([int(person.getWeight) for person in day.getPointerToPersonsDay])) + (day.getWeightAfternoon * sum([int(person.getWeight) for person in day.getPointerToPersonsAfternoon]))
        return component

    def __countWeightScheduleWithPeople(self):
        component = 0
        for day in self.days:
            component += day.getWeightUpdated + (day.getWeightMorning * sum([int(person.getWeight) for person in day.getPointerToPersonsDay])) + (day.getWeightAfternoon * sum([int(person.getWeight) for person in day.getPointerToPersonsAfternoon]))        
        return f'\nThe sum total of the weights with the pople is:{component}'

    def countDaysWeightWithoutPeople(self)  -> str:
        #function that calculates the total of the days according to their weight without the people  -- it works
        return f'\nThe sum total of the weights without the people is:{sum([day.getWeightUpdated + (day.getWeightMorning+day.getWeightAfternoon) for day in self.days])}'
