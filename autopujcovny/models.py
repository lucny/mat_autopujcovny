import os, shutil
from django.db import models
from django.core.validators import EmailValidator, RegexValidator, MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.utils import timezone
from django.utils.timezone import now


class Autopujcovna(models.Model):
    def logo_upload_path(self, filename):
        return os.path.join('autopujcovny', str(self.id), filename)

    nazev = models.CharField(max_length=100, verbose_name='Název', help_text='Zadejte název autopůjčovny')
    adresa = models.CharField(max_length=200, verbose_name='Adresa', help_text='Zadejte adresu autopůjčovny')
    telefon = models.CharField(max_length=20, verbose_name='Telefon',
                               help_text='Zadejte telefonní číslo autopůjčovny (včetně předvolby)',
                               validators=[RegexValidator(regex='^(\\+420)? ?[1-9][0-9]{2}( ?[0-9]{3}){2}$',
                                                          message='Zadejte prosím platné telefonní číslo.'
                                                          )])
    email = models.EmailField(max_length=254, verbose_name='E-mail', help_text='Zadejte e-mailovou adresu autopůjčovny',
                              validators=[EmailValidator('Neplatný e-mail.')])
    logo = models.ImageField(upload_to=logo_upload_path, blank=True, null=True, verbose_name='Logo',
                             help_text='Nahrajte logo autopůjčovny')
    informace = models.TextField(blank=True, verbose_name='Informace',
                                 help_text='Zadejte další informace o autopůjčovně')

    class Meta:
        verbose_name = 'Autopůjčovna'
        verbose_name_plural = 'Autopůjčovny'
        ordering = ['nazev']

    def __str__(self):
        return self.nazev

    # přepsání metody delete tak, abychom zajistili smazání všech příloh
    def delete(self, *args, **kwargs):
        # před smazáním záznamu odstraníme i soubor s logem
        if self.logo:
            logo_path = os.path.join('media', 'autopujcovny', str(self.id))
            # metoda shutil.rmtree() zajistí smazání adresáře včetně jeho obsahu
            shutil.rmtree(logo_path)
        # vyvoláme metodu předka, která vymaže celý objekt - záznam o autopůjčovně v databázi
        super().delete(*args, **kwargs)


