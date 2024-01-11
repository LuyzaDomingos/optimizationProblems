from mip import *

filmes = [
    "All quiet on the Western Front", "Avatar: The Way of Water", "The Banshees of Inisherin", "Elvis", "Everything Everywhere All at Once",
    "The Fabelmans","Tár", "Top Gun: Maverick", "Triangle of Sadness","Women Talking", "Blonde", "To Leslie", "The whale",
    "Living", "Aftersun", "Causeway", "Glass Onion", "Babylon", "Guillermo del Toro's Pinocchio", "Marcel the Shell With Shoes On",
    "Puss in Boots: The Last Wish", "The Sea Beast", "Turning Red", "The Boy, the Mole, the Fox and the Horse",
    "Ice Merchants", "My Year of Dicks", "An Ostrich Told Me the World is Fake, and I Think I Believe It", "An Irish Goodbye",
    "Ivalu","Le Pupille", "Nattrikken", "The Red Suitcase", "Mrs. Harris Goes to Paris", "Batman","Tell It Like a Woman",
    "RRR", "Bardo, False Chronicle of a Handful of Truths", "Empire of Light", "The Elephant Whisperers","Haulout",
    "How Do You Measure a Year?", "The Martha Mitchell Effect", "Stranger at the Gate", "All That Breathes", 
    "Fire of Love", "A House Made of Splinters", "Navalny", "Argentina 1985", "Close", "EO", "The Quiet Girl"
]


tempoFilme = {
    "All quiet on the Western Front": 2.47,
    "Avatar: The Way of Water":3.2,
    "The Banshees of Inisherin":1.9,
    "Elvis":2.65,
    "Everything Everywhere All at Once":2.32,
    "The Fabelmans":2.52,
    "Tár":2.63,
    "Top Gun: Maverick":2.17,
    "Triangle of Sadness":2.45,
    "Women Talking":1.74,
    "Blonde":2.78,
    "To Leslie":1.98,
    "The whale":1.97,
    "Living":1.7,
    "Causeway":1.37,
    "Aftersun":1.7,
    "Glass Onion":2.32,
    "Babylon":3.15,
    "Guillermo del Toro's Pinocchio":1.95 ,
    "Marcel the Shell With Shoes On":1.5,
    "Puss in Boots: The Last Wish":1.7,
    "The Sea Beast":1.92,
    "Turning Red":1.7,
    "The Boy, the Mole, the Fox and the Horse":0.5,
    "Ice Merchants":0.23,
    "My Year of Dicks":0.4,
    "An Ostrich Told Me the World is Fake, and I Think I Believe It":0.19,
    "An Irish Goodbye":0.38,
    "Ivalu":0.27,
    "Le Pupille":0.62,
    "Nattrikken":0.25,
    "The Red Suitcase":0.3,
    "Mrs. Harris Goes to Paris":1.92,
    "Batman":2.93,
    "Tell It Like a Woman":1.87,
    "RRR":3.12,
    "Bardo, False Chronicle of a Handful of Truths":2.65,
    "Empire of Light":1.98,
    "The Elephant Whisperers":0.68,
    "Haulout":0.42,
    "How Do You Measure a Year?":0.48,
    "The Martha Mitchell Effect":0.67,
    "Stranger at the Gate":0.48,
    "All That Breathes":1.62,
    "Fire of Love":1.63,
    "A House Made of Splinters":1.45,
    "Navalny":1.65,
    "Argentina 1985":2.33,
    "Close":1.73,
    "EO":1.33,
    "The Quiet Girl":1.58
 }

genero = ['guerra','ficcaoCientifica', 'comedia', 'biografia', 'musical', 'drama', 'satira','animacao',
          'animacaocurtametragem','dramacurtametragem','misterio','melodrama','documentariocurtametragem','documentario','suspense','acao']

