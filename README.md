# raspagemmega
Este script raspa os dados da Mega-Sena a partir do arquivo divulgado pela Caixa Econômica Federal no site da loteria e o organiza em tabelas, facilitando sua manipulação.

Para a utilização do script, é necessário baixar os resultados divulgados em http://loterias.caixa.gov.br/wps/portal/loterias/landing/megasena, na seção "Download de todos os resultados". O script foi feito tendo como base o arquivo disponibilizado no link "Resultados da Mega sena por ordem de sorteio". Após baixar o arquivo, descompacte o html localmente e configure corretamente a variável "pagina" com o caminho deste arquivo.

Ao rodar o script, será gerado um arquivo do excel com duas tabelas: uma com as apostas ganhadoras da sena classificadas por sorteio e cidade, bem como o prêmio destinado a cada uma, e outra com os dados por sorteio (número do sorteio, data, números sorteados, arrecadações e rateios).

Além disso, a versão inicial do script agrega dados pesquisados externamente à base de dados divulgada pela Caixa: foi incluída uma coluna com os valores únicos de custo de aposta, o que possibilitou também calcular o número de apostas realizadas por sorteio (quando divulgada a arrecadação total).

Um exemplo das tabelas geradas por este script pode ser encontrado em https://docs.google.com/spreadsheets/d/1MT2jtvrlG_ogZ24q0ku66Ab5R3lFAF3KxYrQpEFu3Pc/edit?usp=sharing.

-------------------

Fontes sobre as datas de mudanças dos valores das apostas:

R$ 4,50: http://agenciabrasil.ebc.com.br/economia/noticia/2019-11/apostar-na-loteria-fica-mais-caro-mega-sena-vai-custar-r-450

R$ 3,50: http://agenciabrasil.ebc.com.br/economia/noticia/2015-04/apostar-na-mega-sena-ficara-mais-caro-partir-de-24-de-maio

R$ 2,50: http://agenciabrasil.ebc.com.br/economia/noticia/2014-04/precos-das-apostas-de-loteria-serao-reajustados

R$ 2,00: http://memoria.ebc.com.br/agenciabrasil/noticia/2009-08-13/mega-sena-e-lotofacil-ficam-mais-caras-em-setembro

R$ 1,75: http://g1.globo.com/Noticias/Brasil/0,,MUL588178-5598,00-PRECO+DA+APOSTA+DA+MEGASENA+TERA+AUMENTO+DE.html

R$ 1,50: http://memoria.ebc.com.br/agenciabrasil/noticia/2003-11-04/apostador-ja-paga-mais-caro-para-jogar-nas-loterias-da-caixa