class Auto(models.Model):
    ZNACKA_MAX_LENGTH = 50
    SPZ_LENGTH = 8
    ROK_VYROBY_MIN = 2000
    ROK_VYROBY_MAX = timezone.now().year
    POCET_MIST_MIN = 1
    POCET_MIST_MAX = 9
    VYKON_MAX = 9999
    CENA_MAX = 500

    PREVODOVKA_CHOICES = [
        ('automatická', 'Automatická'),
        ('manuální', 'Manuální'),
    ]

    PALIVO_CHOICES = [
        ('benzín', 'Benzín'),
        ('nafta', 'Nafta'),
        ('lpg', 'LPG'),
    ]

    oznaceni = models.CharField(max_length=ZNACKA_MAX_LENGTH, verbose_name='Označení auta',
                                help_text='Zadejte označení vozu')
    spz = models.CharField(max_length=SPZ_LENGTH, verbose_name='SPZ', help_text='Státní poznávací značka',
                           validators=[RegexValidator(r'^[A-Z0-9]{8}$')])
    rok_vyroby = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Rok výroby',
                                                  help_text='Zadejte rok výroby',
                                                  validators=[MinValueValidator(ROK_VYROBY_MIN),
                                                              MaxValueValidator(ROK_VYROBY_MAX)])
    pocet_mist = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Počet míst',
                                                  help_text='Zadejte počet míst ve vozu (1-9)',
                                                  default=4, validators=[MinValueValidator(POCET_MIST_MIN),
                                                                         MaxValueValidator(POCET_MIST_MAX)])
    prevodovka = models.CharField(verbose_name='Typ převodovky', default='manuální', max_length=15,
                                  choices=PREVODOVKA_CHOICES)
    palivo = models.CharField(verbose_name='Typ paliva', default='benzín', max_length=10, choices=PALIVO_CHOICES)
    vykon = models.PositiveIntegerField(null=True, blank=True, verbose_name='Výkon motoru v kW',
                                        help_text='Zadejte výkon motoru v kW',
                                        validators=[MaxValueValidator(VYKON_MAX)])
    vybava = models.TextField(null=True, blank=True, verbose_name='Výbava vozu', help_text='Uveďte vybavení vozu')
    cena = models.PositiveIntegerField(verbose_name='Cena za 1 hod.', help_text='Zadejte částku v Kč',
                                       validators=[MaxValueValidator(CENA_MAX)])
    foto = models.ImageField(null=True, blank=True, verbose_name='Fotka vozu',
                             help_text='Zde můžete vložit fotografii vozu', upload_to='auto/')
    autopujcovna = models.ForeignKey('Autopujcovna', verbose_name='Autopůjčovna', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Auto'
        verbose_name_plural = 'Auta'
        ordering = ['autopujcovna', '-rok_vyroby']

    def __str__(self):
        return f'{self.oznaceni}, ({self.spz})'


class Zakaznik(models.Model):
    jmeno = models.CharField(max_length=100, verbose_name='Jméno', help_text='Zadejte jméno zákazníka')
    prijmeni = models.CharField(max_length=100, verbose_name='Příjmení', help_text='Zadejte příjmení zákazníka')
    adresa = models.CharField(max_length=200, verbose_name='Adresa', help_text='Zadejte adresu autopůjčovny')
    telefon = models.CharField(max_length=20, verbose_name='Telefon',
                               help_text='Zadejte telefonní číslo zákazníka (včetně předvolby)',
                               validators=[RegexValidator(regex='^(\\+420)? ?[1-9][0-9]{2}( ?[0-9]{3}){2}$',
                                                          message='Zadejte prosím platné telefonní číslo.'
                                                          )])
    email = models.EmailField(max_length=254, verbose_name='E-mail', help_text='Zadejte e-mailovou adresu zákazníka',
                              validators=[EmailValidator('Neplatný e-mail.')])
    cislo_rp = models.CharField(max_length=20, verbose_name='Řidičský průkaz', help_text='Zadejte číslo řidičského průkazu')


    class Meta:
        verbose_name = 'Zákazník'
        verbose_name_plural = 'Zákazníci'
        ordering = ['prijmeni', 'jmeno']

    def __str__(self):
        return f'{self.prijmeni}, {self.jmeno}'


class Hodnoceni(models.Model):
    autopujcovna = models.ForeignKey('Autopujcovna', verbose_name='Autopůjčovna', on_delete=models.CASCADE)
    zakaznik = models.ForeignKey('Zakaznik', verbose_name='Zákazník', on_delete=models.CASCADE)
    cas = models.DateTimeField(auto_now=True)
    komentar = models.TextField(verbose_name='Komentář zákazníka', help_text='Okomentujte úroveň služeb autopůjčovny')
    spokojenost = models.PositiveSmallIntegerField(verbose_name='Spokojenost se službami',
                                                   help_text='Vyjádřete svou spokojenost se službami autopůjčovny (0 až 100 %)',
                                                   validators = [MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        verbose_name = 'Hodnocení zákazníka'
        verbose_name_plural = 'Hodnocení zákazníků'
        ordering = ['-spokojenost']

    def __str__(self):
        return f'{self.zakaznik}: {self.autopujcovna} ({self.spokojenost} %)'


# Tzv. signál je vyvolán před nebo po určité akci ve spojení s konkrétním modelem
# V tomto případě zajistí, aby hned po uložení nového záznamu o autopůjčovně došlo k přejmenování
# dočasného adresáře None, v němž se nachází soubor loga, podle id čerstvě přidaného záznamu
@receiver(models.signals.post_save, sender=Autopujcovna)
def autopujcovna_post_save(sender, instance, created, **kwargs):
    # vytvoření složky s názvem id nově vytvořeného záznamu
    if created:
        directory_path = os.path.join('media', 'autopujcovny', str(instance.id))
        # přejmenování složky None na složku s id
        old_directory_path = os.path.join('media', 'autopujcovny', 'None')
        if os.path.exists(old_directory_path):
            os.rename(old_directory_path, directory_path)
            # nahrazení řetězce None správným id záznamu v cestě uložené v databázi
            instance.logo.name = instance.logo.name.replace('None', str(instance.id))
            instance.save()


class Pronajem(models.Model):
    zakaznik = models.ForeignKey('Zakaznik', verbose_name='Zákazník', on_delete=models.CASCADE)
    auto = models.ForeignKey('Auto', verbose_name='Auto', on_delete=models.CASCADE)
    vypujceno = models.DateTimeField(verbose_name='Vypůjčeno', help_text='Datum a čas zahájení pronájmu', default=now())
    vraceno = models.DateTimeField(verbose_name='Vráceno', help_text='Datum a čas ukončení pronájmu', blank=True, null=True)
    ujeto = models.PositiveIntegerField(verbose_name='Ujeto km', help_text='Zadejte počet ujetých km', default=0,
                                        validators=[MaxValueValidator(9999)])
    poznamka = models.TextField(verbose_name='Poznámka', help_text='Uveďte případné zjištěné závady a problémy', blank=True)
    PLATBA = [
        ('hotovost', 'Hotovost'),
        ('platební karta', 'Platební karta'),
        ('převod', 'Převodem na účet'),
    ]
    platba = models.CharField(choices=PLATBA, max_length=20, verbose_name='Způsob úhrady', help_text='Zvolte způsob úhrady')

    class Meta:
        verbose_name = 'Pronájem auta'
        verbose_name_plural = 'Pronájmy aut'
        ordering = ['auto', '-vypujceno']

    def __str__(self):
        return f'{self.vypujceno.strftime("%Y-%m-%d")}: {self.auto} - {self.zakaznik.jmeno[:1]}. {self.zakaznik.prijmeni}'