from flask import Flask, render_template, jsonify
import csv
from collections import defaultdict
from functools import lru_cache

app = Flask(__name__)


# Function to load CSV data with caching
@lru_cache(maxsize=1)
def _load_csv_from_file():
    """Load CSV data from file (cached)."""
    data = []
    try:
        # Adjust path as needed
        with open("Cosrdetails-Feb.csv", "r", encoding="utf-8") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                # Convert cost to float if possible
                try:
                    row["Cost"] = float(row["Cost"]) if row["Cost"] else 0
                except ValueError:
                    row["Cost"] = 0
                data.append(row)
        return data
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return []


def load_csv_data():
    """Load CSV data with caching."""
    return _load_csv_from_file()


@app.route("/")
def index():
    """
    Main dashboard route that renders the index page with cost analysis data.

    Returns:
        Rendered HTML template with overview metrics, top 5 costs by various dimensions,
        and filter options for interactive data exploration.
    """
    # Load data to calculate metrics
    data = load_csv_data()

    # Calculate overview metrics
    subscription_count = len(set(row.get("SubscriptionId", "") for row in data))
    total_cost = sum(row["Cost"] for row in data)

    # Format the total cost for display (in millions)
    formatted_total_cost = "{:.2f}".format(total_cost / 1000000)

    # Get top 5 subscriptions
    subscription_costs = defaultdict(float)
    for row in data:
        subscription_name = row.get("SUBSCRIPTIONNAME", "Unknown")
        if subscription_name.strip():  # Check if not empty
            subscription_costs[subscription_name] += row["Cost"]

    subscription_result = [
        {
            "SUBSCRIPTIONNAME": name,
            "Sum_of_Cost": cost,
            "Formatted_Cost": "{:.2f}".format(cost / 1000000),
        }
        for name, cost in subscription_costs.items()
    ]
    subscription_result.sort(key=lambda x: x["Sum_of_Cost"], reverse=True)
    top5_subscriptions = subscription_result[:5]
    subscription_total = sum(item["Sum_of_Cost"] for item in top5_subscriptions)
    formatted_subscription_total = "{:.2f}".format(subscription_total / 1000000)

    # Get top 5 applications
    app_costs = defaultdict(float)
    for row in data:
        app_name = row.get("APPLICATION", "Unknown")
        if app_name.strip():  # Check if not empty
            app_costs[app_name] += row["Cost"]

    app_result = [
        {
            "APPLICATION": name,
            "Sum_of_Cost": cost,
            "Formatted_Cost": "{:.2f}".format(cost / 1000000),
        }
        for name, cost in app_costs.items()
    ]
    app_result.sort(key=lambda x: x["Sum_of_Cost"], reverse=True)
    top5_applications = app_result[:5]
    applications_total = sum(item["Sum_of_Cost"] for item in top5_applications)
    formatted_applications_total = "{:.2f}".format(applications_total / 1000000)

    # Get top 5 service names
    service_costs = defaultdict(float)
    for row in data:
        service_name = row.get("ServiceName", "Unknown")
        if service_name.strip():  # Check if not empty
            service_costs[service_name] += row["Cost"]

    service_result = [
        {
            "ServiceName": name,
            "Sum_of_Cost": cost,
            "Formatted_Cost": "{:.2f}".format(cost / 1000000),
        }
        for name, cost in service_costs.items()
    ]
    service_result.sort(key=lambda x: x["Sum_of_Cost"], reverse=True)
    top5_service_names = service_result[:5]
    service_names_total = sum(item["Sum_of_Cost"] for item in top5_service_names)
    formatted_service_names_total = "{:.2f}".format(service_names_total / 1000000)

    # Get top 5 resources
    resource_costs = defaultdict(float)
    for row in data:
        resource_name = row.get("ResourceGroupName", "Unknown")
        if resource_name.strip():  # Check if not empty
            resource_costs[resource_name] += row["Cost"]

    resource_result = [
        {"Resource": name, "Sum_of_Cost": cost, "Formatted_Cost": "{:.2f}".format(cost / 1000000)}
        for name, cost in resource_costs.items()
    ]
    resource_result.sort(key=lambda x: x["Sum_of_Cost"], reverse=True)
    top5_resources = resource_result[:5]
    resources_total = sum(item["Sum_of_Cost"] for item in top5_resources)
    formatted_resources_total = "{:.2f}".format(resources_total / 1000000)

    # Get cost by date
    date_costs = defaultdict(float)
    for row in data:
        start_date = row.get("StartDate", "")
        if start_date:
            date_costs[start_date] += row["Cost"]

    sorted_dates = sorted(date_costs.keys())
    cost_by_date = {
        "dates": sorted_dates,
        "costs": [date_costs[date] for date in sorted_dates],
        "formatted_costs": ["{:.2f}".format(date_costs[date] / 1000000) for date in sorted_dates],
    }

    # Get unique values for filters
    unique_dates = sorted(set(row.get("StartDate", "") for row in data if row.get("StartDate")))
    unique_subscriptions = sorted(
        set(row.get("SUBSCRIPTIONNAME", "") for row in data if row.get("SUBSCRIPTIONNAME").strip())
    )
    unique_applications = sorted(
        set(row.get("APPLICATION", "") for row in data if row.get("APPLICATION").strip())
    )
    unique_service_names = sorted(
        set(row.get("ServiceName", "") for row in data if row.get("ServiceName").strip())
    )

    # Pass metrics to the template
    return render_template(
        "index.html",
        overviewMetrics={
            "subscriptionCount": subscription_count,
            "totalCost": total_cost,
            "formattedTotalCost": formatted_total_cost,
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
        activeTab="overview",
        dates=unique_dates,
        subscriptions=unique_subscriptions,
        applications=unique_applications,
        serviceNames=unique_service_names,
    )


@app.route("/api/top5Subscriptions")
def top5_subscriptions():
    """
    API endpoint to get the top 5 subscriptions by total cost.

    Returns:
        JSON response containing:
        - data: List of top 5 subscriptions with their costs
        - total: Sum of costs for the top 5 subscriptions
    """
    data = load_csv_data()

    # Group by SubscriptionName and sum costs
    subscription_costs = defaultdict(float)
    for row in data:
        subscription_name = row.get("SUBSCRIPTIONNAME", "Unknown")
        if subscription_name.strip():  # Check if not empty
            subscription_costs[subscription_name] += row["Cost"]

    # Convert to list of dictionaries for sorting
    result = [
        {"SUBSCRIPTIONNAME": name, "Sum of Cost": cost} for name, cost in subscription_costs.items()
    ]

    # Sort by cost (highest first) and take top 5
    result.sort(key=lambda x: x["Sum of Cost"], reverse=True)
    top5 = result[:5]

    # Calculate total
    total = sum(item["Sum of Cost"] for item in top5)

    return jsonify({"data": top5, "total": total})


@app.route("/api/top5Applications")
def top5_applications():
    """
    API endpoint to get the top 5 applications by total cost.

    Returns:
        JSON response containing:
        - data: List of top 5 applications with their costs
        - total: Sum of costs for the top 5 applications
    """
    data = load_csv_data()

    # Group by APPLICATION and sum costs
    app_costs = defaultdict(float)
    for row in data:
        app_name = row.get("APPLICATION", "Unknown")
        if app_name.strip():  # Check if not empty
            app_costs[app_name] += row["Cost"]

    # Convert to list of dictionaries for sorting
    result = [{"APPLICATION": name, "Sum of Cost": cost} for name, cost in app_costs.items()]

    # Sort by cost (highest first) and take top 5
    result.sort(key=lambda x: x["Sum of Cost"], reverse=True)
    top5 = result[:5]

    # Calculate total
    total = sum(item["Sum of Cost"] for item in top5)

    return jsonify({"data": top5, "total": total})


@app.route("/api/top5ServiceNames")
def top5_service_names():
    """
    API endpoint to get the top 5 service names by total cost.

    Returns:
        JSON response containing:
        - data: List of top 5 service names with their costs
        - total: Sum of costs for the top 5 service names
    """
    data = load_csv_data()

    # Group by ServiceName and sum costs
    service_costs = defaultdict(float)
    for row in data:
        service_name = row.get("ServiceName", "Unknown")
        if service_name.strip():  # Check if not empty
            service_costs[service_name] += row["Cost"]

    # Convert to list of dictionaries for sorting
    result = [{"ServiceName": name, "Sum of Cost": cost} for name, cost in service_costs.items()]

    # Sort by cost (highest first) and take top 5
    result.sort(key=lambda x: x["Sum of Cost"], reverse=True)
    top5 = result[:5]

    # Calculate total
    total = sum(item["Sum of Cost"] for item in top5)

    return jsonify({"data": top5, "total": total})


@app.route("/api/top5Resources")
def top5_resources():
    """
    API endpoint to get the top 5 resource groups by total cost.

    Returns:
        JSON response containing:
        - data: List of top 5 resource groups with their costs
        - total: Sum of costs for the top 5 resource groups
    """
    data = load_csv_data()

    # Group by ResourceGroupName and sum costs
    resource_costs = defaultdict(float)
    for row in data:
        resource_name = row.get("ResourceGroupName", "Unknown")
        if resource_name.strip():  # Check if not empty
            resource_costs[resource_name] += row["Cost"]

    # Convert to list of dictionaries for sorting
    result = [{"Resource": name, "Sum of Cost": cost} for name, cost in resource_costs.items()]

    # Sort by cost (highest first) and take top 5
    result.sort(key=lambda x: x["Sum of Cost"], reverse=True)
    top5 = result[:5]

    # Calculate total
    total = sum(item["Sum of Cost"] for item in top5)

    return jsonify({"data": top5, "total": total})


@app.route("/api/SumofCost")
def sum_of_cost_by_date():
    """
    API endpoint to get the sum of costs grouped by date.

    Returns:
        JSON response containing:
        - dates: List of dates in sorted order
        - costs: List of total costs corresponding to each date
    """
    data = load_csv_data()

    # Group by StartDate and sum costs
    date_costs = defaultdict(float)
    for row in data:
        start_date = row.get("StartDate", "")
        if start_date:
            date_costs[start_date] += row["Cost"]

    # Sort by date
    sorted_dates = sorted(date_costs.keys())

    result = {"dates": sorted_dates, "costs": [date_costs[date] for date in sorted_dates]}

    return jsonify(result)


@app.route("/api/data")
def get_data():
    """
    API endpoint to get all cost data for filtering purposes.

    Returns:
        JSON response containing all cost records from the CSV file
    """
    # Get all data for filtering purposes
    data = load_csv_data()
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
