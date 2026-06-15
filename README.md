## Contexte : La technicisation de la course à pied
La course à pied a connu un essor majeur ces dernières années, s'accompagnant d'une forte technicisation de la pratique. Les montres GPS sont désormais des outils de suivi de performance incontournables. Parallèlement, la préparation aux courses s'est complexifiée, devenant le domaine de spécialistes de la santé sportive (comme La Clinique du Coureur ou Runwise) et de data analystes.



S'il existe aujourd'hui d'excellents programmes d'entraînement sur-mesure, ces solutions expertes restent coûteuses et peu accessibles. À l'inverse, le marché propose des applications gratuites offrant des plans d'entraînement standards, souvent cohérents mais rigides.

La Problématique : Le manque de modularité
Le véritable angle mort de ces solutions réside dans la modularité. Les coureurs amateurs très impliqués doivent jongler avec des emplois du temps fluctuants, rendant difficile la projection sur un plan d'entraînement strict de trois à six mois. Face à ces imprévus, il devient complexe pour l'athlète de conserver une vision claire de son état de forme réel et d'identifier l'entraînement optimal pour le maintenir ou le développer.


L'enjeux de ce projet de modéliser un  indicateurs de "rendement d'entrainement" ou un groupe réduit d'indicateurs sur lesquels fonder des indicateurs explicites  et des proposition d'entrainement spécifiés. 

Pour répondre à cette problématique, ce projet propose le développement d'une solution analytique hybride (Python et Excel) permettant de visualiser le profil de performance de l'athlète, ainsi que la qualité et le rendement de ses entraînements.

Ce système repose sur un moteur de calcul reproduisant des modèles issus de la littérature académique et de méthodologies d'entraîneurs reconnus. À terme, une fois la fiabilité de ces indicateurs validée, l'objectif théorique final serait d'y intégrer une dimension prédictive : suggérer dynamiquement des séances spécifiques capables de maintenir la forme globale de l'athlète en s'adaptant à ses contraintes temporelles immédiates.

## L'Objectif : L'automatisation avant tout

Il est important de souligner que la finalité première de ce travail est technique et pédagogique. L'enjeu central est de se familiariser avec l'architecture, la manipulation de données complexes et l'automatisation d'un pipeline complet entre Python et Excel. La justesse scientifique absolue ou la validation clinique du modèle physioloqique ne constituent pas l'objectif principal de cette démonstration technique. Cette version est largement optimisable: 

## Les axes d'amélioration : 

La construction d'un modèle calculatoire fiable repose sur la qualité et la complétude des données d'entrée. Des paramètres tels que la puissance moyenne ou la typologie du sol sont déterminants ; or, ces informations présentent actuellement un caractère parcellaire au sein de notre jeu de données.

L'objectif est d'intégrer les paramètres environnementaux du sportif afin de stabiliser la charge d'entraînement moyenne tout en compensant les variations ponctuelles. En l'état, cette solution ne prend pas en compte la périodisation des phases d'entraînement et manque d'éléments prédictifs pour dépasser le stade de l'analyse descriptive.


Un exemple aboutit de cette catégorie de modèle : https://joseph-mestrallet.com/



/performances_sportives
├── data/                       
│   ├── activite_brut.csv       
│   └── activite_clean.csv      
├── reporting/                  
│   └── Dashboard_Pro.xlsx      
├── src/                        
│   ├── __init__.py
│   ├── data_pipeline.py        
│   ├── reporting    # Les briques "Lego" réutilisables
│             
└── main.py                     



Bibliographie : 


Chiron, F. (2025). Optimisation de la performance et de la récupération des athlètes de haut-niveau engagés dans la réitération d'exercices à haute-intensité : exemple du 400 m (Thèse de doctorat, Université Paris-Saclay). HAL Theses. https://theses.hal.science/tel-04988896v1/file/2025UPASW002.pdf

Ehrström, S. (2020). Analyse de la performance en trail courte distance : déterminants physiologiques, spécificité de la sollicitation musculaire et stratégies d'optimisation (Thèse de doctorat, Université Côte d'Azur). HAL Theses. https://theses.hal.science/tel-03187923v1/file/2020COAZ4104.pdf




Banister, E. W., Calvert, T. W., Savage, M. V., & Bach, T. (1975). A systems model of training for athletic performance. Australian Journal of Sports Medicine, 7(3), 57-61.


Chiron, F. (2025). Optimisation de la performance et de la récupération des athlètes de haut-niveau engagés dans la réitération d'exercices à haute-intensité : exemple du 400 m (Thèse de doctorat, Université Paris-Saclay).
