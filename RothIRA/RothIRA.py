def get_dca_timing_advice():
    """Provide dollar cost averaging timing advice"""
    return [
        "Contribute on the same day each month (e.g., 1st or 15th)",
        "Set up automatic transfers to ensure consistency",
        "Don't try to time the market - stick to your schedule",
        "Consider splitting large amounts across multiple days in the month",
        "If you get a lump sum, consider spreading it over 3-6 months"
    ]#!/usr/bin/env python3
"""
Roth IRA Dollar Cost Averaging Calculator
Helps plan monthly contributions and allocation timing for optimal dollar cost averaging
"""

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
import matplotlib.pyplot as plt
import numpy as np

# 2025 Roth IRA contribution limits
ROTH_IRA_LIMITS = {
    "under_50": 7000,
    "50_and_over": 8000
}

def get_contribution_limit(age):
    """Get annual Roth IRA contribution limit based on age"""
    return ROTH_IRA_LIMITS["50_and_over"] if age >= 50 else ROTH_IRA_LIMITS["under_50"]

def calculate_months_remaining(start_date):
    """Calculate months remaining in the tax year from start date"""
    tax_year_end = datetime(start_date.year, 12, 31)
    months_remaining = 0
    current_date = start_date
    
    while current_date.year == start_date.year:
        months_remaining += 1
        current_date += relativedelta(months=1)
        if current_date > tax_year_end:
            break
    
    return months_remaining

def generate_contribution_schedule(start_date, monthly_amount, total_annual_limit):
    """Generate month-by-month contribution schedule"""
    schedule = []
    current_date = start_date
    total_contributed = 0
    
    while current_date.year == start_date.year and total_contributed < total_annual_limit:
        # Calculate contribution for this month
        remaining_limit = total_annual_limit - total_contributed
        contribution_this_month = min(monthly_amount, remaining_limit)
        
        if contribution_this_month > 0:
            schedule.append({
                'date': current_date.strftime('%B %Y'),
                'amount': contribution_this_month,
                'cumulative': total_contributed + contribution_this_month
            })
            total_contributed += contribution_this_month
        
        # Move to next month
        current_date += relativedelta(months=1)
    
    return schedule, total_contributed

# Fidelity ETF portfolio with expense ratios
FIDELITY_PORTFOLIO = {
    'FXAIX': {  # Fidelity 500 Index Fund (S&P 500)
        'name': 'S&P 500 Index',
        'type': 'Large Cap US',
        'expense_ratio': 0.015
    },
    'FZROX': {  # Fidelity ZERO Total Market Index
        'name': 'Total Stock Market',
        'type': 'Total US Market',
        'expense_ratio': 0.00
    },
    'FSMDX': {  # Fidelity Small Cap Index
        'name': 'Small Cap Index',
        'type': 'Small Cap US',
        'expense_ratio': 0.025
    },
    'FTIHX': {  # Fidelity Total International Index
        'name': 'Total International Index',
        'type': 'Ex-US Developed',
        'expense_ratio': 0.06
    },
    'FREL': {   # Fidelity MSCI Real Estate ETF
        'name': 'Real Estate ETF',
        'type': 'REITs',
        'expense_ratio': 0.084
    },
    'FXNAX': {  # Fidelity US Bond Index
        'name': 'US Bond Index',
        'type': 'Bonds',
        'expense_ratio': 0.025
    },
    'FXNAX': {  # Using same bond fund (Fidelity offers limited bond variety)
        'name': 'US Bond Index',
        'type': 'Bonds',
        'expense_ratio': 0.025
    }
}

# Note: For gold/commodities, Fidelity has limited options. Adding external options:
ADDITIONAL_ETFS = {
    'FCOM': {   # Fidelity MSCI Communication Services ETF
        'name': 'Communication Services',
        'type': 'Sector',
        'expense_ratio': 0.084
    },
    'IAU': {    # iShares Gold Trust (available at Fidelity)
        'name': 'Gold Trust',
        'type': 'Commodities/Gold',
        'expense_ratio': 0.25
    }
}

