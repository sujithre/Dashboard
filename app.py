from flask import Flask, render_template, jsonify
import csv
import json
import os
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

# Function to load CSV data
def load_csv_data():
    data = []
    try:
        # Adjust path as needed
        with open('Cosrdetails-Feb.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Convert cost to float if possible
                try:
                    row['Cost'] = float(row['Cost']) if row['Cost'] else 0
                except ValueError:
                    row['Cost'] = 0
                data.append(row)
        return data
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return []

@app.route('/')
def index():
    # Load data to calculate metrics
    data = load_csv_data()
    
    # Calculate overview metrics
    subscription_count = len(set(row.get('SubscriptionId', '') for row in data))
    total_cost = sum(row['Cost'] for row in data)
    
    # Format the total cost for display (in millions)
    formatted_total_cost = "{:.2f}".format(total_cost / 1000000)
    
    # Get top 5 subscriptions
    subscription_costs = defaultdict(float)
    for row in data:
        subscription_name = row.get('SUBSCRIPTIONNAME', 'Unknown')
        if subscription_name.strip():  # Check if not empty
            subscription_costs[subscription_name] += row['Cost']
    
    subscription_result = [{'SUBSCRIPTIONNAME': name, 'Sum_of_Cost': cost, 'Formatted_Cost': "{:.2f}".format(cost / 1000000)} 
                   for name, cost in subscription_costs.items()]
    subscription_result.sort(key=lambda x: x['Sum_of_Cost'], reverse=True)
    top5_subscriptions = subscription_result[:5]
    subscription_total = sum(item['Sum_of_Cost'] for item in top5_subscriptions)
    formatted_subscription_total = "{:.2f}".format(subscription_total / 1000000)
    
    # Get top 5 applications
    app_costs = defaultdict(float)
    for row in data:
        app_name = row.get('APPLICATION', 'Unknown')
        if app_name.strip():  # Check if not empty
            app_costs[app_name] += row['Cost']
    
    app_result = [{'APPLICATION': name, 'Sum_of_Cost': cost, 'Formatted_Cost': "{:.2f}".format(cost / 1000000)} 
                for name, cost in app_costs.items()]
    app_result.sort(key=lambda x: x['Sum_of_Cost'], reverse=True)
    top5_applications = app_result[:5]
    applications_total = sum(item['Sum_of_Cost'] for item in top5_applications)
    formatted_applications_total = "{:.2f}".format(applications_total / 1000000)
    
    # Get top 5 service names
    service_costs = defaultdict(float)
    for row in data:
        service_name = row.get('ServiceName', 'Unknown')
        if service_name.strip():  # Check if not empty
            service_costs[service_name] += row['Cost']
    
    service_result = [{'ServiceName': name, 'Sum_of_Cost': cost, 'Formatted_Cost': "{:.2f}".format(cost / 1000000)} 
                    for name, cost in service_costs.items()]
    service_result.sort(key=lambda x: x['Sum_of_Cost'], reverse=True)
    top5_service_names = service_result[:5]
    service_names_total = sum(item['Sum_of_Cost'] for item in top5_service_names)
    formatted_service_names_total = "{:.2f}".format(service_names_total / 1000000)
    
    # Get top 5 resources
    resource_costs = defaultdict(float)
    for row in data:
        resource_name = row.get('ResourceGroupName', 'Unknown')
        if resource_name.strip():  # Check if not empty
            resource_costs[resource_name] += row['Cost']
    
    resource_result = [{'Resource': name, 'Sum_of_Cost': cost, 'Formatted_Cost': "{:.2f}".format(cost / 1000000)} 
                     for name, cost in resource_costs.items()]
    resource_result.sort(key=lambda x: x['Sum_of_Cost'], reverse=True)
    top5_resources = resource_result[:5]
    resources_total = sum(item['Sum_of_Cost'] for item in top5_resources)
    formatted_resources_total = "{:.2f}".format(resources_total / 1000000)
    
    # Get cost by date
    date_costs = defaultdict(float)
    for row in data:
        start_date = row.get('StartDate', '')
        if start_date:
            date_costs[start_date] += row['Cost']
    
    sorted_dates = sorted(date_costs.keys())
    cost_by_date = {
        'dates': sorted_dates,
        'costs': [date_costs[date] for date in sorted_dates],
        'formatted_costs': ["{:.2f}".format(date_costs[date] / 1000000) for date in sorted_dates]
    }
    
    # Pass metrics to the template
    return render_template(
        'index.html',
        overviewMetrics={
            'subscriptionCount': subscription_count,
            'totalCost': total_cost,
            'formattedTotalCost': formatted_total_cost
        },
        top5Subscriptions=top5_subscriptions,
        top5Applications=top5_applications,
        top5ServiceNames=top5_service_names,
        top5Resources=top5_resources,
        subscriptionTotal=subscription_total,
        formattedSubscriptionTotal=formatted_subscription_total,
        applicationsTotal=applications_total,
        formattedApplicationsTotal=formatted_applications_total,
        serviceNamesTotal=service_names_total,
        formattedServiceNamesTotal=formatted_service_names_total,
        resourcesTotal=resources_total,
        formattedResourcesTotal=formatted_resources_total,
        costByDate=cost_by_date,
        activeTab='overview'
    )

@app.route('/api/top5Subscriptions')
def top5_subscriptions():
    data = load_csv_data()
    
    # Group by SubscriptionName and sum costs
    subscription_costs = defaultdict(float)
    for row in data:
        subscription_name = row.get('SUBSCRIPTIONNAME', 'Unknown')
        if subscription_name.strip():  # Check if not empty
            subscription_costs[subscription_name] += row['Cost']
    
    # Convert to list of dictionaries for sorting
    result = [{'SUBSCRIPTIONNAME': name, 'Sum of Cost': cost} 
             for name, cost in subscription_costs.items()]
    
    # Sort by cost (highest first) and take top 5
    result.sort(key=lambda x: x['Sum of Cost'], reverse=True)
    top5 = result[:5]
    
    # Calculate total
    total = sum(item['Sum of Cost'] for item in top5)
    
    return jsonify({
        'data': top5,
        'total': total
    })

@app.route('/api/top5Applications')
def top5_applications():
    data = load_csv_data()
    
    # Group by APPLICATION and sum costs
    app_costs = defaultdict(float)
    for row in data:
        app_name = row.get('APPLICATION', 'Unknown')
        if app_name.strip():  # Check if not empty
            app_costs[app_name] += row['Cost']
    
    # Convert to list of dictionaries for sorting
    result = [{'APPLICATION': name, 'Sum of Cost': cost} 
             for name, cost in app_costs.items()]
    
    # Sort by cost (highest first) and take top 5
    result.sort(key=lambda x: x['Sum of Cost'], reverse=True)
    top5 = result[:5]
    
    # Calculate total
    total = sum(item['Sum of Cost'] for item in top5)
    
    return jsonify({
        'data': top5,
        'total': total
    })

@app.route('/api/top5ServiceNames')
def top5_service_names():
    data = load_csv_data()
    
    # Group by ServiceName and sum costs
    service_costs = defaultdict(float)
    for row in data:
        service_name = row.get('ServiceName', 'Unknown')
        if service_name.strip():  # Check if not empty
            service_costs[service_name] += row['Cost']
    
    # Convert to list of dictionaries for sorting
    result = [{'ServiceName': name, 'Sum of Cost': cost} 
             for name, cost in service_costs.items()]
    
    # Sort by cost (highest first) and take top 5
    result.sort(key=lambda x: x['Sum of Cost'], reverse=True)
    top5 = result[:5]
    
    # Calculate total
    total = sum(item['Sum of Cost'] for item in top5)
    
    return jsonify({
        'data': top5,
        'total': total
    })

@app.route('/api/top5Resources')
def top5_resources():
    data = load_csv_data()
    
    # Group by ResourceGroupName and sum costs
    resource_costs = defaultdict(float)
    for row in data:
        resource_name = row.get('ResourceGroupName', 'Unknown')
        if resource_name.strip():  # Check if not empty
            resource_costs[resource_name] += row['Cost']
    
    # Convert to list of dictionaries for sorting
    result = [{'Resource': name, 'Sum of Cost': cost} 
             for name, cost in resource_costs.items()]
    
    # Sort by cost (highest first) and take top 5
    result.sort(key=lambda x: x['Sum of Cost'], reverse=True)
    top5 = result[:5]
    
    # Calculate total
    total = sum(item['Sum of Cost'] for item in top5)
    
    return jsonify({
        'data': top5,
        'total': total
    })

@app.route('/api/SumofCost')
def sum_of_cost_by_date():
    data = load_csv_data()
    
    # Group by StartDate and sum costs
    date_costs = defaultdict(float)
    for row in data:
        start_date = row.get('StartDate', '')
        if start_date:
            date_costs[start_date] += row['Cost']
    
    # Sort by date
    sorted_dates = sorted(date_costs.keys())
    
    result = {
        'dates': sorted_dates,
        'costs': [date_costs[date] for date in sorted_dates]
    }
    
    return jsonify(result)

@app.route('/api/data')
def get_data():
    # Get all data for filtering purposes
    data = load_csv_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
