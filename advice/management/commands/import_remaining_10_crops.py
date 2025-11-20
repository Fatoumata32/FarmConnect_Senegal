"""
Management command to import structured advice for remaining 10 Senegalese crops:
- Cotton (Coton)
- Fonio
- Cowpeas (Niébé)
- Cassava (Manioc)
- Sweet Potatoes (Patate douce)
- Tomatoes (Tomates)
- Onions (Oignons)
- Watermelon (Pastèque)
- Peppers (Piment)
- Okra (Gombo)
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import models
from advice.models import CropAdvice
from crops.models import Crop

User = get_user_model()


class Command(BaseCommand):
    help = 'Import structured agricultural advice for remaining 10 Senegalese crops'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting import of structured advice for 10 remaining crops...'))

        # Get or create system user
        author, _ = User.objects.get_or_create(
            username='system_advisor',
            defaults={
                'email': 'advisor@farmconnect.sn',
                'first_name': 'System',
                'last_name': 'Advisor'
            }
        )

        # Define crop advice data for remaining 10 crops
        crop_advice_data = [
            # 6. COTTON (Coton)
            {
                'crop_name': 'Coton',
                'planting_season_fr': """**Période de semis:**

- **Zone cotonnière** (Tambacounda, Kolda, Kédougou): Mi-juin à mi-juillet
- **Conditions optimales**: Après premières pluies utiles (30-50mm)
- **Sol**: Bien humidifié sur 15-20cm de profondeur
- **Température**: Sol > 18°C

**Préparation:**
- Labour profond (25-30cm) avant les pluies
- Billonnage recommandé (zones à pluviométrie > 800mm)
- Traitement des semences obligatoire (fongicides + insecticides)""",

                'maturity_time_fr': """**Cycle cultural:**

- **Variétés** (STAM 129A, STAM 59A): 150-170 jours
- **Variétés précoces** (STAM 18A): 140-150 jours

**Stades de croissance:**
- Levée: 5-8 jours
- 4 feuilles vraies: 20-25 jours
- Boutons floraux: 45-60 jours
- Floraison: 70-85 jours
- Capsules mûres: 140-170 jours

**Indicateurs de maturité:**
- Capsules ouvertes (80-90%)
- Fibres blanches et sèches
- 2-3 passages de récolte nécessaires""",

                'soil_type_fr': """**Types de sol:**

- **Sols légers** sablo-limoneux (préférés)
- **Sols argilo-sableux** bien drainés
- pH optimal: 6.0-7.5
- Éviter sols hydromorphes ou très argileux""",

                'challenges_insects_fr': """**Ravageurs majeurs:**

1. **Chenilles phytophages** (Helicoverpa armigera, Earias spp.)
   - Symptômes: Perforations sur feuilles, fleurs, capsules
   - Période critique: Floraison-fructification
   - Seuil: 2 chenilles/plant

2. **Jassides** (Empoasca spp.)
   - Symptômes: Enroulement, rougissement des feuilles
   - Période: 2 semaines à 2 mois après levée

3. **Pucerons** (Aphis gossypii)
   - Symptômes: Miellat, fumagine, déformation feuilles
   - Vecteurs de viroses

4. **Aleurodes** (Bemisia tabaci)
   - Symptômes: Jaunissement, virus de l'enroulement
   - Difficiles à contrôler

5. **Dysdercus** (punaises rouges du cotonnier)
   - Dégâts sur capsules mûres
   - Tachent les fibres""",

                'challenges_diseases_fr': """**Maladies courantes:**

1. **Bactériose** (Xanthomonas campestris)
   - Symptômes: Taches angulaires noires sur feuilles
   - Conditions: Humidité élevée, blessures
   - Contrôle difficile

2. **Fusariose vasculaire** (Fusarium oxysporum)
   - Symptômes: Flétrissement unilatéral, jaunissement
   - Sol contaminé
   - Variétés résistantes nécessaires

3. **Pourriture des capsules** (Botryodiplodia, Fusarium)
   - Capsules noircies, fibres tachées
   - Favorisée par pluies tardives

4. **Anthracnose** (Colletotrichum gossypii)
   - Taches sur feuilles et capsules
   - Conditions humides

5. **Virose de l'enroulement**
   - Transmise par aleurodes
   - Réduction sévère du rendement""",

                'challenges_environmental_fr': """**Stress environnementaux:**

1. **Sécheresse:**
   - Période critique: Floraison-fructification
   - Chute des organes fructifères
   - Réduction rendement 40-60%

2. **Excès d'eau:**
   - Asphyxie racinaire
   - Favorise maladies cryptogamiques
   - Verse des plants

3. **Températures élevées:**
   - > 38°C: Avortement floral
   - Stress hydrique accru

4. **Vents violents:**
   - Verse des plants
   - Chute des capsules

5. **Carences nutritionnelles:**
   - Azote: Jaunissement
   - Potassium: Nécrose marginale
   - Bore: Chute organes""",

                'tips_prevention_fr': """**Mesures préventives:**

1. **Variétés adaptées:**
   - STAM 129A (haute productivité)
   - STAM 59A (tolérance sécheresse)
   - Semences certifiées et traitées

2. **Rotation culturale:**
   - Rotation 2-3 ans minimum
   - Coton → Céréales → Légumineuses
   - Réduction pression parasitaire

3. **Préparation du sol:**
   - Labour profond 25-30cm
   - Enfouissement résidus culture précédente
   - Billonnage en zone humide

4. **Densité de semis:**
   - 50,000-70,000 plants/ha
   - Espacement: 80cm x 30cm

5. **Traitement des semences:**
   - Fongicide + Insecticide systémique
   - Gaucho 350 FS: 6ml/kg
   - Apron Star: 4g/kg

6. **Gestion intégrée:**
   - Surveillance hebdomadaire
   - Respect seuils d'intervention
   - Préservation auxiliaires""",

                'tips_management_fr': """**Gestion des problèmes:**

1. **Programme phytosanitaire:**
   - 6-8 traitements insecticides/campagne
   - Alternance matières actives
   - Respect délais avant récolte

2. **Contre chenilles:**
   - Pyréthrinoïdes + organophosphorés
   - Produits: Cypercal, Pacha, Nurelle D
   - Dès apparition (seuil 2/plant)

3. **Contre jassides:**
   - Traitement précoce (20-30 jours)
   - Produits systémiques
   - Éviter résistance

4. **Fertilisation raisonnée:**
   - Fond: 150-200kg NPK 15-15-15
   - Couverture: 50kg Urée (45 jours)
   - Apport bore si carence

5. **Sarclo-binages:**
   - 2-3 passages
   - 15, 30, 45 jours après levée
   - Aération sol, gestion adventices

6. **Irrigation complémentaire:**
   - Si possible en période critique
   - Améliore rendement 20-40%""",

                'fertilizers_fr': """**Programme de fertilisation:**

1. **Fumure de fond** (au semis):
   - NPK 15-15-15: 150-200 kg/ha
   - ou NPK 10-18-18: 200 kg/ha
   - Enfouir à 5-7cm des semences

2. **Fumure d'entretien** (45 jours):
   - Urée 46%: 50 kg/ha
   - ou Sulfate d'ammonium: 100 kg/ha
   - En ligne, 10cm du plant

3. **Apports complémentaires:**
   - Bore (Borax): 5-10 kg/ha si carence
   - Soufre: Intégré dans engrais
   - Magnésium si sol carencé

4. **Fumure organique:**
   - Compost: 5-10 t/ha
   - Fumier décomposé: 10-15 t/ha
   - Appliquer avant labour

**Besoins NPK:**
- N: 120-150 kg/ha
- P₂O₅: 60-80 kg/ha
- K₂O: 60-80 kg/ha""",

                'pesticides_fr': """**Produits phytosanitaires:**

1. **Insecticides:**
   - **Cypercal 50 EC**: 0.5L/ha (chenilles)
   - **Pacha 25 EC**: 0.8L/ha (large spectre)
   - **Nurelle D 550 EC**: 1L/ha (chenilles, jassides)
   - **Confidor 200 SL**: 0.5L/ha (aleurodes, pucerons)

2. **Traitement des semences:**
   - **Gaucho 350 FS**: 6ml/kg (insectes sol)
   - **Apron Star 42 WS**: 4g/kg (maladies)

3. **Programme type:**
   - T1 (20 jours): Anti-jassides
   - T2-T5 (30-75 jours): Anti-chenilles
   - T6-T8 (85-120 jours): Protection capsules

**Bonnes pratiques:**
- Alternance matières actives
- Respect doses homologuées
- Équipement protection
- Pulvérisation tôt le matin""",

                'tools_fr': """**Outils et équipements:**

1. **Préparation:**
   - Charrue à disques ou à socs
   - Billonneuse
   - Herse pour ameublissement

2. **Semis:**
   - Semoir monograine de précision
   - Semoir à traction animale (Super Eco)
   - Traiteuse à semences

3. **Entretien:**
   - Sarcleuse mécanique
   - Bineuse
   - Pulvérisateur à dos 15L (petites surfaces)
   - Pulvérisateur à rampe tracté (grandes surfaces)

4. **Récolte:**
   - Sacs en jute (50-100kg)
   - Bâches de séchage
   - Récolteuse mécanique (mécanisation)

5. **Protection:**
   - Équipement pulvérisation (masque, gants, combinaison)
   - Lunettes protection""",

                'innovative_inputs_fr': """**Innovations:**

1. **Variétés Bt** (résistance chenilles):
   - Réduction traitements insecticides
   - Productivité accrue (+15-25%)
   - En cours d'introduction en Afrique

2. **Micro-irrigation:**
   - Goutte-à-goutte
   - Économie eau 50-60%
   - Rendement +40-60%

3. **Lutte biologique:**
   - Trichogrammes (parasitoïdes)
   - Bacillus thuringiensis (Bt)
   - Neem (répulsif)

4. **Fertilisation foliaire:**
   - Bore, zinc (oligo-éléments)
   - Correction carences rapide
   - Pulvérisation foliaire

5. **Agriculture de précision:**
   - GPS pour semis précis
   - Cartographie rendement
   - Modulation doses engrais

6. **Biopesticides:**
   - Extraits neem
   - Bt (Dipel)
   - Huiles essentielles