def get_age_based_allocation(age):
    """Get allocation percentages based on age"""
    if age <= 30:
        return {
            'us_large_cap': 35,      # FXAIX (S&P 500)
            'us_total_market': 25,   # FZROX 
            'us_small_cap': 15,      # FSMDX
            'international': 15,     # FTIHX
            'reits': 5,              # FREL
            'commodities': 5,        # IAU (Gold)
            'bonds': 0               # Young = no bonds
        }
    elif age <= 40:
        return {
            'us_large_cap': 30,
            'us_total_market': 20,
            'us_small_cap': 12,
            'international': 18,
            'reits': 5,
            'commodities': 5,
            'bonds': 10              # FXNAX
        }
    elif age <= 50:
        return {
            'us_large_cap': 25,
            'us_total_market': 20,
            'us_small_cap': 10,
            'international': 15,
            'reits': 5,
            'commodities': 5,
            'bonds': 20
        }
    else:  # Over 50
        return {
            'us_large_cap': 20,
            'us_total_market': 15,
            'us_small_cap': 8,
            'international': 12,
            'reits': 5,
            'commodities': 5,
            'bonds': 35
        }

def calculate_portfolio_allocation(age, monthly_contribution):
    """Calculate detailed portfolio allocation with Fidelity tickers"""
    allocation_percentages = get_age_based_allocation(age)
    
    # Map to specific funds
    fund_mapping = {
        'us_large_cap': ('FXAIX', FIDELITY_PORTFOLIO['FXAIX']),
        'us_total_market': ('FZROX', FIDELITY_PORTFOLIO['FZROX']),
        'us_small_cap': ('FSMDX', FIDELITY_PORTFOLIO['FSMDX']),
        'international': ('FTIHX', FIDELITY_PORTFOLIO['FTIHX']),
        'reits': ('FREL', FIDELITY_PORTFOLIO['FREL']),
        'commodities': ('IAU', ADDITIONAL_ETFS['IAU']),
        'bonds': ('FXNAX', FIDELITY_PORTFOLIO['FXNAX'])
    }
    
    portfolio = {}
    total_expense_weighted = 0
    
    for category, percentage in allocation_percentages.items():
        if percentage > 0:
            ticker, fund_info = fund_mapping[category]
            amount = monthly_contribution * (percentage / 100)
            
            portfolio[ticker] = {
                'name': fund_info['name'],
                'type': fund_info['type'],
                'percentage': percentage,
                'monthly_amount': amount,
                'expense_ratio': fund_info['expense_ratio']
            }
            
            # Calculate weighted expense ratio
            total_expense_weighted += (percentage / 100) * fund_info['expense_ratio']
    
    return portfolio, total_expense_weighted

def recommend_allocation_strategy(age, monthly_contribution):
    """Recommend asset allocation based on age and contribution amount"""
    portfolio, weighted_expense_ratio = calculate_portfolio_allocation(age, monthly_contribution)
    
    # Calculate total stock vs bond percentages
    stock_percentage = sum(
        fund['percentage'] for fund in portfolio.values() 
        if fund['type'] not in ['Bonds']
    )
    bond_percentage = 100 - stock_percentage
    
    return {
        'portfolio': portfolio,
        'weighted_expense_ratio': weighted_expense_ratio,
        'stock_percentage': stock_percentage,
        'bond_percentage': bond_percentage,
        'total_funds': len(portfolio)
    }

