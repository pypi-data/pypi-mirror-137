== Buchungsstapel ==

Ein Buchungsstapel ist eine Sammlung von Stapelzeilen. Die Zeilen eines Stapels sind meistens thematisch zusammenhängend, wie z.B. Einzelbuchungen auf einem Bankauszug oder die Belegeingabe zu einem bestimmten Zeitpunkt. Vor der Eingabe der Stapelzeilen wird auf Ebene des Buchungsstapels ein Journal festgelegt. Diese Festlegung lässt sich nach Eingabe der Stapelzeilen nicht mehr verändern.



== Stapelzeile ==

Eine Stapelzeile ist immer einem Buchungsjournal zugeordnet. Die Stapelzeile wird durch die Einstellung des verwendeten Journals im Buchungsstapel determiniert und grundsätzlich für eine Eingabe im jeweiligen Journal konfiguriert. Auf der Stapelzeile dienen verschiedene Konzepte zur schnellen und effizienten Eingabe von Belegdaten.



=== Vorne Gegenkonto, Hinten Konto ===

Um einen Einzelbeleg in einem Buchungsstapel zu verbuchen, muss generell nur eine einzige Stapelzeile angefertigt werden. Die bisherige eher umständliche Eingabe einer Stapelzeile als T-Konto mit fester Soll und Haben Seite ist ersetzt worden. Die in der gängigen Buchhaltungspraxis übliche Konzeption von ''Gegenkonto'' und ''Konto'' ermöglicht es allein durch das Ändern des Vorzeichens eines eingegebenen Betrages, die Seiten von Soll- und Haben für die Buchung zu vertauschen.



Grundsätzlich gilt:



 * Die Eingabe in der Stapelzeile erfolgt von links nach rechts:

   * ''Vorne'' (= weiter links) steht das Gegenkonto, 

   * ''Hinten'' (= weiter rechts) steht das Konto.



Grundsätzlich wird immer das hintenstehende ''Konto'' (durch das Journal) vorbelegt und das vorne stehende Gegenkonto durch den Benutzer ausgefüllt.



=== Journale ===

Viele der Automatismen bei der Stapelzeile hängen von den Einstellungen des verwendeten Journals ab.



==== Standardfall und umgekehrter Fall ====

Zur Eingabe-Erleichterung unterscheiden wir zwei Fälle, die durch die Auswahl von bestimmten Journaltypen gesteuert werden können.



Der Standard Fall gilt grundsätzlich für alle Journale:

 * Standard Fall:

   * Wenn Betrag positiv, dann

     * stehen ''vorne'' Soll und ''hinten'' Haben



Der umgekehrte Fall gilt nur für die Journale ''Zahlung'' (Typ: cash) und ''Ertrag'' (Typ revenue). Beim Bankauszug werden positive Beträge als Einnahmen auf der Habenseite und negative Beträge als Ausgaben auf der Soll-Seite geführt. Das hat folgende Auswirkung auf die betriebliche Buchhaltung: Positive Haben-Beträge von einem Kontoauszug müssen in der eigenen Buchhaltung auf die Soll-Seite gebucht werden und umgekehrt. Um die Eingabe zu vereinfachen, wird bei Verwendung von Ertrags- und Zahlungsjournalen der o.g. Standard-Fall umgekehrt. Denn gerade bei der Eingabe von Zahlungen ist es einfacher Einnahmen als positive und Ausgaben als negative Beträge einzugeben.



 * Umgekehrter Fall für Zahlungs und Ertrags Journale:

   * Wenn Betrag positiv, dann

     * stehen ''vorne'' Haben und ''hinten'' Soll.



==== Standardkonten ====

Die Standard Soll- und Habenkonten, die bei den Journalen hinterlegt sind, werden danach ausgewählt, ob das Konto ''hinten'' nach o.g. Fällen im Soll oder Haben bebucht werden.





=== Parteien ===

Die Eingabe einer Partei modifiziert das Gegenkonto und fügt dort das jeweilige Forderungen oder Verbindlichkeiten Konto der Partei nach folgenden Regeln ein:



