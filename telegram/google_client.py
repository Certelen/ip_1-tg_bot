from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

import settings

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
INFO = {
    'type': settings.TYPE,
    'project_id': settings.PROJ_ID,
    'private_key_id': settings.KEY_ID,
    'private_key': settings.KEY,
    'client_email': settings.CLIENT_MAIL,
    'client_id': settings.CLIENT_ID,
    'auth_uri': settings.AUTH_URL,
    'token_uri': settings.TOKEN_URL,
    'auth_provider_x509_cert_url': settings.AUTH_X509,
    'client_x509_cert_url': settings.CLIENT_X509,
}
cred = ServiceAccountCreds(scopes=SCOPES, **INFO)


async def spreadsheets_update_value(
        products,
        order

) -> None:
    """Добавление заказов в Гугл-таблицу"""
    async with Aiogoogle(service_account_creds=cred) as aiogoogle:
        values = []
        for product in products[0]:
            values.append([
                order[0], order[1], order[2], order[3], order[4],
                product[0], product[1], product[2]
            ])
        await aiogoogle.as_service_account(
            (await aiogoogle.discover(
                'sheets', 'v4'
            )).spreadsheets.values.append(
                spreadsheetId=settings.SPREAD_ID,
                range="Лист1!A1",
                valueInputOption='USER_ENTERED',
                json={
                    'majorDimension': 'ROWS',
                    'values': values
                }
            )
        )
