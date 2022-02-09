import datetime

#classe per le eccezioni
class ExamException(Exception):
    pass

#classe inizializzazione file
class CSVTimeSeriesFile:
    def __init__(self,name):
        #inizializzo il nome del file
        self.name = name
        
    #funzione per tornare una lista di liste
    def get_data(self):
        
        self.can_read = True

        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        #se non riesce a leggere una riga alzo un'eccezione
        except Exception:
            self.can_read = False
            print("Errore in apertura del file")
            raise ExamException("Impossibile leggere il file.")
            #stampo a schermo l'errore
            
        if not self.can_read:
            print("Errore in apertura!!") 
        else:
            lista = []
            format = "%Y-%m"
            lista2 =[]
            my_file = open(self.name,'r')
            #leggo ogni riga del file
            for line in my_file:

                element = line.replace('\n','').split(',')
                #leggo ogni elemento della riga
                for i in range(len(element)):
                    elem = element[i].strip()
                    
                    try:
                        #se l'elemento è una data in formato (YYYY-MM) vado avanti con il controllo, altimenti guardo se è un intero
                        datetime.datetime.strptime(elem, format)
                        #controllo che venga inserita solo una data nella lista e che venga inserita in prima posizione
                        try:
                            #se c'è già una data non faccio niente
                            datetime.datetime.strptime(lista2[0], format)
                            None
                        except:
                            #se invece c'è un intero metto la data in prima posizione e "scalo" l'intero in seconda posizione
                            if len(lista2) == 1:
                                lista2.insert(0,elem)
                            #se la lista è vuota inserisco la data
                            else:
                                lista2.append(elem)
                    #controllo che sia un intero
                    except:
                            try:
                                int(elem)
                                #se l'elemento è diverso da 0
                                if int(elem) > 0:
                                    #se la lista2 è vuota inserisco il numero(DOMANI RISCRIVI TOGLIENDO IL VALORE ASSOLUTO,SE IL NUMERO è NEGATIVO DEVO SALTARE LA RIGA) 
                                    if len(lista2)== 0:
                                        lista2.append(int(elem))
                                    elif len(lista2) == 1 and type(lista2[0])!= int:
                                        lista2.append(int(elem))        
                            except:
                                None
                #se ho inserito almeno un elemento nella lista2 e questo elemento è una data inserisco la lista2 nella lista principale, se l'elemento è un intero non va inserito in quanto avrò un dato senza la data associata quindi risulterà inutile
                if len(lista2)> 0 and type(lista2[0])!=int:
                    lista.append(lista2)
                    #"azzero" la lista2
                    lista2=[]
            i=1
            #ciclo for per controlare se nella lista principale ci sono date uguali o date non in ordine
            for list in lista:
                data = list[0]
                for x in range(i,len(lista)):
                    if data in lista[x]:
                        raise ExamException("Data duplicata!!")
                    elif data > lista[x][0]:
                        raise ExamException("Date non ordinate!!")
                i+=1
            return lista
            my_file.close()

def lista_pass(time_series,mese,first_year,last_year):
    passeg=[]
    
    for i in range(0,len(time_series)):
        anno = time_series[i][0]
        anno = datetime.datetime.strptime(anno, "%Y-%m")
        
        if int(anno.year) >= int(first_year) and int(anno.year) <= int(last_year):
            if mese == int(anno.month):
                if len(time_series[i])==1:
                    passeg.append(None)
                else:
                    passeg.append(time_series[i][1])
                
         
    return passeg

    
    

    
def calcolo_differenze(time_series,mese,first_year,last_year):
    passeg=[]
    passeg = (lista_pass(time_series,mese,first_year,last_year))
    print(passeg)
    result = []
    None_count = passeg.count(None)
    if int(last_year)-int(first_year) == 1:
        print(232334)
        if None in passeg:
            return 0
        else:
            return passeg[1] - passeg[0]
    else:
        if None_count == len(passeg)-1:
            return 0
        elif None_count == len(passeg):
            return 0
        else:
            for i in range(0,len(passeg)-1):
                if passeg[i] != None and passeg[i+1] != None:
                    result.append(passeg[i+1]-passeg[i])
                if passeg[i] == None and passeg[i+1] != None:
                    result.append(None)
                if passeg[i] != None and passeg[i+1] == None:
                    result.append(None)
    somm = 0
    cont = 0
    x = 0
    while x<len(result):
        if result[x] != None:
            somm = somm + result[x]
            cont = cont + 1
        x=x+1
    if cont == 0:
        return 0
    else: 
        return somm/cont






def compute_avg_monthly_difference(time_series, first_year, last_year):
    if type(first_year) != str:
        raise ExamException('first_year non è in formato stringa!!')
    else:
        try:
            int(first_year)
        except:
            raise ExamException('first_year non è un numero!!')

    if type(last_year) != str:
        raise ExamException('last_year non è in formato stringa!!')
    else:
        try:
            int(last_year)
        except:
            raise ExamException('last_year non è un numero!!')
    if int(first_year) == int(last_year):
        raise ExamException('Gli anni non possono essere uguali!')
    if int(first_year) > int(last_year):
        x=first_year
        first_year = last_year
        last_year = x
    lista = CSVTimeSeriesFile(name='data.csv')
    lista = lista.get_data()
    
    if time_series != lista:
        raise ExamException('La lista è sbagliata!')
    else:
        i=0
        trovato1 = False
        trovato2 = False
        
        while i<len(time_series) and not trovato1:
            anno1 = time_series[i][0]
            anno1 = datetime.datetime.strptime(anno1, "%Y-%m")
            if first_year == str(anno1.year):
                trovato1 = True
            else: 
                i=i+1

        while i<len(time_series) and not trovato2:
            anno2 = time_series[i][0]
            anno2 = datetime.datetime.strptime(anno2, "%Y-%m")
            if last_year == str(anno2.year):
                trovato2 = True
            else: 
                i=i+1

           

        if not trovato1 :
            raise ExamException('Il primo anno inserito non è presente nel file.')
        if not trovato2 :
            raise ExamException('Il secondo anno inserito non è presente nel file.')

        result=[]
        for i in range(0,12):
            result.append(calcolo_differenze(time_series,i+1,first_year,last_year))
        return(result)



time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()
#print(time_series)
result = compute_avg_monthly_difference(time_series,"1949","1951")
print(result)