def plot_allocation_over_time(current_age, save_plot=False):
    """Plot how portfolio allocation changes with age over time"""
    ages = list(range(max(20, current_age - 5), min(80, current_age + 40)))
    
    # Initialize data structures for each asset class
    allocations = {
        'US Large Cap (FXAIX)': [],
        'US Total Market (FZROX)': [],
        'US Small Cap (FSMDX)': [],
        'International (FTIHX)': [],
        'REITs (FREL)': [],
        'Gold/Commodities (IAU)': [],
        'Bonds (FXNAX)': []
    }
    
    # Collect allocation data for each age
    for age in ages:
        age_allocation = get_age_based_allocation(age)
        allocations['US Large Cap (FXAIX)'].append(age_allocation['us_large_cap'])
        allocations['US Total Market (FZROX)'].append(age_allocation['us_total_market'])
        allocations['US Small Cap (FSMDX)'].append(age_allocation['us_small_cap'])
        allocations['International (FTIHX)'].append(age_allocation['international'])
        allocations['REITs (FREL)'].append(age_allocation['reits'])
        allocations['Gold/Commodities (IAU)'].append(age_allocation['commodities'])
        allocations['Bonds (FXNAX)'].append(age_allocation['bonds'])
    
    # Create the plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    fig.suptitle('Fidelity Portfolio Allocation Strategy by Age', fontsize=16, fontweight='bold')
    
    # Plot 1: Stacked area chart showing all allocations
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#17becf']
    
    # Create stacked area plot
    bottom = np.zeros(len(ages))
    for i, (asset_class, values) in enumerate(allocations.items()):
        ax1.fill_between(ages, bottom, bottom + values, 
                        label=asset_class, alpha=0.8, color=colors[i % len(colors)])
        bottom += values
    
    ax1.set_xlabel('Age')
    ax1.set_ylabel('Allocation Percentage (%)')
    ax1.set_title('Complete Portfolio Allocation Over Time')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 100)
    
    # Add current age line
    if current_age in ages:
        ax1.axvline(x=current_age, color='red', linestyle='--', linewidth=2, alpha=0.7)
        ax1.text(current_age, 95, f'Your Age: {current_age}', rotation=90, 
                verticalalignment='top', fontweight='bold', color='red')
    
    # Plot 2: Stock vs Bond allocation trend
    stock_percentages = []
    bond_percentages = []
    expense_ratios = []
    
    for age in ages:
        portfolio, expense_ratio = calculate_portfolio_allocation(age, 1000)  # Use $1000 as baseline
        
        stock_pct = sum(fund['percentage'] for fund in portfolio.values() 
                       if fund['type'] not in ['Bonds'])
        bond_pct = 100 - stock_pct
        
        stock_percentages.append(stock_pct)
        bond_percentages.append(bond_pct)
        expense_ratios.append(expense_ratio * 100)  # Convert to percentage
    
    ax2.plot(ages, stock_percentages, 'b-', linewidth=3, label='Stock Allocation', marker='o', markersize=3)
    ax2.plot(ages, bond_percentages, 'orange', linewidth=3, label='Bond Allocation', marker='s', markersize=3)
    
    # Add expense ratio on secondary y-axis
    ax2_twin = ax2.twinx()
    ax2_twin.plot(ages, expense_ratios, 'g--', linewidth=2, label='Expense Ratio', alpha=0.7)
    ax2_twin.set_ylabel('Expense Ratio (%)', color='green')
    ax2_twin.tick_params(axis='y', labelcolor='green')
    
    ax2.set_xlabel('Age')
    ax2.set_ylabel('Allocation Percentage (%)')
    ax2.set_title('Stock vs Bond Allocation + Expense Ratio Trend')
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='upper right')
    ax2_twin.legend(loc='lower right')
    
    # Add current age line
    if current_age in ages:
        ax2.axvline(x=current_age, color='red', linestyle='--', linewidth=2, alpha=0.7)
    
    # Add annotations for key milestones
    ax2.annotate('Aggressive Growth\n(Young Investor)', xy=(25, 95), xytext=(30, 85),
                arrowprops=dict(arrowstyle='->', color='blue', alpha=0.7),
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.7))
    
    ax2.annotate('Balanced Approach\n(Middle Age)', xy=(45, 75), xytext=(50, 85),
                arrowprops=dict(arrowstyle='->', color='purple', alpha=0.7),
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightpink", alpha=0.7))
    
    ax2.annotate('Conservative\n(Near Retirement)', xy=(65, 35), xytext=(70, 25),
                arrowprops=dict(arrowstyle='->', color='orange', alpha=0.7),
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.7))
    
    plt.tight_layout()
    
    if save_plot:
        plt.savefig('fidelity_allocation_strategy.png', dpi=300, bbox_inches='tight')
        print("📊 Plot saved as 'fidelity_allocation_strategy.png'")
    
    plt.show()
    
    return fig

