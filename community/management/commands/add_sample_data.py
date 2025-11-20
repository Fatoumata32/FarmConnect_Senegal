from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from community.models import MarketPrice, Event
from decimal import Decimal
from datetime import date, time, timedelta

class Command(BaseCommand):
    help = 'Add sample market prices and events data'

    def handle(self, *args, **options):
        User = get_user_model()

        # Get admin user
        try:
            admin = User.objects.get(username='farmconnect_admin')
        except User.DoesNotExist:
            admin = User.objects.filter(is_superuser=True).first()

        # Add Market Prices
        market_prices = [
            {'crop_name': 'Mil', 'region': 'kaolack', 'price_per_kg': Decimal('350'), 'trend': 'up', 'percentage_change': Decimal('5.2')},
            {'crop_name': 'Mil', 'region': 'thies', 'price_per_kg': Decimal('340'), 'trend': 'stable', 'percentage_change': Decimal('0.5')},
            {'crop_name': 'Arachide', 'region': 'kaolack', 'price_per_kg': Decimal('450'), 'trend': 'up', 'percentage_change': Decimal('8.3')},
            {'crop_name': 'Arachide', 'region': 'fatick', 'price_per_kg': Decimal('440'), 'trend': 'up', 'percentage_change': Decimal('6.1')},
            {'crop_name': 'Riz', 'region': 'saint-louis', 'price_per_kg': Decimal('380'), 'trend': 'down', 'percentage_change': Decimal('-2.5')},
            {'crop_name': 'Riz', 'region': 'dakar', 'price_per_kg': Decimal('400'), 'trend': 'stable', 'percentage_change': Decimal('0.8')},
            {'crop_name': 'Mais', 'region': 'tambacounda', 'price_per_kg': Decimal('280'), 'trend': 'up', 'percentage_change': Decimal('3.7')},
            {'crop_name': 'Mais', 'region': 'kolda', 'price_per_kg': Decimal('275'), 'trend': 'stable', 'percentage_change': Decimal('1.2')},
            {'crop_name': 'Oignon', 'region': 'thies', 'price_per_kg': Decimal('500'), 'trend': 'down', 'percentage_change': Decimal('-4.5')},
            {'crop_name': 'Oignon', 'region': 'louga', 'price_per_kg': Decimal('480'), 'trend': 'down', 'percentage_change': Decimal('-3.8')},
            {'crop_name': 'Tomate', 'region': 'dakar', 'price_per_kg': Decimal('600'), 'trend': 'up', 'percentage_change': Decimal('12.0')},
            {'crop_name': 'Tomate', 'region': 'thies', 'price_per_kg': Decimal('550'), 'trend': 'up', 'percentage_change': Decimal('9.5')},
        ]

        prices_created = 0
        for price_data in market_prices:
            price, created = MarketPrice.objects.get_or_create(
                crop_name=price_data['crop_name'],
                region=price_data['region'],
                defaults={
                    'price_per_kg': price_data['price_per_kg'],
                    'trend': price_data['trend'],
                    'percentage_change': price_data['percentage_change'],
                }
            )
            if created:
                prices_created += 1

        self.stdout.write(f'Created {prices_created} market prices')

        # Add Events
        today = date.today()
        events = [
            {
                'title': 'Atelier: Techniques de Conservation des Recoltes',
                'description': 'Apprenez les meilleures pratiques pour conserver vos recoltes et reduire les pertes post-recolte. Formation pratique avec demonstration.',
                'event_type': 'workshop',
                'date': today + timedelta(days=7),
                'start_time': time(9, 0),
                'end_time': time(12, 0),
                'location': 'Centre Agricole de Kaolack',
                'region': 'kaolack',
                'organizer': 'FarmConnect Senegal',
                'contact_phone': '+221771234567',
                'contact_email': 'events@farmconnect.sn',
                'max_participants': 50,
                'is_free': True,
            },
            {
                'title': 'Formation: Irrigation Goutte-a-Goutte',
                'description': 'Formation complete sur l\'installation et la maintenance des systemes d\'irrigation goutte-a-goutte. Economisez de l\'eau et augmentez vos rendements.',
                'event_type': 'training',
                'date': today + timedelta(days=14),
                'start_time': time(8, 30),
                'end_time': time(16, 0),
                'location': 'ISRA - Institut Senegalais de Recherches Agricoles',
                'region': 'dakar',
                'organizer': 'ISRA & FarmConnect',
                'contact_phone': '+221779876543',
                'contact_email': 'formation@isra.sn',
                'max_participants': 30,
                'is_free': False,
                'registration_required': True,
            },
            {
                'title': 'Rencontre: Agriculteurs de la Region de Thies',
                'description': 'Rencontre mensuelle des agriculteurs pour echanger sur les defis et opportunites. Partage d\'experiences et networking.',
                'event_type': 'meeting',
                'date': today + timedelta(days=10),
                'start_time': time(14, 0),
                'end_time': time(17, 0),
                'location': 'Maison des Agriculteurs, Thies',
                'region': 'thies',
                'organizer': 'Association des Agriculteurs de Thies',
                'contact_phone': '+221776543210',
                'is_free': True,
            },
            {
                'title': 'Foire Agricole Regionale de Saint-Louis',
                'description': 'Grande foire agricole avec exposition de produits, materiels et semences. Venez decouvrir les innovations agricoles.',
                'event_type': 'fair',
                'date': today + timedelta(days=21),
                'start_time': time(8, 0),
                'end_time': time(18, 0),
                'location': 'Place Faidherbe, Saint-Louis',
                'region': 'saint-louis',
                'organizer': 'Chambre de Commerce de Saint-Louis',
                'contact_email': 'foire@ccsl.sn',
                'is_free': True,
            },
            {
                'title': 'Webinaire: Acces aux Financements Agricoles',
                'description': 'Decouvrez les opportunites de financement pour votre exploitation agricole. Presentation des programmes de credit et subventions disponibles.',
                'event_type': 'webinar',
                'date': today + timedelta(days=5),
                'start_time': time(15, 0),
                'end_time': time(16, 30),
                'location': 'En ligne (Zoom)',
                'region': 'online',
                'organizer': 'FarmConnect & CNCAS',
                'contact_email': 'webinar@farmconnect.sn',
                'is_free': True,
                'registration_required': True,
            },
        ]

        events_created = 0
        for event_data in events:
            event, created = Event.objects.get_or_create(
                title=event_data['title'],
                date=event_data['date'],
                defaults={
                    'description': event_data['description'],
                    'event_type': event_data['event_type'],
                    'start_time': event_data['start_time'],
                    'end_time': event_data.get('end_time'),
                    'location': event_data['location'],
                    'region': event_data['region'],
                    'organizer': event_data['organizer'],
                    'contact_phone': event_data.get('contact_phone', ''),
                    'contact_email': event_data.get('contact_email', ''),
                    'max_participants': event_data.get('max_participants'),
                    'is_free': event_data.get('is_free', True),
                    'registration_required': event_data.get('registration_required', False),
                    'created_by': admin,
                }
            )
            if created:
                events_created += 1

        self.stdout.write(f'Created {events_created} events')

        self.stdout.write(self.style.SUCCESS('Sample data added successfully!'))
