"""
Seed Data - Tạo dữ liệu mẫu cho hệ thống
"""
from database.db_manager import get_db

def seed_users():
    """Tạo users mẫu"""
    db = get_db()
    
    users = [
        {
            'username': 'admin',
            'password': 'admin123',
            'email': 'admin@musicstore.com',
            'full_name': 'Quản trị viên',
            'phone': '0901234567', 
            'address': 'Hà Nội, Việt Nam',
            'role': 'admin'
        },
        {
            'username': 'customer',
            'password': 'customer123',
            'email': 'customer@example.com',
            'full_name': 'Nguyễn Văn A',
            'phone': '0912345678',
            'address': 'Đà Nẵng, Việt Nam',
            'role': 'customer'
        },
        {
            'username': 'user1',
            'password': '123456',
            'email': 'user1@example.com',
            'full_name': 'Trần Thị B',
            'phone': '0923456789',
            'address': 'TP.HCM, Việt Nam',
            'role': 'customer'
        },
        {
            'username': 'user2',
            'password': '123456',
            'email': 'user2@example.com',
            'full_name': 'Lê Văn C',
            'phone': '0934567890',
            'address': 'Hải Phòng, Việt Nam',
            'role': 'customer'
        }
    ]
    
    print("\n📝 Creating users...")
    for user in users:
        user_id = db.create_user(**user)
        if user_id:
            print(f"  ✅ Created user: {user['username']} ({user['role']})")
        else:
            print(f"  ⚠️  User {user['username']} already exists")

def seed_categories():
    """Tạo danh mục mẫu"""
    db = get_db()
    
    categories = [
        {'name': 'Guitar', 'description': 'Acoustic & Electric Guitars', 'icon': '🎸'},
        {'name': 'Piano', 'description': 'Acoustic & Digital Pianos', 'icon': '🎹'},
        {'name': 'Drums', 'description': 'Drum Sets & Percussion', 'icon': '🥁'},
        {'name': 'Wind', 'description': 'Saxophone, Trumpet, Flute', 'icon': '🎺'},
        {'name': 'Violin', 'description': 'Violin & String Instruments', 'icon': '🎻'},
        {'name': 'Accessories', 'description': 'Cables, Stands, Cases', 'icon': '🎼'}
    ]
    
    print("\n📝 Creating categories...")
    for category in categories:
        cat_id = db.create_category(**category)
        if cat_id:
            print(f"  ✅ Created category: {category['name']}")

