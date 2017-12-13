#Datenbank Infos

## Extraktion der relevanten Daten für die Datenbank

Reihenfolge der Scripte:

1. `extract_and_check_main_fields.py` - wenn man nur den kleinen Datensatz will
2. `extract_authors.py` - alle Autoren der Werke 
3. `extract_authors_lifetime.py` - fügt den Autoren die Lebensdaten hinzu 
4. `extract_topics.py` - alle Themen der Werke 
5. `import_authors_and_count.py` - Autoren Aufschlüsselung
6. `import_topics_and_count.py` - alle Themen aufschlüsseln
7. `import_titles.py` - alle werke hinzufügen
8. `create table dnb.dnb_year_count as select year, count(*) as count from dnb.dnb_item group by year` - Tabelle für alle Jahre die in den Werken vorkommen
9. `import_relations_author.py` - alle Relationstabellen mit Autoren
10. `import_relations_topics.py` - alle Relationen mit Themen