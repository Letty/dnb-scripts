#Datenbank Infos

## Datenanalyse

Ordner: analysis
* fieldsandids.py ist das Skript zur Analyse
* Analyse kann auf dem Gesamtbestand, sowie auf den Daten der GND laufen
* Anpassung des scriptes und des outputs ist im Skript enthalten

Output des Scripts:

```
"feldbezeichner":{
    array_count: wenn es ein Array ist, maximale Länge,
    is_array: gibt an, ob das Feld ein Array ist,
    count: die Häufigkeit des Feldbezeichners in den Werken,
    "weitere_ids": {
        // selbe datenstruktur
    }
}
```

## Extraktion der relevanten Daten für die Datenbank

Ordner: extract
Reihenfolge der Scripte:

1. `extract_and_check_main_fields.py` - wenn man nur den kleinen Datensatz will
2. `extract_authors.py` - alle Autoren der Werke 
3. `extract_authors_lifetime.py` - fügt den Autoren die Lebensdaten hinzu 
4. `extract_topics.py` - alle Themen der Werke 

## Datenbankimporte

Ordner: import
Reihenfolge der Scripte:

5. `import_authors_and_count.py` - Autoren Aufschlüsselung
6. `import_topics_and_count.py` - alle Themen aufschlüsseln
7. `import_titles.py` - alle werke hinzufügen
8. `create table dnb.dnb_year_count as select year, count(*) as count from dnb.dnb_item group by year` - Tabelle für alle Jahre die in den Werken vorkommen
9. `import_relations_author.py` - alle Relationstabellen mit Autoren
10. `import_relations_topics.py` - alle Relationen mit Themen

## Auswertung der Datenstruktur



```
 2.271.910 ['002C'] Inhaltsform
16.564.763 ['003@'] Datensatz ID
 5.214.902 ['004A'] Erste und weitere richtige ISBN
   925.695 ['005A'] ISSN der Vorlage
         1 ['005L'] gelöschte ISSN
 5.709.650 ['010@'] Codes für Sprachen
    73.470 ['011E'] Entstehungsdatum, sonstige Datumsangaben
15.623.024 ['011@'] Erscheinungsjahr
   277.468 ['013D'] Angaben zum Inhalt
13.477.159 ['021A'] Hauptsachtitel, Zusätze, Parallelsachtitel, Verfasserangabe
 1.157.081 ['022A'] Einheitssachtitel oder Formalsachtitel, unter bzw. mit dem die Haupteintragung erfolgt
 8.675.529 ['028A'] 1.Verfasser
 3.502.969 ['028C'] 1. sonstige beteiligte Person
   438.615 ['029A'] 1. Primärkörperschaft
10.563.031 ['033A'] Verlagsort u Verlag
   173.594 ['033D'] ?
 2.864.011 ['039B'] Verknüpfung zur (Haupt-)Zeitschrift
    22.436 ['039C'] "Beilage " (Angabe in der Hauptzeitschrift)
 1.266.977 ['039D'] Horizontale Verknüpfung (Parallele Ausgabe)
   279.388 ['039E'] Chronologische Verknüpfung
    30.850 ['039S'] Titelkonkordanzen
         1 ['039V'] Chronologische Verknüpfung / Vorgänger (Nationales ISSN-Zentrum)
     1.171 ['039X'] Horizontale Verknüpfung (Nationales ISSN-Zentrum)
       914 ['039Z'] Titelkonkordanzen (Nationales ISSN-Zentrum)
   768.701 ['044F'] Schlagwörter aus Altdaten der Deutschen Nationalbibliothek
   475.254 ['044G'] Literarische Gattung
   143.756 ['044H'] Automatisch vergegebenes Schlagwort
   259.970 ['044K'] GND-Schlagwörter
 4.350.351 ['044N'] Deskriptoren aus einem Thesaurus
 1.066.192 ['045C'] 2. + 3.maschinell vergebene Sachgruppen
 4.647.455 ['045E'] Sachgruppen der Deutschen Nationalbibliografie
   110.813 ['045G'] DDC-Notation: Vollständige Notation
 2.176.467 ['047I'] Elektronische Adresse für Dateien mit inhaltlichen Beschreibungen zum Dokument
    41.761 ['047K'] Abstract zur Titelaufnahme
 2.621.471 ['041A']      1.Schlagwortfolge 1.Element
 2.355.042 ['041A/01']   1.Schlagwortfolge 2.Element
 1.556.937 ['041A/02']   1.Schlagwortfolge 3.Element
   870.757 ['041A/03']   1.Schlagwortfolge 4.Element
   436.406 ['041A/04']   1.Schlagwortfolge 5.Element
   192.751 ['041A/05']   1.Schlagwortfolge 6.Element
        29 ['041A/06']   1.Schlagwortfolge 7.Element
        13 ['041A/07']   1.Schlagwortfolge 8.Element
 1.752.704 ['041A/08']  Vorgegebene(s) Permutationsmuster zur 1. Schlagwortfolge
 2.625.849 ['041A/09']  Angaben zur 1. Schlagwortfolge
   495.408 ['041A/10']
   459.875 ['041A/11']
   316.450 ['041A/12']
   173.183 ['041A/13']
    80.427 ['041A/14']
    31.835 ['041A/15']
         5 ['041A/16']
         2 ['041A/17']
   370.781 ['041A/18']  Vorgegebene(s) Permutationsmuster zur 2. Schlagwortfolge
   497.503 ['041A/19']
   111.581 ['041A/20']
   103.462 ['041A/21']
    71.026 ['041A/22']
    36.834 ['041A/23']
    15.995 ['041A/24']
     5.799 ['041A/25']
    81.224 ['041A/28']  Vorgegebene(s) Permutationsmuster zur 3. Schlagwortfolge
   112.309 ['041A/29']
    36.663 ['041A/30']
    34.495 ['041A/31']
    24.562 ['041A/32']
    13.250 ['041A/33']
     5.705 ['041A/34']
     2.082 ['041A/35']
    25.639 ['041A/38'] Vorgegebene(s) Permutationsmuster zur 4. Schlagwortfolge
    36.959 ['041A/39']
    10.551 ['041A/40']
     9.954 ['041A/41']
     7.199 ['041A/42']
     3.736 ['041A/43']
     1.623 ['041A/44']
       577 ['041A/45']
         1 ['041A/46']
    10.719 ['041A/49']
     6.341 ['041A/48']
     2.757 ['041A/50']
     2.688 ['041A/51']
     1.949 ['041A/52']
       963 ['041A/53']
       408 ['041A/54']
       156 ['041A/55']
         2 ['041A/56']
       889 ['041A/58']
     2.839 ['041A/59']
     1.043 ['041A/60']
     1.018 ['041A/61']
       690 ['041A/62']
       296 ['041A/63']
       135 ['041A/64']
        55 ['041A/65']
       113 ['041A/68']
     1.083 ['041A/69']
       575 ['041A/70']
       564 ['041A/71']
       406 ['041A/72']
       178 ['041A/73']
        80 ['041A/74']
        37 ['041A/75']
        74 ['041A/78']
       600 ['041A/79']
       276 ['041A/80']
       272 ['041A/81']
       201 ['041A/82']
        67 ['041A/83']
        28 ['041A/84']
        11 ['041A/85']
         1 ['041A/88']
       292 ['041A/89']
       148 ['041A/90']
       147 ['041A/91']
       112 ['041A/92']
        35 ['041A/93']
        13 ['041A/94']
         6 ['041A/95']
         1 ['041A/98']
       160 ['041A/99']
```