def seed_products():
    """Tạo sản phẩm mẫu"""
    db = get_db()
    
    products = [
        # Guitars
        {
            'category_id': 1,
            'name': 'Yamaha F310 Acoustic Guitar',
            'brand': 'Yamaha',
            'price': 3500000,
            'stock': 15,
            'description': 'Guitar acoustic dành cho người mới bắt đầu, âm thanh ấm áp',
            'specifications': 'Top: Spruce, Back/Sides: Meranti, Finish: Natural',
            'discount_percent': 10
        },
        {
            'category_id': 1,
            'name': 'Fender Stratocaster Electric Guitar',
            'brand': 'Fender',
            'price': 12000000,
            'stock': 8,
            'description': 'Guitar điện huyền thoại với âm thanh đa dạng',
            'specifications': 'Pickups: 3 Single-Coil, Neck: Maple, Body: Alder',
            'discount_percent': 5
        },
        {
            'category_id': 1,
            'name': 'Gibson Les Paul Standard',
            'brand': 'Gibson',
            'price': 35000000,
            'stock': 3,
            'description': 'Guitar điện cao cấp với âm thanh rock đậm đà',
            'specifications': 'Pickups: 2 Humbucker, Neck: Mahogany, Body: Mahogany',
            'discount_percent': 0
        },
        {
            'category_id': 1,
            'name': 'Ibanez RG Series Electric',
            'brand': 'Ibanez',
            'price': 8500000,
            'stock': 10,
            'description': 'Guitar điện phù hợp cho rock và metal',
            'specifications': 'Pickups: HSH, Neck: Wizard III, Tremolo: Edge-Zero II',
            'discount_percent': 8
        },
        {
            'category_id': 1,
            'name': 'Taylor 214ce Acoustic',
            'brand': 'Taylor',
            'price': 18000000,
            'stock': 5,
            'description': 'Guitar acoustic cao cấp với electronics tích hợp',
            'specifications': 'Top: Sitka Spruce, Electronics: ES2',
            'discount_percent': 0
        },
        
        # Pianos
        {
            'category_id': 2,
            'name': 'Yamaha P-45 Digital Piano',
            'brand': 'Yamaha',
            'price': 11000000,
            'stock': 5,
            'description': 'Đàn piano điện nhỏ gọn, phù hợp cho gia đình',
            'specifications': '88 keys, 10 voices, USB connectivity',
            'discount_percent': 12
        },
        {
            'category_id': 2,
            'name': 'Roland FP-30X Digital Piano',
            'brand': 'Roland',
            'price': 15500000,
            'stock': 7,
            'description': 'Piano điện với âm thanh SuperNATURAL chân thực',
            'specifications': '88 keys, Bluetooth, PHA-4 Standard keyboard',
            'discount_percent': 7
        },
        {
            'category_id': 2,
            'name': 'Casio CT-S300 Keyboard',
            'brand': 'Casio',
            'price': 4200000,
            'stock': 12,
            'description': 'Keyboard nhỏ gọn với 400 tones và 77 rhythms',
            'specifications': '61 keys, 400 tones, Dance Music Mode',
            'discount_percent': 15
        },
        {
            'category_id': 2,
            'name': 'Kawai ES110 Digital Piano',
            'brand': 'Kawai',
            'price': 14000000,
            'stock': 4,
            'description': 'Piano điện cao cấp với Responsive Hammer Compact action',
            'specifications': '88 weighted keys, 19 sounds, Bluetooth MIDI',
            'discount_percent': 0
        },
        
        # Drums
        {
            'category_id': 3,
            'name': 'Pearl Export Drum Set',
            'brand': 'Pearl',
            'price': 18000000,
            'stock': 2,
            'description': 'Bộ trống acoustic 5 piece hoàn chỉnh',
            'specifications': '5-piece set, Poplar/Mahogany shells, Hardware included',
            'discount_percent': 10
        },
        {
            'category_id': 3,
            'name': 'Roland TD-17KVX Electronic Drums',
            'brand': 'Roland',
            'price': 32000000,
            'stock': 3,
            'description': 'Bộ trống điện tử với âm thanh chuyên nghiệp',
            'specifications': 'TD-17 module, Mesh heads, Bluetooth connectivity',
            'discount_percent': 5
        },
        {
            'category_id': 3,
            'name': 'Tama Imperialstar Drum Set',
            'brand': 'Tama',
            'price': 15000000,
            'stock': 4,
            'description': 'Bộ trống acoustic chất lượng cao cho người mới',
            'specifications': '5-piece set, Poplar shells, Cymbal stands included',
            'discount_percent': 8
        },
        
        # Wind Instruments
        {
            'category_id': 4,
            'name': 'Yamaha YAS-280 Alto Saxophone',
            'brand': 'Yamaha',
            'price': 25000000,
            'stock': 4,
            'description': 'Saxophone alto chuyên nghiệp cho học sinh',
            'specifications': 'Key: Eb, Gold lacquer finish, Includes case',
            'discount_percent': 0
        },
        {
            'category_id': 4,
            'name': 'Bach TR300H2 Trumpet',
            'brand': 'Bach',
            'price': 8500000,
            'stock': 6,
            'description': 'Kèn trumpet phù hợp cho người mới bắt đầu',
            'specifications': 'Bb trumpet, .459" bore, Includes mouthpiece',
            'discount_percent': 10
        },
        {
            'category_id': 4,
            'name': 'Yamaha YFL-222 Flute',
            'brand': 'Yamaha',
            'price': 12000000,
            'stock': 5,
            'description': 'Sáo flute bạc với chất lượng âm thanh tuyệt vời',
            'specifications': 'Closed hole, Offset G, Silver-plated',
            'discount_percent': 5
        },
        
        # Violins
        {
            'category_id': 5,
            'name': 'Stentor Student I Violin',
            'brand': 'Stentor',
            'price': 3500000,
            'stock': 8,
            'description': 'Violin dành cho học sinh, bao gồm bow và case',
            'specifications': 'Solid tonewoods, Ebony fittings, 4/4 size',
            'discount_percent': 12
        },
        {
            'category_id': 5,
            'name': 'Yamaha V3 Series Violin',
            'brand': 'Yamaha',
            'price': 7500000,
            'stock': 6,
            'description': 'Violin chuyên nghiệp với âm thanh ấm áp',
            'specifications': 'Hand-carved spruce top, Maple back/sides',
            'discount_percent': 0
        },
        
        # Accessories
        {
            'category_id': 6,
            'name': 'Guitar Stand Universal',
            'brand': 'On-Stage',
            'price': 250000,
            'stock': 25,
            'description': 'Giá đỡ guitar phù hợp mọi loại guitar',
            'specifications': 'Adjustable width, Non-slip rubber padding',
            'discount_percent': 0
        },
        {
            'category_id': 6,
            'name': 'Instrument Cable 3m',
            'brand': 'Monster',
            'price': 450000,
            'stock': 30,
            'description': 'Dây tín hiệu chất lượng cao cho nhạc cụ',
            'specifications': '1/4" straight to straight, Oxygen-free copper',
            'discount_percent': 5
        },
        {
            'category_id': 6,
            'name': 'Guitar Strings Set',
            'brand': "D'Addario",
            'price': 180000,
            'stock': 50,
            'description': 'Bộ dây guitar acoustic chất lượng cao',
            'specifications': 'Phosphor Bronze, Light gauge (12-53)',
            'discount_percent': 10
        }
    ]
    
    print("\n📝 Creating products...")
    for product in products:
        prod_id = db.create_product(**product)
        if prod_id:
            print(f"  ✅ Created product: {product['name']}")

def seed_all():
    """Tạo tất cả dữ liệu mẫu"""
    print("=" * 60)
    print("🌱 SEEDING DATABASE")
    print("=" * 60)
    
    # Reset database
    db = get_db()
    print("\n🗑️  Resetting database...")
    db.reset_database()
    
    # Seed data
    seed_users()
    seed_categories()
    seed_products()
    
    print("\n" + "=" * 60)
    print("✅ DATABASE SEEDING COMPLETED!")
    print("=" * 60)
    print("\n📊 Summary:")
    print(f"  • Users: {len(db.get_all_users())}")
    print(f"  • Categories: {len(db.get_all_categories())}")
    print(f"  • Products: {len(db.get_all_products())}")
    print("\n💡 You can now login with:")
    print("  Admin: admin / admin123")
    print("  Customer: customer / customer123")
    print("=" * 60)

if __name__ == "__main__":
    seed_all()