# Databases Project
## Introduction
The aim of this project is to provide students with experience in developing database systems. The project is oriented by the industry’s best practices for software development; thus, students will experience all the main stages of a common software development project, from the very beginning to delivery.
## Objectives
After completing this project, students should be able to:
- Understand how a database application development project is organized, planned and executed
- Master the creation of conceptual and physical data models for supporting and persisting
application data
- Design, implement, test, and deploy a database system
- Install, configure, manage and tune a modern relational DBMS
- Understand client and server-side programming in SQL and PL/pgSQL (or similar).
## Descrição Funcional
Este projeto consiste em desenvolver um sistema típico de leilão, suportado por um sistema de gestão de base de dados. Um leilão é iniciado por um vendedor que define um artigo, indica o preço mínimo que está disposto a receber, e decide o momento em que o leilão vai terminar (data, hora e minuto). Os compradores fazem licitações que vão sucessivamente aumentando o preço até ao término do leilão. Ganha o comprador que licitar o valor mais alto.
Para simplificar a escolha do artigo que vai a leilão considera-se que cada artigo tem um código que o identifica univocamente (por exemplo, o código EAN de 13 dígitos vulgarmente encontrado junto com o código de barras dos artigos, ou o código ISBN de 10 ou 13 dígitos habitualmente usado para identificar livros). Para iniciar um novo leilão, um utilizador escolhe um artigo, limita o preço mínimo que pretende receber, e indica a data, hora e minuto em que o leilão irá terminar.
O sistema deve ser disponibilizado através de uma API REST que permita ao utilizador aceder ao sistema através de pedidos HTTP (quando conteúdo for necessário, deve ser usado JSON). A figura representa uma vista simplificada do sistema a desenvolver. Como podemos observar, o utilizador interage com o web server através da troca de request/response REST e por sua vez o web server interage com o servidor de base de dados através de uma interface SQL (e.g., JDBC no caso do Java, Psycopg no caso de Python).
Esta é uma das arquiteturas mais utilizadas atualmente e suporta muitas das aplicações web e mobile que usamos no dia a dia. Uma vez que o foco da disciplina está nos aspetos de bom desenho de uma base de dados e das funcionalidades associadas, o desenvolvimento de aplicações web ou mobile está fora do âmbito deste trabalho. Para usar ou testar a sua API REST, pode usar um cliente REST tal como o postman.com ou o curl.se. Nos casos em que o formato do pedido (req) e da resposta (res) estiver especificado nos parágrafos abaixo, estes devem ser seguidos. Nos casos em que não estiverem definidos, o grupo deve especificá-los e incluir a sua definição no relatório.
