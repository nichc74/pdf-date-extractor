# pdf-date-extractor

How to run:
docker-compose up --build

Once the containers have spun up you can hit:
http://localhost:8080/

Once the page has loaded you can start uploading files for extraction.
Please note certain pdf files may not be able to be read by the PDF reader(looking at you fw4.pdf...)

Project Document: https://docs.google.com/document/d/1vGUPuPU6t6Xl8aMtUJPhyaKWNvNNzbzHSUsKGjlieuo/edit?usp=sharing

For test PDF documents to try out you can use the ones in "Test harbour documents"
The only document from the samples given is that returns an error is fw4.pdf.
This seems to be an issue between the pdf reader and the data coming from the document.
Further investigation is needed.

Test Documents and contained dates:
t1
11/20/2020
2022/09/12
31 October 2022

t2
2022-04-11
12-07-2022
07 December 2022
11-20-2020

t3
10 September 2022 - 27 November 2022

ada-1
10 December 1815
27 November 1852
02/09/2021

TestInsertMe
11/11/2020

Terms of Service
10/30/2019
April 10, 2019 (not extracted)

fw4 (not readable)
