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