Generell:

 * Wenn Betrag Positiv, dann

   * wird das Verbindlichkeiten Konto der Partei eingetragen

 * sonst,

   * wird das Forderungskonto der Partei eingetragen



 * Bei den Journaltypen Ertrag und Zahlungen werden die Parteien Konten für Forderungen und Verbindlichkeiten getauscht.



=== Storno ===



Die Aktivierung der Storno Checkbox kehrt das Vorzeichen der in der Stapelzeile angegebenen Buchung um.

Festgeschriebene Stapelzeilen lassen sich durch den Assistenten ''Stapelzeilen stornieren'' stornieren. Eine olchermaßen generierte Stornostapelzeile neutralisiert aus Buchhaltungssicht die Originalzeile.


=== Steuer ===

Bei Angabe einer Steuer wird der eingegebene Betrag als Brutto Betrag gewertet. Die jeweilige anzuwendende Steuer errechnet automatisch den Nettobetrag und den Steuerbetrag. 


   * Bei Verwendung einer Steuer in der Stapelzeile wird das Feld ''Rechnung'' in derselben Zeile unveränderlich.


   * Bei Verwendung einer Rechnung in der Stapelzeile werden die Felder ''Storno'' und ''Steuer'' in derselben Zeile unveränderlich.



== Eingabe von Stapelzeilen ==

Hier geht es um die Automatismen bzw. deren Einsatz bei der Eingabe. Es werden von links nach rechts Betrag, Partei, Rechnung, Steuer oder Storno eingegeben. Alle anderen Werte insbesondere Gegenkonto sind nur ausgefüllt, wenn sie automatisch vorbelegt werden können.



Journalkonfiguration:



|| Journal               || Aufwand   ||

|| Standard Haben-Konto  || Aufwand-H ||

|| Standard Soll-Konto   || Aufwand-S ||

|| Journal               || Zahlung   ||

|| Standard Haben-Konto  || Bank-H    ||

|| Standard Soll-Konto   || Bank-S    ||

|| Journal               || Ertrag    ||

|| Standard Haben-Konto  || Ertrag-H  ||

|| Standard Soll-Konto   || Ertrag-S  ||



Vehalten der Stapelzeile bei manueller Eingabe einzelner Werte:



|| Journal  || Betrag       || Partei || Rechnung ||   || Gegenkonto        || Steuer || Konto     ||   || Storno  || Bemerkungen / Fragen                               ||

|| Zahlung  || Null/Positiv ||        ||          || H ||                   ||        || Bank-S    || S ||   [[ ]]   ||                                                    ||

|| Zahlung  || Null/Positiv || Kunde  ||          || H || Forderungen       ||        || Bank-S    || S ||   [[ ]]   ||                                                    ||

|| Zahlung  || Null/Positiv || Kunde  || 1        || H || Forderungen       || XXXXXX || Bank-S    || S || XXXXXXX || Sollen bei pos. Amount nur Ausgangsrechnungen und Lieferantengutschriften auftauchen? ||

|| Zahlung  || Null/Positiv ||        || XXXXXXXX || H ||                   ||        || Bank-S    || S ||   [[X]]   ||                                                    ||

|| Zahlung  || Negativ      ||        ||          || S ||                   ||        || Bank-H    || H ||   [[ ]]   ||                                                    ||

|| Zahlung  || Negativ      || Kunde  ||          || S || Verbindlichkeiten ||        || Bank-H    || H ||   [[ ]]   ||                                                    ||

|| Zahlung  || Negativ      || Kunde  || 2        || S || Verbindlichkeiten || XXXXXX || Bank-H    || H || XXXXXXX || Sollen bei neg. Amount nur Eingangssrechnungen und Kundengutschriften auftauchen? ||

|| Zahlung  || Negativ      ||        || XXXXXXXX || S ||                   ||        || Bank-H    || H ||   [[X]]   ||                                                    ||




