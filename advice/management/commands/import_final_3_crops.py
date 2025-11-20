"""
Management command to import final 3 Senegalese crops:
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
    help = 'Import structured agricultural advice for final 3 Senegalese crops'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting import of final 3 crops...'))

        # Get or create system user
        author, _ = User.objects.get_or_create(
            username='system_advisor',
            defaults={
                'email': 'advisor@farmconnect.sn',
                'first_name': 'System',
                'last_name': 'Advisor'
            }
        )

        # Define crop advice data for final 3 crops
        crop_advice_data = [
            # 13. WATERMELON / PASTÈQUE
            {
                'crop_name': 'Pastèque',
                'planting_season_fr': """**Période de semis/plantation:**

**Zone Niayes et Sud:**
- **Saison sèche chaude** (avec irrigation): Février-Mai
- **Contre-saison** (après hivernage): Octobre-Décembre

**Conditions:**
- Températures 25-30°C (optimales)
- Sol bien drainé et réchauffé
- Irrigation disponible

**Semis:**
- Direct en poquets ou sur billons
- 2-3 graines/poquet, éclaircir à 1 plant
- Peut aussi partir de pépinière (15-20 jours)""",

                'maturity_time_fr': """**Cycle cultural:**
- **Variétés précoces**: 65-75 jours
- **Variétés intermédiaires**: 75-90 jours
- **Variétés tardives**: 90-110 jours

**Stades:**
- Levée: 4-8 jours
- Floraison: 30-40 jours
- Formation fruits: 45-60 jours
- Maturité: 65-110 jours

**Maturité:**
- Son creux au tapotement
- Vrille séchée près du fruit
- Tache au sol jaune (pas blanche)""",

                'soil_type_fr': """**Types de sol:**
- **Sols sableux** ou sablo-limoneux (préférés)
- **Bien drainés** (essentiel)
- **Profonds** (> 40cm)
- pH: 6.0-7.0
- **Riches en matière organique**
- Sols Niayes très favorables""",

                'challenges_insects_fr': """**Ravageurs:**

1. **Mouches des fruits** (Bactrocera cucurbitae)
   - Piqûres et pontes dans fruits
   - Pourriture, asticots
   - Pertes importantes

2. **Pucerons** (Aphis gossypii)
   - Colonies sous feuilles
   - Transmission viroses
   - Miellat, fumagine

3. **Thrips**
   - Décoloration feuilles
   - Transmission viroses

4. **Nématodes à galles**
   - Galles racines
   - Flétrissement
   - Réduction rendement""",

                'challenges_diseases_fr': """**Maladies:**

1. **Fusariose** (Fusarium oxysporum)
   - Flétrissement vasculaire
   - Jaunissement unilatéral
   - Mort plant

2. **Anthracnose** (Colletotrichum lagenarium)
   - Taches brunes feuilles et fruits
   - Pourriture fruits
   - Conditions humides

3. **Oïdium** (Sphaerotheca fuliginea)
   - Poudre blanche feuilles
   - Réduction photosynthèse

4. **Virus mosaïque** (ZYMV, WMV)
   - Mosaïque, déformation feuilles
   - Fruits déformés, petits
   - Transmis par pucerons""",

                'challenges_environmental_fr': """**Stress:**

1. **Sécheresse:**
   - Fruits petits
   - Avortement fleurs
   - Flétrissement

2. **Excès d'eau:**
   - Éclatement fruits
   - Maladies fongiques
   - Pourriture racinaire

3. **Températures élevées:**
   - > 35°C: Avortement floral
   - Coups de soleil fruits

4. **Carences:**
   - Calcium: Nécrose apicale
   - Bore: Difformités""",

                'tips_prevention_fr': """**Prévention:**

1. **Variétés:**
   - Variétés adaptées (Sugar Baby, Crimson Sweet)
   - Résistantes fusariose si disponible
   - Semences certifiées

2. **Préparation sol:**
   - Labour profond 30cm
   - Billonnage recommandé
   - Matière organique 15-20 t/ha

3. **Rotation:**
   - 3 ans sans cucurbitacées
   - Réduit maladies telluriques

4. **Densité:**
   - 3,000-5,000 plants/ha
   - Espacement: 2m x 1-2m

5. **Paillage:**
   - Plastique noir ou paille
   - Réduit adventices
   - Conserve humidité""",

                'tips_management_fr': """**Gestion:**

1. **Irrigation:**
   - Goutte-à-goutte optimal
   - Régularité importante
   - Réduire à maturité

