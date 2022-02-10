import datetime
import math
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
                        #se l'elemento è una data in formato (YYYY-MM) vado avanti con il controllo, altrimenti guardo se è un intero
                        datetime.datetime.strptime(elem, format)
                        mese = datetime.datetime.strptime(elem, "%Y-%m")
                        
                        if int(mese.month) >= 1 or int(mese.month)<= 12:
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
                            if int(elem) != 0:
                                    #se la lista2 è vuota inserisco il numero 
                                if len(lista2)== 0:
                                    lista2.append(abs(int(elem)))
                                elif len(lista2) == 1 and type(lista2[0])!= int:
                                    lista2.append(abs(int(elem)))        
                        except:
                            try:
                                float(elem)
                                if float(elem) > 0:
                                    #se la lista2 è vuota inserisco il numero
                                    if len(lista2)== 0:
                                        lista2.append(abs(math.floor(float(elem))))
                                    elif len(lista2) == 1 and type(lista2[0])!= int:
                                        lista2.append(abs(math.floor(float(elem))))
                                if float(elem)<0: 
                                    if len(lista2)== 0:
                                        lista2.append(abs(math.ceil(float(elem))))
                                    elif len(lista2) == 1 and type(lista2[0])!= int:
                                        lista2.append(abs(math.ceil(float(elem))))
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
                data1 = datetime.datetime.strptime(data, "%Y-%m")
                for x in range(i,len(lista)):
                    data2 = lista[x][0]
                    data2 = datetime.datetime.strptime(data2, "%Y-%m")
                    if data in lista[x]:
                        raise ExamException("Data duplicata!!")
                    elif data1.year == data2.year and int(data1.month) > int(data2.month):
                        raise ExamException("Date non ordinate!!")
                    elif data1.year > data2.year:
                        raise ExamException("Date non ordinate!!")
                i+=1
            my_file.close()         
            return lista
            
#funzione per creare una lista con tutti i numeri dei passeggeri di un determinato mese
def lista_pass(time_series,mese,first_year,last_year):
    passeg=[]
    #ciclo su tutta la lista di liste time_series
    for i in range(0,len(time_series)):
        anno = time_series[i][0]
        anno = datetime.datetime.strptime(anno, "%Y-%m")
        #se l'anno della lista è compreso tra gli anni limiti controllo che il mese sia quello che sto cercando
        diff = int(last_year)-int(first_year)
        cont = 1
        if int(anno.year) >= int(first_year) and int(anno.year) <= int(last_year):
            
            #se il mese è uguale controllo che abbia il numero di passeggeri registrato, in caso contrario inserisco None nella lista
            
            if mese == int(anno.month):
                if len(time_series[i])==1:
                    passeg.append(None)
                else:
                    #se la lista ha il numero registrato, inserisco quel numero nella lista
                    passeg.append(time_series[i][1])
                
                
    #ritorno la lista di passeggeri di quel mese
    return passeg

    
    

#funzione che calcola le differenze e la media
def calcolo_differenze(time_series,mese,first_year,last_year):
    passeg=[]
    #chiamo la funzione che mi contruisce la lista di passeggeri in un determinato mese, in un arco di anni
    passeg = (lista_pass(time_series,mese,first_year,last_year))
    print(passeg)
    result = []
    #funzione che conta quanti None ci sono all'interno della lista di passeggeri
    None_count = passeg.count(None)
    #se sto facendo un calcolo su due anni:
    if int(last_year)-int(first_year) == 1:
        #se dei due mesi c'è anche solo un None restituisco 0
        if None in passeg:
            return 0
        else:
            #altrimenti restituisco solo la differenza
            return passeg[1] - passeg[0]
    #se sto lavorando su più di due anni
    else:
        #se c'è solo un valore dentro la lista restituisco 0
        if None_count == len(passeg)-1:
            return 0
        #se ci sono solo valori None restituisco 0 (in realtà noi supponiamo che ci sia almeno un valore, quindi forse è inutile)
        elif None_count == len(passeg):
            return 0
        else:
            #in tutti gli altri casi faccio un ciclo sulla lista di passeggeri:
            for i in range(0,len(passeg)-1):
                #se non ci sono due valori None faccio la differenza tra i due e la inserisco in una lista result
                if passeg[i] != None and passeg[i+1] != None:
                    result.append(passeg[i+1]-passeg[i])
                #se il primo valore è None e il secondo no, aggiungo None alla lista result
                if passeg[i] == None and passeg[i+1] != None:
                    result.append(None)
                #stessa cosa per il secondo valore
                if passeg[i] != None and passeg[i+1] == None:
                    result.append(None)
    somm = 0
    cont = 0
    x = 0
    #ciclo su lista result
    while x<len(result):
        #se il valore non è None, sommo la somma con il valore e incremento cont di 1
        if result[x] != None:
            somm = somm + result[x]
            cont = cont + 1
        x=x+1
        #se cont è a 0 vuol dire che non ho inserito neanche un valore, restituisco 0
    if cont == 0:
        return 0
    #altrimenti restituisco la somma diviso cont
    else: 
        return somm/cont






def compute_avg_monthly_difference(time_series, first_year, last_year):
    #controllo su input di first e last year
    if type(first_year) != str:
        raise ExamException('first_year non è in formato stringa!!')
    else:
        try:
            #se non è un numero alzo eccezione
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
    #se i due anni sono uguali alzo un'eccezione
    if int(first_year) == int(last_year):
        raise ExamException('Gli anni non possono essere uguali!')
    #se first year viene dopo last year li scambio 
    if int(first_year) > int(last_year):
        x=first_year
        first_year = last_year
        last_year = x
    #richiamo la funzione CSVTimeSeriesFile per poi confrontare il risultato con la time_series inserita, se sono diverse alzo un'eccezione
    lista = CSVTimeSeriesFile(name='data.csv')
    lista = lista.get_data()
    
    if time_series != lista:
        raise ExamException('La lista è sbagliata!')
    else:
        #altrimenti continuo e controllo che gli anni inseriti siano presenti nella time_series
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


        #se non li trova alzo un'eccezione
        if not trovato1:
            raise ExamException('Il primo anno inserito non è presente nel file.')
        if not trovato2:
            raise ExamException('Il secondo anno inserito non è presente nel file.')
        
        result=[]
        #ciclo che per ogni mese chiama la funzione calcolo_differenze e inserisce nella lista result i risultati
        for i in range(0,12):    result.append(calcolo_differenze(time_series,i+1,first_year,last_year))
        return(result)



#time_series_file = CSVTimeSeriesFile(name='data.csv')
#time_series = time_series_file.get_data()
#print(time_series)
#result = compute_avg_monthly_difference(time_series,"1949","1951")
#print(result)