"""
Test script to verify all routes work correctly
"""

from app import create_app
from models import db, BlogPost, seed_sample_data

def test_routes():
    """Test all application routes"""
    print("\n" + "="*60)
    print("🧪 Testing Application Routes")
    print("="*60)
    
    app = create_app()
    
    with app.app_context():
        # Add sample data for testing
        print("\n📝 Adding sample data...")
        seed_sample_data()
        
        # Create test client
        client = app.test_client()
        
        # Test routes
        routes_to_test = [
            ('/', 'Homepage'),
            ('/services', 'Services'),
            ('/blog', 'Blog Listing'),
            ('/contact', 'Contact Form'),
        ]
        
        print("\n🔍 Testing Routes:")
        all_passed = True
        
        for route, name in routes_to_test:
            try:
                response = client.get(route)
                if response.status_code == 200:
                    print(f"  ✓ {name} ({route}) - Status: {response.status_code}")
                else:
                    print(f"  ✗ {name} ({route}) - Status: {response.status_code}")
                    all_passed = False
            except Exception as e:
                print(f"  ✗ {name} ({route}) - Error: {e}")
                all_passed = False
        
        # Test blog post detail
        print("\n🔍 Testing Blog Post Detail:")
        posts = BlogPost.query.filter_by(status='published').first()
        if posts:
            try:
                response = client.get(f'/blog/{posts.slug}')
                if response.status_code == 200:
                    print(f"  ✓ Blog Post Detail (/blog/{posts.slug}) - Status: {response.status_code}")
                else:
                    print(f"  ✗ Blog Post Detail (/blog/{posts.slug}) - Status: {response.status_code}")
                    all_passed = False
            except Exception as e:
                print(f"  ✗ Blog Post Detail - Error: {e}")
                all_passed = False
        else:
            print("  ⚠ No published posts to test")
        
        return all_passed


if __name__ == '__main__':
    import sys
    
    try:
        success = test_routes()
        
        print("\n" + "="*60)
        if success:
            print("✅ All route tests passed!")
            print("="*60)
            print("\n💡 The application is working correctly!")
            print("   You can now run: python app.py")
        else:
            print("❌ Some route tests failed!")
            print("="*60)
            print("\n💡 Check the errors above")
        print()
        
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)