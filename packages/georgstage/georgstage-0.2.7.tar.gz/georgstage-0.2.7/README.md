# Georg Stage vagtplanlægger

> Version 0.2.1

Dette er et hjælpeprogram til vagtplanlægning ombord på Georg Stage (søvagter).
Matematikken bag programmet benytter lineær programming (LP) til at optimere vagterne,
således at alle opgaver varetages, samtidigt med at opgaverne fordeles mellem
gasterne så fair som muligt.

## Installation

Til lokal udvikling:

```bash
pip install -e '.[test]'
```

Kør tests:

```
make test
make lint
```

Start program:

```
make run_local
# or
python src/cli.py
```

## Publicer ny version

> Husk altid at køre tests før du publicerer. TODO: automatiser tests

Kør test:

```
# pip install -e '.[test]'
make lint
make test
```

Hvis en version er tagget med 'v*', f.eks. 'v0.0.1', så vil en Github action
sørge for at der bliver bygget executables til Windows og Mac OS.

```bash
# Husk: skift version til den rigtige
git tag v0.0.1 master
git push origin v0.0.1
```

## Brugervejledning

Kommer snart...

### Kode eksempler

Hvis du kan kode Python, kan du bruge Georg Stages API via kode.

*Auto-udfyldning:*

```python
from georgstage import GeorgStage, Opgave, Vagt
import pandas as pd

# initialiser GeorgStage med kode
vagter = [
    Vagt(dato='2021-05-01', vagt_tid=0, gast=1, opgave=Opgave.VAGTHAVENDE_ELEV),
    Vagt(dato='2021-05-01', vagt_tid=0, gast=2, opgave=Opgave.ORDONNANS),
    Vagt(dato='2021-05-01', vagt_tid=0, gast=3, opgave=Opgave.RORGAENGER),    
    Vagt(dato='2021-05-01', vagt_tid=0, gast=4, opgave=Opgave.UDKIG)
]
gs = GeorgStage(vagter)

# fyld et par uger ud automatisk
for dt in pd.date_range(start='2021-05-01', end='2021-05-14', closed=None).date:
    print(dt)
    fill_result = gs.autofill(dt)
    if fill_result.status == 1:
        gs[dt] = fill_result.vagter

# Check antal dage:
print(f'Antal dage = {len(gs)}')
```

*Load og save:*

```python
# Create gs from other gs
gs2 = GeorgStage(gs.get_vagter())

# Create gs from dataframe
gs3 = GeorgStage.from_dataframe(gs.to_dataframe())

# Save GeorgStage til file
gs.to_dataframe().to_csv('vagter.csv', index=False)

# Load GeorgStage fra file (CSV)
df_vagter = pd.read_csv('vagter.csv')
gs4 = GeorgStage.from_dataframe(df_vagter)
```

*Diverse:*

```python
# Eksporter som dataframe (Pandas)
gs.to_dataframe()

# Eksporter som liste af vagter
gs.get_vagter()

# Eksporter datoer
gs.get_datoer()
```

## Regler vedr. vagter på Georg Stage


Regler for søvagter, som gælder delvist for ankervagter:

- Elever er organiseret i 3 skifter (holod) med 20 gaster (elever) på hver
  - Skifte 1: gaster 1-20
  - Skifte 2: gaster 21-40
  - Skifte 3: Gaster 41-60
- Gaster 61-63 er kokke elever og er altid i køkkenet.
- Vagterne er går igen i 6 perioder per dag, som fordeles på skifte 1-3, så hver
skifte får to perioder per dag
  - Klokken 00 - 04
  - Klokken 04 - 08
  - Klokken 08 - 12
  - Klokken 12 - 16
  - Klokken 16 - 20
  - Klokken 20 - 24
- Det skal være fair, så alle få alle poster cirka lige mange gange
- De faste vagter er
  - Der er 1 kvartermester til hver skifte
  - Der er 1 udkig til hver skifte  
  - Der er 1 rorgænger til hver skifte    
  - Der er 1 ordonnans til hver skifte    
  - Der er 1 vagthavende elev til hver skifte
- De særlige vagter er:
  - Der er 1 dækselev i kabys, kun 8-12 (morgenmad), 12-16 (frokost), 16-20 (aftensmad)  
  - Den vagthavende elev er den samme gast både morgen og aften, går på tur, dag for dag, også når skifterne får nye vagter.
  - Pejlegast A fra dagen før, er pejlegast B dagen efter.
  - pejlegaster findes kun på 16-20 vagten
  - Der er udvalgte gaster der udtages til håndværksmæssig uddannelse hver dag.

Der findes også ankervagter, men det kører en smule anderledes.


## Til udviklere

> Se https://trello.com/b/nId6IuH1/georg-stage  

### Sådan kører du tests

Ved hjælp af make:

```
make test
```

### Sådan publicerer du en ny version

Trin (kan måske forbedre):

1. Opdater version and download_url felter i setup.py
1. Kør git add + commit + push
1. Opret ny release på GitHub (check source-code link, skal matche download_url i setup.py)
1. Kør `python setup.py sdist`
1. Kør `twine upload dist/* --verbose` (hvis ej installet, kør `pip install twine` først)
