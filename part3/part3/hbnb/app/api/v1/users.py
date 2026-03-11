from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.extensions import bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=False)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Crée un utilisateur public SANS token OU admin avec token."""
        from flask_jwt_extended import verify_jwt_in_request, get_jwt
        user_data = api.payload
        if not user_data:
            return {'error': 'Invalid input data'}, 400
        
         # Si un token est fourni, vérifier que c'est un admin
        try:
            verify_jwt_in_request(optional=True)
            claims = get_jwt()
            # Token présent mais pas admin → refus
            if claims and not claims.get('is_admin', False):
                return {'error': 'Admin privileges required'}, 403
        except Exception:
            pass

        try:
            existing_user = facade.get_user_by_email(user_data.get('email', ''))
            if existing_user:
                return {'error': 'Email already registered'}, 400

            # Hachage du password avant stockage
            if 'password' in user_data:
                user_data['password'] = bcrypt.generate_password_hash(
                    user_data['password']
                ).decode('utf-8')

            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400 # Transforme l'erreur du modèle en 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        users = facade.get_all_users()
        users_list = []
        for user in users:
            users_list.append({
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email
                    })
        return {'users': users_list}, 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        print("user_id:", user_id)
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @jwt_required()
    @api.expect(user_model, validate=False)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Token JWT manquant ou invalide')
    @api.response(403, 'Action non autorisée')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Mise à jour utilisateur — soi-même (sans email/password) ou admin (tout)."""
        from flask_jwt_extended import get_jwt
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)


        # Un utilisateur non-admin ne peut modifier que son propre profil
        if not is_admin and current_user_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        user_data = api.payload

        if not user_data:
            return {'error': 'Invalid input data'}, 400

        # Un utilisateur non-admin ne peut pas modifier email ni password
        if not is_admin and ('email' in user_data or 'password' in user_data):
            return {'error': 'You cannot modify email or password'}, 400

        # Admin : vérification unicité email si fourni
        if is_admin and 'email' in user_data:
            existing = facade.get_user_by_email(user_data['email'])
            if existing and existing.id != user_id:
                return {'error': 'Email already in use'}, 400

        # Admin : hachage du password si fourni
        if is_admin and 'password' in user_data:
            user_data['password'] = bcrypt.generate_password_hash(
                user_data['password']
            ).decode('utf-8')

        try:
            # Vérification de l'existence de l'utilisateur en base
            user = facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404

            # Mise à jour via la facade (seuls first_name et last_name sont modifiés)
            updated_user = facade.update_user(user_id, user_data)

            # Retourne le profil mis à jour sans le password pour la sécurité
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200
        except ValueError as e:
            # Erreur de validation levée 
            return {'error': str(e)}, 400
