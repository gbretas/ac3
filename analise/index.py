import os
import sys

# 1.1 -> WriteBack e LRU - Trace 1
# 1.2 -> WriteBack e LRU - Trace 2
# 2.1 -> WriteBack e FIFO - Trace 1
# 2.2 -> WriteBack e FIFO - Trace 2
# 3.1 -> WriteThrough e LRU- Trace 1
# 3.2 -> WriteThrough e LRU - Trace 2
# 4.1 -> WriteThrough e FIFO- Trace 1
# 4.2 -> WriteThrough e FIFO - Trace 2

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

    final = open('final/'+nome, 'w')

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
            
            result1 = readfile('resultados/'+file)
            result2 = readfile('resultados/'+file2)

            iguais = 0
            diferencas = 0
            dados_comparados = 0
            
            file_final_name = file.split(".txt")[0]
            file2_final_name = file2.split(".txt")[0]

            final_name = "final/"+file_final_name+"-"+file2_final_name+".txt"

            final = open(final_name, 'w')

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
                        # final.write(" |  (" + str(porcentagem_show) + "%)")
                        final.write(" | ("+str(change_show)+"%)\n")
                    else:
                        iguais+=1
                        final.write(": " + str(round(dado1,3)) + " = " + str(round(dado2,3)) + "\n")

                else:
                    dados_comparados-=1

            # print("Dados comparados: " + str(dados_comparados))
            # print("Quantidade de diferenças entre os resultados : " + str(diferencas))
            # print("Quantidade de dados iguais entre os resultados : " + str(iguais))

            print("Comparação entre " + file + " e " + file2 + " finalizada")

            final.write("="*75 + "\n\n")
            final.write("Dados comparados: " + str(dados_comparados) + "\n")
            final.write("Quantidade de diferenças entre os resultados : " + str(diferencas) + "\n")
            final.write("Quantidade de dados iguais entre os resultados : " + str(iguais) + "\n\n")
            final.write("Percentual de diferenças entre os resultados : " + str(round(diferencas/dados_comparados*100, 2)) + "%\n")
            final.write("Percentual de iguais entre os resultados : " + str(round(iguais/dados_comparados*100,2)) + "%\n\n")
            final.write("="*75 + "\n")



            final.close()
    print(str(comparacoes)+" comparações finalizada")

    

if __name__ == "__main__":
    choice = int(input("1 - Manual\n2 - Auto\nDigite a sua escolha: "))
    if choice == 1:
        manual()
    elif choice == 2:
        auto()
    else:
        print("Invalid choice")
        exit()