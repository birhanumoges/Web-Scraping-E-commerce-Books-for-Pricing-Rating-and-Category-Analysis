"""
Advanced Analysis Script for Book Price Tracker
Calculates average price per rating and generates comprehensive report
"""

import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class BookAnalyzer:
    def __init__(self, host='localhost', user='root', password='your_password', database='books_tracker'):
        """Initialize database connection"""
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            auth_plugin='mysql_native_password'
        )
        self.cursor = self.connection.cursor()
        print("✅ Connected to database")
    
    def get_average_price_per_rating(self):
        """Main requirement: Calculate average price per rating"""
        query = """
        SELECT 
            rating,
            COUNT(*) as book_count,
            ROUND(AVG(price), 2) as average_price,
            ROUND(MIN(price), 2) as cheapest,
            ROUND(MAX(price), 2) as most_expensive,
            ROUND(STDDEV(price), 2) as price_std
        FROM books
        WHERE rating IS NOT NULL AND rating BETWEEN 1 AND 5
        GROUP BY rating
        ORDER BY rating DESC
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        
        # Convert to DataFrame for better display
        columns = ['rating', 'book_count', 'average_price', 'cheapest', 'most_expensive', 'price_std']
        df = pd.DataFrame(results, columns=columns)
        return df
    
    def display_results(self):
        """Display formatted results"""
        df = self.get_average_price_per_rating()
        
        print("\n" + "="*80)
        print("📊 BOOK PRICE TRACKER - FINAL ANALYSIS REPORT")
        print("="*80)
        print(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
        print("\n📈 AVERAGE PRICE PER RATING (Main Requirement)")
        print("-"*80)
        print(f"{'Rating':<10} {'Books':<10} {'Average Price':<15} {'Min':<10} {'Max':<10} {'Std Dev':<10}")
        print("-"*80)
        
        for _, row in df.iterrows():
            stars = '★' * int(row['rating'])
            print(f"{stars} ({row['rating']}){' ' * (5 - len(str(row['rating'])))}\t"
                  f"{int(row['book_count']):<10} "
                  f"£{row['average_price']:<14} "
                  f"£{row['cheapest']:<9} "
                  f"£{row['most_expensive']:<9} "
                  f"£{row['price_std']:<9}")
        
        print("-"*80)
        
        # Additional insights
        print("\n💡 KEY INSIGHTS")
        print("-"*80)
        
        max_rating = df.loc[df['average_price'].idxmax()]
        min_rating = df.loc[df['average_price'].idxmin()]
        
        print(f"• Most expensive rating: {int(max_rating['rating'])}★ (£{max_rating['average_price']})")
        print(f"• Least expensive rating: {int(min_rating['rating'])}★ (£{min_rating['average_price']})")
        print(f"• Price difference: £{abs(max_rating['average_price'] - min_rating['average_price'])}")
        print(f"• Total books analyzed: {df['book_count'].sum()}")
        
        # Check if higher rating means higher price
        correlation = self.get_price_rating_correlation()
        if correlation > 0:
            print(f"• Price-Rating Correlation: Positive ({correlation:.3f})")
            print("  → Higher rated books tend to cost MORE")
        else:
            print(f"• Price-Rating Correlation: Negative ({correlation:.3f})")
            print("  → Higher rated books tend to cost LESS")
        
        print("="*80)
        
        return df
    
    def get_price_rating_correlation(self):
        """Calculate correlation between price and rating"""
        query = """
        SELECT 
            (COUNT(*) * SUM(price * rating) - SUM(price) * SUM(rating)) /
            (SQRT(COUNT(*) * SUM(price * price) - POW(SUM(price), 2)) *
             SQRT(COUNT(*) * SUM(rating * rating) - POW(SUM(rating), 2)))
        as correlation
        FROM books
        WHERE rating IS NOT NULL AND price IS NOT NULL
        """
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result[0] if result[0] else 0
    
    def create_visualization(self):
        """Create price-rating visualization"""
        df = self.get_average_price_per_rating()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Bar chart - Average price by rating
        ax1.bar(df['rating'], df['average_price'], color=['red', 'orange', 'yellow', 'lightgreen', 'green'])
        ax1.set_xlabel('Rating (Stars)')
        ax1.set_ylabel('Average Price (£)')
        ax1.set_title('Average Book Price by Rating')
        ax1.set_xticks(df['rating'])
        
        # Add value labels on bars
        for i, v in enumerate(df['average_price']):
            ax1.text(df['rating'][i] - 0.15, v + 0.5, f'£{v}', fontweight='bold')
        
        # Line chart - Book count by rating
        ax2.plot(df['rating'], df['book_count'], marker='o', linewidth=2, markersize=8)
        ax2.set_xlabel('Rating (Stars)')
        ax2.set_ylabel('Number of Books')
        ax2.set_title('Number of Books by Rating')
        ax2.fill_between(df['rating'], df['book_count'], alpha=0.3)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        print("✅ Visualization saved as 'price_rating_analysis.png'")
    
    def generate_sql_for_report(self):
        """Generate SQL queries for project report"""
        sql_queries = """
        -- ============================================
        -- SQL QUERIES FOR PROJECT REPORT
        -- ============================================
        
        -- 1. Average Price per Rating (Main Requirement)
        SELECT 
            rating,
            COUNT(*) as book_count,
            ROUND(AVG(price), 2) as average_price
        FROM books
        WHERE rating IS NOT NULL
        GROUP BY rating
        ORDER BY rating DESC;
        
        -- 2. Complete Analysis with Statistics
        SELECT 
            rating,
            COUNT(*) as book_count,
            ROUND(AVG(price), 2) as avg_price,
            ROUND(MIN(price), 2) as min_price,
            ROUND(MAX(price), 2) as max_price,
            ROUND(MAX(price) - MIN(price), 2) as price_range
        FROM books
        GROUP BY rating
        ORDER BY rating DESC;
        
        -- 3. Overall Statistics
        SELECT 
            COUNT(*) as total_books,
            ROUND(AVG(price), 2) as avg_price_all,
            ROUND(AVG(rating), 1) as avg_rating_all
        FROM books;
        """
        
        with open('project_queries.sql', 'w') as f:
            f.write(sql_queries)
        print("✅ SQL queries saved to 'project_queries.sql'")
    
    def close(self):
        """Close database connection"""
        self.cursor.close()
        self.connection.close()
        print("\n🔌 Database connection closed")

def main():
    """Main execution function"""
    print("🚀 Starting Book Price Tracker Analysis...")
    
    # Initialize analyzer
    analyzer = BookAnalyzer(
        host='localhost',
        user='root',
        password='0989',  # Change this!
        database='books_tracker'
    )
    
    try:
        # Display main results
        results_df = analyzer.display_results()
        
        # Export to CSV
        analyzer.export_to_csv('average_price_per_rating.csv')
        
        # Create visualization
        analyzer.create_visualization()
        
        # Generate SQL for report
        analyzer.generate_sql_for_report()
        
        print("\n✅ Analysis completed successfully!")
        print("\n📁 Generated files:")
        print("   - average_price_per_rating.csv")
        print("   - price_rating_analysis.png")
        print("   - project_queries.sql")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        analyzer.close()

if __name__ == "__main__":
    main()