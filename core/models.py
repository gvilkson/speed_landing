from django.db import models
from django.contrib.auth import get_user_model
import geoip2.database
from user_agents import parse as parse_ua

User = get_user_model()

########################## Monitoramento #####################################
class AccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField()
    path = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    device = models.CharField(max_length=255, null=True, blank=True)
    user_agent = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        if not self.latitude or not self.longitude:
            self._set_lat_long()
        if not self.device:
            self._set_device()
        super().save(*args, **kwargs)

    def _set_lat_long(self):
        # Caminho para o banco de dados GeoLite2
        # Baixe o arquivo GeoLite2-City.mmdb.gz em https://dev.maxmind.com/geoip/geoip2/geolite2/
        # e descompacte-o
        geoip2_db_path = 'core/GeoLite2-City.mmdb'

        # Abre o banco de dados GeoLite2
        with geoip2.database.Reader(geoip2_db_path) as reader:
            try:
                # Obtém informações geográficas a partir do endereço IP
                response = reader.city(self.ip_address)
                # Define latitude e longitude
                self.latitude = response.location.latitude
                self.longitude = response.location.longitude
            except geoip2.errors.AddressNotFoundError:
                # Caso o endereço IP não seja encontrado no banco de dados
                # Define latitude e longitude como None
                self.latitude = None
                self.longitude = None

    def _set_device(self):
        # Obtém o User-Agent do usuário
        user_agent = parse_ua(self.user_agent)
        # Obtém o tipo de dispositivo
        device = user_agent.device.family if user_agent.device.family else "Unknown"
        # Define o tipo de dispositivo
        self.device = device

    def _set_user(self, request):
        if request.user.is_authenticated:
            self.user = request.user