class ExamException(Exception):
    pass




class CSVTimeSeriesFile:

    def __init__(self, name):
        
        # Setto il nome del file
        self.name = name


    def get_data(self):

        # lista vuota per salvare i valori
        values = []

        if( type(self.name) is not str or self.name == None):
            raise ExamException("Nome file non è una stringa")
        

        # Provo ad aprire il file per estrarne i dati. Se non ci riesco, avverto dell'errore, interrompo esecuzione

        try: 
            my_file = open(self.name, 'r')

        except:
            raise ExamException('Errore nella lettura del file')
            return None


        # leggo il file
        for line in my_file:
            
            # Faccio lo split di ogni linea sulla virgola
            try:
                elements = line.split(',')
                assert(len(elements) == 2)
            except:
                 continue
                
                

            # Non processo l'intestazione
            if elements[0] != 'epoch':
                    
                # Setto la data ed il valore
                epoch  = elements[0]
                temperature = elements[1]


                # converto "epoch" in int e "temperature" in float se non riesco devo fare in modo che si salti il valore silenziosamente (errore recoverable)
                
                try:
                    epoch = int(epoch)
                    temperature = float(temperature)
                except:

                    # Vado al prossimo "giro" del ciclo, NON eseguo l'append
                    continue
                
                
                
                # Aggiungo alla lista dei valori questo valore
                subList = (epoch, temperature)
                values.append(list(subList))


        # Controllo se lista finale è vuota, nel caso avrò file vuoto o valori non convertibili secondo esigenza
    
        if values == []:
            raise ExamException("File in input è vuoto o tutti valori non utilizzabili")
        

        # Controllo date siano ordine crescente
        epo = []
        for i in values:
            epo.append(i[0])

        ord = sorted(epo)
        
        try: 
            assert(epo == ord) 
        except:
            raise ExamException("Le misurazioni non sono ordinate")

        # controllo se ci sono date doppie
        for i in range(1,len(values)):
            if values[i][0] == ord[i-1]:
                raise ExamException("Sono presenti epoch duplicati")


        
        my_file.close()
        return values

        

#______________________________________________________________
#--------------------------------------------------------------
#______________________________________________________________




#data lista in input creo un altra lista con min, max, media di ogni giorno
def daily_stats(lista_dati):
    
    i = 0
    j = 0
    giorni = [] #lista con valore inizio tutti i giorni del mese
    risultato = []


    #controllo lista in input sia effettivamente una lista
    try:
        assert(type(lista_dati) is list)
    except:
        raise ExamException("Errore: non hai dato una lista in input")

    # controllo se ho una lista di liste
    for el in lista_dati:
        if type(el) is not list or len(el) != 2:
            raise ExamException("Errore: elemento lista in input non è una lista di due elementi")




    # creo lista con giorni di origine della misurazione
    for n in range(len(lista_dati)):
        day_start_epoch = lista_dati[n][0] - (lista_dati[n][0] % 86400)
        giorni.append(day_start_epoch)
        


    #controllo se giorni è ordinato
    ord = sorted(giorni)
    try: 
        giorni == ord 
    except:
        raise ExamException("Le misurazioni non sono ordinate")

    #tolgo doppioni e riordino giorni
    giorni = list(sorted(set(giorni)))


    '''controllo se ho un mese di dati
    try:
        assert(len(giorni) in [28, 29, 30, 31])
    except:
        raise ExamException("Mese non completo, dati mancanti")'''


    #--------------------------------------------------------------------
    #creo lista con valori temp giorno per giorno e ne calcolo min, max, media
    #--------------------------------------------------------------------

    while i < len(giorni):

        #lista temperature per giornata
        temp_g = []

        # se il giono di partenza continua ad essere lo stesso iterando su lista_dati salvo le temperature su temp_g

        while (j < len(lista_dati)) and giorni[i] == (lista_dati[j][0] - (lista_dati[j][0] % 86400)):

            temp_g.append(lista_dati[j][1])
            j+=1
        
        mas = max(temp_g)
        mini = min(temp_g)
        media = sum(temp_g)/ len(temp_g)

        risultato.append([mini, mas, media])
        i+=1


    return risultato 
        


try:
    time_series_file = CSVTimeSeriesFile(name='data.csv')
    time_series = time_series_file.get_data()
    print(daily_stats(time_series))
except ExamException as t:
    print(t)
