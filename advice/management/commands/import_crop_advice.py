"""
Management command to import crop advice from the provided data
Usage: python manage.py import_crop_advice
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from advice.models import AdviceEntry
from crops.models import Crop
from farmconnect_app.models import User


class Command(BaseCommand):
    help = 'Import agricultural advice for various crops'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Starting advice import...'))

        # Get or create admin user for authorship
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            self.stdout.write(self.style.ERROR('No admin user found. Creating advice without author.'))

        # Agricultural advice data from the table
        advice_data = [
            # PEANUT
            {
                'crop_name': 'Arachide',
                'title_fr': 'Culture de l\'arachide - Guide complet',
                'category': 'general',
                'stage': 'general',
                'severity': 'low',
                'short_description_fr': 'Guide complet pour la culture de l\'arachide au Sénégal',
                'content_fr': '''L'arachide est une culture importante au Sénégal nécessitant des conditions spécifiques pour un bon rendement.

**Sol optimal:** Sol bien drainé, léger et sablonneux.

**Plantation:** Rotation des cultures recommandée pour éviter l'épuisement du sol et les maladies. Éviter de planter pendant les fortes pluies.

**Irrigation:** Arrosage modéré et régulier. Utiliser l'inoculation pour favoriser la fixation de l'azote.

**Maladies:** Surveiller régulièrement les signes de maladies fongiques et bactériennes.

**Récolte:** Récolter après maturation complète des gousses, généralement 90-120 jours après la plantation.''',
                'action_steps_fr': '''Préparer un sol bien drainé
Effectuer une rotation des cultures
Planter en début de saison des pluies
Arroser modérément
Surveiller les maladies
Récolter au bon moment
Sécher correctement avant stockage''',
                'tags': 'arachide,rotation,sol drainé,pluies,inoculation',
                'priority': 80
            },

            # TOMATO
            {
                'crop_name': 'Tomate',
                'title_fr': 'Culture de la tomate - Techniques optimales',
                'category': 'general',
                'stage': 'general',
                'severity': 'low',
                'short_description_fr': 'Guide pour réussir la culture de tomate avec gestion de l\'eau et des maladies',
                'content_fr': '''La tomate est une culture maraîchère importante nécessitant une attention particulière à l'irrigation et aux maladies.

**Sol optimal:** Sol limoneux, riche en matière organique avec bon drainage.

**Tuteurage:** Utiliser des tuteurs pour soutenir les plants et faciliter la circulation d'air.

**Irrigation:** Arrosage régulier et profond. Éviter l'arrosage excessif qui favorise les maladies.

**Fertilisation:** Apporter des engrais azotés régulièrement pour une bonne croissance.

**Protection:** Contrôler rapidement les maladies fongiques et bactériennes.

**Récolte:** Cueillir les fruits à maturité, au bon stade de coloration.''',
                'action_steps_fr': '''Préparer un sol riche et bien drainé
Installer des tuteurs solides
Arroser régulièrement sans excès
Appliquer des engrais azotés
Surveiller les maladies
Traiter rapidement si nécessaire
Récolter à maturité optimale''',
                'tags': 'tomate,tuteurage,irrigation,azote,maladies,humidité',
                'priority': 85
            },

            # TOMATO - Disease Control
            {
                'crop_name': 'Tomate',
                'title_fr': 'Contrôle des maladies sur tomate',
                'category': 'disease',
                'stage': 'growth',
                'severity': 'high',
                'short_description_fr': 'Prévention et traitement des maladies fongiques et bactériennes sur tomate',
                'content_fr': '''Les tomates sont particulièrement sensibles aux maladies fongiques et bactériennes, surtout en conditions d'humidité élevée.

**Maladies courantes:**
- Mildiou (temps humide)
- Alternariose (taches brunes)
- Flétrissement bactérien

**Conditions favorables aux maladies:**
- Humidité excessive (>80%)
- Mauvaise circulation d'air
- Arrosage par aspersion
- Densité de plantation trop élevée

**Prévention:**
- Éviter l'excès d'humidité
- Espacer correctement les plants
- Arroser au pied des plants
- Éliminer les feuilles malades

**Traitement:**
- Fongicides cuivrés pour le mildiou
- Rotation des cultures
- Utiliser des variétés résistantes''',
                'action_steps_fr': '''Inspecter régulièrement les plants
Espacer les plants (60-80 cm)
Arroser au pied uniquement
Éliminer les feuilles atteintes
Appliquer des fongicides préventifs
Améliorer la circulation d'air
Éviter de travailler sur plants mouillés''',
                'tags': 'tomate,maladies,mildiou,humidité,fongicide,prévention',
                'priority': 90
            },

            # RICE
            {
                'crop_name': 'Riz',
                'title_fr': 'Riziculture - Gestion de l\'eau et du sol',
                'category': 'general',
                'stage': 'general',
                'severity': 'low',
                'short_description_fr': 'Guide pour la culture du riz avec gestion optimale de l\'eau',
                'content_fr': '''Le riz nécessite une gestion particulière de l'eau et du sol pour des rendements optimaux.

**Sol optimal:** Sol argileux ou limoneux avec bonne capacité de rétention d'eau.

**Gestion de l'eau:**
- Maintenir 5-10 cm d'eau pendant la croissance
- Drainage avant la récolte
- Plantation au début de la saison des pluies

**Fertilisation:** Utiliser des engrais équilibrés NPK selon l'analyse du sol.

**Désherbage:** Gérer les adventices qui concurrencent le riz pour les nutriments.

**Récolte:** Récolter quand 80-90% des grains sont mûrs (grains dorés).

**Stockage:** Sécher à 13-14% d'humidité avant stockage.''',
                'action_steps_fr': '''Préparer le sol argileux
Planter au début des pluies
Maintenir niveau d'eau constant
Fertiliser selon analyse sol
Désherber régulièrement
Drainer avant récolte
Récolter au bon stade
Sécher correctement''',
                'tags': 'riz,eau,irrigation,argile,saison pluies,drainage',
                'priority': 85
            },

            # HONEY BEE
            {
                'crop_name': 'Miel',
                'title_fr': 'Apiculture - Protection des ruches',
                'category': 'general',
                'stage': 'general',
                'severity': 'medium',
                'short_description_fr': 'Guide pour la gestion des ruches et protection contre les conditions climatiques',
                'content_fr': '''L'apiculture nécessite une attention particulière aux conditions climatiques et à la protection des ruches.

**Emplacement:** Choisir un site protégé du vent fort et des inondations.

**Protection climatique:**
- Ombrage pendant les fortes chaleurs
- Protection contre les pluies torrentielles
- Éviter les zones d'inondation

**Gestion des ruches:**
- Inspection régulière
- Contrôle des parasites (varroa)
- Alimentation de complément si nécessaire

**Récolte du miel:**
- Récolter pendant la saison sèche
- Éviter les périodes de chaleur extrême
- Manipuler avec précaution

**Sécurité:** Porter équipement de protection complet.''',
                'action_steps_fr': '''Choisir emplacement protégé
Installer ombrage si nécessaire
Protéger contre vents forts
Surélever ruches contre inondations
Inspecter régulièrement
Contrôler parasites
Récolter au bon moment
Porter équipement protection''',
                'tags': 'miel,apiculture,ruches,climat,protection,récolte',
                'priority': 70
            },

            # MAIZE
            {
                'crop_name': 'Maïs',
                'title_fr': 'Culture du maïs - Fertilisation et irrigation',
                'category': 'general',
                'stage': 'general',
                'severity': 'low',
                'short_description_fr': 'Guide pour la culture du maïs avec gestion de l\'eau et fertilisation',
                'content_fr': '''Le maïs est une culture céréalière importante nécessitant chaleur et eau adéquate.

**Sol optimal:** Sol bien drainé, profond et fertile.

**Conditions climatiques:**
- Température optimale: 20-30°C
- Pluviométrie: 500-800 mm bien répartie
- Éviter les températures extrêmes (<10°C ou >35°C)

**Plantation:** Planter au début de la saison des pluies pour assurer germination.

**Irrigation:** Arrosage régulier, surtout pendant la floraison et formation des épis.

**Fertilisation:**
- Appliquer engrais NPK au semis
- Apport azoté en couverture à 30-40 jours

**Maladies:** Contrôler la rouille, le charbon et les foreurs de tiges.

**Récolte:** Récolter quand les grains sont durs et secs (25-30% humidité).''',
                'action_steps_fr': '''Préparer sol profond et fertile
Planter au début saison pluies
Arroser régulièrement
Fertiliser au semis et en couverture
Contrôler maladies et ravageurs
Butter les plants
Récolter au bon stade
Sécher avant stockage''',
                'tags': 'maïs,chaleur,pluies,fertilisation,irrigation,température',
                'priority': 85
            },

            # WEATHER-BASED ADVICE

            # High Temperature - Irrigation
            {
                'crop_name': 'Tomate',
                'title_fr': 'Irrigation en période de forte chaleur',
                'category': 'watering',
                'stage': 'growth',
                'severity': 'high',
                'short_description_fr': 'Comment gérer l\'irrigation des tomates pendant les périodes de chaleur intense',
                'content_fr': '''En période de forte chaleur (>35°C), les tomates nécessitent une attention particulière à l'irrigation pour éviter le stress hydrique.

**Symptômes de stress:**
- Flétrissement des feuilles en journée
- Chute des fleurs
- Petits fruits déformés

**Stratégies d'irrigation:**
- Arroser tôt le matin (6h-8h)
- Arroser tard le soir (18h-20h)
- Augmenter la fréquence mais pas la quantité
- Pailler le sol pour réduire évaporation

**Quantité d'eau:**
- 3-5 litres par plant/jour en forte chaleur
- Ajuster selon taille des plants

**Signes d'excès:** Feuilles jaunes, pourriture des racines.''',
                'action_steps_fr': '''Arroser tôt le matin ou tard le soir
Augmenter fréquence d'arrosage
Pailler le sol (10-15 cm)
Vérifier humidité du sol régulièrement
Ombrager si possible (voile d'ombrage 30%)
Éviter arrosage en pleine journée
Surveiller signes de stress''',
                'tags': 'chaleur,irrigation,tomate,stress hydrique,paillage,température élevée',
                'priority': 95
            },

            # Rain - Disease Prevention
            {
                'crop_name': 'Tomate',
                'title_fr': 'Protection contre les maladies en saison des pluies',
                'category': 'disease',
                'stage': 'growth',
                'severity': 'critical',
                'short_description_fr': 'Prévention des maladies fongiques pendant les périodes pluvieuses',
                'content_fr': '''Les périodes de pluie créent des conditions idéales pour le développement des maladies fongiques sur tomate.

**Risques principaux:**
- Mildiou (Phytophthora infestans)
- Alternariose
- Pourriture des fruits
- Septoriose

**Conditions favorables:**
- Humidité >80%
- Températures 20-25°C
- Feuillage mouillé >6 heures

**Prévention:**
- Application préventive de bouillie bordelaise
- Espacer les plants pour aération
- Effeuiller la base des plants
- Drainer l'excès d'eau

**Traitement curatif:**
- Fongicides à base de cuivre
- Éliminer parties atteintes
- Améliorer drainage''',
                'action_steps_fr': '''Appliquer bouillie bordelaise préventive
Espacer plants (80 cm minimum)
Effeuiller base des plants
Améliorer drainage du sol
Tuteurer pour éviter contact sol
Éliminer feuilles malades immédiatement
Ne pas travailler sur plants mouillés
Pulvériser fongicide après chaque pluie''',
                'tags': 'pluie,maladie,mildiou,fongicide,prévention,humidité,tomate',
                'priority': 98
            },

            # Low Humidity - Drought
            {
                'crop_name': 'Arachide',
                'title_fr': 'Gestion de la sécheresse sur arachide',
                'category': 'watering',
                'stage': 'flowering',
                'severity': 'high',
                'short_description_fr': 'Techniques pour maintenir la production d\'arachide en conditions sèches',
                'content_fr': '''L'arachide peut tolérer la sécheresse mais nécessite de l'eau pendant certaines phases critiques.

**Phases critiques:**
- Germination (0-15 jours)
- Floraison (40-60 jours)
- Formation des gousses (60-90 jours)

**Symptômes de stress:**
- Feuilles qui s'enroulent
- Floraison réduite
- Gousses mal remplies

**Stratégies:**
- Arrosage ciblé aux phases critiques
- Paillage pour conserver l'humidité
- Variétés tolérantes à la sécheresse
- Semis précoce pour profiter des pluies

**Irrigation d'appoint:**
- 25-30 mm pendant floraison
- 30-40 mm formation gousses
- Arrêter 2 semaines avant récolte''',
                'action_steps_fr': '''Identifier phase de croissance
Arroser en priorité floraison
Pailler entre les rangs
Biner léger pour casser croûte
Arroser tôt matin ou soir
Surveiller enroulement feuilles
Réduire densité si sécheresse sévère
Choisir variétés résistantes''',
                'tags': 'sécheresse,arachide,irrigation,stress hydrique,paillage,humidité faible',
                'priority': 92
            },

            # High Wind - Protection
            {
                'crop_name': 'Maïs',
                'title_fr': 'Protection du maïs contre les vents forts',
                'category': 'weather',
                'stage': 'growth',
                'severity': 'medium',
                'short_description_fr': 'Mesures de protection contre les dégâts causés par les vents violents',
                'content_fr': '''Les vents forts peuvent causer des dommages importants aux cultures de maïs, notamment la verse.

**Risques:**
- Verse (plants couchés)
- Brisure des tiges
- Dommages aux feuilles
- Pollinisation réduite
- Verse racinaire

**Prévention:**
- Buttage renforcé des plants
- Choix de variétés résistantes à la verse
- Orientation des rangs perpendiculaire aux vents dominants
- Haies brise-vent

**Actions après vents forts:**
- Redresser plants si possible (dans les 24h)
- Butter à nouveau
- Évaluer dommages
- Fertilisation azotée pour récupération

**Période critique:** 30-60 jours après semis (plants hauts mais enracinement incomplet).''',
                'action_steps_fr': '''Butter solidement les plants
Planter haies brise-vent si possible
Orienter rangs perpendiculairement au vent
Choisir variétés résistantes verse
Renforcer buttage avant vents annoncés
Redresser plants tombés rapidement
Fertiliser pour récupération
Évaluer pertes et ajuster densité''',
                'tags': 'vent,maïs,verse,protection,buttage,haie brise-vent',
                'priority': 85
            },
        ]

        # Import the advice
        created_count = 0
        updated_count = 0
        error_count = 0

        with transaction.atomic():
            for advice_item in advice_data:
                try:
                    # Get crop by name
                    crop_name = advice_item.pop('crop_name')
                    crop = Crop.objects.filter(name_fr__icontains=crop_name).first()

                    if not crop:
                        self.stdout.write(
                            self.style.WARNING(f'Crop "{crop_name}" not found, skipping advice: {advice_item["title_fr"]}')
                        )
                        error_count += 1
                        continue

                    # Check if advice already exists
                    existing = AdviceEntry.objects.filter(
                        crop=crop,
                        title_fr=advice_item['title_fr']
                    ).first()

                    if existing:
                        # Update existing
                        for key, value in advice_item.items():
                            setattr(existing, key, value)
                        existing.author = admin_user
                        existing.save()
                        updated_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'Updated: {advice_item["title_fr"]}')
                        )
                    else:
                        # Create new
                        advice_entry = AdviceEntry.objects.create(
                            crop=crop,
                            author=admin_user,
                            **advice_item
                        )
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'Created: {advice_item["title_fr"]}')
                        )

                except Exception as e:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f'Error importing advice "{advice_item.get("title_fr", "Unknown")}": {str(e)}')
                    )

        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'✅ Import completed!'))
        self.stdout.write(f'  Created: {created_count}')
        self.stdout.write(f'  Updated: {updated_count}')
        self.stdout.write(f'  Errors: {error_count}')
        self.stdout.write(f'  Total processed: {len(advice_data)}')
        self.stdout.write('='*50)