generoFilme = {
    "All quiet on the Western Front": 'guerra',
    "Avatar: The Way of Water":'ficcaoCientifica',
    "The Banshees of Inisherin":'comedia',
    "Elvis":'musical',
    "Everything Everywhere All at Once":'ficcaoCientifica',
    "The Fabelmans":'biografia',
    "Tár":'drama',
    "Top Gun: Maverick":'aventura',
    "Triangle of Sadness":'satira',
    "Women Talking":'drama',
    "Blonde":'biografia',
    "To Leslie":'drama',
    "The whale":'drama',
    "Living":'drama',
    "Causeway":'drama',
    "Aftersun":'drama',
    "Glass Onion":'misterio',
    "Babylon":'comedia',
    "Guillermo del Toro's Pinocchio":'animacao',
    "Marcel the Shell With Shoes On":'animacao',
    "Puss in Boots: The Last Wish":'animacao',
    "The Sea Beast":'animacao',
    "Turning Red":'animacao',
    "The Boy, the Mole, the Fox and the Horse":'animacaocurtametragem',
    "Ice Merchants":'animacaocurtametragem',
    "My Year of Dicks":'animacaocurtametragem',
    "An Ostrich Told Me the World is Fake, and I Think I Believe It":'animacaocurtametragem',
    "An Irish Goodbye":'dramacurtametragem',
    "Ivalu":'dramacurtametragem',
    "Le Pupille":'dramacurtametragem',
    "Nattrikken":'dramacurtametragem',
    "The Red Suitcase":'dramacurtametragem',
    "Mrs. Harris Goes to Paris":'melodrama',
    "Batman":'acao',
    "Tell It Like a Woman":'drama',
    "RRR":'acao',
    "Bardo, False Chronicle of a Handful of Truths":'comedia',
    "Empire of Light":'romance',
    "The Elephant Whisperers":'documentariocurtametragem',
    "Haulout":'documentariocurtametragem',
    "How Do You Measure a Year?":'documentariocurtametragem',
    "The Martha Mitchell Effect":'documentariocurtametragem',
    "Stranger at the Gate":'documentariocurtametragem',
    "All That Breathes":'documentario',
    "Fire of Love":'documentario',
    "A House Made of Splinters":'documentario',
    "Navalny":'documentario',
    "Argentina 1985":'suspense',
    "Close":'drama',
    "EO":'drama',
    "The Quiet Girl":'drama'
}

#inicialização dos dados
HD = 6
D = range(1, 25)
F = range(len(filmes))
Tf = list(tempoFilme.values())
G = range(len(genero))
Fg = []
for g in genero:
  aux = []
  for f in F:
    if generoFilme[filmes[f]] == g:
      aux.append(f)
  Fg.append(aux)
F_index = {i: f for i, f in enumerate(filmes)}
G_index = {i: g for i, g in enumerate(genero)}

#modelo
modelo = Model(sense = MINIMIZE, solver_name = CBC)

#variaveis
x = {f: {d: modelo.add_var(var_type=BINARY,name=f"x_{f}_{d}") for d in D} for f in F}
y = {d: modelo.add_var(var_type=BINARY,name=f"y_{d}") for d in D}
z = {g: {d: modelo.add_var(var_type=BINARY,name=f"z_{g}_{d}") for d in D} for g in G}

#função objetivo
modelo.objective = xsum(y[d] for d in D)

#um filme deve ser assistido exatamente em um dia
for f in F:
    modelo += xsum(x[f][d] for d in D) == 1

#a capacidade de horas não pode ser excedida no dia
for d in D:
    modelo += xsum(x[f][d] * Tf[f] for f in F)<= HD * y[d]

#filmes do mesmo gênero não pode ser assistidos no mesmo dia
for d in D:
  for g in G:
    modelo += xsum(x[f][d] for f in Fg[g]) <= z[g][d]

#modelo escrito
modelo.write("modelo.lp")
with open("modelo.lp", "r") as r:
  print(r.read())
  
#otimizar modelo  
modelo.optimize()
status = modelo.optimize()
print(f"Status = {status}\n")

#solução
if status == OptimizationStatus.OPTIMAL:
    print(f"São necessários no mínimo {int(modelo.objective_value)} dias para assistir todos os filmes.\n")
    
    dia = 1
    print("Filmes para assitir no ")
    for d in D:
        filmes = [(F_index[f], Tf[f], generoFilme[F_index[f]]) for f in F if int(x[f][d].x) >= 0.99]
        if filmes:
            print(f"\n Dia {dia}:")
            total_time = 0
            for filme, tempo, genero in filmes:
                print(f"\t- Filme: {filme}")
                print(f"\t  Tempo: {tempo} horas")
                print(f"\t  Gênero: {genero}")
                total_time += tempo
                hora = total_time * 60
                resto = ((hora % 60) / 100)*60
                quociente = hora // 60
                hora1 = resto + (quociente*60)
                horareal = hora1/60
            print(f"Tempo total gasto no dia:" "{0:.2f}h".format(horareal))
            dia += 1
else:
    print(f"Solução não foi encontrada\n")