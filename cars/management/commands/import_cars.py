from django.core.management.base import BaseCommand
import pandas as pd
from cars.models import Car
from datetime import datetime

class Command(BaseCommand):
    help = 'Import cars from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def parse_date(self, date_str):
        if pd.isna(date_str):
            return None
        try:
            # Convert numeric date (e.g., 20250107) to datetime
            return datetime.strptime(str(int(date_str)), '%Y%m%d')
        except:
            return None

    def parse_time(self, time_val):
        if pd.isna(time_val):
            return None
        try:
            # Convert numeric time (e.g., 1000.0) to time string
            time_str = f"{int(time_val):04d}"
            return datetime.strptime(time_str, '%H%M').time()
        except:
            return None

    def handle(self, *args, **options):
        try:
            df = pd.read_csv(options['csv_file'])
            self.stdout.write(f"Found {len(df)} records to import")
            
            success_count = 0
            for _, row in df.iterrows():
                try:
                    Car.objects.create(
                        yard_name=row['yard_name'] if pd.notna(row['yard_name']) else '',
                        lot_number=str(row['lot_number']) if pd.notna(row['lot_number']) else '',
                        year=int(row['year']) if pd.notna(row['year']) else 0,
                        make=row['make'] if pd.notna(row['make']) else '',
                        model_group=row['model_group'] if pd.notna(row['model_group']) else '',
                        model_detail=row['model_detail'] if pd.notna(row['model_detail']) else '',
                        color=row['color'] if pd.notna(row['color']) else '',
                        damage_description=row['damage_description'] if pd.notna(row['damage_description']) else '',
                        secondary_damage=row['Secondary Damage'] if pd.notna(row.get('Secondary Damage')) else '',
                        vin=row['vin'] if pd.notna(row['vin']) else '',
                        engine=row['engine'] if pd.notna(row['engine']) else '',
                        drive=row['drive'] if pd.notna(row['drive']) else '',
                        transmission=row['transmission'] if pd.notna(row['transmission']) else '',
                        fuel_type=row['fuel_type'] if pd.notna(row['fuel_type']) else '',
                        cylinders=str(row['cylinders']) if pd.notna(row['cylinders']) else '',
                        runs_drives=row['runs_drives'] if pd.notna(row['runs_drives']) else '',
                        sale_status=row['sale_status'] if pd.notna(row['sale_status']) else '',
                        location_city=row['location_city'] if pd.notna(row['location_city']) else '',
                        location_state=row['location_state'] if pd.notna(row['location_state']) else '',
                        # Handle date and time with custom parsing
                        sale_date=self.parse_date(row['sale_date M/D/CY']),
                        sale_time=self.parse_time(row['sale_time (HHMM)']),
                        time_zone=row['Time Zone'] if pd.notna(row.get('Time Zone')) else '',
                        # Optional fields
                        sale_title_state=row.get('sale_title_state', ''),
                        sale_title_type=row.get('sale_title_type', ''),
                        has_keys=str(row.get('has_keys', '')).upper() == 'YES',
                        odometer=int(float(row['odometer'])) if pd.notna(row.get('odometer')) else None,
                        image_url=row.get('image_url', '')
                    )
                    success_count += 1
                    if success_count % 100 == 0:  # Progress indicator
                        self.stdout.write(f"Imported {success_count} records...")
                        
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Error importing row: {e}\nRow data: {row.to_dict()}'
                        )
                    )
                    continue
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully imported {success_count} cars out of {len(df)} records')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Fatal error during import: {str(e)}')
            ) 