7. **Conservation Agriculture:**
   - Couverture sol permanente
   - Réduction labour
   - Amélioration fertilité""",

                'additional_notes_fr': """**Recommandations complémentaires:**

**Rendements:**
- Traditionnel: 800-1,200 kg coton-graine/ha
- Amélioré: 1,500-2,000 kg/ha
- Potentiel: 2,500-3,500 kg/ha

**Récolte:**
- 2-3 passages espacés de 15 jours
- Par temps sec
- Éviter souillures (qualité fibre)

**Commercialisation:**
- Contrat avec sociétés cotonnières (SODEFITEX)
- Prix garanti
- Fourniture intrants à crédit

**Post-récolte:**
- Séchage capsules (humidité < 12%)
- Stockage en sacs jute
- Protection contre humidité

**Crédit:**
- Crédit de campagne via sociétés
- Remboursement à la vente
- Assurance agricole disponible"""
            },

            # 7. FONIO
            {
                'crop_name': 'Fonio',
                'planting_season_fr': """**Période de semis:**

- **Zone sud** (Casamance, Kédougou): Mai à Juillet
- **Zones traditionnelles**: Début hivernage
- **Conditions**: Premières pluies utiles (20-30mm)

**Préparation:**
- Labour léger (10-15cm) suffisant
- Sol bien ameubli
- Fonio tolère sols pauvres et acides""",

                'maturity_time_fr': """**Cycle cultural:**

- **Variétés locales**: 90-120 jours
- **Variétés améliorées**: 80-100 jours

**Stades:**
- Levée: 4-6 jours
- Tallage: 15-25 jours
- Montaison: 40-55 jours
- Épiaison: 55-70 jours
- Maturité: 80-120 jours

**Maturité:**
- Épis penchés, grains durs
- Récolte avant dispersion graines""",

                'soil_type_fr': """**Types de sol:**

- **Sols légers** sableux ou sablo-limoneux (préférés)
- **Sols pauvres** tolérés
- **pH acide** toléré (pH 5-6.5)
- Éviter sols lourds et hydromorphes
- Bonne adaptation terres marginales""",

                'challenges_insects_fr': """**Ravageurs:**

1. **Oiseaux granivores** (Quelea quelea)
   - Principal problème
   - Période: Maturation
   - Dégâts très importants

2. **Foreurs des tiges** (occasionnels)
   - Dégâts limités généralement

3. **Criquets**
   - Défoliation
   - Attaques sporadiques

4. **Charançons de stockage**
   - Post-récolte
   - Détérioration grains""",

                'challenges_diseases_fr': """**Maladies:**

1. **Pyriculariose** (Pyricularia grisea)
   - Taches grisâtres sur feuilles
   - Conditions humides

2. **Helminthosporiose**
   - Taches brunes feuilles
   - Réduit photosynthèse

3. **Charbon**
   - Transformation épis en masses noires
   - Peu fréquent

**Remarque:** Fonio généralement peu sensible aux maladies""",

                'challenges_environmental_fr': """**Contraintes environnementales:**

1. **Sécheresse:**
   - Bonne tolérance du fonio
   - Résiste mieux que mil/sorgho

2. **Sols pauvres:**
   - Bien adapté
   - Peu exigeant en nutriments

3. **Pluies excessives:**
   - Verse possible
   - Qualité grain affectée

4. **Adventices:**
   - Compétition importante
   - Plante à croissance lente initialement""",

                'tips_prevention_fr': """**Mesures préventives:**

1. **Choix variétal:**
   - Variétés améliorées (plus productives)
   - Semences propres et saines

2. **Préparation sol:**
   - Labour léger suffisant
   - Bon ameublissement
   - Faux-semis pour réduire adventices

3. **Densité:**
   - Semis dense: 20-30 kg/ha
   - Semis à la volée ou en lignes
   - Espacement lignes: 20-25cm

4. **Rotation:**
   - Fonio → Légumineuses
   - Améliore fertilité sol

5. **Protection oiseaux:**
   - Préparer dispositifs effarouchement
   - Surveillance dès maturation

6. **Association culturale:**
   - Possible avec niébé, arachide""",

                'tips_management_fr': """**Gestion:**

1. **Contre oiseaux:**
   - Surveillance constante (maturation)
   - Épouvantails, filets
   - Bruits (bidons, pétards)
   - Récolte précoce si nécessaire

2. **Désherbage:**
   - 1-2 sarclages (20, 40 jours)
   - Important car croissance lente
   - Désherbage manuel ou mécanique

3. **Fertilisation légère:**
   - 50-100kg NPK/ha si sol très pauvre
   - Compost: 2-5 t/ha bénéfique
   - Urée 25kg/ha à 30 jours

4. **Récolte:**
   - Faucher à maturité
   - Battre immédiatement ou après séchage
   - Vannage soigné (grains très petits)

5. **Post-récolte:**
   - Séchage grains (12% humidité)
   - Décorticage (qualité importante)
   - Stockage hermétique""",

                'fertilizers_fr': """**Fertilisation:**

1. **Fumure de fond:**
   - NPK 15-15-15: 50-100 kg/ha
   - Fonio peu exigeant
   - Inutile si sol fertile

2. **Fumure entretien:**
   - Urée: 25 kg/ha (30 jours)
   - Facultatif

3. **Matière organique:**
   - Compost: 2-5 t/ha
   - Fumier décomposé: 3-5 t/ha
   - Très bénéfique

**Remarque:** Fonio valorise bien résidus organiques""",

                'pesticides_fr': """**Produits phytosanitaires:**

1. **Traitement semences:**
   - Fongicide léger si disponible
   - Apron Star: 3g/kg

2. **Insecticides:**
   - Rarement nécessaires
   - Si foreurs: Cypercal 0.3L/ha

**Remarque:** Fonio nécessite très peu de traitements chimiques (culture écologique)""",

                'tools_fr': """**Outils:**

1. **Préparation:**
   - Houe, daba
   - Charrue légère

2. **Semis:**
   - Semis à la volée (traditionnel)
   - Semoir en ligne possible

3. **Entretien:**
   - Hilaire pour sarclage
   - Houe

4. **Récolte:**
   - Faucille
   - Couteau de récolte
   - Batteuse (pilon, fléaux)
   - Vannoir

5. **Décorticage:**
   - Mortier-pilon (traditionnel)
   - Décortiqueuse mécanique (amélioration qualité)""",

                'innovative_inputs_fr': """**Innovations:**

1. **Variétés améliorées:**
   - Rendement supérieur (+30-50%)
   - Cycle plus court
   - Meilleure productivité

2. **Décortiqueuse mécanique:**
   - Améliore qualité grain
   - Réduit temps traitement
   - Augmente valeur marchande

3. **Micro-dose engrais:**
   - 3-5g NPK/poquet
   - Rentabilité accrue

4. **Filets anti-oiseaux:**
   - Protection efficace
   - Investissement rentable

5. **Séchoirs améliorés:**
   - Meilleure conservation
   - Qualité supérieure

6. **Emballage sous vide:**
   - Conservation longue durée
   - Marchés d'exportation

7. **Certification bio:**
   - Fonio naturellement bio
   - Valorisation marchés premium""",

                'additional_notes_fr': """**Recommandations complémentaires:**

**Rendements:**
- Traditionnel: 300-600 kg/ha
- Amélioré: 800-1,200 kg/ha
- Potentiel: 1,500-2,000 kg/ha

**Intérêt du fonio:**
- Culture sécuritaire (cycle court)
- Tolère sols pauvres et sécheresse
- Valeur nutritionnelle élevée
- Prix rémunérateur
- Demande croissante (marchés urbains, export)

**Transformation:**
- Décorticage critique pour qualité
- Cuisson rapide (5-10 min)
- Produits dérivés: couscous, farine

**Commercialisation:**
- Marchés locaux et urbains
- Export (diaspora, marchés bio)
- Prix: 500-1000 FCFA/kg (décortiqué)

**Conservation:**
- Séchage à 12% humidité
- Stockage hermétique
- Éviter humidité (moisissures)"""
            },

            # 8. COWPEAS / NIÉBÉ
            {
                'crop_name': 'Niébé',
                'planting_season_fr': """**Période de semis:**

**Culture pure:**
- **Zone nord**: Mi-juillet à début août
- **Zone centre**: Juillet
- **Zone sud**: Juin-juillet

**Culture associée** (avec mil, maïs, sorgho):
- Semis 2-3 semaines après céréale
- Juillet-août

**Culture de décrue:**
- Septembre-octobre (bas-fonds, valleys)

**Conditions:**
- Premières pluies utiles
- Sol humide sur 10cm
- Température > 18°C""",

                'maturity_time_fr': """**Cycle cultural:**

- **Variétés précoces** (Mouride, 58-53): 60-75 jours
- **Variétés intermédiaires** (Mélakh, Bambey 21): 75-90 jours
- **Variétés tardives** (Locale): 90-120 jours

**Stades:**
- Levée: 4-7 jours
- Floraison: 30-45 jours
- Formation gousses: 45-60 jours
- Maturité: 60-120 jours

**Maturité:**
- Gousses sèches, brunâtres
- Grains durs
- Récolter avant éclatement gousses""",

                'soil_type_fr': """**Types de sol:**

