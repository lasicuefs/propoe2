# Propoe-V2

## Visão Geral

O [PROPOE](https://linguamatica.com/index.php/linguamatica/article/view/369) *(prose to poem)* é uma ferramenta que gera poemas a partir de sentenças métricas extraídas de prosas literárias brasileiras. A extração das sentenças das obras literárias é realizada através do [MIVES](https://github.com/lasicuefs/mives) *(Mining Verse Structure)*.  Por sua vez, o PROPOE combina essas sentenças mediante um algoritmo guloso que busca otimizar localmente os critérios rítmicos.

Nessa segunda versão foram implementadas melhorias e adicionados novos critérios rítmicos em comparação com a [primeira versão](https://github.com/lasicuefs/propoe), além da migração do código-fonte de JAVA para Python. Foram implementados ajustes na filtragem de sentenças candidatas, no cálculo dos escores dos versos, alteração do parâmetro de metro para que o usuário possa definir metros diferentes para cada verso, adição dos critérios de rima interna, consoante e toante, inclusão dos parâmetros de esquema rítmico e peso dos critérios. Este último permite que o usuário defina quais critérios devem ser mais importantes no momento da montagem do poema.

## Código

Para roda o código basta executar o arquivo *propoe2/run.py*

Os parâmentros podem ser alterados no arquivo *propoe2/configuration/conf.py*. Abaixo segue a definição de cada um dos parâmetros:

**- padrao_ritmico:** define a quantidade de versos e estrofes do poema, bem como a estrutura de rima.

**- mives_xml:** arquivo com as sentenças métricas extraídas do MIVES. No código está o conjunto de sentenças referentes à obra *Os Sertões* de Euclides da Cunha.

**- metrificacao:** é o metro de cada um dos versos. Esse *array* deve ter o tamanho igual à quantidade de versos do poema.

**- pesos_avaliacao:** nesse dicionário são configurados os pesos dos critérios, os quais definem a importância de cada um dos critérios na montagem do poema.

**- seed:** é a semente aleatória, caso seja alterada de *None* para algum número positivo irá gerar o mesmo poema diante dos mesmos parâmetros de entrada.

**- filename:** este não é um parâmetro de fato do sistema, é um arquivo que guarda um *log* da execução do sistema.
