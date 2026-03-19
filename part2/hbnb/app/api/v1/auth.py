"""
Module d'authentification JWT.
Gère la connexion des utilisateurs et la protection des endpoints.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from app.services import facade

api = Namespace('auth', description='Opérations d\'authentification')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='Email de l\'utilisateur'),
    'password': fields.String(required=True, description='Mot de passe de l\'utilisateur')
})


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'Connexion réussie')
    @api.response(401, 'Identifiants invalides')
    def post(self):
        """Authentifie l'utilisateur et retourne un token JWT"""
        credentials = api.payload

        user = facade.get_user_by_email(credentials['email'])
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Identifiants invalides'}, 401

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin}
        )
        return {'access_token': access_token}, 200


@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    @api.response(200, 'Accès autorisé')
    @api.response(401, 'Token invalide ou manquant')
    def get(self):
        """Endpoint protégé nécessitant un token JWT valide"""
        current_user = get_jwt_identity()
        return {'message': f'Bonjour, utilisateur {current_user}'}, 200
