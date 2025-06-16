from django.core.management.base import BaseCommand
from scrapers.models import ScrapeJob
from scrapers.marchespublics.scraper import MarchesPublicsScraper
from scrapers.marsamaroc.scraper import MarsaMarocScraper
from scrapers.royalairmaroc.scraper import RoyalAirMarocScraper
from scrapers.offresonline.scraper import OffresonlineScraper
from scrapers.adm.scraper import AdmScraper

class Command(BaseCommand):
    help = 'Run scraper for specified website'

    def add_arguments(self, parser):
        parser.add_argument('site', type=str, help='Site to scrape (e.g. marchespublics)')

    def handle(self, *args, **options):
        site = options['site']
        
        self.stdout.write(self.style.NOTICE(f'Démarrage du scraping pour le site: {site}'))
        
        if site not in ['marchespublics', 'marsamaroc', 'royalairmaroc', 'offresonline', 'adm']:
            self.stdout.write(
                self.style.ERROR(
                    f'Erreur: Le scraper pour {site} n\'est pas encore implémenté. '
                    'Les sites disponibles sont: "marchespublics", "marsamaroc", "royalairmaroc", "offresonline" et "adm".'
                )
            )
            return
        
        # Create scrape job
        try:
            self.stdout.write('Création d\'une nouvelle tâche de scraping...')
            job = ScrapeJob.objects.create(site_name=site)
            self.stdout.write(self.style.SUCCESS('Tâche créée avec succès!'))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'Erreur lors de la création de la tâche: {str(e)}'
                )
            )
            return
        
        try:
            self.stdout.write('Initialisation du scraper...')
            if site == 'marchespublics':
                scraper = MarchesPublicsScraper()
            elif site == 'marsamaroc':
                scraper = MarsaMarocScraper()
            elif site == 'royalairmaroc':
                scraper = RoyalAirMarocScraper()
            elif site == 'offresonline':
                scraper = OffresonlineScraper()
            else:  # adm
                scraper = AdmScraper()
            
            self.stdout.write('Lancement du scraping...')
            tenders_count = scraper.scrape()
            
            job.status = ScrapeJob.SUCCESS
            job.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Scraping terminé avec succès! {tenders_count} appels d\'offres récupérés depuis {site}\n'
                    f'Les données ont été exportées dans le dossier data/marchespublics/'
                )
            )
            
        except Exception as e:
            job.status = ScrapeJob.FAILED
            job.save()
            
            self.stdout.write(
                self.style.ERROR(
                    f'Échec du scraping pour {site}:\n'
                    f'Erreur: {str(e)}\n\n'
                    'Suggestions de dépannage:\n'
                    '1. Vérifiez votre connexion internet\n'
                    '2. Assurez-vous que les identifiants sont corrects\n'
                    '3. Vérifiez que le site est accessible\n'
                    '4. Regardez les logs ci-dessus pour plus de détails'
                )
            )