2. **Fertilisation:**
   - NPK riche en potassium
   - Apports fractionnés

3. **Taille:**
   - Tailler à 2-3 tiges
   - Limiter 2-3 fruits/plant (gros calibre)

4. **Protection:**
   - Pièges à mouches (attractifs)
   - Traiter oïdium préventivement
   - Filets anti-insectes si possible""",

                'fertilizers_fr': """**Fertilisation:**

1. **Fumure fond:**
   - NPK 10-20-20: 300 kg/ha
   - Compost: 15-20 t/ha

2. **Couverture:**
   - NPK 15-5-30: 150 kg/ha (floraison)
   - Urée: 50 kg/ha (croissance)

**Besoins:**
- N: 80-120 kg/ha
- P₂O₅: 60-80 kg/ha
- K₂O: 120-150 kg/ha""",

                'pesticides_fr': """**Phytosanitaires:**

1. **Insecticides:**
   - Success 2.5 SC: 0.2L/ha (mouches)
   - Cypercal: 0.4L/ha (pucerons)

2. **Fongicides:**
   - Soufre mouillable: 3kg/ha (oïdium)
   - Banko Plus: 2kg/ha (anthracnose)

3. **Pièges:**
   - Pièges à phéromones mouches""",

                'tools_fr': """**Outils:**

1. **Préparation:** Charrue, billonneuse
2. **Semis:** Plantoir, cordeau
3. **Irrigation:** Goutte-à-goutte
4. **Récolte:** Sécateur, brouette""",

                'innovative_inputs_fr': """**Innovations:**

1. **Variétés sans pépins** (triploïdes)
2. **Greffage** (porte-greffe résistant fusariose)
3. **Goutte-à-goutte** + fertigation
4. **Paillage plastique**
5. **Lutte intégrée** mouches (pièges + biopesticides)""",

                'additional_notes_fr': """**Rendements:**
- 20-40 tonnes/ha (traditionnel)
- 40-60 tonnes/ha (amélioré)

**Commercialisation:**
- Marchés locaux et urbains
- 100-250 FCFA/kg
- Forte demande saison chaude

**Conservation:** 2-3 semaines (frais, ventilé)"""
            },

            # 14. PEPPERS / PIMENT
            {
                'crop_name': 'Piment',
                'planting_season_fr': """**Période semis/repiquage:**

**Zone Niayes:**
- **Pépinière**: Août-Octobre
- **Repiquage**: Octobre-Décembre

**Autres zones:**
- Début saison des pluies (Mai-Juin)
- Contre-saison avec irrigation

**Pépinière:**
- 6-8 semaines avant repiquage
- Plants 15-20cm, 6-8 vraies feuilles""",

                'maturity_time_fr': """**Cycle:**
- **Variétés précoces**: 60-75 jours après repiquage
- **Intermédiaires**: 75-100 jours
- **Tardives**: 100-130 jours

**Stades:**
- Floraison: 40-50 jours
- Premiers fruits: 60-80 jours
- Récolte: Échelonnée 2-3 mois""",

                'soil_type_fr': """**Sols:**
- **Argilo-sableux** ou sablo-limoneux
- **Bien drainés**
- pH: 6.0-7.0
- **Riches** en matière organique""",

                'challenges_insects_fr': """**Ravageurs:**

1. **Thrips** (Frankliniella)
   - Décoloration feuilles/fruits
   - Transmission viroses

2. **Pucerons**
   - Colonies, transmission viroses

3. **Mouche blanche**
   - TYLCV, affaiblissement

4. **Noctuelle**
   - Chenilles perforent fruits""",

                'challenges_diseases_fr': """**Maladies:**

1. **Flétrissement bactérien** (Ralstonia)
   - Flétrissement irréversible
   - Sol contaminé

2. **Anthracnose** (Colletotrichum)
   - Taches fruits mûrs
   - Pertes post-récolte

3. **Oïdium**
   - Poudre blanche

4. **Viroses** (PVY, TYLCV)
   - Mosaïque, nanisme
   - Transmises par vecteurs""",

                'challenges_environmental_fr': """**Stress:**

1. **Températures extrêmes:**
   - < 15°C ou > 35°C: Avortement floral

2. **Excès d'eau:**
   - Pourriture racinaire

3. **Sécheresse:**
   - Chute fleurs/fruits

4. **Carences:**
   - Calcium: Nécrose apicale""",

                'tips_prevention_fr': """**Prévention:**

1. **Variétés résistantes:**
   - Hybrides résistants viroses
   - Adaptés climat local

