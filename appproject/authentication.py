# authentication.py

import requests
from rest_framework import authentication, exceptions
from django.conf import settings

class ExternalTokenAuthentication(authentication.BaseAuthentication):
    """
    Autenticação baseada em token Bearer que valida o token via uma aplicação externa.
    """
    
    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header or auth_header[0].lower() != b'bearer':
            return None  # Não autentica se não houver token Bearer

        if len(auth_header) == 1:
            msg = 'Token inválido. Sem token fornecido.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth_header) > 2:
            msg = 'Token inválido. Token contém espaços.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth_header[1].decode('utf-8')
        except UnicodeError:
            msg = 'Token inválido. Não pode decodificar.'
            raise exceptions.AuthenticationFailed(msg)

        # Valida o token com a aplicação externa
        user_pk = self.validate_token(token)
        if not user_pk:
            raise exceptions.AuthenticationFailed('Token inválido ou expirado.')

        # Retorna um objeto de usuário personalizado com o pk
        user = ExternalUser(pk=user_pk)
        return (user, token)

    def validate_token(self, token):
        """
        Envia uma requisição para a aplicação externa para validar o token e obter o pk do usuário.
        """
        validation_url = settings.EXTERNAL_AUTH_URL  # URL da API de validação de token
        try:
            response = requests.post(
                validation_url,
                headers={'Authorization': f'Bearer {token}'},
                timeout=5  # Tempo limite para a requisição
            )
            if response.status_code == 200:
                data = response.json()
                return data.get('user_pk')  # Supondo que a resposta contenha 'user_pk'
            else:
                return None
        except requests.RequestException:
            return None

class ExternalUser:
    """
    Classe de usuário genérico para representar o usuário autenticado externamente.
    """
    def __init__(self, pk):
        self.pk = pk
        self.is_authenticated = True

    def __str__(self):
        return f'ExternalUser(pk={self.pk})'

    def has_perm(self, perm, obj=None):
        return False

    def has_module_perms(self, app_label):
        return False

    @property
    def is_staff(self):
        return False

    @property
    def is_superuser(self):
        return False
