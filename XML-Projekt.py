import xml.etree.ElementTree as ET
import json
from xmlschema import XMLSchema
import os

# XML-Datei einlesen
tree = ET.parse('02_rechnungsbeleg.xml')
root = tree.getroot()

# XML-Schema validieren und wenn inkorrekt abbrechen
schema = XMLSchema('02_rechnungsbeleg.xsd')
if schema.is_valid(tree):
    print('XML ist gültig.')
else:
    print('XML ist nicht gültig. Das Programm wird beendet.')
    exit()

# Namespaces für default / adressen und positionen definieren
namespace = {
    'default': 'http://buchungsbestaetigungen.ch/rechnungen/',
    'adressen': 'http://buchungsbestaetigungen.ch/adressen/',
    'pos': 'http://buchungsbestaetigungen.ch/positionen/'
}

# Funktion um die Elementen aus dem XML umzuformen
def get_element_with_namespace(element, prefix, tag):
    return element.find(f'.//{{{namespace[prefix]}}}{tag}')

# Daten aus XML in eine Python-Struktur umwandeln
data = {
    'rechnungsnummer': root.get('rechnungsnummer'),
    'rechnungsdatum': root.get('rechnungsdatum'),
    'rechnungsort': root.get('rechnungsort'),
    'lieferant': {
        'firma': get_element_with_namespace(root, 'default', 'firma').text,
        'adresse': get_element_with_namespace(root, 'default', 'adresse').text,
        'ort': get_element_with_namespace(root, 'default', 'ort').text,
        'plz': get_element_with_namespace(root, 'default', 'plz').text,
        'telefon': get_element_with_namespace(root, 'default', 'telefon').text,
        'email': get_element_with_namespace(root, 'default', 'email').text,
        'webseite': get_element_with_namespace(root, 'default', 'webseite').text
    },
    'lieferadresse': {
        'anrede': get_element_with_namespace(root, 'adressen', 'anrede').text,
        'vorname': get_element_with_namespace(root, 'adressen', 'vorname').text,
        'nachname': get_element_with_namespace(root, 'adressen', 'nachname').text,
        'adresse': get_element_with_namespace(root, 'adressen','adresse').text,
        'plz': get_element_with_namespace(root, 'adressen','plz').text,
        'ort': get_element_with_namespace(root, 'adressen', 'ort').text
    },
    'bestellinformationen': {
        'bestelldatum': get_element_with_namespace(root, 'default', 'bestelldatum').text,
        'kunden-nr': get_element_with_namespace(root, 'default', 'kunden-nr').text,
        'bestell-nr': get_element_with_namespace(root, 'default', 'bestell-nr').text
    },
    'artikel-positionen': [],
    'kosten': {
        'zwischentotal': get_element_with_namespace(root, 'default', 'zwischentotal').text,
        'cumulus-bon': get_element_with_namespace(root, 'default', 'cumulus-bon').text,
        'total': get_element_with_namespace(root, 'default', 'total').text
    },
    'zahlungsinformationen': {
        'cumulus-nr': get_element_with_namespace(root, 'default', 'cumulus-nr').text,
        'club-nr': get_element_with_namespace(root, 'default', 'club-nr').text,
        'mwst': get_element_with_namespace(root, 'default', 'mwst').text,
        'zahlungskondition': get_element_with_namespace(root, 'default', 'zahlungskondition').text
    }
}
#Beim Auslesen der Liste hat es diverse Einträge nicht erkannt. Da dieser Punkt zu spät erkannt wurde,
# ist diese Funktion noch nicht vollunfänglich eingesetzt und hiermit ausgeklammert.
"""
artikel_positionen = root.find()

    for position in artikel_positionen.iter():
        position_data = {
            'anz-lief': position.find('{http://buchungsbestaetigungen.ch/positionen/}anz-lief').text,
            'anz-best': position.find('{http://buchungsbestaetigungen.ch/positionen/}anz-best').text,
            'artikelnummer': position.find('{http://buchungsbestaetigungen.ch/positionen/}artikelnummer').text,
            'bezeichnung': position.find('{http://buchungsbestaetigungen.ch/positionen/}bezeichnung').text,
            'mwst-code': position.find('{http://buchungsbestaetigungen.ch/positionen/}mwst-code').text,
            'preis': position.find('{http://buchungsbestaetigungen.ch/positionen/}preis').text,
            'total-srf': position.find('{http://buchungsbestaetigungen.ch/positionen/}total-srf').text
        }
        data['artikel-positionen'].append(position_data)
"""
# Pfad für das speichern der JSON-Datei interaktiv abfragen
json_file_path = input("Geben Sie den Pfad zum Speichern der Json Datei inkl. den Dateinamen an: ")

# Wenn kein Pfad angegeben wird, Standardpfadprogrammpfad verwenden
if not json_file_path:
    json_file_path = 'rechnungsbeleg.json'

# Auf Dateiendung prüfen und allenfalls ergänzen
if not json_file_path.lower().endswith('.json'):
    json_file_path += '.json'

# Überprüfen, ob die Datei unter diesem Pfad bereits existiert
if os.path.exists(json_file_path):
    #Falls die Datei bereits existiert unter diesem Pfad, fragen sie überschrieben werden soll
    overwrite = input("Die Datei existiert bereits. Möchten Sie sie überschreiben? (Ja/Nein): ")

    #Falls nicht ja eingegeben wird, soll die Datei nicht überschrieben werden
    if overwrite != 'ja':
        print("Die Datei wurde nicht überschrieben. Das Programm wird beendet.")
        exit()
    else:
        #Sonst, Datei übeschreiben -> In JSON-File speichern
        print("Die vorhandene Datei wird überschrieben.")
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

print(f'Die XML-Daten wurden erfolgreich in ein JSON-File exportiert.')
