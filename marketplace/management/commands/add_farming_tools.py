from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from marketplace.models import Product
from decimal import Decimal

class Command(BaseCommand):
    help = 'Add 15 different useful farming tools to the marketplace'

    def handle(self, *args, **options):
        User = get_user_model()

        # Get or create a default seller
        seller, created = User.objects.get_or_create(
            username='farmconnect_store',
            defaults={
                'email': 'store@farmconnect.sn',
                'first_name': 'FarmConnect',
                'last_name': 'Store'
            }
        )

        if created:
            seller.set_password('farmconnect2024')
            seller.save()
            self.stdout.write(self.style.SUCCESS('Created default seller: farmconnect_store'))

        # 15 useful farming tools for Senegalese agriculture
        farming_tools = [
            {
                'name': 'Houe Traditionnelle (Hilaire)',
                'description': 'Houe traditionnelle sénégalaise pour le sarclage et le désherbage. Manche en bois dur et lame en acier trempé. Idéale pour le travail du sol dans les cultures de mil, maïs et arachide.',
                'price': Decimal('8500.00'),
                'category': 'Outils Manuels',
                'quantity_available': 50,
            },
            {
                'name': 'Machette Agricole',
                'description': 'Machette robuste pour le défrichage et la coupe de végétation. Lame en acier carbone de 50cm avec manche ergonomique en bois. Parfaite pour préparer les champs et tailler les arbres fruitiers.',
                'price': Decimal('6500.00'),
                'category': 'Outils de Coupe',
                'quantity_available': 75,
            },
            {
                'name': 'Pulvérisateur à Dos 16L',
                'description': 'Pulvérisateur manuel à dos de 16 litres pour l\'application de pesticides et engrais foliaires. Pompe à pression avec buse réglable. Bretelles rembourrées pour un confort optimal.',
                'price': Decimal('35000.00'),
                'category': 'Équipement de Traitement',
                'quantity_available': 30,
            },
            {
                'name': 'Semoir Manuel à Main',
                'description': 'Semoir manuel pour le semis précis des graines. Permet un espacement régulier et une profondeur uniforme. Adapté pour les semences de légumes, céréales et arachides.',
                'price': Decimal('12000.00'),
                'category': 'Équipement de Semis',
                'quantity_available': 40,
            },
            {
                'name': 'Arrosoir en Zinc 10L',
                'description': 'Arrosoir traditionnel en zinc galvanisé de 10 litres. Pomme d\'arrosage amovible pour un arrosage fin ou direct. Robuste et durable pour un usage quotidien au jardin.',
                'price': Decimal('7500.00'),
                'category': 'Irrigation',
                'quantity_available': 60,
            },
            {
                'name': 'Binette à Long Manche',
                'description': 'Binette avec manche en bois de 150cm pour travailler debout. Lame affûtée en acier pour sarcler entre les rangs de cultures sans se baisser. Réduit la fatigue du dos.',
                'price': Decimal('9000.00'),
                'category': 'Outils Manuels',
                'quantity_available': 45,
            },
            {
                'name': 'Brouette de Chantier 80L',
                'description': 'Brouette robuste de 80 litres avec roue pneumatique. Cuve en acier galvanisé et châssis renforcé. Idéale pour transporter le fumier, la terre et les récoltes.',
                'price': Decimal('45000.00'),
                'category': 'Transport',
                'quantity_available': 20,
            },
            {
                'name': 'Râteau à Dents Métalliques',
                'description': 'Râteau avec 14 dents en acier pour niveler le sol et ramasser les débris. Manche en bois dur de 140cm. Indispensable pour la préparation des planches de culture.',
                'price': Decimal('6000.00'),
                'category': 'Outils Manuels',
                'quantity_available': 55,
            },
            {
                'name': 'Sécateur Professionnel',
                'description': 'Sécateur à lames franches en acier trempé pour la taille des arbres fruitiers (manguiers, agrumes, papayers). Poignées antidérapantes avec système de verrouillage de sécurité.',
                'price': Decimal('15000.00'),
                'category': 'Outils de Coupe',
                'quantity_available': 35,
            },
            {
                'name': 'Fourche à Bêcher 4 Dents',
                'description': 'Fourche à bêcher avec 4 dents plates en acier forgé. Parfaite pour retourner le sol, incorporer le compost et récolter les tubercules sans les abîmer.',
                'price': Decimal('11000.00'),
                'category': 'Outils Manuels',
                'quantity_available': 40,
            },
            {
                'name': 'Tuyau d\'Arrosage 25m',
                'description': 'Tuyau d\'arrosage flexible de 25 mètres en PVC renforcé. Résistant aux UV et à la pression. Livré avec raccords et pistolet d\'arrosage multi-jets.',
                'price': Decimal('28000.00'),
                'category': 'Irrigation',
                'quantity_available': 25,
            },
            {
                'name': 'Plantoir à Bulbes',
                'description': 'Plantoir en acier inoxydable avec graduation de profondeur. Idéal pour planter oignons, ail et autres bulbes à la bonne profondeur. Poignée en bois confortable.',
                'price': Decimal('4500.00'),
                'category': 'Équipement de Semis',
                'quantity_available': 65,
            },
            {
                'name': 'Filet Anti-Oiseaux 4x10m',
                'description': 'Filet de protection contre les oiseaux, dimensions 4x10 mètres. Mailles fines en polyéthylène résistant aux UV. Protège les cultures de riz, mil et fruits.',
                'price': Decimal('18000.00'),
                'category': 'Protection des Cultures',
                'quantity_available': 30,
            },
            {
                'name': 'Pelle Ronde en Acier',
                'description': 'Pelle à tête ronde en acier trempé pour creuser et déplacer la terre. Manche en fibre de verre ultra-résistant de 120cm. Légère et durable.',
                'price': Decimal('13500.00'),
                'category': 'Outils Manuels',
                'quantity_available': 50,
            },
            {
                'name': 'Kit Goutte-à-Goutte 100m²',
                'description': 'Système d\'irrigation goutte-à-goutte pour 100m² de culture. Comprend tuyaux, goutteurs, raccords et filtre. Économise jusqu\'à 70% d\'eau par rapport à l\'arrosage traditionnel.',
                'price': Decimal('65000.00'),
                'category': 'Irrigation',
                'quantity_available': 15,
            },
        ]

        tools_created = 0
        for tool_data in farming_tools:
            product, created = Product.objects.get_or_create(
                name=tool_data['name'],
                defaults={
                    'description': tool_data['description'],
                    'price': tool_data['price'],
                    'seller': seller,
                    'category': tool_data['category'],
                    'quantity_available': tool_data['quantity_available'],
                    'is_available': True,
                }
            )
            if created:
                tools_created += 1
                self.stdout.write(f"Created: {product.name}")
            else:
                self.stdout.write(f"Already exists: {product.name}")

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully added {tools_created} farming tools to the marketplace!')
        )
