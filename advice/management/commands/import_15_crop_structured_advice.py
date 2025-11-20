"""
Management command to import structured advice for 15 common Senegalese crops
Each crop gets comprehensive advice covering:
- Planting season
- Maturity time
- Challenges (insects, diseases, environmental)
- Tips (prevention and management)
- Recommended materials (fertilizers, pesticides, tools, innovative inputs)
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from advice.models import CropAdvice
from crops.models import Crop

User = get_user_model()


class Command(BaseCommand):
    help = 'Import structured agricultural advice for 15 common Senegalese crops'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting import of structured advice for 15 crops...'))

        # Get or create system user
        author, _ = User.objects.get_or_create(
            username='system_advisor',
            defaults={
                'email': 'advisor@farmconnect.sn',
                'first_name': 'System',
                'last_name': 'Advisor'
            }
        )

        # Define crop advice data for 15 crops
        crop_advice_data = [
            # 1. MILLET (Mil)
            {
                'crop_name': 'Mil (Souna)',
                'planting_season_fr': """**Saison de plantation optimale:**

Le mil se plante au début de la saison des pluies:
- **Période principale**: Juin à Juillet
- **Zone nord** (Louga, Matam): Mi-juin à fin juillet
- **Zone centre** (Kaolack, Fatick): Début juin à mi-juillet
- **Zone sud** (Casamance): Mi-mai à fin juin

**Conditions idéales pour planter:**
- Premières pluies utiles (au moins 20-30mm)
- Sol bien humidifié sur 10-15cm de profondeur
- Température du sol supérieure à 15°C""",

                'maturity_time_fr': """**Durée du cycle cultural:**

- **Variétés précoces** (Souna 3, IBV 8004): 75-90 jours
- **Variétés intermédiaires** (Sanio, Thialack): 90-110 jours
- **Variétés tardives** (Locale): 120-150 jours

**Stades de croissance:**
- Levée: 5-7 jours après semis
- Tallage: 15-25 jours
- Montaison: 30-45 jours
- Épiaison: 45-60 jours
- Floraison: 55-70 jours
- Maturation: 75-150 jours (selon variété)

**Indicateurs de maturité:**
- Grains durs et secs
- Épis penchés vers le sol
- Feuilles jaunies et sèches""",

                'challenges_insects_fr': """**Principaux insectes ravageurs:**

1. **Foreurs des tiges** (Coniesta ignefusalis, Sesamia calamistis)
   - Symptômes: Trous dans les tiges, flétrissement, cœurs morts
   - Période critique: 20-45 jours après levée

2. **Chenilles mineuses** (Amsacta spp.)
   - Symptômes: Défoliation, feuilles trouées
   - Plus actives en début de cycle

3. **Pucerons** (Melanaphis sacchari)
   - Symptômes: Miellat, fumagine, jaunissement
   - Période: Montaison à floraison

4. **Cantharides** (Mylabris spp.)
   - Symptômes: Défoliation rapide
   - Attaque en groupe

5. **Oiseaux granivores** (Quelea quelea)
   - Dégâts: Consommation des grains
   - Période critique: Maturation""",

                'challenges_diseases_fr': """**Maladies courantes:**

1. **Mildiou** (Sclerospora graminicola)
   - Symptômes: Feuilles étroites, déformées, croissance naine
   - Conditions favorables: Humidité élevée, températures 20-25°C

2. **Charbon** (Tolyposporium penicillariae)
   - Symptômes: Transformation des grains en masses noires
   - Perte de rendement importante

3. **Ergot** (Claviceps fusiformis)
   - Symptômes: Sclérotes noirs sur les épis
   - Toxique pour le bétail

4. **Rouille** (Puccinia substriata)
   - Symptômes: Pustules orangées sur feuilles
   - Affaibl it la plante

5. **Helminthosporiose** (Exserohilum turcicum)
   - Symptômes: Taches brunes allongées sur feuilles""",

                'challenges_environmental_fr': """**Stress environnementaux:**

1. **Sécheresse:**
   - Périodes critiques: Floraison et remplissage des grains
   - Symptômes: Enroulement des feuilles, épis vides
   - Réduction du rendement jusqu'à 70%

2. **Températures extrêmes:**
   - Températures > 40°C: Stérilité florale
   - Températures < 15°C: Ralentissement de croissance

3. **Excès d'eau:**
   - Engorgement: Asphyxie racinaire, jaunissement
   - Favorise les maladies cryptogamiques

4. **Vents violents:**
   - Verse des plants
   - Bris des tiges

5. **Sols pauvres:**
   - Déficience en azote, phosphore
   - Plants chétifs, rendement faible""",

                'prevention_tips_fr': """**Mesures préventives:**

1. **Choix variétal:**
   - Utiliser des semences certifiées
   - Préférer variétés adaptées à votre zone
   - Variétés résistantes au mildiou (ex: Souna 3, IBV 8004)

2. **Rotation culturale:**
   - Rotation mil/légumineuses (niébé, arachide)
   - Ne pas cultiver mil > 2 années consécutives

3. **Préparation du sol:**
   - Labour profond (20-30cm) avant les pluies
   - Enfouissement des résidus de récolte
   - Nivelage pour éviter stagnation d'eau

4. **Traitement des semences:**
   - Traiter avec fongicide (Apron Star, Calthio)
   - Dose: 3-4g/kg de semences

5. **Gestion de l'eau:**
   - Billons ou lignes de niveau en zone de pente
   - Paillage pour conserver l'humidité

6. **Lutte intégrée:**
   - Installer des perchoirs pour oiseaux prédateurs
   - Préserver les ennemis naturels
   - Sarclo-binages réguliers""",

                'management_tips_fr': """**Gestion des problèmes:**

1. **Contre les foreurs:**
   - Application de pesticide biologique (Bt)
   - Dose: 1L/ha à 20-30 jours après levée
   - Répéter si nécessaire

2. **Contre le mildiou:**
   - Arracher et brûler plants malades
   - Application fongicide (Ridomil)
   - Ne pas replanter mil l'année suivante

3. **Contre les pucerons:**
   - Traitement avec insecticide (Cypercal, Decis)
   - Favoriser coccinelles et chrysopes

4. **Contre les oiseaux:**
   - Surveillance constante à partir de la maturation
   - Effaroucheurs: épouvantails, filets, bruits
   - Récolte précoce si nécessaire

5. **Fertilisation d'appoint:**
   - Urée en cas de jaunissement: 50kg/ha
   - Application à la montaison

