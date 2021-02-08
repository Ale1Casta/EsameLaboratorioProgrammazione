class ExamException(Exception):
    pass




class CSVTimeSeriesFile:

    def __init__(self, name):
        
        # Setto il nome del file
        self.name = name


    def get_data(self):

        # lista vuota per salvare i valori
        values = []
        

        # Provo ad aprire il file per estrarne i dati. Se non ci riesco, avverto dell'errore, interrmompo esecuzione

        try: 
            my_file = open(self.name, 'r')

        except:
            raise ExamException('Errore nella lettura del file')
            return None # Esco dalla funzione


        # leggo il file
        for line in my_file:
            
            # Faccio lo split di ogni linea sulla virgola
            try:
                elements = line.split(',')
                assert(len(elements) == 2)
            except:
                 print("La lista non è di due elementi: ", line)

            # Non processo l'intestazione
            if elements[0] != 'epoch':
                    
                # Setto la data ed il valore
                epoch  = elements[0]
                temperature = elements[1]
                
                # converto "epoch" in int se non riesco devo fare in modo che si salti il valore silenziosamente (errore recoverable)
                # converto "temperature"
                
                try:
                    epoch = int(epoch)
                    temperature = float(temperature)
                except:

                    # Vado al prossimo "giro" del ciclo, NON eseguo l'append
                    continue
                
                
                
                # Infine aggiungo alla lista dei valori questo valore
                subList = (epoch, temperature)
                values.append(list(subList))


        # Controllo se lista finale è vuota, nel caso avrò file vuoto o valori no nconvertibili secondo esigenza
        
        if values == []:
            raise ExamException("File in imput è vuoto o contiene valori non utilizzabili")
        

        # Controllo misurazioni ordine crescente
        epo = []
        for i in values:
            epo.append(i[0])

        ord = sorted(epo)
        
        try: 
            assert(epo == ord) 
        except:
            raise ExamException("Le misurazioni non sono ordinate")


        

    
        my_file.close()
        return values



#-____________________________________________________________-
#--------------------------------------------------------------
#______________________________________________________________


def daily_stats(lista_dati):
    
    i = 0
    j = 0

    # creo lista con valore inizio tutti i giorni del mese
    giorni = []

   

    # lista con min, max, media di ogni giorno
    risult = []

    for n in range(len(lista_dati)):
        day_start_epoch = lista_dati[n][0] - (lista_dati[n][0] % 86400)
        giorni.append(day_start_epoch)
        


    '''#controllo se giorni è ordinato
    ord = sorted(giorni)
    try: 
        giorni == ord 
    except:
        raise ExamException("Le misurazioni non sono ordinate")'''

    #tolgo doppioni e riordino giorni
    giorni = list(sorted(set(giorni)))


    '''controllo se ho un mese di dati
    try:
        assert(len(giorni) in [28, 29, 30, 31])
    except:
        raise ExamException("Mese non completo, dati mancanti")'''


    #--------------------------------------------------------------------------
    #creo lista con valori temp giorno per giorno e ne calcolo min, max, media
    #--------------------------------------------------------------------------

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

        risult.append([mini, mas, media])
        i+=1


    return risult 
        




try:
    time_series_file = CSVTimeSeriesFile(name='data.csv')
    time_series = time_series_file.get_data()
    print(daily_stats(time_series))
except ExamException as t:
    print(t)
