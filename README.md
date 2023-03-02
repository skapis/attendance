# Docházkový systém
V této složce se nachází docházkový systém, který může sloužit pro malé firmy pro evidenci docházky jejich zaměstnanců. 
Aplikace je vytvořena v frameworku Django a pro frontendovou část je použit Bootstrap 4. Pro používání aplikace je nutné, aby každý zaměstnance i manažer měl vytvořený účet. Z důvodu omezení uživatelů může vytvářet účty pouze uživatel s admin rolí a manažer.

## Docházka
Po přihlášení do účtu je uživatel s rolí zaměstnance přesměrován na přehled docházky pro aktuální měsíc. Pokud se uživatel přihlásil poprvé do aplikace, tak je mu automaticky vygenerována docházka na celý měsíc. Uživatel může poté záznamy editovat podle odpracovaných hodin. Uživatel také může exportovat všechny záznamy do excelového souboru.
Vyexportovaný soubor bude obsahovat 2 listy, první list obsahuje souhrn, kde je docházka sečtena podle kategorií a druhý list obsahuje detail docházky.
![Přehled docházky](https://github.com/skapis/appscreenshots/blob/main/Attendance/Doch%C3%A1zka.png)
### Odeslání/Potvrzení docházky
Pokud má uživatel vyplněnou docházku za celý měsíc a splněné požadované hodiny, tak se zpřístupní možnost "Odeslat". Po odeslání docházky se vypočítá celková měsíční docházka a uživatel již nemůže záznamy editovat. V případě, že docházka obsahuje chyby je možné ji upravit, ale po odeslání může editovat docházku pouze uživatel, který má roli manažera.

## Projekty
Sekce projekty slouží pro zápis odpracovaných hodin na jednotlivých projektech, na kterých uživatel pracoval. Na přehledu projektů může uživatel vytvořit nový záznam, kde vyplní název projektu, datum a čas od kdy do kdy na projektu pracoval. Na základě těchto záznamů se plní tabulka souhrnu, kde jsou sečteny všechny hodiny podle jednotlivých projektů. Stejně jako u docházky může uživatel exportovat souhrn a detailní přehled do excelového souboru.
V případě, že má uživatel zaznamenané všechny odpracované hodiny na projektech za daný měsíc, tak může odeslat projekty, čímž se stejně jako u docházky znemožní následná editace záznamů.
![Přehled projektů](https://github.com/skapis/appscreenshots/blob/main/Attendance/Projekty.png)

## Přehled zaměstnanců
Přehled všech zaměstnanců slouží uživateli s rolí manažera ke kontrole docházky a projektů zaměstnanců. Na přehledu manažer vidí všechny zaměstnance, které jsou v systému registrováni. Dále také může vytvořit účet novému uživateli/zaměstnanci. Uživateli s rolí manažera se zobrazí položka "Zaměstnanci" v horním menu, zaměstnanci (běžní uživatelé) tuto možnost nemají.
![Přehled zaměstnanců](https://github.com/skapis/appscreenshots/blob/main/Attendance/P%C5%99ehled%20zam%C4%9Bstnanc%C5%AF.png)

### Vytvoření nového uživatele
Pro vytvoření nového uživatele je potřeba vyplnit všechny pole obsažená ve formuláři. Formulář kontroluje duplicitní uživatelské jméno, dále jsou nastaveny požadavky na heslo. Manažer také vyplní výši úvazku a další informace. Výše úvazku se vyplní jako číslo, přičemž 1 = plný úvazek, 0,5 = poloviční úvazek. Podle tohoto koeficientu se pak řídí počet hodin, které zaměstnanec musí odpracovat/vyplnit do docházky.
![Nový uživatel](https://github.com/skapis/appscreenshots/blob/main/Attendance/Nov%C3%BD%20u%C5%BEivatel.png)

### Detail zaměstnance
V detailu zaměstnance může manažer deaktivovat přístup zaměstnance do systému kliknutím na tlačítko "Deaktivovat uživatele". Tato možnost je v systému pro případ, že by zaměstnanec ve firmě ukončil pracovní poměr a bylo zapotřebí zamezit mu přístup do systému. Dále si manažer může procházet docházku a projekty zaměstnance a editovat jeho docházku/projekty. V případě, že docházka/projekty nejsou ještě odeslané, tak se zobrazí pouze detailní záznamy. Po potvrzení se zobrazí souhrny a možnost zobrazit detail.
Manažer má také možnost exportovat docházku/projekty do excelového souboru. Soubor má stejný formát jako u bežných uživatelů.
![Detail zaměstnance](https://github.com/skapis/appscreenshots/blob/main/Attendance/Zam%C4%9Bstanec.png)

## Vytvoření kalendáře
Pro správné fungování aplikace je nutné, aby admin systému vytvořil v databázi kalendář, který bude obsahovat jednotlivé dny a budou označeny víkendové dny a svátky. Níže je skript, který vytvoří záznamy pro všechny dny v roce a označí víkendy. Svátky se musí označit ručně v administraci, kam má admin přístup.
```
from core.models import Calendar
from datetime import datetime as dt
import calendar

cur_year = dt.today().year
months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

for month in months:
    num_days = calendar.monthrange(year=cur_year, month=month)[1]
    days = [dt(year=cur_year, month=month, day=day).date() for day in range(1, num_days+1)]
    
    for d in days:
        if d.weekday() in (5, 6):
            Calendar.objects.create(date=d, month=d.month, year=d.year, weekend=True, holiday=False)
        else:
            Calendar.objects.create(date=d, month=d.month, year=d.year, weekend=False, holiday=False)
```
