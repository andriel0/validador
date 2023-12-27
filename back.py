import numpy as np
import pandas as pd
import requests
import json


class Validator:
    def __init__(self, path, cod, ind_file):
        self.path = path
        self.cod = cod
        self.ind_file = ind_file
        self.df_val = pd.DataFrame({})
        self.api = ''
        self.df_api = pd.DataFrame({})

    def pat_to_csv(self):
        with open(self.path, 'r') as pat_file:
            data = ''.join(pat_file.readlines())

        with open('my_file.csv', 'w') as csv:
            csv.write(data)

    def csv_to_df(self):
        df = pd.read_csv('my_file.csv', header=None, dtype=str)
        df.columns = ['tipo_doc', 'co_mun', 'registro_tombo', 'exer_orç', 'co_orgao',
                      'co_uni_orcamentaria', 'data_empenho', 'nu_empenho', 'data_ref']
        # df = df.sort_values(by='registro_tombo')
        self.df_val = df
        df.to_csv('df_att.csv', index=False)

    def get_json(self):
        api = requests.get(f'https://api-dados-abertos.tce.ce.gov.br/empenhos_bens?codigo_municipio={self.cod}&quantidade=100&deslocamento=0&data_referencia=202311')
        api_json = api.json()
        self.api = api_json['data']['data']
        if self.cod != '061':
            api = requests.get(f'https://api.tce.ce.gov.br/index.php/sim/1_0/empenhos_bens.json?codigo_municipio={self.cod}')
            api_json = api.json()
            self.api = api_json['rsp']['_content']
        self.df_api = pd.DataFrame(self.api)
        self.df_api.to_csv('./df_da_api.csv', index=False)

    def relationship_cols(self):
        self.df_val['registro_tombo'] = self.df_val['registro_tombo'].astype('str')
        regs_bem = [self.df_api.iloc[row, 1] for row in range(len(self.df_api))]

        match self.ind_file:
            case 1:
                with open('Relatório.txt', 'w') as txt:
                    txt.write(f'Arquivo BN - Código {self.cod}')
                for ind, value in enumerate(self.df_val['registro_tombo']):
                    # if len(value) < 20:
                    #     self.df_val.iloc[ind, 2] = f"{('0'* (20 - len(value))) + value}"
                    if self.df_val.iloc[ind, 2] in regs_bem:
                        with open('Relatório.txt', 'r') as read:
                            data_txt = ''.join(read.readlines())
                            with open('Relatório.txt', 'w') as txt:
                                txt.write(f'{data_txt}\nLinha {ind+1} - O Número de Registro ou Tombo do Bem já está cadastrado.')
                    else:
                        texto = ''
                        # ind_tombo = regs_bem.index(self.df_val.iloc[ind, 2])
                        if len(self.df_val.iloc[ind, 0]) != 3:
                            texto += f'Tipo de Documento têm {len(self.df_val.iloc[ind, 0])} posições e tem de ter 3 posições.'
                        if len(self.df_val.iloc[ind, 1]) != 3:
                            texto += f'Código de Município têm {len(self.df_val.iloc[ind, 1])} posições e tem de ter 3 posições.'
                        if len(self.df_val.iloc[ind, 2]) != 20:
                            texto += f'Número de Registro ou Tombo do Bem têm {len(self.df_val.iloc[ind, 2])} posições e tem de ter 20 posições.'
                        if len(self.df_val.iloc[ind, 3]) != 6:
                            texto += f'Exercício do Orçamento têm {len(self.df_val.iloc[ind, 3])} posições e tem de ter 6 posições.'
                        if len(self.df_val.iloc[ind, 4]) != 2:
                            texto += f'Código do Órgão que emitiu o Empenho para a Aquisição do Bem têm {len(self.df_val.iloc[ind, 4])} posições e tem de ter 2 posições.'
                        if len(self.df_val.iloc[ind, 5]) != 2:
                            texto += f'Código da Unidade Orçamentária que emitiu o Empenho para a Aquisição do Bem têm {len(self.df_val.iloc[ind, 5])} posições e tem de ter 2 posições.'
                        if len(self.df_val.iloc[ind, 6]) != 8:
                            texto += f'Data da Nota de Empenho de Aquisição do Bem têm {len(self.df_val.iloc[ind, 4])} posições e tem de ter 8 posições.'
                        if not 0 < len(str(self.df_val.iloc[ind, 7])) <= 8:
                            texto += f'Número da Nota de Empenho de Aquisição do Bem têm {len(self.df_val.iloc[ind, 4])} posições e tem de ter de 1 até 8 posições.'
                        if self.df_val.iloc[ind, 7] is np.NaN:
                            texto += f'Número da Nota de Empenho de Aquisição do Bem está nulo e tem de ter de 1 até 8 posições.'
                        if len(self.df_val.iloc[ind, 8]) != 6:
                            texto += f'Data de Referência da Documentação têm {len(self.df_val.iloc[ind, 4])} posições e tem de ter 6 posições.'
                        if texto != '':
                            with open('Relatório.txt', 'r') as read:
                                data_txt = ''.join(read.readlines())
                            with open('Relatório.txt', 'w') as txt:
                                txt.write(f'{data_txt}\nLinha {ind+1} - {texto}')

            case _:
                pass
