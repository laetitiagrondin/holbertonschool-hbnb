from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Token JWT manquant ou invalide')
    @api.response(403, 'Tentative d\'évaluation de son propre lieu')
    def post(self):
        """Register a new review"""
        current_user_id = get_jwt_identity()
        review_data = api.payload

        # Injection du user_id depuis le JWT (jamais depuis le client)
        review_data['user_id'] = current_user_id

        try:
            new_review = facade.create_review(review_data)
            return new_review.to_dict(), 201
        except PermissionError as e:
            return {'error': str(e)}, 403
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {"message": "Review not found"}, 404
        return review.to_dict(), 200

    @jwt_required()
    @api.expect(review_model)
    @api.response(401, 'Token JWT manquant ou invalide')
    @api.response(403, 'Action non autorisée')
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Modifie un avis — auteur ou admin."""
        from flask_jwt_extended import get_jwt
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'message': 'Review not found'}, 404

        # Vérification auteur — bypassed si admin
        if not is_admin and review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        try:
            updated_review = facade.update_review(review_id, api.payload)
            return {
                'review': updated_review.text,
                'message': 'Review updated successfully'
            }, 200
        except ValueError as e:
            return {'message': str(e)}, 400

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(401, 'Token JWT manquant ou invalide')
    @api.response(403, 'Action non autorisée')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Supprime un avis — auteur ou admin."""
        from flask_jwt_extended import get_jwt
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'message': 'Review not found'}, 404

         # Vérification auteur — bypassed si admin
        if not is_admin and review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200