def main():
    print("🎯 Roth IRA Dollar Cost Averaging Calculator")
    print("=" * 50)
    
    try:
        # Get user inputs
        age = int(input("Enter your current age: "))
        
        print("\nEnter your preferred start date:")
        start_month = int(input("Month (1-12): "))
        start_year = int(input("Year: "))
        start_date = datetime(start_year, start_month, 1)
        
        monthly_contribution = float(input("\nEnter your expected monthly contribution ($): "))
        
        # Calculate contribution limits and schedule
        annual_limit = get_contribution_limit(age)
        months_remaining = calculate_months_remaining(start_date)
        max_monthly_to_hit_limit = annual_limit / months_remaining if months_remaining > 0 else annual_limit
        
        print(f"\n📊 ANALYSIS FOR {start_year}")
        print("=" * 30)
        print(f"Annual Roth IRA limit: ${annual_limit:,.2f}")
        print(f"Months remaining in tax year: {months_remaining}")
        print(f"Monthly amount needed to max out: ${max_monthly_to_hit_limit:.2f}")
        
        # Generate contribution schedule
        schedule, total_annual = generate_contribution_schedule(start_date, monthly_contribution, annual_limit)
        
        print(f"\n📅 CONTRIBUTION SCHEDULE")
        print("=" * 25)
        print(f"{'Month':<15} {'Amount':<10} {'Cumulative':<12}")
        print("-" * 40)
        
        for entry in schedule:
            print(f"{entry['date']:<15} ${entry['amount']:<9.2f} ${entry['cumulative']:<11.2f}")
        
        print(f"\nTotal for {start_year}: ${total_annual:,.2f}")
        if total_annual < annual_limit:
            print(f"⚠️  You'll contribute ${annual_limit - total_annual:,.2f} less than the maximum limit")
        
        # Asset allocation recommendation
        allocation = recommend_allocation_strategy(age, monthly_contribution)
        print(f"\n🎯 FIDELITY PORTFOLIO ALLOCATION (Age {age})")
        print("=" * 45)
        print(f"{'Ticker':<8} {'Fund Name':<25} {'Type':<18} {'%':<4} {'$/Month':<8} {'Exp Ratio'}")
        print("-" * 75)
        
        for ticker, fund in allocation['portfolio'].items():
            print(f"{ticker:<8} {fund['name'][:24]:<25} {fund['type']:<18} "
                  f"{fund['percentage']:>3}% ${fund['monthly_amount']:>6.2f}   {fund['expense_ratio']:.3f}%")
        
        print("-" * 75)
        print(f"Portfolio Summary:")
        print(f"  • Total Funds: {allocation['total_funds']}")
        print(f"  • Stock Allocation: {allocation['stock_percentage']:.0f}%")
        print(f"  • Bond Allocation: {allocation['bond_percentage']:.0f}%")
        print(f"  • Weighted Average Expense Ratio: {allocation['weighted_expense_ratio']:.3f}%")
        print(f"  • Annual Expense on ${monthly_contribution * 12:,.0f}: ${(allocation['weighted_expense_ratio']/100) * monthly_contribution * 12:.2f}")
        
        # Dollar cost averaging advice
        print(f"\n💡 DOLLAR COST AVERAGING TIPS")
        print("=" * 30)
        for i, tip in enumerate(get_dca_timing_advice(), 1):
            print(f"{i}. {tip}")
        
        # Additional recommendations
        print(f"\n🚀 OPTIMIZATION SUGGESTIONS")
        print("=" * 28)
        if monthly_contribution < max_monthly_to_hit_limit:
            print(f"• Consider increasing to ${max_monthly_to_hit_limit:.2f}/month to maximize your {start_year} contribution")
        if total_annual < annual_limit:
            shortfall = annual_limit - total_annual
            print(f"• Make a catch-up contribution of ${shortfall:.2f} before April 15, {start_year + 1}")
        
        print(f"• Review and rebalance your portfolio quarterly")
        print(f"• Fidelity offers $0 minimum investments and no transaction fees for these funds")
        print(f"• Consider FZROX (0.00% expense ratio) as your core holding")
        print(f"• Set up automatic investing for consistent dollar-cost averaging")
        print(f"• Annual portfolio cost is very low at {allocation['weighted_expense_ratio']:.3f}% expense ratio")
        
        # Fund purchase suggestions
        print(f"\n📋 MONTHLY PURCHASE PLAN")
        print("=" * 25)
        print("Set up automatic investments in Fidelity for:")
        for ticker, fund in allocation['portfolio'].items():
            if fund['monthly_amount'] >= 1:  # Only show funds with meaningful allocation
                print(f"  • {ticker}: ${fund['monthly_amount']:.2f} on the same day each month")
        
        # Generate allocation plot
        print(f"\n📊 Generating allocation strategy chart...")
        try:
            plot_allocation_over_time(age, save_plot=True)
        except ImportError:
            print("⚠️  matplotlib not available. Install with: pip install matplotlib")
        except Exception as e:
            print(f"⚠️  Could not generate plot: {e}")
            print("   Make sure you have matplotlib installed: pip install matplotlib")
        
    except ValueError as e:
        print("❌ Invalid input. Please enter numeric values where requested.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()