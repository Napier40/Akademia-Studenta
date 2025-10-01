"""
Database initialization script
Run this to create all database tables
"""

from app import app, db, BlogPost
from datetime import datetime

def init_database():
    """Initialize the database and create all tables"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created successfully!")
        
        # Check if we need to add sample data
        post_count = BlogPost.query.count()
        if post_count == 0:
            print("\nNo blog posts found. Would you like to add sample data? (y/n)")
            response = input().lower()
            if response == 'y':
                add_sample_data()
        else:
            print(f"\n✓ Database already contains {post_count} blog post(s)")

def add_sample_data():
    """Add sample blog posts"""
    with app.app_context():
        print("\nAdding sample blog posts...")
        
        # Sample post 1
        post1 = BlogPost(
            title_en='Getting Started with Our Services',
            title_pl='Rozpoczęcie pracy z naszymi usługami',
            slug='getting-started-with-our-services',
            content_en='''
# Welcome to Our Services

This is a comprehensive guide to getting started with our professional services. We cover everything you need to know to make the most of what we offer.

## Understanding Your Needs

Before diving into any service, it's crucial to understand what you're looking to achieve. We recommend taking time to assess your current situation and define clear objectives.

## Our Process

We've developed a streamlined process that ensures consistent results:

1. **Initial Consultation** - We begin with a thorough consultation
2. **Strategy Development** - We develop a customized strategy
3. **Implementation** - We execute the plan efficiently
4. **Monitoring** - We continuously monitor and optimize

## What Makes Us Different

In a crowded marketplace, we stand out through our commitment to transparency, quality, and results.

## Getting Started

Ready to begin? Contact us today for a free consultation.
            ''',
            content_pl='''
# Witamy w naszych usługach

To jest kompleksowy przewodnik po rozpoczęciu pracy z naszymi profesjonalnymi usługami. Omawiamy wszystko, co musisz wiedzieć, aby jak najlepiej wykorzystać to, co oferujemy.

## Zrozumienie Twoich potrzeb

Przed rozpoczęciem korzystania z jakiejkolwiek usługi, kluczowe jest zrozumienie, co chcesz osiągnąć. Zalecamy poświęcenie czasu na ocenę obecnej sytuacji i określenie jasnych celów.

## Nasz proces

Opracowaliśmy usprawniony proces, który zapewnia spójne rezultaty:

1. **Wstępna konsultacja** - Zaczynamy od dokładnej konsultacji
2. **Opracowanie strategii** - Opracowujemy dostosowaną strategię
3. **Wdrożenie** - Skutecznie realizujemy plan
4. **Monitorowanie** - Stale monitorujemy i optymalizujemy

## Co nas wyróżnia

Na zatłoczonym rynku wyróżniamy się zaangażowaniem w przejrzystość, jakość i rezultaty.

## Rozpoczęcie

Gotowy do rozpoczęcia? Skontaktuj się z nami już dziś, aby uzyskać bezpłatną konsultację.
            ''',
            excerpt_en='Learn how to make the most of our professional services and achieve your business goals.',
            excerpt_pl='Dowiedz się, jak najlepiej wykorzystać nasze profesjonalne usługi i osiągnąć cele biznesowe.',
            category_en='Business Tips',
            category_pl='Porady biznesowe',
            featured_image='https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=1200',
            status='published',
            published_at=datetime.utcnow()
        )
        
        # Sample post 2
        post2 = BlogPost(
            title_en='5 Tips for Business Growth',
            title_pl='5 wskazówek dotyczących rozwoju firmy',
            slug='5-tips-for-business-growth',
            content_en='''
# 5 Essential Tips for Business Growth

Growing a business requires strategy, dedication, and the right approach. Here are five proven tips to help you scale successfully.

## 1. Focus on Customer Experience

Your customers are your greatest asset. Invest in understanding their needs and exceeding their expectations.

## 2. Leverage Technology

Modern tools and automation can significantly improve efficiency and reduce costs.

## 3. Build a Strong Team

Your team is the backbone of your business. Invest in hiring, training, and retaining top talent.

## 4. Monitor Your Metrics

What gets measured gets managed. Track key performance indicators and make data-driven decisions.

## 5. Stay Adaptable

The business landscape is constantly changing. Stay flexible and be ready to pivot when necessary.

## Conclusion

Implementing these tips can help you build a sustainable, growing business. Start with one or two and gradually incorporate the rest.
            ''',
            content_pl='''
# 5 podstawowych wskazówek dotyczących rozwoju firmy

Rozwój firmy wymaga strategii, zaangażowania i właściwego podejścia. Oto pięć sprawdzonych wskazówek, które pomogą Ci skutecznie się rozwijać.

## 1. Skup się na doświadczeniu klienta

Twoi klienci to Twój największy atut. Zainwestuj w zrozumienie ich potrzeb i przekraczanie ich oczekiwań.

## 2. Wykorzystaj technologię

Nowoczesne narzędzia i automatyzacja mogą znacznie poprawić wydajność i obniżyć koszty.

## 3. Zbuduj silny zespół

Twój zespół jest kręgosłupem Twojej firmy. Zainwestuj w zatrudnianie, szkolenie i utrzymanie najlepszych talentów.

## 4. Monitoruj swoje wskaźniki

To, co jest mierzone, jest zarządzane. Śledź kluczowe wskaźniki wydajności i podejmuj decyzje oparte na danych.

## 5. Pozostań elastyczny

Krajobraz biznesowy stale się zmienia. Pozostań elastyczny i bądź gotowy do zmiany kierunku, gdy to konieczne.

## Podsumowanie

Wdrożenie tych wskazówek może pomóc w zbudowaniu zrównoważonej, rozwijającej się firmy. Zacznij od jednej lub dwóch i stopniowo włączaj resztę.
            ''',
            excerpt_en='Discover proven strategies to scale your business and increase profitability.',
            excerpt_pl='Odkryj sprawdzone strategie skalowania firmy i zwiększania rentowności.',
            category_en='Business Tips',
            category_pl='Porady biznesowe',
            featured_image='https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1200',
            status='published',
            published_at=datetime.utcnow()
        )
        
        # Sample post 3
        post3 = BlogPost(
            title_en='Industry Trends 2025',
            title_pl='Trendy branżowe 2025',
            slug='industry-trends-2025',
            content_en='''
# Industry Trends to Watch in 2025

As we move through 2025, several key trends are shaping the business landscape. Here's what you need to know.

## Digital Transformation Acceleration

The pace of digital transformation continues to accelerate, with businesses of all sizes adopting new technologies.

## Sustainability Focus

Environmental responsibility is no longer optional. Businesses are integrating sustainability into their core strategies.

## Remote Work Evolution

The future of work is hybrid, with companies finding new ways to support distributed teams.

## AI and Automation

Artificial intelligence and automation are transforming how businesses operate and compete.

## Customer-Centric Approaches

Businesses are putting customers at the center of everything they do, from product development to service delivery.

## Conclusion

Staying ahead of these trends can give your business a competitive advantage. Start planning now for the future.
            ''',
            content_pl='''
# Trendy branżowe do obserwowania w 2025 roku

W miarę jak przechodzimy przez 2025 rok, kilka kluczowych trendów kształtuje krajobraz biznesowy. Oto, co musisz wiedzieć.

## Przyspieszenie transformacji cyfrowej

Tempo transformacji cyfrowej nadal przyspiesza, a firmy wszystkich rozmiarów przyjmują nowe technologie.

## Skupienie na zrównoważonym rozwoju

Odpowiedzialność środowiskowa nie jest już opcjonalna. Firmy integrują zrównoważony rozwój ze swoimi podstawowymi strategiami.

## Ewolucja pracy zdalnej

Przyszłość pracy jest hybrydowa, a firmy znajdują nowe sposoby wspierania rozproszonych zespołów.

## AI i automatyzacja

Sztuczna inteligencja i automatyzacja przekształcają sposób, w jaki firmy działają i konkurują.

## Podejścia skoncentrowane na kliencie

Firmy stawiają klientów w centrum wszystkiego, co robią, od rozwoju produktu po dostarczanie usług.

## Podsumowanie

Wyprzedzanie tych trendów może dać Twojej firmie przewagę konkurencyjną. Zacznij planować teraz na przyszłość.
            ''',
            excerpt_en='Stay ahead of the curve with our analysis of emerging trends and opportunities.',
            excerpt_pl='Wyprzedź konkurencję dzięki naszej analizie pojawiających się trendów i możliwości.',
            category_en='Technology',
            category_pl='Technologia',
            featured_image='https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200',
            status='published',
            published_at=datetime.utcnow()
        )
        
        db.session.add(post1)
        db.session.add(post2)
        db.session.add(post3)
        db.session.commit()
        
        print("✓ Sample blog posts added successfully!")
        print("\nAdded posts:")
        print("  1. Getting Started with Our Services")
        print("  2. 5 Tips for Business Growth")
        print("  3. Industry Trends 2025")

if __name__ == '__main__':
    init_database()
    print("\n" + "="*50)
    print("Database initialization complete!")
    print("You can now run the application with: flask run")
    print("="*50)