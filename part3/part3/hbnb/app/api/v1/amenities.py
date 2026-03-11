from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    def post(self):
        # Crée un équipement — admin uniquement.
        # Vérification du rôle admin via les claims JWT
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403
        
        amenity_data = api.payload
        if not amenity_data or 'name' not in amenity_data or not amenity_data['name']:
            return {'error': 'Invalid input data'}, 400
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return {'id': new_amenity.id, 'name': new_amenity.name}, 201
        except ValueError as e:
            return {'error': str(e)}, 400 # Transforme l'erreur du modèle en 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        # Liste tous les équipements
        amenities = facade.get_all_amenities()
        return [{'id': amenity.id, 'name': amenity.name}
                for amenity in amenities], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

    @jwt_required()
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    def put(self, amenity_id):
        # Modifie un équipement — admin uniquement.
        # Vérification du rôle admin via les claims JWT
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403
        
        amenity_data = api.payload
        if not amenity_data or 'name' not in amenity_data or not amenity_data['name']:
            return {'error': 'Invalid input data'}, 400
        try:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {'error': 'Amenity not found'}, 404
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return {'id': updated_amenity.id, 'name': updated_amenity.name}, 200
        except ValueError as e:
            return {'error': str(e)}, 400 # Transforme l'erreur du modèle en 400
