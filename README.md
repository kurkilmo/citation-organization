# Lähdeviitteiden hallintasovellus
### TEKA3003 Ohjelmistotuotanto -kurssin miniprojekti

![GHA workflow badge](https://github.com/kurkilmo/citation-organization/workflows/CI/badge.svg)
## [Alustava sovelluksen kuvaus](https://ohjelmistotuotanto-jyu.github.io/speksi/)
- viitteitä täytyy pystyä lisäämään järjestelmään ihmiselle hyvässä muodossa, esimerkiksi jonkun lomakkeen avulla
- järjestelmässä olevista viitteistä pitää saada generoitua LaTeX-dokumenttiin sopiva BibTeX-muotoinen tiedosto
-myös viitteiden listaaminen ihmiselle sopivammassa formaatissa pitää onnistua
- viitelistoja pitäisi pystyä jotenkin rajoittamaan
  - esim. kirjoittajan, vuoden, julkaisun mukaan
  - olisi kyllä hyvä, jos jokaiseen viitteeseen voisi liittää joukon kategorioita tai tägejä, jotka mahdollistaisivat tarkemmat haut
- ihan jees jos kyseessä on yhdellä koneella toimiva sovellus, parempi olisi kuitenkin jos se olisi verkossa ja joka paikassa käytettävissä
- jos toimii vaan paikallisella koneella, pitää eri koneiden välillä pystyä jotenkin synkronoimaan talletetut viitteet
- sellainen olisi loistavaa, että jos antaa linkin esim. ACM:n digitaaliseen kirjastoon, esim. näin, niin softa crawlaa sieltä viitteen tiedot
  - myös muita tiedokantoja kuten Google Scholaria voi tukea
- jopa vielä parempi feature olisi datan haku DOI-tunnisteen perusteella
- kannattaa muistaa että LaTeX mahdollistaa vaikka mitä kenttiä eri viitetyypeille, näistä kentistä aika moni on kuitenkin ainakin kandin tekijöille ihan turhia
