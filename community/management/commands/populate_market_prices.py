from django.core.management.base import BaseCommand
from community.models import MarketPrice
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Populate market prices with sample data for Senegalese crops'

    def handle(self, *args, **kwargs):
        # Clear existing data
        MarketPrice.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing market prices'))

        # Common Senegalese crops with base prices (FCFA per kg)
        crops_data = {
            'Mil': 250,
            'Arachide': 350,
            'Niébé': 400,
            'Maïs': 200,
            'Riz': 450,
            'Sorgho': 220,
            'Manioc': 180,
            'Patate douce': 160,
            'Tomate': 300,
            'Oignon': 350,
            'Gombo': 250,
            'Aubergine': 280,
            'Piment': 500,
            'Bissap': 600,
        }

        regions = [
            'dakar', 'thies', 'kaolack', 'saint-louis', 'ziguinchor',
            'tambacounda', 'kolda', 'matam', 'louga', 'fatick',
            'diourbel', 'kaffrine', 'kedougou', 'sedhiou'
        ]

        trends = ['up', 'down', 'stable']

        count = 0

        for crop, base_price in crops_data.items():
            # Create price for 3-5 random regions per crop
            selected_regions = random.sample(regions, k=random.randint(3, 5))

            for region in selected_regions:
                # Add random variation to base price (±20%)
                variation = random.uniform(-0.2, 0.2)
                price = Decimal(str(round(base_price * (1 + variation), 2)))

                # Random trend
                trend = random.choice(trends)

                # Percentage change based on trend
                if trend == 'up':
                    percentage = Decimal(str(round(random.uniform(2, 15), 2)))
                elif trend == 'down':
                    percentage = Decimal(str(round(random.uniform(-15, -2), 2)))
                else:
                    percentage = Decimal(str(round(random.uniform(-2, 2), 2)))

                MarketPrice.objects.create(
                    crop_name=crop,
                    region=region,
                    price_per_kg=price,
                    trend=trend,
                    percentage_change=percentage
                )
                count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {count} market price entries for {len(crops_data)} crops across multiple regions'
            )
        )