2. **Pépinière protégée:**
   - Filet anti-insectes
   - Substrat désinfecté

3. **Rotation:** 3-4 ans sans solanacées

4. **Densité:** 25,000-30,000 plants/ha

5. **Paillage** et irrigation goutte-à-goutte""",

                'tips_management_fr': """**Gestion:**

1. **Lutte vecteurs:**
   - Traiter thrips/pucerons précocement
   - Filets anti-insectes

2. **Fongicides préventifs:**
   - Dès floraison

3. **Fertigation:**
   - Apports fractionnés NPK

4. **Tuteurage:**
   - Variétés hautes

5. **Récolte:**
   - Fruits verts ou rouges selon marché""",

                'fertilizers_fr': """**Fertilisation:**

1. **Fond:** NPK 10-20-20: 400 kg/ha
2. **Couverture:**
   - Urée: 50 kg/ha (30j)
   - NPK 15-5-30: 100 kg/ha (60j)

**Besoins:**
- N: 120-150 kg/ha
- P₂O₅: 80-100 kg/ha
- K₂O: 150-180 kg/ha""",

                'pesticides_fr': """**Phytosanitaires:**

1. **Insecticides:**
   - Confidor: 0.5L/ha (mouches blanches)
   - Success: 0.2L/ha (chenilles)
   - Cypercal: 0.4L/ha (thrips)

2. **Fongicides:**
   - Banko Plus: 2kg/ha
   - Ridomil: 2.5kg/ha""",

                'tools_fr': """**Outils:**

1. **Pépinière:** Plaques alvéolées, filet
2. **Préparation:** Motoculteur, billonneuse
3. **Irrigation:** Goutte-à-goutte
4. **Récolte:** Sécateur, cagettes""",

                'innovative_inputs_fr': """**Innovations:**

1. **Hybrides F1** résistants viroses
2. **Culture sous abri** (serres tunnels)
3. **Fertigation automatisée**
4. **Lutte biologique** (Orius, Macrolophus)
5. **Pièges colorés** monitoring""",

                'additional_notes_fr': """**Rendements:**
- 15-25 tonnes/ha (frais)
- 30-50 tonnes/ha (sous abri)

**Commercialisation:**
- Frais: 300-800 FCFA/kg
- Séché: 1,500-3,000 FCFA/kg
- Transformation: Poudre, sauce

**Nutrition:** Très riche vitamine C, capsaïcine""",
            },

            # 15. OKRA / GOMBO
            {
                'crop_name': 'Gombo',
                'planting_season_fr': """**Période de semis:**

**Hivernage:**
- **Zone nord**: Juillet-Août
- **Zone centre**: Juin-Juillet
- **Zone sud**: Mai-Juillet

**Contre-saison** (avec irrigation):
- Février-Avril
- Septembre-Octobre

**Conditions:**
- Températures > 20°C
- Sol réchauffé et humide
- Semis direct en poquets""",

                'maturity_time_fr': """**Cycle:**
- **Variétés précoces**: 50-60 jours
- **Intermédiaires**: 60-75 jours
- **Tardives**: 75-90 jours

**Stades:**
- Levée: 5-8 jours
- Floraison: 40-50 jours
- Première récolte: 50-60 jours
- Récolte: Échelonnée 2-3 mois

**Récolte:** Gousses tendres (8-12cm)""",

                'soil_type_fr': """**Sols:**
- **Tous types** tolérés
- **Préférence:** Sableux ou sablo-limoneux
- **Bien drainés**
- pH: 6.0-7.5
- Tolère sols pauvres""",

                'challenges_insects_fr': """**Ravageurs:**

1. **Pucerons** (Aphis gossypii)
   - Colonies sous feuilles
   - Déformation jeunes pousses

2. **Altises**
   - Perforation feuilles
   - Jeunes plants sensibles

3. **Jassides**
   - Jaunissement, enroulement feuilles

4. **Foreurs fruits** (Helicoverpa)
   - Chenilles dans gousses
   - Dégâts directs""",

                'challenges_diseases_fr': """**Maladies:**

1. **Fusariose** (Fusarium oxysporum)
   - Flétrissement, jaunissement

2. **Cercosporiose** (Cercospora)
   - Taches foliaires brunes

3. **Virus mosaïque**
   - Mosaïque, déformation
   - Transmis par pucerons

