from flask import Blueprint, request, jsonify
from .models import Item, SessionLocal

items_bp = Blueprint('items', __name__)

# Create an item
@items_bp.route('/items', methods=['POST'])
def create_item():
    data = request.json
    session = SessionLocal()
    item = Item(
        name=data.get('name'),
        description=data.get('description'),
        location=data.get('location'),
        is_found=data.get('is_found', False),
        user_id=data.get('user_id')
    )
    session.add(item)
    session.commit()
    session.refresh(item)
    session.close()
    return jsonify({'id': item.id}), 201

# List/search/filter/sort items
@items_bp.route('/items', methods=['GET'])
def list_items():
    session = SessionLocal()
    query = session.query(Item)
    # Filtering
    is_found = request.args.get('is_found')
    if is_found is not None:
        query = query.filter(Item.is_found == (is_found.lower() == 'true'))
    location = request.args.get('location')
    if location:
        query = query.filter(Item.location.ilike(f'%{location}%'))
    # Sorting
    sort_by = request.args.get('sort_by', 'date_reported')
    sort_order = request.args.get('sort_order', 'desc')
    if hasattr(Item, sort_by):
        column = getattr(Item, sort_by)
        if sort_order == 'asc':
            query = query.order_by(column.asc())
        else:
            query = query.order_by(column.desc())
    items = query.all()
    session.close()
    return jsonify([
        {
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'location': item.location,
            'date_reported': item.date_reported,
            'is_found': item.is_found,
            'user_id': item.user_id
        } for item in items
    ])

# Update an item
@items_bp.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    session = SessionLocal()
    item = session.query(Item).get(item_id)
    if not item:
        session.close()
        return jsonify({'error': 'Item not found'}), 404
    for key in ['name', 'description', 'location', 'is_found', 'user_id']:
        if key in data:
            setattr(item, key, data[key])
    session.commit()
    session.refresh(item)
    session.close()
    return jsonify({'message': 'Item updated'})

# Delete an item
@items_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    session = SessionLocal()
    item = session.query(Item).get(item_id)
    if not item:
        session.close()
        return jsonify({'error': 'Item not found'}), 404
    session.delete(item)
    session.commit()
    session.close()
    return jsonify({'message': 'Item deleted'})

# Auto-suggest endpoint
@items_bp.route('/items/suggest', methods=['GET'])
def suggest_items():
    query_text = request.args.get('q', '')
    session = SessionLocal()
    results = session.query(Item).filter(
        (Item.name.ilike(f'%{query_text}%')) |
        (Item.description.ilike(f'%{query_text}%'))
    ).limit(10).all()
    session.close()
    return jsonify([
        {
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'location': item.location,
            'date_reported': item.date_reported,
            'is_found': item.is_found,
            'user_id': item.user_id
        } for item in results
    ])