6. **Gestion du stress hydrique:**
   - Binage pour aération du sol
   - Paillage pour réduire évaporation
   - Irrigation d'appoint si possible (10-15mm/semaine)""",

                'recommended_fertilizers_fr': """**Programme de fertilisation:**

1. **Fumure de fond** (au semis):
   - NPK 15-15-15: 100-150 kg/ha
   - ou NPK 6-20-10: 150-200 kg/ha
   - Compost: 5-10 tonnes/ha (très recommandé)

2. **Fumure d'entretien** (30-35 jours après levée):
   - Urée 46%: 50 kg/ha
   - ou Sulfate d'ammonium: 100 kg/ha

3. **Microdosage** (pour petits producteurs):
   - 6g NPK au poquet au semis
   - 2g Urée par poquet à 30 jours

4. **Amendements organiques:**
   - Fumier décomposé: 5-10 t/ha
   - Compost: 5-10 t/ha
   - Appliquer 2-3 semaines avant semis

**Modalités d'application:**
- Enfouir engrais à 5cm du plant
- Ne pas mettre en contact direct avec graines
- Appliquer après pluie ou arrosage""",

                'recommended_pesticides_fr': """**Produits phytosanitaires:**

1. **Insecticides:**
   - **Cypercal 50 EC**: 0.5L/ha (foreurs, pucerons)
   - **Décis 12.5 EC**: 0.3L/ha (chenilles)
   - **Lambda Super 2.5 EC**: 0.3L/ha (large spectre)
   - **Bt (Bacillus thuringiensis)**: 1L/ha (bio, chenilles)

2. **Fongicides:**
   - **Apron Star 42 WS**: 4g/kg semences (traitement)
   - **Ridomil Gold Plus**: 2kg/ha (mildiou)
   - **Banko Plus**: 2kg/ha (maladies foliaires)

3. **Traitement des semences:**
   - **Calthio C**: 3g/kg (insectes du sol)
   - **Apron Star**: 4g/kg (mildiou, charbon)

**Précautions d'emploi:**
- Porter équipement de protection
- Respecter doses prescrites
- Délai avant récolte: 21 jours minimum
- Ne pas traiter pendant floraison (abeilles)""",

                'recommended_tools_fr': """**Outils et équipements:**

1. **Préparation du sol:**
   - Charrue bovine ou tracteur
   - Houe manga pour labour manuel
   - Herse pour émiettage
   - Niveleuse artisanale

2. **Semis:**
   - Semoir manuel à traction (2-4 rangs)
   - Semoir Aitchison (précision)
   - Cordeau pour alignement
   - Piquets de marquage

3. **Entretien:**
   - Sarcleuse manuelle (hilaire)
   - Houe pour binage
   - Serfouette
   - Pulvérisateur à dos 15-20L

4. **Récolte:**
   - Faucille ou couteau
   - Bâches de séchage
   - Batteuse mécanique (si disponible)
   - Vannoir manuel

5. **Stockage:**
   - Greniers traditionnels améliorés
   - Sacs en jute traités
   - Fûts métalliques hermétiques (50-100kg)""",

                'innovative_inputs_fr': """**Innovations et techniques modernes:**

1. **Semences améliorées:**
   - Variétés hybrides (rendement +30-50%)
   - Souna 3, IBV 8004 (tolérantes sécheresse)
   - Gampela 1 (précoce, 75 jours)

2. **Microdosage d'engrais:**
   - Économise 50-70% d'engrais
   - Augmente rendement de 40-120%
   - Technique: 6g NPK + 2g Urée/poquet

3. **Biochar (charbon végétal):**
   - Améliore rétention d'eau et nutriments
   - Dose: 2-5 t/ha
   - Durée d'effet: plusieurs années

4. **Biofertilisants:**
   - Mycorhizes (améliore absorption phosphore)
   - Rhizobium (fixation azote)
   - Application au semis

5. **Zaï mécanisé:**
   - Poquets améliorés avec compost
   - Rétention d'eau optimale
   - Rendement +50-100% en zone sèche

6. **Biopesticides:**
   - Neem (azadirachtine): Répulsif insectes
   - Bt (Bacillus): Contre chenilles
   - Pièges à phéromones

7. **Irrigation goutte-à-goutte:**
   - Économie d'eau 50-70%
   - Augmente rendement
   - Système solaire pour pompage

8. **Application mobile:**
   - Suivi cultural
   - Alertes météo
   - Conseils personnalisés""",

                'additional_notes_fr': """**Recommandations complémentaires:**

**Densité de semis:**
- Culture pure: 15,000-20,000 plants/ha
- Association (mil+niébé): 10,000-15,000 plants/ha
- Espacement: 80cm x 40cm ou 75cm x 50cm

**Rendements attendus:**
- Traditionnel: 400-800 kg/ha
- Avec bonnes pratiques: 1,200-1,800 kg/ha
- Potentiel variétés améliorées: 2,000-3,000 kg/ha

**Conservation:**
- Sécher grains à 12-14% humidité
- Stocker en lieu sec, aéré
- Traiter avec insecticide de stockage (Actellic)
- Vérifier régulièrement (charançons)

**Association culturale:**
- Mil + Niébé: complémentarité azote
- Mil + Arachide: rotation bénéfique
- Mil + Sorgho: partage des risques

**Crédit et soutien:**
- S'informer sur subventions semences/engrais
- Crédit agricole de campagne
- Assurance agricole indicielle"""
            },

            # 2. MAIZE (Maïs)
            {
                'crop_name': 'Maïs',
                'planting_season_fr': """**Période de semis:**

- **Saison principale** (hivernage): Mai à Juillet
- **Zone nord**: Juillet-Août
- **Zone centre**: Juin-Juillet
- **Zone sud** (Casamance): Mai-Juin
- **Culture de contre-saison** (irrigation): Novembre-Décembre

**Conditions requises:**
- Pluie utile de 30-40mm minimum
- Sol humide sur 15-20cm
- Température > 12°C""",

                'maturity_time_fr': """**Durée du cycle:**

- **Variétés précoces** (EV, Obatanpa): 90-100 jours
- **Variétés intermédiaires** (CMS 8704): 100-120 jours
- **Variétés tardives** (Locale): 120-150 jours

**Stades clés:**
- Levée: 5-8 jours
- 8-10 feuilles: 30-35 jours
- Floraison mâle: 50-60 jours
- Floraison femelle: 55-65 jours
- Maturité: 90-150 jours

**Signes de maturité:**
- Point noir à la base du grain
- Spathes sèches et brunes
- Grains durs, brillants
- Humidité < 25%""",

                'challenges_insects_fr': """**Ravageurs majeurs:**

1. **Foreurs des tiges** (Busseola fusca, Sesamia calamistis)
   - Galeries dans tiges
   - Bris de tige, verse
   - Perte 20-50%

2. **Légionnaire d'automne** (Spodoptera frugiperda)
   - Défoliation sévère
   - Ravageur émergent très destructeur
   - Toutes les zones

3. **Pucerons** (Rhopalosiphum maidis)
   - Jaunissement, fumagine
   - Vecteur de virus

4. **Termites**
   - Attaque racines et tiges
   - Plus en saison sèche

5. **Charançons du maïs** (Sitophilus zeamais)
   - Ravageur de stock
   - Perte 30-50% en 6 mois""",

                'challenges_diseases_fr': """**Maladies importantes:**

1. **Striure du maïs** (MSV - Maize Streak Virus)
   - Stries jaunes parallèles
   - Transmis par cicadelles
   - Peut détruire culture

2. **Helminthosporiose** (Turcicum)
   - Taches brunes sur feuilles
   - Dessèchement prématuré

3. **Charbon commun** (Ustilago maydis)
   - Galles sur épis, tiges
   - Réduit rendement

4. **Fusariose** (Fusarium spp.)
   - Pourriture de l'épi
   - Mycotoxines dangereuses

5. **Cercosporiose**
   - Taches foliaires
   - Réduction photosynthèse""",

                'challenges_environmental_fr': """**Stress abiotiques:**

1. **Déficit hydrique:**
   - Critique à la floraison
   - Mauvaise pollinisation
   - Épis mal remplis

2. **Températures élevées** (>35°C):
   - Stérilité pollinique
   - Dessèchement prématuré

3. **Carences nutritionnelles:**
   - Azote: Jaunissement, croissance ralentie
   - Phosphore: Coloration pourpre
   - Potassium: Brûlures marginales

4. **Toxicité aluminium:**
   - Sols acides (pH<5.5)
   - Mauvais développement racinaire

5. **Verse:**
   - Vents forts
   - Mauvais ancrage racinaire""",

                'prevention_tips_fr': """**Stratégies préventives:**

1. **Variétés résistantes:**
   - EV 8422-SR (résistant MSV)
   - Obatanpa (QPM, nutritif)
   - Hybrides résistants foreurs

2. **Rotation:**
   - Maïs/légumineuses/céréales
   - Casser cycle parasitaire

3. **Densité optimale:**
   - 50,000-66,000 plants/ha
   - Espacement: 75cm x 25cm

4. **Dates de semis:**
   - Semis groupé au niveau village
   - Éviter hôtes des ravageurs

5. **Travail du sol:**
   - Labour pour enfouir résidus
   - Détruire refuges de ravageurs

6. **Associations:**
   - Maïs + niébé (azote)
   - Plantes répulsives (basilic)""",

                'management_tips_fr': """**Gestion en cours de culture:**

1. **Contre légionnaire d'automne:**
   - Dépistage régulier
   - Traitement localisé (verticille)
   - Biopesticides (Bt, neem)
   - Lâchers d'ennemis naturels

2. **Contre foreurs:**
   - Application pesticide au verticille
   - Trichogrammes (parasitoïdes)

3. **Fertilisation raisonnée:**
   - Fractionnée (semis, 30j, 45j)
   - Adapter aux besoins plante

4. **Irrigation complémentaire:**
   - 20-30mm/semaine
   - Critique floraison-remplissage

5. **Sarclages:**
   - 2-3 passages
   - Buttage à 30-40 jours

6. **Surveillance maladies:**
   - Éliminer plants viroses
   - Fongicides préventifs""",

                'recommended_fertilizers_fr': """**Fertilisation:**

1. **Fumure de fond:**
   - NPK 15-15-15: 200-300 kg/ha
   - ou DAP 18-46-0: 100-150 kg/ha
   - Compost: 10-15 t/ha

2. **Couverture (30 jours):**
   - Urée 46%: 100-150 kg/ha
   - En 2 apports (30j et 45j)

3. **Microdosage:**
   - 10g NPK/poquet au semis
   - 5g Urée/poquet à 30j

4. **Organiques:**
   - Fumier: 10-20 t/ha
   - Compost enrichi
   - Mulch de résidus

**Besoins NPK:**
- Pour 4 t/ha: 120N-60P-40K
- Adapter selon analyse sol""",

                'recommended_pesticides_fr': """**Protection phytosanitaire:**

1. **Insecticides:**
   - **Belt 480 SC**: 0.1L/ha (légionnaire)
   - **Ampligo**: 0.2L/ha (large spectre)
   - **Emacot**: 0.5L/ha (foreurs)
   - **Bt**: 1-2L/ha (bio)

2. **Fongicides:**
   - **Banko Plus**: 2kg/ha (helminthosporiose)
   - **Score 250 EC**: 0.5L/ha (cercosporiose)
   - **Traitement semences** (Apron, Gaucho)

3. **Herbicides:**
   - **Atrazine**: 2-3L/ha (pré-levée)
   - **Nicosulfuron**: 1.5L/ha (post-levée)
   - Désherbage manuel préférable

**Stockage:**
- **Actellic Super**: 50ml/100kg grains
- **Phostoxin**: Fumigation (silos)""",

                'recommended_tools_fr': """**Équipements:**

1. **Travail du sol:**
   - Charrue à disques/socs
   - Pulvériseur
   - Billonneuse

2. **Semis:**
   - Semoir de précision
   - Semoir maraîcher manuel

3. **Entretien:**
   - Sarclo-bineuse
   - Pulvérisateur 15-20L
   - Épandeur engrais

4. **Récolte:**
   - Égreneuse mécanique
   - Batteuse (grandes surfaces)
   - Décortiqueuse

5. **Séchage:**
   - Cribs métalliques
   - Bâches plastiques
   - Séchoirs solaires

6. **Stockage:**
   - Silos métalliques hermétiques
   - Sacs PICS (triple ensachage)""",

                'innovative_inputs_fr': """**Innovations:**

1. **Semences hybrides:**
   - Rendement +100-150%
   - Hybrides F1 (renouveler chaque année)
   - QPM (Quality Protein Maize)

2. **Push-Pull:**
   - Desmodium (répulsif) entre lignes
   - Herbe à éléphant (attractif) en bordure
   - Réduit foreurs et striga

3. **Biostimulants:**
   - Algues marines
   - Acides aminés
   - Mycorhizes

4. **Irrigation goutte-à-goutte:**
   - Économie eau 60%
   - Fertigation
   - Automatisation

5. **Sacs PICS:**
   - Conservation hermétique
   - Sans pesticide
   - Dure 2-3 ans

6. **Drones:**
   - Épandage précis
   - Cartographie parasitaire
   - Gain temps

7. **Maïs Bt (résistant foreurs):**
   - Si autorisé
   - Réduit pesticides

8. **Agriculture de conservation:**
   - Semis direct
   - Couverture permanente
   - Rotations""",

                'additional_notes_fr': """**Informations complémentaires:**

**Rendements:**
- Traditionnel: 1-2 t/ha
- Amélioré: 3-5 t/ha
- Irrigué: 6-10 t/ha

**Valeur nutritionnelle:**
- QPM: 2x lysine, tryptophane
- Meilleure nutrition enfants

**Transformation:**
- Farine, semoule
- Aliment bétail
- Brasserie (malt)

**Marchés:**
- Consommation humaine
- Alimentation animale
- Industrie (amidon)

**Crédit:**
- Subventions intrants
- Warrantage
- Assurance indicielle""",
            },

            # 3. SORGHUM (Sorgho)
            {
                'crop_name': 'Sorgho',
                'planting_season_fr': """**Période de semis:**

- **Saison principale**: Juin à Août
- **Zone sèche** (Nord): Juillet-Août
- **Zone humide** (Sud): Juin-Juillet
- **Contre-saison** (bas-fonds): Novembre-Décembre

**Conditions:**
- Première pluie utile (25mm min)
- Sol réchauffé (>15°C)
- Humidité suffisante""",

                'maturity_time_fr': """**Cycle cultural:**

- **Variétés précoces** (CE180-33, IRAT204): 90-105 jours
- **Intermédiaires** (CSM63, CSM219): 110-125 jours
- **Tardives** (Locale): 130-160 jours

**Phases:**
- Levée: 6-10 jours
- Tallage: 20-30 jours
- Montaison: 40-55 jours
- Épiaison: 60-75 jours
- Floraison: 65-85 jours
- Maturité: 90-160 jours

**Maturité:**
- Grains durs
- Point noir visible
- Humidité <20%""",

                'challenges_insects_fr': """**Ravageurs:**

1. **Pucerons du sorgho** (Melanaphis/Rhopalosiphum)
   - Colonies denses
   - Miellat, fumagine
   - Transmettent virus

2. **Foreurs des tiges** (Busseola, Sesamia, Chilo)
   - Galeries, cœurs morts
   - Verse des plants

3. **Punaises** (Eurystylus, Campylomma)
   - Piquent grains laiteux
   - Grains vides

4. **Cécidomyie** (Stenodiplosis)
   - Déformation panicule
   - Grains avortés

5. **Oiseaux** (Quelea)
   - Consomment grains
   - Pertes 20-100%

6. **Charançons du grain**
   - Ravageur stock
   - Perte qualité""",

                'challenges_diseases_fr': """**Maladies:**

1. **Charbon couvert** (Sporisorium sorghi)
   - Grains remplacés par spores
   - Transmission par semences

2. **Anthracnose** (Colletotrichum graminicola)
   - Taches rouges, dessèchement
   - Favorisée par humidité

3. **Mildiou** (Peronosclerospora sorghi)
   - Plants nanifiés, déformés
   - Transmission sol/semences

4. **Rouille** (Puccinia purpurea)
   - Pustules rouges/brunes
   - Affaiblit plante

5. **Maladies virales** (SCMV)
   - Mosaïques, panachures
   - Transmis par pucerons

6. **Ergot**
   - Sclérotes noirs
   - Toxique""",

                'challenges_environmental_fr': """**Stress environnementaux:**

1. **Sécheresse:**
   - Tolérant mais sensible à floraison
   - Mauvais remplissage grains

2. **Températures:**
   - Optimal 25-30°C
   - >40°C: stress thermique

3. **Striga** (plante parasite):
   - Sorgho sensible
   - Réduit rendement 20-80%

4. **Toxicité aluminium:**
   - Sols acides
   - Racines brûlées

5. **Carences:**
   - Azote, phosphore
   - Plants chétifs

6. **Excess eau:**
   - Asphyxie racinaire
   - Favorise maladies""",

                'prevention_tips_fr': """**Prévention:**

1. **Variétés améliorées:**
   - CE180-33 (précoce)
   - CSM63E (résistant sécheresse)
   - F2-20 (grain blanc)

2. **Traitement semences:**
   - Apron Star (charbon, mildiou)
   - Calthio (insectes sol)

3. **Rotation:**
   - Sorgho/légumineuses
   - Éviter succession sorgho/maïs

4. **Dates de semis:**
   - Respecter calendrier
   - Semis groupé (oiseaux)

5. **Densité:**
   - 100,000-150,000 plants/ha
   - Espacement: 80cm x 20cm

6. **Travail sol:**
   - Labour profond
   - Bonne préparation
   - Drainage si besoin

7. **Lutte Striga:**
   - Rotation niébé
   - Variétés tolérantes
   - Herbicides sélectifs""",

                'management_tips_fr': """**Gestion culturale:**

1. **Contre pucerons:**
   - Traitement préventif
   - Dès apparition colonies
   - Favoriser auxiliaires

2. **Contre foreurs:**
   - Pesticides au verticille
   - Lâchers trichogrammes

3. **Protection oiseaux:**
   - Gardiennage dès épiaison
   - Effaroucheurs divers
   - Filets si possible
   - Récolte à temps

4. **Désherbage:**
   - 2-3 sarclages
   - Buttage à 30j
   - Paillage

5. **Fertilisation:**
   - Apport fractionné
   - NPK puis Urée
   - Selon besoin

6. **Irrigation d'appoint:**
   - Si possible
   - Floraison-remplissage

7. **Surveillance:**
   - Dépistage régulier
   - Intervention rapide""",

                'recommended_fertilizers_fr': """**Fertilisation:**

1. **Fumure fond** (semis):
   - NPK 15-15-15: 150-200 kg/ha
   - ou NPK 6-20-10: 200 kg/ha
   - DAP: 100 kg/ha

2. **Couverture** (30-35j):
   - Urée 46%: 50-100 kg/ha
   - Sulfate ammonium: 100-150 kg/ha

3. **Amendements:**
   - Compost: 10-15 t/ha
   - Fumier: 10-20 t/ha
   - Enfouis avant semis

4. **Microdosage:**
   - 6g NPK/poquet semis
   - 2g Urée/poquet 30j
   - Économie 50% engrais

5. **Correction carences:**
   - Phosphore: TSP, DAP
   - Azote: Urée fractionnée
   - K: Chlorure potassium

**Besoins moyens:**
- 3 t/ha: 100N-50P-30K""",

                'recommended_pesticides_fr': """**Produits phytosanitaires:**

1. **Insecticides:**
   - **K-Optimal**: 0.5L/ha (pucerons)
   - **Cypercal**: 0.4L/ha (foreurs)
   - **Décis**: 0.3L/ha (punaises)
   - **Neem**: 2-3L/ha (bio)

2. **Fongicides:**
   - **Apron Star**: traitement semences
   - **Banko Plus**: 2kg/ha (anthracnose)
   - **Mancozèbe**: 2.5kg/ha (préventif)

3. **Herbicides:**
   - **Atrazine**: 2L/ha (pré-levée)
   - **2,4-D**: 2L/ha (dicotylédones)
   - Désherbage manuel préférable

4. **Anti-Striga:**
   - **Imazapyr**: 75g/ha
   - Traitement localisé

5. **Stockage:**
   - **Actellic**: 50ml/100kg
   - **Sofagrain**: fumigation

**Sécurité:**
- EPI obligatoire
- Délai avant récolte
- Respecter doses""",

                'recommended_tools_fr': """**Outils nécessaires:**

1. **Préparation:**
   - Charrue (bœufs/tracteur)
   - Houe manga
   - Herse
   - Rouleau

2. **Semis:**
   - Semoir multi-rangs
   - Semoir Aitchison
   - Cordeau marquage
   - Rayonneur

3. **Entretien:**
   - Sarcleuse hilaire
   - Houe, serfouette
   - Pulvérisateur 15-20L
   - Épandeur manuel

4. **Récolte:**
   - Couteau/faucille
   - Batteuse mécanique
   - Vannoir
   - Bâches séchage

5. **Stockage:**
   - Greniers améliorés
   - Silos métalliques
   - Fûts hermétiques
   - Sacs PICS

6. **Transformation:**
   - Décortiqueuse
   - Moulin à meule""",

                'innovative_inputs_fr': """**Innovations:**

1. **Variétés hybrides:**
   - Rendement +50-100%
   - CSM63 (résistant sécheresse)
   - Pablo (grain sucré)

2. **Sorgho sucré:**
   - Double usage (grain + jus)
   - Biocarburant
   - Sirop alimentaire

3. **Lutte intégrée Striga:**
   - Variétés tolérantes
   - Herbicides sélectifs
   - Rotation cultures pièges

4. **Biofortification:**
   - Sorgho riche en fer
   - Pro-vitamine A
   - Meilleure nutrition

5. **Microdose + Zaï:**
   - Poquets améliorés
   - +80-120% rendement
   - Zone sèche

6. **Sorgho photopériode:**
   - Floraison contrôlée
   - Optimise eau

7. **Biopesticides:**
   - Extraits neem
   - Bt contre foreurs
   - Sans résidus

8. **Technologies:**
   - Drones pulvérisation
   - Capteurs humidité
   - Alerte précoce oiseaux""",

                'additional_notes_fr': """**Informations utiles:**

**Rendements:**
- Traditionnel: 600-1000 kg/ha
- Amélioré: 2000-3500 kg/ha
- Potentiel: 5000+ kg/ha

**Conservation:**
- Sécher <14% humidité
- Stocker lieu sec, frais
- Traiter contre charançons
- Contrôles réguliers

**Valorisation:**
- Consommation humaine (couscous, bouillie)
- Aliment bétail
- Brasserie (bière locale)
- Biocarburant
- Construction (tiges)

**Avantages sorgho:**
- Résistant sécheresse
- Sol pauvre toléré
- Multiples usages
- Bonne conservation

**Marché:**
- Demande croissante
- Prix stable
- Warrantage possible

**Associations:**
- Sorgho + niébé
- Rotation arachide/sorgho""",
            },

            # 4. RICE (Riz)
            {
                'crop_name': 'Riz',
                'planting_season_fr': """**Périodes de semis:**

**Riz irrigué:**
- **Saison chaude**: Février-Avril
- **Hivernage**: Juillet-Août

**Riz pluvial strict:**
- Juin-Juillet (début hivernage)

**Riz de mangrove:**
- Juin-Août

**Bas-fonds:**
- Mai-Juillet

**Conditions:**
- Disponibilité eau assurée
- Sol bien préparé
- Température >15°C""",

                'maturity_time_fr': """**Durée cycle:**

- **Variétés précoces** (Sahel 108, 134): 90-105 jours
- **Intermédiaires** (Sahel 201, 202): 110-125 jours
- **Tardives** (Locale, aromati ques): 130-160 jours

**Stades phénologiques:**
- Levée: 5-10 jours
- Tallage: 20-40 jours
- Montaison: 45-60 jours
- Épiaison: 70-90 jours
- Floraison: 72-95 jours
- Maturation: 90-160 jours

**Indicateurs maturité:**
- Grains durs
- Panicules penchées
- Paille jaunissante
- Humidité grains <25%""",

                'challenges_insects_fr': """**Ravageurs principaux:**

1. **Foreurs de tige** (Maliarpha, Chilo, Sesamia)
   - Cœurs morts jeunes plants
   - Panicules blanches
   - Verse

2. **Galle du riz** (Orseolia oryzivora)
   - Talles déformées (galles)
   - Pas de panicules
   - Perte rendement importante

3. **Punaises** (Aspavia armigera)
   - Piquent grains laiteux
   - Grains vides, piquetés

4. **Criquets** (Hieroglyphus, Locusta)
   - Défoliation
   - Attaques ponctuelles

5. **Rats** (Mastomys, Arvicanthis)
   - Consomment grains
   - Creusent digues

6. **Oiseaux** (Quelea, mange-mil)
   - Déprédation grains mûrs
   - Pertes élevées""",

                'challenges_diseases_fr': """**Maladies majeures:**

1. **Pyriculariose** (Pyricularia oryzae)
   - Taches losangiques feuilles
   - Panicules desséchées
   - Maladie la plus grave

2. **Helminthosporiose** (Bipolaris oryzae)
   - Taches brunes sur feuilles
   - Réduit photosynthèse

3. **Panachure jaune** (RYMV - virus)
   - Stries jaunes feuilles
   - Plants rabougris
   - Transmis par insectes

4. **Sheath rot** (Sarocladium)
   - Pourriture gaine foliaire
   - Panicules partiellement sorties

5. **Maladies des racines** (Fusarium)
   - Pourriture système racinaire
   - Jaunissement, mort

6. **Bactériose** (Xanthomonas)
   - Stries translucides
   - Flétrissement""",

                'challenges_environmental_fr': """**Contraintes environnementales:**

1. **Gestion de l'eau:**
   - Inondation excessive: asphyxie
   - Déficit eau: stress
   - Contrôle niveau eau crucial

2. **Températures:**
   - Froid (<15°C): croissance ralentie
   - Chaud (>35°C): stérilité florale

3. **Toxicité fer:**
   - Sols hydromorphes acides
   - Feuilles brunes ("bronzing")

4. **Carences:**
   - Azote: jaunissement
   - Phosphore: croissance faible
   - Zinc: plants nanifiés

5. **Salinité:**
   - Vallées fluviales
   - Réduit rendement

6. **Adventices:**
   - Compétition forte
   - Herbes aquatiques
   - Chiendent, souchet""",

                'prevention_tips_fr': """**Mesures préventives:**

1. **Variétés adaptées:**
   - **Irrigué**: Sahel 108, 134, 201, 202
   - **Pluvial**: NERICA 1-4
   - **Résistantes**: Sahel 177 (RYMV)

2. **Semences certifiées:**
   - Pureté garantie
   - Germination >80%
   - Traitement fongicide

3. **Préparation rizière:**
   - Labour, hersage
   - Nivellement précis
   - Digues étanches

4. **Rotation cultures:**
   - Riz/légumineuses
   - Jachère améliorée

5. **Calendrier cultural:**
   - Semis groupé
   - Respecter dates

6. **Gestion eau:**
   - Lame d'eau appropriée
   - Drainage au besoin
   - Assèchement avant récolte

7. **Lutte intégrée:**
   - Désherbage précoce
   - Espacements réguliers
   - Surveillance""",

                'management_tips_fr': """**Conduite culture:**

1. **Pépinière** (semis indirect):
   - Planche bien préparée
   - Semis dense (50-60g/m²)
   - Inonder après levée
   - Repiquer à 20-25 jours

2. **Repiquage:**
   - 2-3 plants/poquet
   - Espacement 20x20cm
   - Profondeur 2-3cm

3. **Désherbage:**
   - 2-3 passages (15, 30, 45 jours)
   - Sarcleuse rotative
   - Herbicides sélectifs

4. **Fertilisation:**
   - NPK fond + urée couverture
   - Apport fractionné azote

5. **Gestion eau:**
   - 5-10cm tallage-montaison
   - 10-15cm floraison-maturation
   - Assécher 15j avant récolte

6. **Contre maladies:**
   - Fongicides préventifs
   - Éliminer plants viroses

7. **Protection oiseaux:**
   - Gardiennage
   - Effaroucheurs
   - Filets""",

                'recommended_fertilizers_fr': """**Programme fertilisation:**

**Riz irrigué:**

1. **Fumure fond** (15 jours avant repiquage):
   - NPK 15-15-15: 200-300 kg/ha
   - ou DAP 18-46-0: 150 kg/ha
   - Urée: 50 kg/ha

2. **Couverture:**
   - **30 jours**: Urée 50-75 kg/ha
   - **45-50 jours**: Urée 50-75 kg/ha
   - **Initiation paniculaire**: Urée 25 kg/ha

3. **Amendements:**
   - Compost: 10-15 t/ha
   - Fumier: 15-20 t/ha
   - Enfouir à sec

**Riz pluvial:**
- NPK 15-15-15: 150-200 kg/ha (semis)
- Urée 46%: 50-100 kg/ha (30-40j)

**Besoins moyens (4-5 t/ha):**
- 120-150 kg N/ha
- 60-80 kg P2O5/ha
- 60-80 kg K2O/ha

**Application:**
- Enfouir engrais
- Eau présente
- Éviter surdosage N (verse)""",

                'recommended_pesticides_fr': """**Protection phytosanitaire:**

**Insecticides:**
1. **Foreurs/Galle:**
   - **Furadan 5G**: 20-30 kg/ha (à l'eau)
   - **Marshal 20 CS**: 1.5L/ha
   - **Regent 800 WG**: 25g/ha

2. **Punaises:**
   - **Décis**: 0.5L/ha
   - **Cypercal**: 0.5L/ha

**Fongicides:**
1. **Pyriculariose:**
   - **Hinosan 50 EC**: 2L/ha
   - **Beam 75 WG**: 200g/ha
   - **Tricyclazole**: 300g/ha

2. **Helminthosporiose:**
   - **Tilt 250 EC**: 0.5L/ha
   - **Banko Plus**: 2kg/ha

3. **Traitement semences:**
   - **Apron Star**: 4g/kg

**Herbicides:**
1. **Pré-levée:**
   - **Ronstar 25 EC**: 6L/ha
   - **Stampede**: 2-3L/ha

2. **Post-levée:**
   - **Topstar**: 500g/ha (graminées)
   - **Nominee**: 1L/ha (souchet)
   - **2,4-D**: 3L/ha (dicotylédones)

**Précautions:**
- Vidanger rizière avant traitement
- Remettre eau 24-48h après
- EPI requis
- Délai avant récolte""",

                'recommended_tools_fr': """**Équipements:**

**Préparation sol:**
1. Tracteur + charrue à disques
2. Herse rotative (pulvériseur)
3. Planche niveleuse
4. Rouleau

**Semis/Repiquage:**
1. Semoir en ligne
2. Repiqueuse mécanique (6-8 rangs)
3. Marqueur espacement

**Entretien:**
1. Sarcleuse rotative (push weeder)
2. Pulvérisateur dorsal 15-20L
3. Épandeur engrais

**Irrigation:**
1. Motopompe diesel/essence
2. Tuyaux PVC
3. Vannes contrôle eau

**Récolte:**
1. Faucheuse-lieuse
2. Batteuse mécanique/décortiqueuse
3. Moissonneuse-batteuse (grandes surfaces)
4. Bâches séchage

**Transformation:**
1. Décortiqueuse/blanchisseuse
2. Trieuse

**Stockage:**
1. Sacs en jute/plastique
2. Magasin aéré
3. Palettes

**Outils manuels:**
1. Faucille
2. Bassines, seaux
3. Râteaux""",

                'innovative_inputs_fr': """**Innovations:**

1. **NERICA (New Rice for Africa):**
   - Hybride riz africain x asiatique
   - Résistant sécheresse
   - Cycle court (90-100j)
   - Rendement élevé

2. **SRI (System of Rice Intensification):**
   - Repiquage jeunes plants (8-12j)
   - 1 plant/poquet, large espacement
   - Sol humide (non inondé)
   - Rendement +20-100%

3. **Variétés tolérantes submersion:**
   - Sahel 328, 329
   - Survivent 14j inondation

4. **Riz aromatique:**
   - Parfumé type Basmati
   - Valeur marchande élevée

5. **Biofortification:**
   - Riz enrichi fer, zinc
   - Combat malnutrition

6. **Micro-dose engrais:**
   - Précision, économie
   - Placement localisé

7. **Herbicides bio:**
   - Extraits plantes
   - Sans résidus

8. **Drones:**
   - Traitement localisé
   - Cartographie rizières

9. **Capteurs:**
   - Niveau eau automatique
   - Humidité sol

10. **Semis direct:**
    - Sans labour
    - Conservation sol
    - Économie eau/temps""",

                'additional_notes_fr': """**Informations complémentaires:**

**Rendements:**
- Traditionnel: 2-3 t/ha
- Irrigué intensif: 5-7 t/ha
- Record: >10 t/ha (SRI)

**Conservation paddy:**
- Sécher <14% humidité
- Stocker lieu sec, aéré
- Traiter contre charançons
- Contrôle régulier

**Transformation:**
- Rendement usinage: 65-70%
- Brisures: 15-25%
- Perte: 10%

**Qualité grain:**
- Grains entiers valorisés
- Minimiser brisures
- Propreté (pas cailloux)

**Utilisations:**
- Consommation (bouillie, riz blanc)
- Aliment bétail (son, brisures)
- Paille (fourrage, construction)

**Systèmes rizicoles Sénégal:**
- Delta/Vallée (irrigué): 70% production
- Bas-fonds: 15%
- Pluvial: 15%

**Crédit/soutien:**
- Subventions engrais/semences
- CNCAS (crédit)
- SAED (encadrement delta)
- Assurance agricole

**Association:**
- Riz-poisson (aquaculture)
- Rotation riz-maraîchage

**Défis:**
- Maîtrise eau
- Coût production
- Compétition riz importé
- Mécanisation limitée""",
            },

            # 5. GROUNDNUTS (Arachide)
            {
                'crop_name': 'Arachide',
                'planting_season_fr': """**Périodes de semis:**

- **Bassin arachidier** (Kaolack, Fatick, Kaffrine): Mi-juin à mi-juillet
- **Zone nord** (Louga, Thiès): Fin juin à fin juillet
- **Zone sud** (Casamance): Début juin à mi-juillet
- **Culture de décrue** (Fleuve): Novembre-Décembre

**Conditions optimales:**
- Première pluie utile (30-40mm)
- Sol réchauffé (>18°C)
- Humidité sol suffisante (10-15cm)
- Éviter semis trop précoce (pourriture)

**Préparation:**
- Décortiquer juste avant semis
- Graines saines, calibrées
- Traiter semences (fongicide)""",

                'maturity_time_fr': """**Durée cycle:**

- **Variétés précoces** (55-437, GH119-20): 90-100 jours
- **Variétés semi-tardives** (73-33, 28-206): 105-120 jours
- **Variétés tardives** (Locale): 120-150 jours

**Stades végétatifs:**
- Levée: 5-8 jours
- Installation: 15-25 jours
- Floraison: 25-35 jours
- Formation gousses: 35-50 jours
- Grossissement: 50-80 jours
- Maturation: 90-150 jours

**Signes de maturité:**
- Jaunissement feuillage
- Coque intérieure colorée (rose, violet)
- Graines remplissent gousse
- Veines gousses foncées

**Test maturité:**
- Arracher quelques plants
- Observer 50-70% gousses matures
- Goûter grain (croquant, goût prononcé)""",

                'challenges_insects_fr': """**Ravageurs majeurs:**

1. **Termites** (Macrotermes, Microtermes)
   - Attaquent plants, gousses
   - Pertes 10-50%
   - Plus en fin de cycle, sol sec

2. **Jassides** (Empoasca spp.)
   - Piquent feuilles (hopperburn)
   - Jaunissement, recroquevill ement
   - Début croissance

3. **Pucerons** (Aphis craccivora)
   - Colonies face inférieure feuilles
   - Enroulement, déformation
   - Transmettent virus

4. **Thrips** (Frankliniella, Megalurothrips)
   - Décoloration, déformation feuilles
   - Réduisent photosynthèse

5. **Chenilles défoliatrices** (Spodoptera, Amsacta)
   - Défoliation sévère
   - Attaques ponctuelles

6. **Sauteriaux** (Zonocerus, Oedaleus)
   - Rongent feuilles, tiges

7. **Vers blancs** (Scarabaeidae)
   - Racines, gousses
   - Présence dans sol riche matière organique

8. **Coléoptères des gousses** (Caryedon serratus)
   - Ravageur de stock
   - Perfore graines""",

                'challenges_diseases_fr': """**Maladies importantes:**

1. **Rosette** (Peanut Rosette Virus)
   - Nanisme, rosettes foliaires
   - Transmis par pucerons
   - Peut détruire culture (100%)

2. **Cercosporioses** (Cercospora/Cercosporidium)
   - Taches brunes/noires feuilles
   - Défoliation prématurée
   - Réduit photosynthèse et rendement

3. **Rouille** (Puccinia arachidis)
   - Pustules orangées feuilles
   - Affaiblit plante

4. **Pourriture des gousses** (Aspergillus, Rhizoctonia)
   - Gousses noircies, pourries
   - Favorisée humidité élevée
   - Aflatoxines (toxiques)

5. **Flétrissement bactérien** (Ralstonia solanacearum)
   - Flétrissement brutal
   - Mort plants
   - Favorisé par chaleur, humidité

6. **Pourriture des racines** (Sclerotium rolfsii)
   - Pourriture collet
   - Plants flétris, morts

7. **Maladies virales** (PStV, TSV)
   - Mosaïques, déformations
   - Transmis par thrips, pucerons""",

                'challenges_environmental_fr': """**Stress environnementaux:**

1. **Déficit hydrique:**
   - Critique floraison-remplissage
   - Gousses mal formées, vides
   - Graines ridées

2. **Excès d'eau:**
   - Pourriture gousses
   - Aflatoxines
   - Maladies cryptogamiques

3. **Températures:**
   - Optimal 25-30°C
   - >35°C: mauvaise fécondation
   - <15°C: croissance ralentie

4. **Sols:**
   - Préfère sols légers, sableux
   - Sols lourds: difficultés pénétration gynophores
   - pH optimal 6.0-6.5
   - Sensible salinité

5. **Carences:**
   - Calcium: gousses vides, mal formées
   - Soufre: jaunissement
   - Bore: fructification réduite

6. **Toxicité aluminium:**
   - Sols acides
   - Mauvais développement racinaire

7. **Adventices:**
   - Compétition forte début cycle
   - Striga en zone sahélienne""",

                'prevention_tips_fr': """**Stratégies préventives:**

1. **Variétés améliorées:**
   - **55-437**: précoce, résistante rosette
   - **GH119-20**: tolérante cercosporioses
   - **73-33**: semi-tardive, bon rendement
   - **Fleur 11**: résistante rosette, cycle court

2. **Semences certifiées:**
   - Pureté variétale
   - Germination >70%
   - Indemnes maladies

3. **Traitement semences:**
   - Fongicide: Apron Star (4ml/kg)
   - Insecticide: Gaucho (7ml/kg)
   - Améliore levée, protège début cycle

4. **Rotation culturale:**
   - Arachide/céréales/jachère
   - Ne pas cultiver >2 ans consécutifs
   - Rotation 3-4 ans idéale
   - Casse cycle maladies/ravageurs

5. **Travail du sol:**
   - Labour profond (20-30cm)
   - Bon émiettage
   - Nivellement pour drainage

6. **Densité optimale:**
   - Espacement: 50cm x 15-20cm
   - 130,000-160,000 plants/ha
   - Éviter densité excessive (maladies)

7. **Gypse (apport calcium):**
   - 200-300 kg/ha
   - Application floraison-début fructification
   - Améliore qualité gousses

8. **Désherbage précoce:**
   - Période critique: 15-45 jours
   - Maintenir culture propre

9. **Lutte intégrée ravageurs:**
   - Traiter termitières (Fipronil)
   - Favoriser ennemis naturels (oiseaux, chrysopes)""",

                'management_tips_fr': """**Conduite culturale:**

1. **Semis:**
   - Profondeur 4-5cm
   - 2-3 graines/poquet
   - Resemis si levée <70%
   - Démariage à 10-15 jours (1-2 plants/poquet)

2. **Désherbage:**
   - **1er**: 15-20 jours (manuel/chimique)
   - **2ème**: 30-35 jours avec buttage léger
   - Paillage pour réduire adventices

3. **Contre pucerons/jassides:**
   - Traitement insecticide à apparition
   - Cypercal, Décis: 0.5L/ha
   - Protège contre virus

4. **Contre cercosporioses:**
   - Fongicides préventifs (floraison+)
   - Banko Plus, Tilt: 2 applications
   - Intervalle 15 jours

5. **Contre termites:**
   - Traitement termitières environnantes
   - Fipronil, Regent
   - Traitement localisé sol

6. **Fertilisation:**
   - NPK 6-20-10: 150-200 kg/ha (semis)
   - Urée: 50 kg/ha (30j) si jaunissement
   - Gypse: 200-300 kg/ha (floraison)
   - Compost: 5-10 t/ha (recommandé)

7. **Gestion eau:**
   - Irrigation d'appoint si sécheresse prolongée
   - Critique: floraison-grossissement gousses
   - 20-30mm/semaine

8. **Récolte:**
   - Arracher manuellement
   - Sécher immédiatement (bâches, aires)
   - Éviter contact sol (aflatoxines)
   - Battre quand bien sec

9. **Post-récolte:**
   - Sécher à 8-10% humidité
   - Trier (enlever avariées)
   - Stocker lieu sec, aéré
   - Traiter contre Caryedon""",

                'recommended_fertilizers_fr': """**Programme fertilisation:**

1. **Fumure de fond** (au semis):
   - **NPK 6-20-10**: 150-200 kg/ha
   - ou **TSP** (45% P2O5): 100 kg/ha + **KCl**: 50 kg/ha
   - **Compost/Fumier**: 5-10 t/ha (très bénéfique)

2. **Apport calcium** (à floraison):
   - **Gypse agricole** (CaSO4): 200-300 kg/ha
   - ou **Chaux**: 150-200 kg/ha
   - Améliore remplissage gousses
   - Épandre début floraison

3. **Azote d'appoint** (si besoin):
   - Légumineuse: fixe azote atmosphérique
   - Urée 46%: 50 kg/ha seulement si jaunissement
   - Application 30 jours après levée

4. **Inoculation rhizobium:**
   - Bactéries fixatrices azote
   - Traitement semences
   - Améliore nodulation
   - Économise azote

5. **Micro-éléments:**
   - **Bore**: 1-2 kg/ha (améliore fructification)
   - **Soufre**: apporté par gypse
   - **Molybdène**: favorise nodulation

6. **Amendements:**
   - Si sol acide (pH<5.5): chauler 1-2 t/ha
   - Incorporer 2-3 semaines avant semis

**Application:**
- Enfouir engrais à côté poquet
- Ne pas mettre en contact graines
- Arroser/attendre pluie

**Besoins moyens (2 t/ha gousses):**
- 10-20 kg N/ha (si pas inoculation)
- 40-60 kg P2O5/ha
- 40-60 kg K2O/ha
- 40-60 kg CaO/ha (gypse)""",

                'recommended_pesticides_fr': """**Produits phytosanitaires:**

**Traitement des semences:**
1. **Apron Star 42 WS**: 4ml/kg (maladies)
2. **Gaucho 350 SC**: 7ml/kg (termites, insectes sol)
3. **Cruiser 350 FS**: 7ml/kg (alternative)

**Insecticides:**
1. **Contre pucerons/jassides:**
   - **Cypercal 50 EC**: 0.5L/ha
   - **Décis 12.5 EC**: 0.5L/ha
   - **Confidor 200 SL**: 0.35L/ha
   - Traiter dès apparition

2. **Contre termites:**
   - **Fipronil 200 SC**: 0.5-1L/ha (termitières)
   - **Regent 800 WG**: 25-50g/ha (sol)
   - Application localisée

3. **Contre chenilles:**
   - **Lambda-cyhalothrine**: 0.3L/ha
   - **Bt**: 1-2L/ha (bio)

**Fongicides:**
1. **Cercosporioses:**
   - **Banko Plus 48 WP**: 2kg/ha
   - **Tilt 250 EC**: 0.5L/ha
   - **Amistar 250 SC**: 0.5L/ha
   - 2-3 applications (intervalle 15j)
   - Début floraison

2. **Pourriture gousses:**
   - **Mancozèbe 80 WP**: 2.5kg/ha (préventif)
   - Éviter excès eau

**Herbicides:**
1. **Pré-levée:**
   - **Pendimethaline 400 EC**: 3-4L/ha
   - **Alachlore 480 EC**: 3L/ha
   - Application après semis, avant levée

2. **Post-levée:**
   - **Imazethapyr**: 1L/ha (sélectif arachide)
   - **Quizalofop-éthyl**: 1L/ha (graminées)
   - 15-20 jours après levée

3. **Désherbage manuel préférable:**
   - Moins coûteux
   - Pas résidus
   - Buttage bénéfique

**Stockage:**
1. **Actellic Super**: 50ml/100kg (charançons)
2. **Phosphine** (Phostoxin): fumigation (grandes quantités)

**Sécurité:**
- Port équipement protection
- Respecter doses
- Délai avant récolte: 21-28 jours
- Manipulation semences traitées avec gants""",

                'recommended_tools_fr': """**Outils et équipements:**

**Préparation sol:**
1. **Charrue** (bœufs/tracteur)
   - Labour 20-30cm profondeur
2. **Houe manga** (labour manuel)
3. **Pulvériseur/herse** (émiettage)
4. **Rouleau** (nivellement)

**Semis:**
1. **Semoir à traction animale/manuelle**
   - Semoir arachide 2-4 rangs
   - Précision espacement
2. **Cordeau** de marquage
3. **Rayonneur** pour lignes

**Entretien:**
1. **Sarcleuse** manuelle (hilaire)
2. **Houe** pour binage/buttage
3. **Pulvérisateur à dos** 15-20L
   - Traitement insecticide/fongicide
4. **Épandeur** manuel (engrais, gypse)

**Récolte:**
1. **Arracheuse** mécanique (grande surface)
   - Tirée par tracteur/bœufs
2. **Houe, fourche** (arrachage manuel)
3. **Bâches plastiques** séchage
4. **Aires de battage** (cimentées de préférence)
5. **Batteuse** mécanique
6. **Décortiqueuse** (extraction graines)

**Séchage:**
1. **Séchoirs solaires améliorés**
2. **Bâches imperméables**
3. **Claies surélevées**
4. **Humidimètre** (contrôle humidité)

**Stockage:**
1. **Magasins/entrepôts** aérés
2. **Sacs en jute/polypropylène**
3. **Palettes** (éviter contact sol)
4. **Fûts métalliques hermétiques** (semences)

**Transformation:**
1. **Décortiqueuse** petite échelle
2. **Presse à huile** (extraction artisanale)
3. **Moulin** (pâte d'arachide)

**Mesure/pesée:**
1. **Balance** (commercialisation)
2. **Bassines standardisées**""",

                'innovative_inputs_fr': """**Innovations et techniques modernes:**

1. **Variétés améliorées à haut rendement:**
   - **Fleur 11**: cycle court (90j), tolérante rosette
   - **GH 119-20**: bon rendement, tolérante cercosporioses
   - **55-437**: résistante rosette, adaptée zones sèches
   - Rendement potentiel: 2.5-3.5 t/ha

2. **Inoculation rhizobium:**
   - Bactéries fixatrices azote
   - Traitement semences avant semis
   - Économie 50-100kg urée/ha
   - Augmente rendement 15-30%
   - Produits: Biomoor, HiStick

3. **Mycorhizes arbusculaires:**
   - Champignons symbiotiques
   - Améliore absorption eau, phosphore
   - Tolérance sécheresse accrue
   - Application semences/sol

4. **Microdosage engrais + gypse:**
   - 6g NPK/poquet semis
   - 10g gypse/plant floraison
   - Économie 50% engrais
   - Rendement +20-40%

5. **Biopesticides:**
   - **Neem** (azadirachtine): Contre insectes piqueurs
   - **Bt** (Bacillus thuringiensis): Chenilles
   - **Trichoderma**: Champignons antagonistes (maladies sol)
   - Moins toxiques, pas résidus

6. **Pièges à phéromones:**
   - Capture insectes ravageurs
   - Surveillance populations
   - Lutte raisonnée

7. **Séchage amélioré:**
   - Séchoirs solaires tunnels
   - Réduit aflatoxines
   - Meilleure qualité
   - Séchage homogène

8. **Stockage hermétique:**
   - **Sacs PICS** (Purdue Improved Cowpea Storage)
   - Triple ensachage
   - Conservation 2 ans sans pesticide
   - Préserve qualité graines

9. **Mécanisation:**
   - Semoirs de précision
   - Arracheuses mécaniques
   - Décortiqueuses performantes
   - Gain temps, rendement

10. **Agriculture de conservation:**
    - Semis direct (mulch)
    - Couverture végétale
    - Rotation diversifiée
    - Conservation humidité sol

11. **Drones agricoles:**
    - Pulvérisation localisée
    - Cartographie parcelles
    - Détection précoce maladies

12. **Applications mobiles:**
    - Diagnostic maladies (photo)
    - Alertes météo
    - Conseils personnalisés
    - Prix du marché

13. **Biofortification:**
    - Variétés enrichies (fer, zinc)
    - Combat malnutrition
    - Graines plus nutritives

14. **Assurance agricole indicielle:**
    - Basée sur pluviométrie
    - Compense déficit pluie
    - Sécurise revenus agriculteurs""",

                'additional_notes_fr': """**Informations complémentaires importantes:**

**Rendements moyens:**
- **Traditionnel**: 800-1,200 kg/ha gousses
- **Avec bonnes pratiques**: 1,500-2,200 kg/ha
- **Potentiel variétés améliorées**: 2,500-3,500 kg/ha
- **Record recherche**: >4,000 kg/ha

**Qualité commerciale:**
- **Extra**: Graines calibre 44/48 (grosses)
- **Première**: Calibre 38/42
- **Deuxième**: Calibre 34/38
- Bonus prix pour arachides propres, sèches

**Conservation gousses/graines:**
- Sécher à 8-10% humidité maximum
- Stocker lieu sec, aéré, frais
- Éviter contact direct sol (aflatoxines)
- Traiter contre charançons (Caryedon)
- Contrôle régulier (humidité, insectes)
- Durée conservation optimale: 6-12 mois

**Utilisations multiples:**
- **Graines**: Consommation (rôties, bouillies), pâte, huile
- **Fanes**: Fourrage bétail (riche protéines)
- **Coque**: Combustible, litière, compost
- **Tourteau** (après extraction huile): Aliment bétail, engrais

**Valorisation:**
- Transformation (pâte, huile): +Valeur ajoutée
- Vente groupée (coopératives): Meilleurs prix
- Certification bio/équitable: Marchés premium

**Marchés:**
- **Local**: Consommation directe, transformation artisanale
- **Industrie**: Huileries (huile, tourteau)
- **Export**: Arachides de bouche vers Europe, Asie

**Systèmes de culture:**
- **Culture pure**: Rendement maximal
- **Association** (arachide + mil/sorgho): Partage risques, diversification
- **Rotation** (arachide/céréales/jachère): Fertilité sol, santé cultures

**Crédit et soutien:**
- **Subventions d'État**: Semences, engrais
- **Crédit campagne**: CNCAS, IMF
- **Warrantage**: Stockage contre crédit
- **Assurance agricole**: Protection contre aléas climatiques
- **Organisations de producteurs**: Accès intrants, commercialisation groupée

**Contraintes actuelles:**
- Prix fluctuants
- Compétition cultures vivrières (céréales)
- Dégradation fertilité sols
- Coût intrants élevé
- Problème aflatoxines (rejet lots)

**Opportunités:**
- Demande locale/régionale forte
- Potentiel transformation (huile, pâte)
- Export arachides bouche
- Amélioration génétique (rendement, résistance)
- Mécanisation croissante

**Conseils clés réussite:**
1. Utiliser semences certifiées
2. Respecter calendrier cultural
3. Traiter semences (maladies, insectes)
4. Rotation culturale stricte
5. Apporter gypse (calcium) à floraison
6. Désherbage précoce et régulier
7. Protéger contre pucerons (virus)
8. Récolter à bonne maturité
9. Sécher rapidement et bien
10. Stocker correctement (sec, aéré)""",
            },
        ]

        # Process first 5 crops (1-5)
        created_count = 0
        updated_count = 0

        for advice_data in crop_advice_data:
            try:
                crop = Crop.objects.get(name_fr__icontains=advice_data['crop_name'].split('(')[0].strip())

                advice, created = CropAdvice.objects.update_or_create(
                    crop=crop,
                    defaults={
                        'planting_season_fr': advice_data['planting_season_fr'],
                        'maturity_time_fr': advice_data['maturity_time_fr'],
                        'challenges_insects_fr': advice_data['challenges_insects_fr'],
                        'challenges_diseases_fr': advice_data['challenges_diseases_fr'],
                        'challenges_environmental_fr': advice_data['challenges_environmental_fr'],
                        'prevention_tips_fr': advice_data['prevention_tips_fr'],
                        'management_tips_fr': advice_data['management_tips_fr'],
                        'recommended_fertilizers_fr': advice_data['recommended_fertilizers_fr'],
                        'recommended_pesticides_fr': advice_data['recommended_pesticides_fr'],
                        'recommended_tools_fr': advice_data['recommended_tools_fr'],
                        'innovative_inputs_fr': advice_data['innovative_inputs_fr'],
                        'additional_notes_fr': advice_data.get('additional_notes_fr', ''),
                        'is_active': True,
                        'created_by': author,
                    }
                )

                if created:
                    created_count += 1
                    self.stdout.write(f'[+] Created: {crop.name_fr}')
                else:
                    updated_count += 1
                    self.stdout.write(f'[*] Updated: {crop.name_fr}')

            except Crop.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'[!] Crop not found: {advice_data["crop_name"]}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'[!] Error processing {advice_data["crop_name"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'\n[OK] Import completed (Part 1 of 3)!'))
        self.stdout.write(self.style.SUCCESS(f'   - Created: {created_count} entries'))
        self.stdout.write(self.style.SUCCESS(f'   - Updated: {updated_count} entries'))
        self.stdout.write(self.style.SUCCESS(f'   - Total: {created_count + updated_count} entries'))
        self.stdout.write(self.style.WARNING(f'\nNote: This imports crops 1-5 (Mil, Maïs, Sorgho, Riz, Arachide)'))
        self.stdout.write(self.style.WARNING(f'Run this command again to continue with remaining 10 crops'))
