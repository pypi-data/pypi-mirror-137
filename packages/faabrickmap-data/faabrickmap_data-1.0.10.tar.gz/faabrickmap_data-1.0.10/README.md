# Faabrick-Map-data

** How to import a csv file **

- Use comma as separator in the csv fils
    <!> delete all comma kin the file before
- the order of fields should be : name, logo, activity, siren, address, postcode, city, website, mail, phone
- delete the name of columns, you should only have data

1 - put the csv file to the server root
2 - `python manage.py import_csv [file name]`
3 - You'll be able to readthe line for wich it didn't find the lat and lng 
