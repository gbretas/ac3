import os
import sys
import random
import shutil

#esquema de analise final

# analise/final/trace-XY/Z-V.txt
# X é a trace de comparacao 1
# Y é a trace de comparacao 2
# Z é a arquitetura 1
# V é a arquitetura 2

# Ou seja, na pasta trace-11 eu so comparo execuções da trace 1 vs execuções da trace 1

# Em um arquivo 1-2.txt eu comparo a arquitetura 1 com a arquitetura 2

# Pasta de resultados brutos:
# res_brutos/XY.txt
# X é a arquitetura
# Y é a trace



# 1.1 -> WriteBack e LRU - Trace 1
# 1.2 -> WriteBack e LRU - Trace 2
# 2.1 -> WriteBack e FIFO - Trace 1
# 2.2 -> WriteBack e FIFO - Trace 2
# 3.1 -> WriteThrough e LRU- Trace 1
# 3.2 -> WriteThrough e LRU - Trace 2
# 4.1 -> WriteThrough e FIFO- Trace 1
# 4.2 -> WriteThrough e FIFO - Trace 2

# 1 -> WriteBack e LRU
# 2 -> WriteBack e FIFO
# 3 -> WriteThrough e LRU
# 4 -> WriteThrough e FIFO

def readfile(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    return lines

def manual():
    invert = 0 

    arq1 = str(input("Digite o numero da arquitetura 1: "))
    arq2 = str(input("Digite o numero da arquitetura 2: "))
    trace1 = str(input("Digite o numero do trace 1: "))
    trace2 = str(input("Digite o numero do trace 2: "))

    nome = "arq-" + arq1 + "-" + arq2 + "-tr-" + trace1 + "-"+trace2+".txt"
    
    if nome == "":
        print("Nome inválido")
        exit()

    #check file exists
    if not os.path.isfile('result1.txt'):
        print("File result1.txt not found")
        exit()
    if not os.path.isfile('result2.txt'):
        print("File result2.txt not found")
        exit()

    if invert == 1:
        result1 = readfile('result2.txt')
        result2 = readfile('result1.txt')
    else:
        result1 = readfile('result1.txt')
        result2 = readfile('result2.txt')

    if len(result1) != len(result2):
        print("Files have different number of lines")
        exit()

    iguais = 0
    diferencas = 0
    dados_comparados = 0

    if not os.path.exists('final_manual'):
        os.makedirs('final_manual')

    final = open('final_manual'+nome, 'w')

    for i in range(len(result1)):
        dados_comparados += 1
        linha1 = result1[i]
        linha2 = result2[i]

        text = linha1.split(":")


        final.write(text[0])

        # if line is empty
        if ":" in linha1:
            dado1 = float(linha1.split(":")[1].strip())
            dado2 = float(linha2.split(":")[1].strip())

            if linha1 != linha2:
                diferencas+=1
                #calculate percentage
                porcentagem = (dado2/dado1)
                porcentagem_show = round(porcentagem*100,3)

                diff = dado2 - dado1
                change = round(diff/dado1,3)
                if change > 0:
                    change_show = "+" + str(round(change*100,2))
                else:
                    change_show = str(round(change*100,2))


                final.write(": " + str(round(dado1,3)) + " != " + str(round(dado2,3)))
                # final.write(" |  (" + str(porcentagem_show) + "%)")
                final.write(" | ("+str(change_show)+"%)\n")
            else:
                iguais+=1
                final.write(": " + str(round(dado1,3)) + " = " + str(round(dado2,3)) + "\n")

        else:
            dados_comparados-=1

    print("Dados comparados: " + str(dados_comparados))
    print("Quantidade de diferenças entre os resultados : " + str(diferencas))
    print("Quantidade de dados iguais entre os resultados : " + str(iguais))

    final.write("="*75 + "\n\n")
    final.write("Dados comparados: " + str(dados_comparados) + "\n")
    final.write("Quantidade de diferenças entre os resultados : " + str(diferencas) + "\n")
    final.write("Quantidade de dados iguais entre os resultados : " + str(iguais) + "\n\n")
    final.write("Percentual de diferenças entre os resultados : " + str(round(diferencas/dados_comparados*100, 2)) + "%\n")
    final.write("Percentual de iguais entre os resultados : " + str(round(iguais/dados_comparados*100,2)) + "%\n\n")
    final.write("="*75 + "\n")



    final.close()

def auto():

    #read all files from folder resultados
    files = os.listdir('res_brutos')
    comparacoes = 0
    for file in files:
        for file2 in files:
            if file == file2:
                print("Saltando arquivo iguais: " + file+"")
                continue

            comparacoes += 1
            
            result1 = readfile('res_brutos/'+file)
            result2 = readfile('res_brutos/'+file2)

            iguais = 0
            diferencas = 0
            dados_comparados = 0
            
            file_final_name = file.split(".")[0]
            file2_final_name = file2.split(".")[0]

            trace1 = int(file.split(".")[1])
            trace2 = int(file2.split(".")[1])

            if(trace1 == 1) and (trace2 == 1):
                trace_folder = "trace-11"
            elif(trace1 == 1) and (trace2 == 2):
                trace_folder = "trace-12"
            elif(trace1 == 2) and (trace2 == 1):
                trace_folder = "trace-21"
            elif(trace1 == 2) and (trace2 == 2):
                trace_folder = "trace-22"
            else:
                print("Trace não encontrado")
                exit()

            if not os.path.exists('final'):
                os.makedirs('final')

            final_name = "final/"+trace_folder+"/"+file_final_name+"-"+file2_final_name+".txt"

            final = open(final_name, 'w')

            for i in range(len(result1)):
                ultimo = ""
                dados_comparados += 1
                linha1 = result1[i]
                linha2 = result2[i]

                text = linha1.split(":")

                final.write(text[0])

                # if line is empty
                if ":" in linha1:
                    dado1 = float(linha1.split(":")[1].strip())
                    dado2 = float(linha2.split(":")[1].strip())

                    if linha1 != linha2:
                        diferencas+=1
                        #calculate percentage
                        try:
                            porcentagem = (dado2/dado1)
                            diff = dado2 - dado1
                            change = round(diff/dado1,3)
                        except ZeroDivisionError:
                            porcentagem = 0
                        porcentagem_show = round(porcentagem*100,3)
     
                        if change > 0:
                            change_show = "+" + str(round(change*100,2))
                        else:
                            change_show = str(round(change*100,2))


                        final.write(": " + str(round(dado1,3)) + " != " + str(round(dado2,3)))
                        final.write(" | ("+str(change_show)+"%)\n")
                    else:
                        iguais+=1
                        final.write(": " + str(round(dado1,3)) + " = " + str(round(dado2,3)))
                        final.write(" | (0.0%)\n")

                else:
                    dados_comparados-=1

            # print("Dados comparados: " + str(dados_comparados))
            # print("Quantidade de diferenças entre os resultados : " + str(diferencas))
            # print("Quantidade de dados iguais entre os resultados : " + str(iguais))

            # print("Comparação entre " + file + " e " + file2 + " finalizada")

            final.write("="*75 + "\n\n")
            final.write("Dados comparados: " + str(dados_comparados) + "\n")
            final.write("Quantidade de diferenças entre os resultados : " + str(diferencas) + "\n")
            final.write("Quantidade de dados iguais entre os resultados : " + str(iguais) + "\n\n")
            final.write("Percentual de diferenças entre os resultados : " + str(round(diferencas/dados_comparados*100, 2)) + "%\n")
            final.write("Percentual de iguais entre os resultados : " + str(round(iguais/dados_comparados*100,2)) + "%\n\n")
            final.write("="*75 + "\n")



            final.close()
    print(str(comparacoes)+" comparações finalizada")

def comparar_arquiteturas(arquitetura1, trace1, arquitetura2, trace2):
    file1 = readfile('res_brutos/'+str(arquitetura1)+'.'+str(trace1)+'.txt')
    file2 = readfile('res_brutos/'+str(arquitetura2)+'.'+str(trace2)+'.txt')

    iguais = 0
    diferencas = 0
    dados_comparados = 0

    for i in range(len(file1)):
        dados_comparados += 1
        linha1 = file1[i]
        linha2 = file2[i]

        text = linha1.split(":")

        if ":" not in linha1 and linha1 != "\n" and linha1 != "\n":
            print (linha1)

        if ":" not in linha1:
            dados_comparados-=1

        if ":" in linha1:
            dado1 = float(linha1.split(":")[1].strip())
            dado2 = float(linha2.split(":")[1].strip())
            if linha1 != linha2:
                diferencas+=1
                try:
                    porcentagem = (dado2/dado1)
                    diff = dado2 - dado1
                    change = round(diff/dado1,3)
                except ZeroDivisionError:
                    porcentagem = 0
     
                if change > 0:
                    change_show = "+" + str(round(change*100,2))
                else:
                    change_show = str(round(change*100,2))

                dadoanalisado = text[0]
                if change > 0:
                    print(dadoanalisado + " cresceu de " + str(round(dado1,3)) + " para " + str(round(dado2,3)) + " representando um crescimento de " + str(change_show) + "%")
                elif change < 0:
                    print(dadoanalisado + " diminuiu de " + str(round(dado1,3)) + " para " + str(round(dado2,3)) + " representando uma queda de " + str(change_show) + "%")

                # print(text[0] + ": " + str(round(dado1,3)) + " != " + str(round(dado2,3)) + " | ("+str(change_show)+"%)")
            else:
                iguais+=1

    if iguais == dados_comparados:
        print("\nTodos os dados são iguais")


    return

def comparar():
    print("\nArquiteturas:")
    print("1 - WB e LRU")
    print("2 - WB e FIFO")
    print("3 - WT e LRU")
    print("4 - WT e FIFO")

    print("\nTraces:")
    print("1 - Muita leitura de dado(16), Muito Fetch de Instrução(16) e Pouca Gravação de dado(8)")
    print("2 - Média gravação de dado(12), Muito fetch de instrução(20) e pouca leitura de dado(8)")
    print("")

    arquitetura1 = int(input("Digite o número da primeira arquitetura [1-4]: "))
    trace1 = int(input("Digite o trace da primeira arquitetura [1-2]: "))

    print("")

    arquitetura2 = int(input("Digite o número da primeira arquitetura [1-4]: "))
    trace2 = int(input("Digite o trace da primeira arquitetura [1-2]: "))

    if arquitetura1 > 4 or arquitetura1 < 1 or arquitetura2 > 4 or arquitetura2 < 1:
        print("Arquitetura inválida")
        exit()
    if trace1 > 2 or trace1 < 1 or trace2 > 2 or trace2 < 1:
        print("Trace inválido")
        exit()

    if arquitetura1 == 1:
        arq_text = "WB e LRU"
    elif arquitetura1 == 2:
        arq_text = "WB e FIFO"
    elif arquitetura1 == 3:
        arq_text = "WT e LRU"
    elif arquitetura1 == 4:
        arq_text = "WT e FIFO"

    if arquitetura2 == 1:
        arq_text2 = "WB e LRU"
    elif arquitetura2 == 2:
        arq_text2 = "WB e FIFO"
    elif arquitetura2 == 3:
        arq_text2 = "WT e LRU"
    elif arquitetura2 == 4:
        arq_text2 = "WT e FIFO"


    print("\nComparando arquitetura "+str(arq_text)+" usando trace "+str(trace1)+" com a arquitetura "+str(arq_text2)+" usando trace "+str(trace2)+"\n")
    print("="*75)
    comparar_arquiteturas(arquitetura1, trace1, arquitetura2, trace2)


    return
    
def gerador_trace():
    traces = int(input("Digite a quantidade de traces para gerar: "))
    if not os.path.exists('tracegen'):
        os.makedirs('tracegen')
    if traces < 1:
        print("Número inválido")
        exit()
    for i in range(traces):
        trace = open("tracegen/trace" + str(i) + ".txt", "w")
        for i in range(random.randint(0,50)):
            trace.write(str(random.choice([0, 1, 2])) + " " + str(random.choice([0,1,2,3,4,5,6,7,8,9,10,"a","b","c","d","e","f"])) + "\n")
        trace.close()

def delete_all_traces():
    if os.path.exists('tracegen'):
        shutil.rmtree('tracegen')
    return


def comparar_tempo_total():
    
    desempenho = []

    folders = [f.path for f in os.scandir('./final') if f.is_dir()]
    for folder in folders:
        arqs = os.listdir(folder)
        for arq in arqs:
            if arq.endswith(".txt"):
                arq_path = os.path.join(folder, arq)
                line_number = 0
                with open(arq_path, 'r') as f:
                    for line in f:
                        line_number+=1
                        if line_number == 57:
                            change = line.split("| ")[1].strip()
                            trace = folder.split("/")[-1]
                            arq_helper = arq_path.split("/")[-1]
                            arq_helper = arq_helper.split(".")[0]
                            arq1 = arq_helper.split("-")[0]
                            arq2 = arq_helper.split("-")[1]

                            change = change.replace("(", "")
                            change = change.replace(")", "")
                            change = change.replace("%", "")

                            obj = {"trace": trace, "arq1": arq1, "arq2": arq2, "change": change}
                            desempenho.append(obj)
    #Saiu do loop

    #order by change and consider negative
    desempenho = sorted(desempenho, key=lambda k: float(k['change']), reverse=False)
    for i in desempenho:
        if float(i['change']) > 0:
            print(i["trace"]+" - A arquitetura "+i["arq1"]+" em relação a arquitetura "+i["arq2"]+", aumentou o tempo total em "+i["change"]+"%")
        elif float(i['change']) < 0:
            print(i["trace"]+" - A arquitetura "+i["arq1"]+" em relação a arquitetura "+i["arq2"]+", diminuiu o tempo total em "+i["change"]+"%")
        else:
            print(i["trace"]+" - A arquitetura "+i["arq1"]+" em relação a arquitetura "+i["arq2"]+", não alterou o tempo total")
    # print(desempenho)
        #ler cada arquivo e organizar pela linha 57



if __name__ == "__main__":
    print("\nBem vindo ao Robo-Cache\n")
    print("============ Comparações =============")
    print("1 - Comprar duas arquiteturas/traces")
    print("2 - Comparar entre vários arquivos brutos")
    print("========= Analisar arquivos ==========")
    print("3 - Analisar estatistícas entre duas arquiteturas/traces")
    print("4 - Analisar tempo total geral")
    print("========= Funções de Traces  =========")
    print("6 - Gerar traces aleatórias")
    print("7 - Deletar todos os arquivos de traces")
    print("")
    choice = int(input("Digite a sua escolha: "))
    if choice == 1:
        manual()
    elif choice == 2:
        auto()
    elif choice == 3:
        comparar()
    elif choice == 4:
        comparar_tempo_total()
    elif choice == 6:
        gerador_trace()
    elif choice == 7:
        delete_all_traces()
    else:
        print("Invalid choice")
        exit()