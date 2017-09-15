Datenbank Infos

1. Import aller "kompletten” Datensätze für

    - Keywords (import_keyword.py)
    - Personen (import_person.py)
    - Titel (import_manifesto.py)

2. Extraktion des reduzierten Datensatzes für Titel

    extract_and_check_main_fields.py    

3. Extraktion der Hilfstabellen
    
    - Alle Autoren der reduzierten Titeldaten (extract_authors.py)
    - Alle Themen - '' - (extract_topics.py)
    - Alle Jahre - '' - (extract_years.py)

4. Import der Hilfstabellen in die Datenbank

    - Autoren und Häufigkeit (import_reduced_authors_and_count.py)
    - Themen und Häufigkeit (import_reduced_topics_and_count.py)
    - Jahre und Häufigkeit TODO!

5. Import der reduzierten Titeldaten mit den zugehörigen Beziehungstabellen

    - Titel (import_reduced_title.py)
    - Beziehung Titel <-> Jahre
    - Beziehung Titel <-> Themen
    - Beziehung Titel <-> Personen




------

Python Skript für folgende Tabellen + Inhalt

    -> TODO: Namenskonvention für diese Tabellen, damit sie eindeutig unterscheidbar zu den Datenimporten sind

* Tabelle year_publication erstellen:
    - create table dnb.dnb_reduced_year_count as select year, count(*) as count from dnb.dnb_reduced_title group by year 
    - Falls ich die Updatefunktion einbaue, brauche ich einen update trigger
    - Eigentlich müsste man die Jahre cleanen
* Top <Zahl> Titel
* Top <Zahl> Personen
* Top <Zahl> Schlagworte

#select * from dnb.dnb_person where surname != '' limit 500
#select count(*) from dnb.dnb_person
#select * from dnb.dnb_person where surname
#SELECT * FROM testdb.articles
 #       WHERE MATCH (title,body)
 #       AGAINST ('mysql' IN NATURAL LANGUAGE MODE);
 #select * from testdb.articles where title like '%data%' or body like '%after%'
# select * from dnb.dnb_person  limit 50
#select * from dnb.dnb_keyword where geographic like '%Staat%' limit 500 
#select * from dnb.dnb_title where author_lastname like '%goethe%'
#select * from dnb.dnb_title where content != '' order by year DESC
#select * from dnb.dnb_title where thesaurus like '%online resource%' limit 50
# select * from dnb.count_pub order by year
#create table dnb.year_pub as select year, count(*) as count from dnb.dnb_title group by year 
#select * from dnb.year_pub
#SELECT * FROM dnb.year_pub WHERE id >= (SELECT FLOOR( MAX(id) * RAND()) FROM dnb.year_pub ) ORDER BY id LIMIT 1;
#SELECT * FROM dnb.year_pub ORDER BY RAND() LIMIT 0,1;
#SELECT * FROM dnb.dnb_title ORDER BY RAND() LIMIT 0,1;
select * from dnb.dnb_keyword
