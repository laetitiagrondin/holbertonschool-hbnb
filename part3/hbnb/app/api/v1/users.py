from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.extensions import bcrypt

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True,
                                description='First name of the user'),
    'last_name': fields.String(required=True,
                               description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=False, description='Password of the user')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=False)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Création d'un utilisateur."""
        user_data = api.payload
        if not user_data:
            return {'error': 'Invalid input data'}, 400
        try:
            existing_user = facade.get_user_by_email(user_data.get('email', ''))
            if existing_user:
                return {'error': 'Email already registered'}, 400
        if 'password' in user_data:
            user_data['password'] = bcrypt.generate_password_hash(
                user_data['password']).decode('utf-8')
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

    @api.expect(user_model, validate=False)
    @api.response(200, 'User details retrieved successfully')
    @api.response(400, 'Email already registered')
    @api.response(404, 'User not found')
    def put(self, user_id):
        print("user_id:", user_id)
        try:
            user = facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404
            existing_user = facade.get_user(user_id)
            if existing_user and existing_user.id != user_id:
                return {'error': 'User already registered'}, 400
            updated_user = facade.update_user(user_id, api.payload)
            return {
                    'id': updated_user.id,
                    'first_name': updated_user.first_name,
                    'last_name': updated_user.last_name,
                    'email': updated_user.email
                    }, 200
        except ValueError as e:
            return {'error': str(e)}, 400 # Transforme l'erreur du modèle en 400