- **Sols légers** sableux ou sablo-limoneux (préférés)
- **Sols bien drainés** essentiels
- pH: 6.0-7.5 (optimal)
- Tolère sols pauvres (légumineuse fixatrice d'azote)
- Éviter sols hydromorphes ou trop argileux""",

                'challenges_insects_fr': """**Ravageurs majeurs:**

1. **Pucerons** (Aphis craccivora)
   - Colonies sur jeunes pousses
   - Période: Floraison
   - Transmission virus de la mosaïque
   - Seuil: Dès apparition colonies

2. **Thrips** (Megalurothrips sjostedti)
   - Piqûres sur fleurs et gousses
   - Chute fleurs, déformation gousses
   - Période critique: Floraison

3. **Foreurs des gousses** (Maruca vitrata)
   - Chenilles dans gousses
   - Dégâts directs sur graines
   - 40-60% pertes possibles

4. **Bruches** (Callosobruchus maculatus)
   - Post-récolte et stockage
   - Perforation graines
   - Perte totale si non contrôlées

5. **Punaises suceuses** (Clavigralla, Anoplocnemis)
   - Piqûres sur gousses
   - Graines avortées""",

                'challenges_diseases_fr': """**Maladies:**

1. **Virus de la mosaïque** (CABMV, BICMV)
   - Transmis par pucerons
   - Mosaïque, déformation feuilles
   - Nanisme, perte rendement importante

2. **Flétrissement bactérien** (Xanthomonas)
   - Flétrissement brutal
   - Lésions sur feuilles et gousses
   - Conditions humides

3. **Anthracnose** (Colletotrichum)
   - Taches brunes feuilles, gousses
   - Pluies fréquentes
   - Réduction qualité et rendement

4. **Pourriture racinaire** (Rhizoctonia, Fusarium)
   - Flétrissement, jaunissement
   - Excès d'eau
   - Mauvais drainage

5. **Oïdium** (Erysiphe polygoni)
   - Poudre blanche sur feuilles
   - Réduit photosynthèse""",

                'challenges_environmental_fr': """**Stress environnementaux:**

1. **Sécheresse:**
   - Période critique: Floraison-remplissage gousses
   - Avortement fleurs et gousses
   - Réduction rendement 50-70%

2. **Excès d'eau:**
   - Asphyxie racinaire
   - Pourriture racinaire
   - Niébé sensible engorgement

3. **Températures élevées:**
   - > 35°C: Avortement floral
   - Stress hydrique
   - Période floraison très sensible

4. **Sols acides:**
   - pH < 5.5: Mauvaise nodulation
   - Fixation azote réduite
   - Croissance ralentie

5. **Carences:**
   - Phosphore: Floraison réduite
   - Potassium: Mauvais remplissage gousses""",

                'tips_prevention_fr': """**Mesures préventives:**

1. **Choix variétal:**
   - Variétés résistantes virus (IT89KD-288)
   - Variétés adaptées zone (précoces si nord)
   - Semences certifiées

2. **Rotation culturale:**
   - Rotation 2-3 ans
   - Éviter légumineuses successives
   - Alterner avec céréales

3. **Préparation sol:**
   - Labour léger suffisant
   - Bon drainage essentiel
   - Enfouissement résidus

4. **Densité et espacement:**
   - Culture pure: 30,000-40,000 plants/ha
   - Lignes: 50cm x 20cm ou 60cm x 15cm
   - Associée: Réduire densité 50%

5. **Inoculation Rhizobium:**
   - Si première culture sur parcelle
   - Améliore fixation azote
   - Augmente rendement

6. **Traitement semences:**
   - Insecticide contre insectes sol
   - Fongicide si conditions humides
   - Calthio C: 3g/kg""",

                'tips_management_fr': """**Gestion:**

1. **Lutte contre pucerons:**
   - Traitement précoce dès apparition
   - Cypercal, Décis: 0.3L/ha
   - 2-3 traitements espacés 7 jours

2. **Contre foreurs gousses:**
   - Traitement à la floraison
   - 2-3 applications (10 jours d'intervalle)
   - Lambda Super, Nurelle D

3. **Protection contre bruches:**
   - Traitement gousses avant stockage
   - Actellic Super: 20ml/100kg
   - Stockage hermétique (triple sac)

4. **Désherbage:**
   - 1-2 sarclages (15, 30 jours)
   - Critique avant floraison
   - Compétition adventices forte

5. **Fertilisation:**
   - Phosphore important: 50-100kg TSP/ha
   - Azote limité (légumineuse)
   - Potasse: 50kg KCl/ha

6. **Gestion eau:**
   - Irrigation d'appoint floraison-remplissage
   - 20-30mm/semaine période critique
   - Améliore rendement 40-60%""",

                'fertilizers_fr': """**Fertilisation:**

1. **Fumure de fond:**
   - TSP (Triple Super Phosphate): 100 kg/ha
   - ou NPK 10-18-18: 100 kg/ha
   - Phosphore essentiel nodulation

2. **Fumure potassique:**
   - KCl (Chlorure de potassium): 50 kg/ha
   - Améliore remplissage gousses

3. **Azote:**
   - Dose faible: 20-30 kg N/ha
   - Légumineuse fixe azote atmosphérique
   - Excès azote réduit nodulation

4. **Matière organique:**
   - Compost: 3-5 t/ha
   - Fumier: 5-10 t/ha
   - Améliore structure sol

5. **Inoculation Rhizobium:**
   - 200g inoculum/ha
   - À la volée ou avec semences
   - Si première culture légumineuse

**Application:**
- Localiser engrais près des semences
- Enfouir légèrement""",

                'pesticides_fr': """**Produits phytosanitaires:**

1. **Insecticides végétation:**
   - **Cypercal 50 EC**: 0.3L/ha (pucerons, thrips)
   - **Décis 12.5 EC**: 0.25L/ha (pucerons)
   - **Lambda Super 2.5 EC**: 0.3L/ha (foreurs, punaises)
   - **Nurelle D**: 0.8L/ha (large spectre)

2. **Insecticides stockage:**
   - **Actellic Super Dust**: 50g/100kg grains
   - **K-Obiol 25 EC**: Trempage sacs
   - Application avant stockage

3. **Traitement semences:**
   - **Calthio C**: 3g/kg (insectes sol)
   - **Apron Star**: 3g/kg (maladies)

4. **Fongicides:**
   - **Banko Plus**: 2kg/ha (anthracnose)
   - Rarement nécessaire

**Programme type:**
- T1 (floraison): Anti-pucerons + thrips
- T2-T3 (formation gousses): Anti-foreurs""",

                'tools_fr': """**Outils:**

1. **Préparation:**
   - Charrue légère
   - Houe pour billons
   - Daba pour labour manuel

2. **Semis:**
   - Semoir monograine
   - Cordeau pour alignement
   - Plantoir manuel

3. **Entretien:**
   - Hilaire, sarcleuse
   - Houe pour binage
   - Pulvérisateur 15L

4. **Récolte:**
   - Arrachage manuel
   - Faucille pour couper plants
   - Bâches pour séchage
   - Bâtons pour battage

5. **Stockage:**
   - Triple sac PICS (hermétique)
   - Fûts métalliques
   - Greniers traditionnels améliorés""",

                'innovative_inputs_fr': """**Innovations:**

1. **Variétés améliorées:**
   - IT89KD-288 (résistante virus, foreurs)
   - Mouride (précoce 60j, tolérante sécheresse)
   - Rendement +50-100%

2. **Triple sac PICS:**
   - Stockage hermétique
   - Protection bruches sans insecticide
   - Conservation 18-24 mois

3. **Inoculation Rhizobium:**
   - Améliore fixation azote
   - Réduit besoin engrais azoté
   - +20-40% rendement

4. **Micro-irrigation:**
   - Goutte-à-goutte période critique
   - Économie eau 50-70%
   - Rendement +60-80%

5. **Variétés fourragères:**
   - Double usage (grain + fourrage)
   - Intégration agriculture-élevage
   - Revenus additionnels

6. **Biopesticides:**
   - Neem contre pucerons
   - Extraits botaniques
   - Agriculture biologique

7. **Pièges à phéromones:**
   - Monitoring foreurs
   - Réduction traitements
   - Lutte intégrée

8. **Semis direct:**
   - Conservation humidité
   - Réduction érosion
   - Agriculture de conservation""",

                'additional_notes_fr': """**Recommandations complémentaires:**

**Rendements:**
- Traditionnel: 200-400 kg/ha
- Amélioré: 600-1,000 kg/ha
- Potentiel: 1,500-2,500 kg/ha
- Irrigué: 2,000-3,000 kg/ha

**Avantages niébé:**
- Fixe azote atmosphérique (40-80 kg N/ha)
- Améliore fertilité sol
- Protéines végétales (23-25%)
- Cycle court (sécurité alimentaire)
- Fanes fourragères pour bétail

**Récolte:**
- 2-3 passages si variétés indéterminées
- Récolter tôt le matin (gousses cassantes)
- Séchage gousses avant battage

**Conservation:**
- Sécher grains à 12-14% humidité
- Stockage hermétique (triple sac PICS)
- Éviter bruches (traitement ou hermétique)
- Durée: 12-18 mois

**Commercialisation:**
- Marchés locaux (consommation directe)
- Transformation (farine, akara)
- Export (pays côtiers)
- Prix: 300-600 FCFA/kg

**Nutrition:**
- Riche en protéines, fer, zinc
- Complément céréales
- Sécurité nutritionnelle"""
            },

            # 9. CASSAVA / MANIOC
            {
                'crop_name': 'Manioc',
                'planting_season_fr': """**Période de plantation:**

**Zone sud** (Casamance, Kédougou):
- **Plantation principale**: Mai-Juillet (début hivernage)
- **Plantation secondaire**: Septembre-Octobre

**Préparation:**
- Labour profond (30cm) avant pluies
- Billonnage recommandé (améliore drainage)
- Boutures de 20-25cm, 5-7 nœuds

**Conditions:**
- Sol bien humidifié
- Après premières pluies utiles
- Boutures de plants sains (8-12 mois)""",

                'maturity_time_fr': """**Cycle cultural:**

- **Variétés précoces**: 8-10 mois
- **Variétés intermédiaires**: 10-12 mois
- **Variétés tardives**: 12-18 mois

**Stades de croissance:**
- Débourrement bourgeons: 7-15 jours
- Enracinement: 15-30 jours
- Croissance active: 3-6 mois
- Formation tubércules: 4-8 mois
- Maturité tubércules: 8-18 mois

**Période optimale récolte:**
- Après 10-12 mois (bon compromis rendement/qualité)
- Possible après 8 mois (si nécessaire)
- Peut rester en terre 18-24 mois (réserve)""",

                'soil_type_fr': """**Types de sol:**

- **Sols légers** sableux ou sablo-limoneux (préférés)
- **Sols bien drainés** essentiels
- **pH**: 5.5-6.5 (tolère acidité)
- Profondeur > 50cm (développement tubercules)
- Éviter absolument sols hydromorphes ou engorgés
- Tolère sols pauvres (culture rustique)""",

                'challenges_insects_fr': """**Ravageurs:**

1. **Cochenilles farineuses** (Phenacoccus manihoti)
   - Colonies blanches sur jeunes pousses
   - Déformation feuilles, arrêt croissance
   - Peut causer 50-80% pertes

2. **Acariens verts** (Mononychellus tanajoa)
   - Face inférieure feuilles
   - Décoloration, chute feuilles
   - Réduction photosynthèse

3. **Mouche blanche** (Aleurodicus, Bemisia)
   - Transmission viroses (mosaïque)
   - Fumagine (champignon noir)
   - Affaiblissement plant

4. **Termites** (diverses espèces)
   - Attaque tubercules en terre
   - Galeries, pourriture
   - Perte qualité et rendement

5. **Thrips**
   - Dégâts sur jeunes feuilles
   - Déformation, croissance ralentie""",

                'challenges_diseases_fr': """**Maladies:**

1. **Mosaïque africaine** (ACMD - African Cassava Mosaic Disease)
   - Virus transmis par mouches blanches
   - Mosaïque feuilles, nanisme sévère
   - Peut réduire rendement 80-95%
   - Maladie la plus grave du manioc

2. **Bactériose vasculaire** (Xanthomonas axonopodis)
   - Flétrissement feuilles, exsudat
   - Taches huileuses sur feuilles
   - Pourriture tubercules
   - Conditions humides

3. **Anthracnose** (Colletotrichum gloeosporioides)
   - Chancres sur tiges
   - Taches brunes feuilles
   - Mort des pousses terminales

4. **Pourriture des tubercules** (divers pathogènes)
   - Post-récolte
   - Tubercules blessés
   - Stockage > 2-3 jours

5. **Taches foliaires** (Cercospora henningsii)
   - Taches brunes avec halo
   - Défoliation
   - Affaiblissement""",

                'challenges_environmental_fr': """**Stress environnementaux:**

1. **Sécheresse prolongée:**
   - Bonne tolérance générale
   - Mais rendement réduit si > 3 mois sans pluie
   - Période 3-6 mois critique

2. **Excès d'eau / Engorgement:**
   - Très sensible
   - Pourriture racinaire
   - Asphyxie tubercules
   - Perte totale possible

3. **Sols compacts:**
   - Tubercules déformés
   - Rendement faible
   - Difficultés de récolte

4. **Carences nutritionnelles:**
   - Azote: Jaunissement feuilles
   - Potassium: Tubercules petits, faible teneur amidon
   - Phosphore: Croissance ralentie

5. **Température:**
   - Optimum: 25-29°C
   - < 15°C: Croissance arrêtée
   - Gel: Mort du plant""",

                'tips_prevention_fr': """**Mesures préventives:**

1. **Matériel de plantation sain:**
   - Boutures de plants exempts de maladies
   - Éviter zones infectées mosaïque
   - Sélection plants vigoureux (8-12 mois)
   - Tiges lignifiées, 1-2cm diamètre

2. **Variétés résistantes:**
   - Variétés résistantes mosaïque (TMS, TME)
   - Variétés résistantes bactériose
   - Variétés adaptées zone

3. **Rotation culturale:**
   - Rotation 2-3 ans minimum
   - Ne pas replanter sur même parcelle
   - Réduction pression parasitaire

4. **Préparation sol:**
   - Labour profond 30cm
   - Billonnage (améliore drainage)
   - Enfouissement matière organique

5. **Densité plantation:**
   - 10,000 plants/ha
   - Espacement: 1m x 1m ou 1m x 0.8m
   - Plantation inclinée (45°) en billons

6. **Traitement boutures:**
   - Trempage solution insecticide si cochenilles
   - Fongicide si conditions humides

7. **Gestion adventices:**
   - Désherbage précoce (2-3 premiers mois)
   - Manioc sensible compétition initiale
   - Paillage bénéfique""",

                'tips_management_fr': """**Gestion:**

1. **Contre cochenilles:**
   - Lutte biologique: Lâcher parasitoïdes (Anagyrus, Apoanagyrus)
   - Insecticide si forte infestation: Cypercal 0.5L/ha
   - Traitement boutures avant plantation

2. **Contre mosaïque:**
   - PAS DE TRAITEMENT CURATIF
   - Arracher et détruire plants malades
   - Utiliser UNIQUEMENT variétés résistantes
   - Contrôler vecteurs (mouches blanches)

3. **Contre bactériose:**
   - Détruire plants infectés
   - Utiliser boutures saines
   - Éviter blessures lors travaux
   - Désinfecter outils (eau de javel 10%)

4. **Fertilisation:**
   - NPK 15-15-15: 200-300 kg/ha (si sol pauvre)
   - Application 2-3 mois après plantation
   - Compost/fumier: 10-20 t/ha (très bénéfique)

5. **Désherbage:**
   - 2-3 sarclages premiers 4 mois
   - 1er: 1 mois, 2ème: 2-3 mois, 3ème: 4-5 mois
   - Buttage lors dernier sarclage

6. **Récolte:**
   - Couper tiges à 20-30cm du sol
   - Conserver pour boutures
   - Arrachage manuel ou charrue
   - Transformer rapidement (24-48h)""",

                'fertilizers_fr': """**Fertilisation:**

1. **Fumure de fond:**
   - NPK 10-18-18: 200-300 kg/ha
   - ou NPK 15-15-15: 200-300 kg/ha
   - Application 2-3 mois après plantation

2. **Fumure azotée:**
   - Urée: 50 kg/ha
   - Application 4-5 mois après plantation
   - Favorise développement végétatif

3. **Fumure potassique:**
   - Importante pour formation tubercules
   - KCl: 100 kg/ha
   - Améliore teneur amidon

4. **Matière organique:**
   - Compost: 10-20 t/ha
   - Fumier décomposé: 15-25 t/ha
   - Appliquer avant plantation
   - Très bénéfique (améliore structure sol)

**Besoins nutritionnels:**
- N: 80-120 kg/ha
- P₂O₅: 40-60 kg/ha
- K₂O: 120-180 kg/ha (très important)

**Remarque:** Manioc tolère sols pauvres mais répond bien à la fertilisation""",

                'pesticides_fr': """**Produits phytosanitaires:**

1. **Insecticides:**
   - **Cypercal 50 EC**: 0.5L/ha (cochenilles, acariens)
   - **Confidor 200 SL**: 0.5L/ha (mouches blanches)
   - **Décis 12.5 EC**: 0.3L/ha (thrips)

2. **Traitement boutures:**
   - Trempage dans solution insecticide (15-20 min)
   - Cypercal: 50ml/10L eau
   - Séchage avant plantation

3. **Acaricides:**
   - **Vertimec 18 EC**: 0.5L/ha (acariens verts)
   - Application face inférieure feuilles

**Remarque:**
- Lutte biologique préférable (cochenilles)
- Variétés résistantes meilleure solution (viruses)
- Traitements chimiques limités en culture manuelle""",

                'tools_fr': """**Outils:**

1. **Préparation sol:**
   - Charrue à disques
   - Billonneuse
   - Houe pour labour manuel

2. **Plantation:**
   - Plantoir
   - Machette pour couper boutures
   - Cordeau pour alignement

3. **Entretien:**
   - Houe, daba pour sarclage
   - Machette pour désherbage
   - Buttoir

4. **Récolte:**
   - Machette (couper tiges)
   - Houe pour déterrer tubercules
   - Charrue pour faciliter arrachage
   - Paniers, sacs transport

5. **Transformation:**
   - Éplucheuse mécanique
   - Râpe pour gari
   - Presse pour extraction eau
   - Séchoir solaire""",

                'innovative_inputs_fr': """**Innovations:**

1. **Variétés améliorées:**
   - **TMS 30572, TME 419** (résistantes mosaïque)
   - **TMS 97/2205** (rendement élevé)
   - **Résistantes** bactériose
   - Rendement +100-150%

2. **Lutte biologique:**
   - **Anagyrus lopezi** (parasitoïde cochenilles)
   - **Typhlodromalus aripo** (prédateur acariens)
   - Efficacité 60-90%, durable

3. **Transformation moderne:**
   - Râpe mécanique (gari, attieké)
   - Presse hydraulique
   - Séchoir solaire amélioré
   - Ajout valeur important

4. **Produits dérivés:**
   - Gari (farine fermentée)
   - Attieké (couscous manioc)
   - Farine haute qualité (HQCF)
   - Chips, croquettes

5. **Conservation tubercules:**
   - Enrobage cire (8-10 jours)
   - Stockage réfrigéré (1-2 mois)
   - Transformation immédiate (optimal)

6. **Densité améliorée:**
   - Plantation 12,500-15,000 plants/ha
   - Espacement réduit (0.8m x 0.8m)
   - Augmente rendement 20-30%

7. **Association culturale:**
   - Manioc + Maïs première année
   - Manioc + Niébé
   - Optimisation espace et revenus

8. **Mécanisation récolte:**
   - Arracheuse mécanique
   - Réduit pénibilité
   - Récolte rapide grandes surfaces""",

                'additional_notes_fr': """**Recommandations complémentaires:**

**Rendements:**
- Traditionnel: 8-12 tonnes/ha (tubercules frais)
- Amélioré: 15-25 tonnes/ha
- Potentiel variétés améliorées: 30-45 tonnes/ha
- Rendement matière sèche: 3-8 tonnes/ha

**Avantages manioc:**
- Tolérance sécheresse
- Peut rester en terre (réserve alimentaire)
- Peu exigeant en intrants
- Valorisation multiple (alimentaire, industriel)
- Culture de sécurité alimentaire

**Récolte et transformation:**
- Récolter selon besoins (si pas de maladies)
- TRANSFORMER RAPIDEMENT (24-48h max)
- Détérioration post-récolte très rapide
- Conservation tubercules frais: 2-3 jours

**Produits transformation:**
- Gari (farine fermentée, grillée)
- Attieké (couscous, spécialité ivoirienne)
- Farine HQCF (haute qualité, substitut blé)
- Amidon industriel
- Tapioca

**Commercialisation:**
- Tubercules frais: 50-100 FCFA/kg
- Gari: 200-400 FCFA/kg
- Farine HQCF: 300-500 FCFA/kg
- Demande industrielle croissante

**Nutrition:**
- Riche en glucides (amidon)
- Pauvre en protéines
- Consommer avec sources protéines
- Toxicité cyanure: Transformation élimine

**Culture commerciale:**
- Potentiel agro-industriel important
- Transformation ajoute valeur
- Filière en développement Sénégal"""
            },

            # 10. SWEET POTATOES / PATATE DOUCE
            {
                'crop_name': 'Patate douce',
                'planting_season_fr': """**Période de plantation:**

**Zone sud et côtière** (Casamance, Niayes):
- **Saison des pluies**: Juin-Août
- **Saison sèche** (avec irrigation): Octobre-Février

**Zone Niayes** (production intensive):
- **Toute l'année** avec irrigation
- Période optimale: Octobre-Mars (saison sèche)

**Préparation:**
- Boutures de tiges (lianes) 25-30cm
- 3-4 nœuds par bouture
- Plants âgés de 2-3 mois (donner boutures)

**Conditions:**
- Sol bien préparé, meuble
- Billonnage recommandé
- Irrigation si saison sèche""",

                'maturity_time_fr': """**Cycle cultural:**

- **Variétés précoces**: 3-4 mois (90-120 jours)
- **Variétés intermédiaires**: 4-5 mois
- **Variétés tardives**: 5-6 mois

**Stades:**
- Reprise boutures: 7-15 jours
- Enracinement et initiation tubercules: 1 mois
- Croissance végétative: 2-3 mois
- Grossissement tubercules: 2-4 mois
- Maturité: 3-6 mois

**Optimum récolte:**
- 4 mois (bon compromis rendement/qualité)
- Possibilité récolte échelonnée
- Récolter avant températures basses""",

                'soil_type_fr': """**Types de sol:**

- **Sols légers** sableux ou sablo-limoneux (optimaux)
- **Sols bien drainés** essentiels
- **pH**: 5.5-6.5
- Profondeur > 30cm
- **Sols Niayes** (sableux) très favorables
- Éviter sols lourds argileux et compacts (tubercules déformés)""",

                'challenges_insects_fr': """**Ravageurs:**

1. **Charançon de la patate douce** (Cylas puncticollis, C. brunneus)
   - Ravageur le plus important
   - Larves dans tubercules (galeries)
   - Tubercules amers, impropres consommation
   - Pertes 60-100% possible

2. **Criocères** (Acrothinium spp.)
   - Coléoptères sur feuilles
   - Défoliation
   - Réduit photosynthèse

3. **Altises** (Chaetocnema spp.)
   - Petits coléoptères sauteurs
   - Perforation feuilles (aspect criblé)
   - Jeunes plants sensibles

4. **Chenilles défoliatrices** (diverses)
   - Consommation feuilles
   - Réduit croissance

5. **Nématodes à galles** (Meloidogyne spp.)
   - Galles sur tubercules
   - Déformation, qualité réduite""",

                'challenges_diseases_fr': """**Maladies:**

1. **Viroses** (SPVD - Sweet Potato Virus Disease)
   - Mosaïque, déformation feuilles
   - Nanisme sévère
   - Transmission par pucerons
   - Réduction rendement 50-90%

2. **Fusariose** (Fusarium solani)
   - Pourriture sèche tubercules
   - Taches brunes, liégeuses
   - Stockage et champ

3. **Gale** (Monilochaetes infuscans)
   - Lésions liégeuses sur tubercules
   - Qualité réduite
   - Sols alcalins

4. **Pourriture molle bactérienne** (Erwinia)
   - Pourriture aqueuse tubercules
   - Post-récolte, stockage
   - Blessures porte d'entrée

5. **Alternariose** (Alternaria spp.)
   - Taches foliaires
   - Défoliation
   - Conditions humides""",

                'challenges_environmental_fr': """**Stress environnementaux:**

1. **Sécheresse:**
   - Tubercules petits, peu nombreux
   - Période 2-4 mois critique (grossissement)
   - Irrigation essentielle zones sèches

2. **Excès d'eau:**
   - Pourriture tubercules
   - Maladies fongiques
   - Drainage important

3. **Températures basses:**
   - < 15°C: Croissance ralentie
   - < 10°C: Dégâts tubercules
   - Éviter récolte période froide

4. **Sols compacts:**
   - Tubercules déformés, petits
   - Difficultés récolte

5. **Carences:**
   - Potassium: Tubercules petits
   - Azote excès: Feuillage exubérant, peu tubercules""",

                'tips_prevention_fr': """**Mesures préventives:**

1. **Matériel sain:**
   - Boutures de plants exempts viroses et charançon
   - Multiplication sur parcelle isolée
   - Sélection vigoureux plants

2. **Variétés résistantes/tolérantes:**
   - Variétés chair orange (riches vitamine A)
   - Résistantes/tolérantes viroses
   - Adaptées zone (précoces si saison courte)

3. **Rotation culturale:**
   - Rotation 2-3 ans minimum
   - Ne pas replanter patate douce même parcelle
   - Réduit charançon et nématodes

4. **Préparation sol:**
   - Labour profond 25-30cm
   - Billonnage systématique (améliore drainage, récolte)
   - Ameublissement complet

5. **Densité plantation:**
   - 30,000-40,000 plants/ha
   - Billons: 80-100cm, plants 30-40cm sur billon
   - Plantation horizontale ou inclinée

6. **Lutte contre charançon:**
   - Récolte complète (pas de tubercules résiduels)
   - Rotation stricte
   - Élimination débris végétaux
   - Paillage réduit pontes

7. **Gestion irrigation:**
   - Irrigation régulière si saison sèche
   - 25-30mm/semaine
   - Réduire fin cycle (favorise maturité)""",

                'tips_management_fr': """**Gestion:**

1. **Contre charançon:**
   - Mesures préventives essentielles (pas de curatif efficace)
   - Récolte précoce (3-4 mois) limite dégâts
   - Paillage (réduit pontes)
   - Rotation stricte

2. **Contre viroses:**
   - Utiliser boutures saines UNIQUEMENT
   - Éliminer plants malades immédiatement
   - Contrôle vecteurs (pucerons): Insecticides si nécessaire

3. **Fertilisation:**
   - NPK 10-20-20: 300-400 kg/ha (riche K)
   - Application 2-3 semaines après plantation
   - Urée 50kg/ha si croissance lente (6 semaines)

4. **Désherbage:**
   - 2-3 sarclages premiers 2 mois
   - Couverture sol après: Lianes couvrent sol
   - Buttage lors dernier sarclage

5. **Irrigation:**
   - Hebdomadaire en saison sèche
   - Réduire 2 semaines avant récolte
   - Critique période grossissement tubercules

6. **Récolte:**
   - Couper lianes 2 semaines avant
   - Récolte délicate (éviter blessures)
   - Transformer rapidement ou conserver (12-14 jours, 28-30°C, 80-90% HR)""",

                'fertilizers_fr': """**Fertilisation:**

1. **Fumure de fond:**
   - NPK 10-20-20: 300-400 kg/ha
   - ou NPK 15-15-15: 250-300 kg/ha
   - Riche en potassium (important)
   - Application 2-3 semaines après plantation

2. **Fumure azotée:**
   - Urée 46%: 50 kg/ha
   - Si croissance lente (6 semaines après plantation)
   - NE PAS EXAGÉRER azote (favorise feuillage vs tubercules)

3. **Potassium important:**
   - Essentiel formation et qualité tubercules
   - KCl: 100-150 kg/ha si sol pauvre
   - Améliore rendement et teneur sucre

4. **Matière organique:**
   - Compost: 10-15 t/ha
   - Fumier bien décomposé: 15-20 t/ha
   - Application avant billonnage
   - Améliore structure sol sableux

**Besoins NPK:**
- N: 60-80 kg/ha
- P₂O₅: 80-100 kg/ha
- K₂O: 120-150 kg/ha (très important)

**Remarque:** Patate douce modérément exigeante en azote, très exigeante en potassium""",

                'pesticides_fr': """**Produits phytosanitaires:**

1. **Insecticides végétation:**
   - **Cypercal 50 EC**: 0.4L/ha (altises, chenilles)
   - **Décis 12.5 EC**: 0.25L/ha (pucerons vecteurs)
   - **Lambda Super**: 0.3L/ha (criocères)

2. **Contre charançon:**
   - PAS de traitement chimique vraiment efficace
   - Prévention uniquement (rotation, récolte complète)

3. **Traitement post-récolte:**
   - Trempage tubercules eau chaude (47-50°C, 45 min)
   - Réduit pourriture stockage
   - Aucun insecticide homologué tubercules

4. **Nématodes:**
   - Rotation avec céréales
   - Variétés tolérantes
   - Nématicides chimiques rarement justifiés

**Remarque:** Culture nécessite peu de traitements chimiques si bonnes pratiques culturales""",

                'tools_fr': """**Outils:**

1. **Préparation sol:**
   - Charrue, motoculteur
   - Billonneuse
   - Houe pour billons manuels

2. **Plantation:**
   - Plantoir
   - Cordeau pour alignement
   - Machette pour couper boutures

3. **Entretien:**
   - Houe, daba pour sarclage
   - Buttoir
   - Système irrigation (aspersion ou goutte-à-goutte)

4. **Récolte:**
   - Fourche bêche (moins de blessures que houe)
   - Machette pour couper lianes
   - Paniers, cageots transport

5. **Post-récolte:**
   - Chambre cure (28-30°C, 80-90% HR)
   - Caisses stockage
   - Éplucheuse pour transformation""",

                'innovative_inputs_fr': """**Innovations:**

1. **Variétés à chair orange** (riches vitamine A):
   - Resisto, Irene, Ejumula
   - Nutrition améliorée (lutte carence vitamine A)
   - Rendement élevé

2. **Variétés tolérantes viroses:**
   - SPK004 (Tanzanie)
   - Rendement stable même avec viroses

3. **Lutte intégrée charançon:**
   - Phéromones (monitoring)
   - Paillage (barrière physique)
   - Récolte précoce (3-4 mois)
   - Rotation stricte

4. **Goutte-à-goutte:**
   - Économie eau 40-50%
   - Rendement +30-50%
   - Qualité tubercules améliorée

5. **Multiplication rapide:**
   - Pépinières boutures
   - Technologie aéroponie (boutures saines)
   - Production matériel certifié

6. **Transformation:**
   - Farine patate douce (substitut partiel blé)
   - Chips, croquettes
   - Purée, conserve
   - Ajout valeur important

7. **Conditioning post-récolte:**
   - Cure 28-30°C, 80-90%HR, 10-14 jours
   - Cicatrisation blessures
   - Conservation 4-6 mois

8. **Bio-fortification:**
   - Variétés très riches vitamine A (chair orange foncé)
   - Lutte malnutrition
   - Promotion santé publique""",

                'additional_notes_fr': """**Recommandations complémentaires:**

**Rendements:**
- Traditionnel: 8-12 tonnes/ha
- Amélioré: 15-25 tonnes/ha
- Potentiel irrigué: 30-40 tonnes/ha
- Niayes (conditions optimales): 20-35 tonnes/ha

**Avantages patate douce:**
- Cycle court (3-4 mois)
- Tolère sols pauvres sableux
- Nutrition excellente (chair orange: vitamine A)
- Feuilles comestibles (légume-feuilles nutritif)
- Culture de sécurité alimentaire

**Nutrition:**
- Variétés chair orange: Très riches vitamine A
- Glucides complexes (index glycémique moyen)
- Fibres, potassium
- Feuilles: Protéines, fer, calcium

**Conservation:**
- Tubercules frais: 10-14 jours (température ambiante)
- Après cure: 4-6 mois (conditions contrôlées: 13-15°C, 80-85%HR)
- NE PAS réfrigérer (< 10°C: détérioration)

**Commercialisation:**
- Tubercules frais: 150-300 FCFA/kg (saison)
- Contre-saison: 400-600 FCFA/kg
- Chips, produits transformés: Valeur ajoutée importante
- Export potentiel (variétés spécifiques)

**Filière Niayes:**
- Production intensive toute l'année
- Irrigation maîtrisée
- Marchés urbains Dakar
- Revenus importants maraîchers

**Double usage:**
- Tubercules: Consommation humaine
- Feuilles: Légume nutritif (consommer jeunes)
- Tiges (lianes): Fourrage bétail (petits ruminants)

**Transformation:**
- Farine (substitut 10-20% blé pâtisserie)
- Chips (snacks)
- Purée, conserve
- Produits infantiles (riches vitamine A)"""
            },

            # 11. TOMATOES / TOMATES
            {
                'crop_name': 'Tomate',
                'planting_season_fr': """**Période de semis/repiquage:**

**Zone Niayes** (production intensive):
- **Toute l'année** avec irrigation
- Période optimale: Octobre-Février (saison fraîche)

**Autres zones:**
- **Saison fraîche**: Novembre-Février (après hivernage)
- **Contre-saison chaude** (avec irrigation): Mars-Mai

**Pépinière:**
- Semis en pépinière: 4-6 semaines avant repiquage
- Repiquage au stade 4-5 vraies feuilles
- Plants de 15-20cm de hauteur

**Conditions:**
- Températures 18-30°C (optimales 20-25°C)
- Sol bien préparé et enrichi
- Irrigation disponible""",

                'maturity_time_fr': """**Cycle cultural:**

- **Variétés précoces**: 60-75 jours après repiquage
- **Variétés intermédiaires**: 75-90 jours
- **Variétés tardives**: 90-120 jours

**Stades:**
- Reprise transplantation: 7-10 jours
- Première floraison: 30-45 jours
- Premiers fruits: 45-60 jours
- Pleine production: 60-90 jours
- Fin récolte: 120-150 jours

**Récolte:**
- Échelonnée sur 2-3 mois
- 2-3 cueillettes par semaine
- Stades: Vert-mature, tournant, rouge (selon marché)""",

                'soil_type_fr': """**Types de sol:**

- **Sols riches** argilo-sableux ou sablo-limoneux (préférés)
- **Bien drainés** (essentiel)
- **Profonds** (> 40cm)
- pH: 6.0-7.0 (optimal)
- **Riche en matière organique**
- Sols Niayes très favorables
- Éviter sols trop argileux ou hydromorphes""",

                'challenges_insects_fr': """**Ravageurs principaux:**

1. **Mouche blanche** (Bemisia tabaci)
   - Transmission viroses (TYLCV - virus enroulement foliaire)
   - Ponction sève, affaiblissement
   - Fumagine
   - Ravageur le plus problématique

2. **Noctuelle de la tomate** (Helicoverpa armigera)
   - Chenilles perforent fruits
   - Dégâts directs importants
   - Difficile à contrôler si retard traitement

3. **Mineuse de la tomate** (Tuta absoluta)
   - Mines dans feuilles, tiges, fruits
   - Invasion récente Afrique
   - Très destructrice

4. **Pucerons** (Myzus persicae, Aphis gossypii)
   - Transmission viroses
   - Déformation jeunes pousses
   - Miellat, fumagine

5. **Acariens** (Tetranychus spp.)
   - Face inférieure feuilles
   - Jaunissement, dessèchement
   - Conditions chaudes et sèches

6. **Nématodes à galles** (Meloidogyne spp.)
   - Galles sur racines
   - Flétrissement, nanisme
   - Sols infestés""",

                'challenges_diseases_fr': """**Maladies importantes:**

1. **Virus de l'enroulement foliaire** (TYLCV)
   - Transmis par mouches blanches
   - Enroulement, jaunissement feuilles
   - Nanisme sévère
   - Pertes 80-100% si infection précoce

2. **Mildiou** (Phytophthora infestans)
   - Taches brunes feuilles et fruits
   - Très destructeur conditions humides
   - Progression rapide

3. **Flétrissement bactérien** (Ralstonia solanacearum)
   - Flétrissement brutal et irréversible
   - Pas de traitement curatif
   - Sol contaminé

4. **Flétrissement fusarien** (Fusarium oxysporum)
   - Jaunissement unilatéral
   - Flétrissement progressif
   - Variétés résistantes existent

5. **Alternariose** (Alternaria solani)
   - Taches concentriques sur feuilles
   - Affaiblit plant
   - Conditions humides

6. **Moisissure grise** (Botrytis cinerea)
   - Pourriture fruits mûrs
   - Conditions humides et fraîches
   - Pertes post-récolte

7. **Oïdium** (Leveillula taurica)
   - Poudre blanche sous feuilles
   - Conditions sèches""",

                'challenges_environmental_fr': """**Stress environnementaux:**

1. **Températures élevées:**
   - > 35°C: Avortement floral, coulure
   - Fruits petits, déformés
   - Coups de soleil sur fruits

2. **Températures basses:**
   - < 10°C: Arrêt croissance
   - < 5°C: Dégâts irréversibles
   - Floraison perturbée

3. **Sécheresse:**
   - Flétrissement
   - Nécrose apicale fruits (manque calcium)
   - Fruits petits

4. **Excès d'eau:**
   - Éclatement fruits
   - Asphyxie racinaire
   - Maladies fongiques

5. **Carences nutritionnelles:**
   - Azote: Jaunissement
   - Calcium: Nécrose apicale
   - Magnésium: Jaunissement internervaire
   - Bore: Difformités fruits""",

                'tips_prevention_fr': """**Mesures préventives:**

1. **Choix variétal:**
   - Variétés résistantes TYLCV (Tylka, etc.)
   - Résistantes fusariose (F, FF)
   - Adaptées saison et marché
   - Hybrides performants

2. **Plants sains:**
   - Pépinière protégée (filet anti-insectes)
   - Substrat désinfecté
   - Plants vigoureux pour repiquage

3. **Préparation sol:**
   - Labour profond 30-40cm
   - Apport important matière organique (20-30t/ha)
   - Désinfection sol si nématodes (solarisation)
   - Billonnage ou planches surélevées

4. **Densité plantation:**
   - Culture tuteurée: 25,000-30,000 plants/ha
   - Espacement: 1.5m x 30cm ou 1.2m x 35cm
   - Culture rampante: 15,000-20,000 plants/ha

5. **Rotation:**
   - 3-4 ans sans solanacées (tomate, piment, aubergine)
   - Rotation avec légumineuses, céréales

6. **Protection physique:**
   - Filets anti-insectes (mouches blanches)
   - Paillage plastique (nématodes, adventices)
   - Abris (saison pluies)

7. **Irrigation:**
   - Goutte-à-goutte recommandé
   - Éviter mouiller feuillage (maladies)
   - Régularité importante""",

                'tips_management_fr': """**Gestion:**

1. **Lutte contre mouches blanches:**
   - Filets anti-insectes (prévention)
   - Insecticides systémiques: Confidor 0.5L/ha
   - Pièges jaunes englués (monitoring)
   - Traiter dès apparition

2. **Contre chenilles (Helicoverpa, Tuta):**
   - Bacillus thuringiensis (Bt) - bio
   - Spinosad (Success) - bio
   - Pyréthrinoïdes si nécessaire
   - Traiter tôt le matin ou soir

3. **Protection contre mildiou:**
   - Fongicides préventifs dès floraison
   - Manèbe, Mancozèbe (préventifs)
   - Ridomil, Banko Plus (curatifs)
   - Traiter tous les 7-10 jours conditions humides

4. **Fertigation:**
   - Fractionnement apports NPK
   - Hebdomadaire via goutte-à-goutte
   - Adapter selon stades

5. **Taille et conduite:**
   - Taille à 1-2 tiges
   - Suppression gourmands
   - Tuteurage solide
   - Effeuillage modéré (aération)

6. **Entretien:**
   - Désherbage régulier ou paillage
   - Buttage après 30 jours
   - Arrosage régulier (éviter stress hydrique)

7. **Récolte:**
   - Stade selon marché (vert-mature à rouge)
   - Manipuler délicatement
   - Récolter frais le matin""",

                'fertilizers_fr': """**Fertilisation:**

1. **Fumure de fond:**
   - NPK 10-20-20: 400-600 kg/ha
   - ou NPK 15-15-15: 400 kg/ha
   - Matière organique: 20-30 t/ha (compost, fumier)
   - Application avant plantation

2. **Fumure d'entretien** (fertigation):
   - **Phase végétative** (0-40j):
     - NPK 20-20-20: 50 kg/ha/semaine
     - ou Nitrate ammonium + Potasse

   - **Phase productive** (40-120j):
     - NPK 15-5-30: 60-80 kg/ha/semaine
     - ou formules riches K

   - **Calcium** (prévention nécrose apicale):
     - Nitrate de calcium: 50 kg/ha/semaine

3. **Oligo-éléments:**
   - Bore, magnésium (pulvérisation foliaire)
   - Si carences observées

**Besoins totaux:**
- N: 150-200 kg/ha
- P₂O₅: 100-150 kg/ha
- K₂O: 200-300 kg/ha
- Ca: 100-150 kg/ha

**Remarque:** Tomate très exigeante, fertigation optimale""",

                'pesticides_fr': """**Programme phytosanitaire:**

1. **Insecticides:**
   - **Confidor 200 SL**: 0.5L/ha (mouches blanches, pucerons)
   - **Success 2.5 SC**: 0.2L/ha (Tuta, chenilles) - bio
   - **Cypercal 50 EC**: 0.5L/ha (chenilles)
   - **Vertimec 18 EC**: 0.5L/ha (acariens)
   - **Bt (Dipel)**: 0.5-1L/ha (chenilles) - bio

2. **Fongicides:**
   - **Manèbe 80 WP**: 2kg/ha (préventif mildiou)
   - **Ridomil Gold Plus**: 2.5kg/ha (mildiou curatif)
   - **Banko Plus 72 WP**: 2kg/ha (alternariose, mildiou)
   - **Score 250 EC**: 0.5L/ha (oïdium)
   - **Switch**: 1kg/ha (botrytis)

3. **Désinfection sol:**
   - Solarisation (6-8 semaines, saison chaude)
   - ou Nématicides si fort niveau nématodes

**Programme type:**
- Traitement hebdomadaire dès transplantation
- Alternance matières actives (résistance)
- Traiter tôt matin ou soir
- Mouiller bien face inférieure feuilles""",

                'tools_fr': """**Outils et équipements:**

1. **Pépinière:**
   - Plaques alvéolées (105, 150 alvéoles)
   - Substrat (tourbe + compost)
   - Ombrière ou serre
   - Filet anti-insectes

2. **Préparation sol:**
   - Motoculteur, tracteur
   - Billonneuse
   - Paillage plastique (mulch noir ou paillette)

3. **Plantation et conduite:**
   - Plantoir
   - Tuteurs (bambous, bois) 1.5-2m
   - Ficelle, clips de tuteurage
   - Cordeau

4. **Irrigation:**
   - Système goutte-à-goutte (optimal)
   - Goutteurs 2-4L/h, espacés 30cm
   - Filtre, injecteur engrais
   - Minuterie

5. **Protection:**
   - Pulvérisateur à dos 15-20L (petites surfaces)
   - Pulvérisateur à moteur (moyennes surfaces)
   - Atomiseur (grandes surfaces)
   - EPI (masque, gants, combinaison)

6. **Récolte:**
   - Cagettes plastique 10-15kg
   - Sécateurs
   - Emballages carton

7. **Post-récolte:**
   - Chambre froide (si possible)
   - Tables tri et emballage""",

                'innovative_inputs_fr': """**Innovations:**

1. **Variétés hybrides résistantes:**
   - Résistantes TYLCV + Fusariose (TY + F)
   - Mongal F1, Padma F1
   - Productivité +50-100%
   - Uniformité fruits

2. **Culture sous abri:**
   - Serre tunnel plastique
   - Protection pluies et ravageurs
   - Production contre-saison
   - Revenus accrus

3. **Fertigation automatisée:**
   - Injecteur Venturi ou pompe doseuse
   - Programmation apports
   - Optimisation nutrition
   - Rendement +30-50%

4. **Pièges et monitoring:**
   - Pièges jaunes englués (mouches blanches)
   - Pièges à phéromones (Tuta, Helicoverpa)
   - Seuils d'intervention
   - Réduction traitements

5. **Lutte biologique:**
   - Macrolophus (prédateur Tuta, mouches blanches)
   - Trichogrammes (parasitoïdes)
   - Nématodes entomopathogènes
   - Compatible agriculture biologique

6. **Mycorhizes et biostimulants:**
   - Amélioration nutrition
   - Tolérance stress
   - Rendement amélioré

7. **Greffage:**
   - Porte-greffe résistants nématodes et fusariose
   - Vigueur accrue
   - Technique en développement

8. **Agriculture de précision:**
   - Sondes tensiométriques (irrigation précise)
   - Fertigation raisonnée
   - Capteurs climat""",

                'additional_notes_fr': """**Recommandations complémentaires:**

**Rendements:**
- Plein champ traditionnel: 20-30 tonnes/ha
- Amélioré avec irrigation: 40-60 tonnes/ha
- Sous abri avec fertigation: 80-120 tonnes/ha
- Niayes (conditions optimales): 60-100 tonnes/ha

**Filière Niayes:**
- Production intensive toute l'année
- Goutte-à-goutte et fertigation
- Variétés hybrides
- Marchés urbains Dakar
- Revenus élevés (rentabilité)

**Qualité fruits:**
- Fermeté importante (transport)
- Couleur uniforme
- Calibre selon marché
- Absence défauts

**Conservation:**
- 12-15°C, 85-90% HR: 2-3 semaines
- Éviter < 10°C (dégâts froid)
- Stade vert-mature: Meilleure conservation
- Mûrissage contrôlé possible

**Commercialisation:**
- Tomate fraîche: 150-400 FCFA/kg (saison)
- Contre-saison: 500-800 FCFA/kg
- Export possible (variétés longue conservation)
- Transformation: Concentré, séchée

**Économie:**
- Culture très rentable
- Exigeante en intrants et main d'œuvre
- Risques sanitaires importants
- Accès marché essentiel

**Protection TYLCV:**
- Variétés résistantes PRIORITAIRES
- Filets anti-insectes
- Gestion mouches blanches stricte
- Virus peut détruire 100% récolte"""
            },

            # 12. ONIONS / OIGNONS
            {
                'crop_name': 'Oignon',
                'planting_season_fr': """**Période de semis/repiquage:**

**Zone Niayes** (production principale):
- **Pépinière**: Septembre-Octobre
- **Repiquage**: Novembre-Décembre
- **Récolte**: Mars-Mai

**Vallée du Fleuve Sénégal:**
- **Saison fraîche**: Octobre-Novembre (repiquage)
- **Contre-saison chaude**: Février-Mars (déconseillé: montaison)

**Préparation:**
- Semis en pépinière dense: 4-6 semaines
- Repiquage plants 15-20cm (grosseur crayon)
- Sol bien préparé, nivelé, enrichi

**Conditions:**
- Saison fraîche (températures 15-25°C)
- Photopériode longue (> 12h) pour bulbaison
- Irrigation disponible""",

                'maturity_time_fr': """**Cycle cultural:**

- **Variétés courtes**: 90-110 jours après repiquage
- **Variétés intermédiaires**: 110-130 jours
- **Variétés longues**: 130-150 jours

**Stades:**
- Reprise: 7-10 jours
- Croissance végétative: 60-90 jours
- Bulbaison (grossissement bulbe): 30-45 jours
- Maturité: 90-150 jours

**Indicateurs maturité:**
- Chute feuillage (50-80%)
- Bulbes bien formés
- Tunicules externes sèches""",

                'soil_type_fr': """**Types de sol:**

- **Sols limoneux** ou limono-sableux (optimaux)
- **Profonds, meubles, bien drainés**
- pH: 6.0-7.0 (optimal)
- **Riches en matière organique**
- Sols Niayes très favorables
- Éviter sols lourds argileux (bulbes déformés)
- Éviter sols hydromorphes""",

                'challenges_insects_fr': """**Ravageurs:**

1. **Thrips** (Thrips tabaci)
   - Principal ravageur
   - Piqûres sur feuilles (aspect argenté)
   - Vecteur de viroses
   - Réduction rendement 30-60%

2. **Mouches de l'oignon** (Delia antiqua)
   - Larves dans bulbes
   - Pourriture, destruction plants
   - Jeunes plants sensibles

3. **Vers gris** (Agrotis spp.)
   - Chenilles coupent jeunes plants
   - Nuit
   - Dégâts début culture

4. **Nématodes** (Ditylenchus dipsaci)
   - Gonflement col, distorsion feuilles
   - Bulbes mous, fissurés
   - Pertes stockage

5. **Acariens**
   - Occasionnels
   - Conditions chaudes et sèches""",

                'challenges_diseases_fr': """**Maladies:**

1. **Mildiou** (Peronospora destructor)
   - Taches grisâtres sur feuilles
   - Dessèchement feuillage
   - Conditions humides et fraîches
   - Très dommageable

2. **Alternariose** (Alternaria porri)
   - Taches concentriques violacées
   - Affaiblissement plant
   - Bulbes petits

3. **Pourriture blanche** (Sclerotium cepivorum)
   - Pourriture racinaire
   - Mycélium blanc sur bulbe
   - Sol contaminé (persistance 20 ans)

4. **Fusariose** (Fusarium oxysporum)
   - Pourriture basale bulbe
   - Flétrissement feuilles
   - Chaleur favorise

5. **Bactériose** (Xanthomonas, Erwinia)
   - Pourriture molle et humide
   - Post-récolte et stockage
   - Blessures porte d'entrée

6. **Charbon** (Urocystis cepulae)
   - Stries noires sur jeunes plants
   - Mort seedlings""",

                'challenges_environmental_fr': """**Stress environnementaux:**

1. **Températures élevées:**
   - > 30°C: Stress, montaison prématurée
   - Bulbes petits
   - Dormance rompue (conservation réduite)

2. **Photopériode courte:**
   - < 12h: Pas de bulbaison (croissance végétative)
   - Variétés adaptées zone essentielles

3. **Excès d'eau:**
   - Maladies fongiques
   - Asphyxie racinaire
   - Éclatement bulbes

4. **Stress hydrique:**
   - Bulbes petits
   - Montaison prématurée
   - Régularité irrigation critique

5. **Carences:**
   - Soufre: Essentiel (goût, conservation)
   - Azote excès: Végétation, mauvaise conservation""",

                'tips_prevention_fr': """**Mesures préventives:**

1. **Choix variétal:**
   - Variétés adaptées photopériode zone
   - **Niayes**: Violet de Galmi, Orient Express, Safari
   - **Fleuve**: Noflaye, Texas Grano
   - Semences certifiées

2. **Pépinière soignée:**
   - Substrat désinfecté
   - Filet anti-insectes (thrips)
   - Arrosage régulier
   - Traitement fongicide si nécessaire

3. **Préparation sol:**
   - Labour profond 30cm
   - Enfouissement matière organique (15-20t/ha)
   - Nivelage parfait (irrigation surface)
   - Planches 1-1.2m de large

4. **Densité:**
   - 400,000-500,000 plants/ha
   - Lignes: 15-20cm, plants 10cm sur ligne
   - 4-5 lignes par planche

5. **Rotation:**
   - 3-4 ans sans Allium (oignon, ail)
   - Réduit maladies telluriques
   - Rotation avec céréales, légumineuses

6. **Désinfection sol:**
   - Solarisation si pourriture blanche
   - 6-8 semaines saison chaude

7. **Irrigation:**
   - Goutte-à-goutte ou aspersion
   - Régularité essentielle
   - Arrêt 2-3 semaines avant récolte (conservation)""",

                'tips_management_fr': """**Gestion:**

1. **Lutte contre thrips:**
   - Filets anti-insectes pépinière
   - Insecticides dès apparition:
     - Success, Cypercal, Décis
   - Traiter tôt le matin
   - Alterner matières actives

2. **Protection contre mildiou:**
   - Fongicides préventifs dès croissance active
   - Manèbe, Banko Plus
   - Traiter tous les 7-10 jours
   - Surtout conditions humides

3. **Fertilisation fractionnée:**
   - Fond + 2-3 apports couverture
   - Réduire azote fin cycle (conservation)
   - Soufre important

4. **Irrigation raisonnée:**
   - Régulière phase végétative
   - Réduire progressivement bulbaison
   - Arrêter 2-3 semaines avant récolte
   - Améliore conservation

5. **Désherbage:**
   - Oignon peu compétitif adventices
   - 3-4 désherbages manuels
   - ou Herbicides sélectifs (Goal)

6. **Récolte:**
   - Quand 50-80% fanes couchées
   - Arracher, laisser sécher champ 2-3 jours
   - Couper fanes, calibrer
   - Stocker en lieu sec, aéré

7. **Conservation:**
   - Séchage soigné (tunicques sèches)
   - Stocker en caisses ajourées
   - Ventilation bonne
   - Température 25-30°C, HR 60-70%""",

                'fertilizers_fr': """**Fertilisation:**

1. **Fumure de fond:**
   - NPK 10-20-20: 400-600 kg/ha
   - ou NPK 15-15-15: 400 kg/ha
   - Matière organique: 15-20 t/ha (compost bien décomposé)
   - Soufre: 30-50 kg/ha (améliore conservation)

2. **Fumure d'entretien:**
   - **1er apport** (15 jours après repiquage):
     - Urée: 50 kg/ha
     - ou Nitrate ammonium: 75 kg/ha

   - **2ème apport** (30 jours):
     - Urée: 50 kg/ha

   - **3ème apport** (45-60 jours):
     - NPK 20-10-10: 100 kg/ha
     - Arrêter azote 3 semaines avant récolte

3. **Oligo-éléments:**
   - Bore: 2 kg/ha (prévention anomalies)
   - Soufre essentiel (goût, conservation)

**Besoins totaux:**
- N: 120-150 kg/ha
- P₂O₅: 80-100 kg/ha
- K₂O: 100-150 kg/ha
- S: 30-50 kg/ha

**Remarque:** Ne pas exagérer azote fin cycle (bulbes mous, mauvaise conservation)""",

                'pesticides_fr': """**Produits phytosanitaires:**

1. **Insecticides (thrips):**
   - **Success 2.5 SC**: 0.2L/ha (bio)
   - **Cypercal 50 EC**: 0.5L/ha
   - **Décis 12.5 EC**: 0.3L/ha
   - **Confidor 200 SL**: 0.5L/ha
   - Traiter hebdomadaire si forte pression

2. **Fongicides (mildiou, alternariose):**
   - **Manèbe 80 WP**: 2kg/ha (préventif)
   - **Banko Plus 72 WP**: 2kg/ha (mildiou)
   - **Ridomil Gold Plus**: 2.5kg/ha (curatif mildiou)
   - **Score 250 EC**: 0.5L/ha (alternariose)
   - Traiter tous les 7-10 jours

3. **Herbicides:**
   - **Goal 2XL**: 0.25L/ha (pré-levée)
   - Désherbage manuel préférable

**Programme:**
- Démarrer traitements 2-3 semaines après repiquage
- Alternance matières actives
- Adjuvants mouillants pour thrips""",

                'tools_fr': """**Outils:**

1. **Pépinière:**
   - Planches 1m x 10m
   - Filet anti-insectes
   - Arrosoir pommeau fin
   - Ombrière

2. **Préparation sol:**
   - Motoculteur
   - Houe rotative
   - Planche-niveleuse
   - Traçoir pour lignes

3. **Repiquage:**
   - Plantoir
   - Cordeau
   - Arrosoir

4. **Irrigation:**
   - Goutte-à-goutte (optimal)
   - ou Aspersion
   - Tuyaux, goutteurs

5. **Entretien:**
   - Houe pour sarclage
   - Pulvérisateur à dos 15-20L
   - Brouette

6. **Récolte et post-récolte:**
   - Fourche bêche
   - Sécateurs (couper fanes)
   - Caisses ajourées plastique
   - Calibreuse (si disponible)
   - Filets stockage (25-50kg)""",

                'innovative_inputs_fr': """**Innovations:**

1. **Variétés hybrides:**
   - Orient Express F1 (Niayes)
   - Safari F1
   - Rendement +30-50%
   - Uniformité, conservation améliorée

2. **Semis direct:**
   - Évite repiquage
   - Semoir de précision
   - Économie main d'œuvre
   - En développement

3. **Fertigation:**
   - Apports fractionnés optimaux
   - Via goutte-à-goutte
   - Rendement +20-30%

4. **Paillage plastique:**
   - Contrôle adventices
   - Conservation humidité
   - Bulbes plus propres

5. **Filets anti-thrips:**
   - Protection pépinière et culture
   - Réduction traitements insecticides
   - Culture biologique

6. **Stockage amélioré:**
   - Magasins ventilés
   - Caisses ajourées empilables
   - Conservation 6-8 mois
   - Réduit pertes

7. **Certification semences:**
   - Pureté variétale
   - Vigueur garantie
   - Rendement régulier

8. **Oignon déshydraté:**
   - Transformation
   - Valeur ajoutée
   - Marchés export""",

                'additional_notes_fr': """**Recommandations complémentaires:**

**Rendements:**
- Traditionnel: 15-20 tonnes/ha
- Amélioré: 30-40 tonnes/ha
- Niayes avec fertigation: 50-70 tonnes/ha
- Record: > 80 tonnes/ha

**Filière Niayes:**
- Zone de production majeure Sénégal
- Variété Violet de Galmi dominante
- Production saison fraîche (Nov-Mai)
- Approvisionnement marchés nationaux et sous-région

**Conservation:**
- Essentielle pour régulation marchés
- Séchage soigné (tunicques 2-3 épaisseurs sèches)
- Ventilation bonne
- Température 25-30°C
- HR 60-70%
- Durée: 6-8 mois (variétés adaptées)

**Commercialisation:**
- Récolte: 100-150 FCFA/kg
- Stockage et revente contre-saison: 300-600 FCFA/kg
- Calibrage important (prix)
- Export sous-région (Mali, Guinée)

**Qualité:**
- Bulbes fermes, bien formés
- Tunicques sèches, adhérentes
- Absence maladies, pourritures
- Calibre uniforme

**Économie:**
- Culture très rentable Niayes
- Forte main d'œuvre
- Intrants importants
- Stockage permet spéculation
- Risques: Prix volatils, maladies

**Nutrition:**
- Riche en quercétine (antioxydant)
- Vitamines C, B
- Composés soufrés (santé)"""
            },

            # 13-15: Remaining crops to be added in next iteration
            # Watermelon, Peppers, Okra
        ]

        # Field name mapping from data keys to model fields
        field_mapping = {
            'tips_prevention_fr': 'prevention_tips_fr',
            'tips_prevention_wo': 'prevention_tips_wo',
            'tips_prevention_en': 'prevention_tips_en',
            'tips_management_fr': 'management_tips_fr',
            'tips_management_wo': 'management_tips_wo',
            'tips_management_en': 'management_tips_en',
            'fertilizers_fr': 'recommended_fertilizers_fr',
            'fertilizers_wo': 'recommended_fertilizers_wo',
            'fertilizers_en': 'recommended_fertilizers_en',
            'pesticides_fr': 'recommended_pesticides_fr',
            'pesticides_wo': 'recommended_pesticides_wo',
            'pesticides_en': 'recommended_pesticides_en',
            'tools_fr': 'recommended_tools_fr',
            'tools_wo': 'recommended_tools_wo',
            'tools_en': 'recommended_tools_en',
            'innovative_inputs_fr': 'innovative_inputs_fr',
            'innovative_inputs_wo': 'innovative_inputs_wo',
            'innovative_inputs_en': 'innovative_inputs_en',
        }

        # Import each crop advice
        imported_count = 0
        updated_count = 0
        skipped_count = 0

        for crop_data in crop_advice_data:
            crop_name = crop_data.pop('crop_name')

            try:
                # Find the crop
                crop = Crop.objects.filter(
                    models.Q(name_fr__icontains=crop_name) |
                    models.Q(name_wo__icontains=crop_name)
                ).first()

                if not crop:
                    self.stdout.write(
                        self.style.WARNING(f'Crop not found: {crop_name} - Skipping')
                    )
                    skipped_count += 1
                    continue

                # Map field names from data keys to model fields
                mapped_data = {}
                for key, value in crop_data.items():
                    mapped_key = field_mapping.get(key, key)
                    mapped_data[mapped_key] = value

                # Check if advice already exists
                advice, created = CropAdvice.objects.update_or_create(
                    crop=crop,
                    defaults={
                        **mapped_data,
                        'created_by': author,
                        'is_active': True
                    }
                )

                if created:
                    imported_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'[OK] Created advice for: {crop.name_fr}')
                    )
                else:
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'[OK] Updated advice for: {crop.name_fr}')
                    )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error importing {crop_name}: {str(e)}')
                )
                skipped_count += 1

        # Summary
        self.stdout.write(self.style.SUCCESS(f'\n=== Import Summary ==='))
        self.stdout.write(self.style.SUCCESS(f'Created: {imported_count}'))
        self.stdout.write(self.style.SUCCESS(f'Updated: {updated_count}'))
        if skipped_count > 0:
            self.stdout.write(self.style.WARNING(f'Skipped: {skipped_count}'))
        self.stdout.write(self.style.SUCCESS(f'Total processed: {imported_count + updated_count + skipped_count}'))
        self.stdout.write(self.style.SUCCESS('\n[SUCCESS] Import completed successfully!'))
