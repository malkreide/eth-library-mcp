# Use Cases & Examples — eth-library-mcp

Real-world queries by audience. Indicate per example whether an API key is required.

### 🏫 Bildung & Schule
Lehrpersonen, Schulbehörden, Fachreferent:innen

**Historische Lehrmittel für den Unterricht**
«Ich suche historische Lehrmittel und Schulbücher für den Mathematikunterricht, die in der Schweiz erschienen sind.»
→ `eth_search_education(topic="Mathematik Lehrmittel historisch", resource_type="books", open_access_only=true)`
Warum nützlich: Erlaubt Lehrpersonen, gezielt auf historische Bestände und digitalisierte Lehrmittel der ETH-Bibliothek für den Unterricht oder für Ausstellungsprojekte zuzugreifen.
*(Auth nötig: Ja)*

**Schweizer Schulgeschichte im Archiv**
«Gibt es im Hochschularchiv Dokumente oder Berichte zur Entwicklung der Volksschule im 19. Jahrhundert?»
→ `eth_search_archive(archive="ETH_Hochschularchiv", query="any,contains,Volksschule 19. Jahrhundert", limit=15)`
Warum nützlich: Hilft Schulbehörden und Historiker:innen, Primärquellen und Archivmaterial zur institutionellen Entwicklung des Bildungswesens schnell ausfindig zu machen.
*(Auth nötig: Ja)*

### 👨‍👩‍👧 Eltern & Schulgemeinde
Elternräte, interessierte Erziehungsberechtigte

**Fachliteratur zur Pädagogik**
«Welche frei zugänglichen Ratgeber oder Bücher gibt es zum Thema Reformpädagogik und Schulmodelle?»
→ `eth_search_education(topic="Reformpädagogik", resource_type="books", open_access_only=true)`
Warum nützlich: Bietet interessierten Eltern direkten Zugang zu fundierter Fachliteratur über verschiedene pädagogische Ansätze, ohne vor Ort in der Bibliothek sein zu müssen.
*(Auth nötig: Ja)*

**Naturwissenschaftliche Kinderbücher**
«Ich suche nach illustrierten Büchern oder Zeitschriften, die sich mit Naturwissenschaften für Kinder beschäftigen.»
→ `eth_search_resources(query="any,contains,Naturwissenschaften Kinder", resource_type="books", open_access_only=false)`
Warum nützlich: Unterstützt Eltern dabei, verlässliche und altersgerechte MINT-Literatur für ihre Kinder in der grössten naturwissenschaftlichen Bibliothek der Schweiz zu finden.
*(Auth nötig: Ja)*

### 🗳️ Bevölkerung & öffentliches Interesse
Allgemeine Öffentlichkeit, politisch und gesellschaftlich Interessierte

**Historische Karten der Heimatregion**
«Ich möchte alte Landkarten oder Pläne der Region Zürich aus dem 18. Jahrhundert sehen.»
→ `eth_search_by_type(resource_type="maps", query="any,contains,Zürich 18. Jahrhundert", open_access_only=true)`
Warum nützlich: Ermöglicht an Lokalgeschichte interessierten Bürger:innen den direkten Zugriff auf digitalisierte historische Kartenbestände.
*(Auth nötig: Ja)*

**Nachlass berühmter Persönlichkeiten**
«Welche Dokumente oder Briefe befinden sich im Thomas-Mann-Archiv zum Thema Exil?»
→ `eth_search_archive(archive="ETH_ThomasMannArchiv", query="any,contains,Exil", limit=20)`
Warum nützlich: Schafft Transparenz über das kulturelle Erbe und ermöglicht der Öffentlichkeit einen niederschwelligen Zugang zu wertvollen Nachlässen, die an der ETH verwahrt werden.
*(Auth nötig: Ja)*

### 🤖 KI-Interessierte & Entwickler:innen
MCP-Enthusiast:innen, Forscher:innen, Prompt Engineers, öffentliche Verwaltung

**Umfassende Metadaten-Extraktion**
«Zeige mir die vollständigen bibliografischen Metadaten und Verfügbarkeiten für die Publikation mit der MMS-ID 990075811280205503.»
→ `eth_get_resource(mmsid="990075811280205503", include_availability=true, lang="de")`
Warum nützlich: Erlaubt Entwickler:innen die tiefe Integration von Metadaten und Ausleihstatus in eigene Katalogsysteme, Chatbots oder Forschungsanwendungen.
*(Auth nötig: Ja)*

**Kombination von Parlamentsdaten und historischen Archivquellen (Multi-Server)**
«Suche nach aktuellen Debatten zur Bildungsforschung im Parlament und vergleiche die Themen mit historischen Archivmaterialien im Hochschularchiv der ETH.»
→ `parlament_search_affairs(query="Bildungsforschung")` (via [parlament-mcp](https://github.com/malkreide/parlament-mcp))
→ `eth_search_archive(archive="ETH_Hochschularchiv", query="any,contains,Bildungsforschung")`
Warum nützlich: Demonstriert die Leistungsfähigkeit von Multi-Server-Abfragen, indem aktuelle politische Diskussionen mit dem historischen Gedächtnis der ETH-Bibliothek verknüpft und verglichen werden können.
*(Auth nötig: Ja)*

### 🔧 Technische Referenz: Tool-Auswahl nach Anwendungsfall

| Ich möchte… | Tool(s) | Auth nötig? |
| :--- | :--- | :--- |
| **Allgemeine Bücher, Bilder oder Medien im Katalog suchen** | `eth_search_resources` | Ja |
| **Ein spezifisches Archiv (z. B. Max-Frisch-Archiv) durchsuchen** | `eth_search_archive` | Ja |
| **Nur einen bestimmten Medientyp (z. B. Karten oder Noten) finden** | `eth_search_by_type` | Ja |
| **Gezielt nach pädagogischer Literatur und Lehrmitteln suchen** | `eth_search_education` | Ja |
| **Die kompletten Metadaten und den Ausleihstatus eines Werks abrufen** | `eth_get_resource` | Ja |
| **Nach Personen (Autoren, historische Figuren) im Katalog suchen** | `eth_search_persons` | Ja |
| **Einen Überblick über alle verfügbaren Archive und Medientypen erhalten** | `eth_library_info` | Nein |