4. **Pourriture racinaire**
   - Excès d'eau""",

                'challenges_environmental_fr': """**Stress:**

1. **Températures basses:**
   - < 15°C: Croissance ralentie

2. **Sécheresse:**
   - Gousses fibreuses, dures
   - Réduction rendement

3. **Excès d'eau:**
   - Pourriture racinaire

4. **Sols compacts:**
   - Mauvais développement""",

                'tips_prevention_fr': """**Prévention:**

1. **Variétés:**
   - Variétés locales adaptées
   - Clemson Spineless (populaire)

2. **Préparation sol:**
   - Labour léger suffisant
   - Billonnage si humide

3. **Densité:**
   - 40,000-60,000 plants/ha
   - Espacement: 60cm x 30cm

4. **Rotation:**
   - Rotation avec céréales/légumineuses

5. **Traitement semences:**
   - Fongicide si conditions humides""",

                'tips_management_fr': """**Gestion:**

1. **Lutte pucerons:**
   - Traiter dès apparition
   - Cypercal, Décis

2. **Fertilisation:**
   - NPK modérée
   - Compost bénéfique

3. **Irrigation:**
   - Régulière période floraison
   - Éviter stress hydrique

4. **Désherbage:**
   - 2-3 sarclages
   - Important jeunes plants

5. **Récolte:**
   - Tous les 2-3 jours
   - Gousses tendres (8-12cm)
   - Ne pas laisser durcir""",

                'fertilizers_fr': """**Fertilisation:**

1. **Fond:**
   - NPK 15-15-15: 150-200 kg/ha
   - Compost: 10-15 t/ha

2. **Couverture:**
   - Urée: 50 kg/ha (30 jours)

**Besoins:**
- N: 60-80 kg/ha
- P₂O₅: 40-60 kg/ha
- K₂O: 60-80 kg/ha

**Remarque:** Gombo peu exigeant""",

                'pesticides_fr': """**Phytosanitaires:**

1. **Insecticides:**
   - Cypercal: 0.3L/ha (pucerons)
   - Décis: 0.25L/ha (jassides)
   - Bt (Dipel): 0.5L/ha (chenilles) - bio

2. **Fongicides:**
   - Banko Plus: 2kg/ha (cercosporiose)
   - Rarement nécessaire

**Remarque:** Gombo nécessite peu de traitements""",

                'tools_fr': """**Outils:**

1. **Préparation:** Charrue légère, houe
2. **Semis:** Plantoir, cordeau
3. **Entretien:** Houe, sarcleur
4. **Récolte:** Panier, sacs
5. **Irrigation:** Arrosoir ou goutte-à-goutte""",

                'innovative_inputs_fr': """**Innovations:**

1. **Variétés améliorées:**
   - Sans épines (Spineless)
   - Précoces (50 jours)

2. **Micro-irrigation:**
   - Goutte-à-goutte
   - Économie eau

3. **Paillage:**
   - Conservation humidité
   - Réduction adventices

4. **Association culturale:**
   - Gombo + Niébé
   - Gombo + Maïs

5. **Séchage solaire:**
   - Conservation gousses
   - Valeur ajoutée""",

                'additional_notes_fr': """**Rendements:**
- 8-12 tonnes/ha (frais)
- Irrigué: 15-20 tonnes/ha

**Avantages:**
- Culture rustique, peu exigeante
- Cycle court (récolte rapide)
- Récolte échelonnée
- Tolère chaleur et sols pauvres

**Nutrition:**
- Riche fibres, vitamines A, C
- Mucilage bénéfique digestion

**Commercialisation:**
- Frais: 200-500 FCFA/kg
- Séché: 800-1,500 FCFA/kg
- Forte demande marchés urbains
- Consommation locale importante

**Usages:**
- Consommation fraîche (sauces)
- Séchage (conservation)
- Feuilles comestibles (légume-feuilles)
- Graines: Huile, fourrage"""
            },
        ]

        # Field name mapping
        field_mapping = {
            'tips_prevention_fr': 'prevention_tips_fr',
            'tips_management_fr': 'management_tips_fr',
            'fertilizers_fr': 'recommended_fertilizers_fr',
            'pesticides_fr': 'recommended_pesticides_fr',
            'tools_fr': 'recommended_tools_fr',
            'innovative_inputs_fr': 'innovative_inputs_fr',
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

                # Map field names
                mapped_data = {}
                for key, value in crop_data.items():
                    mapped_key = field_mapping.get(key, key)
                    mapped_data[mapped_key] = value

                # Create or update
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
        self.stdout.write(self.style.SUCCESS('\n[SUCCESS] Import completed - All 15 crops done!'))
