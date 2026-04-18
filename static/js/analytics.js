// Analytics Dashboard JavaScript

class AnalyticsDashboard {
    constructor() {
        this.apiBase = '';
        this.charts = {};
        this.init();
    }

    init() {
        this.loadDashboardData();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // What-If Analysis Form
        document.getElementById('whatIfForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.performWhatIfAnalysis();
        });

        // Recommendations Form
        document.getElementById('recommendationsForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.getLoanRecommendations();
        });
    }

    async loadDashboardData() {
        try {
            const response = await fetch(`${this.apiBase}/analytics-dashboard`);
            const result = await response.json();

            if (result.success) {
                this.updateMetrics(result.data);
                this.createCharts(result.data);
            } else {
                console.error('Failed to load dashboard data:', result.error);
                this.showAlert('Failed to load dashboard data', 'danger');
            }
        } catch (error) {
            console.error('Dashboard loading error:', error);
            this.showAlert('Network error loading dashboard', 'danger');
        }
    }

    updateMetrics(data) {
        // Update key metrics with animation
        this.animateCounter('totalPredictions', data.total_predictions);
        this.animateCounter('lowRiskCount', data.risk_distribution.low);
        this.animateCounter('mediumRiskCount', data.risk_distribution.medium);
        this.animateCounter('highRiskCount', data.risk_distribution.high);
    }

    createCharts(data) {
        this.createRiskDistributionChart(data.risk_distribution);
        this.createTrendsChart(data.recent_trends);
        this.createFeatureImportanceChart(data.feature_importance);
    }

    createRiskDistributionChart(riskData) {
        const ctx = document.getElementById('riskDistributionChart').getContext('2d');
        
        // Destroy existing chart if it exists
        if (this.charts.riskDistribution) {
            this.charts.riskDistribution.destroy();
        }

        this.charts.riskDistribution = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Low Risk', 'Medium Risk', 'High Risk'],
                datasets: [{
                    data: [riskData.low, riskData.medium, riskData.high],
                    backgroundColor: [
                        '#28a745',
                        '#ffc107',
                        '#dc3545'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return `${context.label}: ${context.parsed} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }

    createTrendsChart(trendsData) {
        const ctx = document.getElementById('trendsChart').getContext('2d');
        
        // Destroy existing chart if it exists
        if (this.charts.trends) {
            this.charts.trends.destroy();
        }

        const labels = trendsData.map(trend => `#${trend.index + 1}`);
        const probabilities = trendsData.map(trend => trend.probability * 100);
        const riskColors = trendsData.map(trend => {
            if (trend.risk_level === 'Low') return 'rgba(40, 167, 69, 0.8)';
            if (trend.risk_level === 'Medium') return 'rgba(255, 193, 7, 0.8)';
            return 'rgba(220, 53, 69, 0.8)';
        });

        this.charts.trends = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Default Probability (%)',
                    data: probabilities,
                    borderColor: '#007bff',
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: riskColors,
                    pointBorderColor: riskColors,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Risk: ${context.parsed.y.toFixed(1)}%`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    }

    createFeatureImportanceChart(featureData) {
        const ctx = document.getElementById('featureImportanceChart').getContext('2d');
        
        // Destroy existing chart if it exists
        if (this.charts.featureImportance) {
            this.charts.featureImportance.destroy();
        }

        const features = featureData.feature_importance.slice(0, 10); // Top 10 features
        const labels = features.map(f => f.feature);
        const data = features.map(f => f.importance);
        const colors = features.map(f => f.direction === 'positive' ? '#28a745' : '#dc3545');

        this.charts.featureImportance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Importance (%)',
                    data: data,
                    backgroundColor: colors,
                    borderWidth: 1,
                    borderColor: colors
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y',
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Importance: ${context.parsed.x.toFixed(2)}%`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    }

    async performWhatIfAnalysis() {
        const baseCreditScore = parseInt(document.getElementById('baseCreditScore').value);
        const newCreditScore = parseInt(document.getElementById('newCreditScore').value);
        const baseIncome = parseInt(document.getElementById('baseIncome').value);
        const newIncome = parseInt(document.getElementById('newIncome').value);

        // Create sample applicant data
        const applicantData = {
            age: 35,
            income: baseIncome,
            loan_amount: 25000,
            credit_score: baseCreditScore,
            employment_length: 5,
            debt_to_income_ratio: 0.25,
            home_ownership: 'RENT',
            loan_purpose: 'debt_consolidation',
            employment_status: 'employed'
        };

        const featureChanges = {};
        if (baseCreditScore !== newCreditScore) {
            featureChanges.credit_score = newCreditScore;
        }
        if (baseIncome !== newIncome) {
            featureChanges.income = newIncome;
        }

        if (Object.keys(featureChanges).length === 0) {
            this.showAlert('Please make at least one change to analyze', 'warning');
            return;
        }

        try {
            const response = await fetch(`${this.apiBase}/what-if-analysis`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    applicant_data: applicantData,
                    feature_changes: featureChanges
                })
            });

            const result = await response.json();

            if (result.success) {
                this.displayWhatIfResults(result.data);
            } else {
                this.showAlert(result.error || 'Analysis failed', 'danger');
            }
        } catch (error) {
            console.error('What-if analysis error:', error);
            this.showAlert('Network error during analysis', 'danger');
        }
    }

    displayWhatIfResults(data) {
        const resultsDiv = document.getElementById('whatIfResults');
        
        let html = `
            <div class="alert alert-info">
                <h6><i class="fas fa-info-circle me-2"></i>Base Prediction</h6>
                <p>Risk Level: <span class="badge bg-${this.getRiskBadgeClass(data.base_prediction.risk_level)}">${data.base_prediction.risk_level}</span></p>
                <p>Probability: ${(data.base_prediction.probability * 100).toFixed(1)}%</p>
            </div>
            <h6><i class="fas fa-magic me-2"></i>Scenario Analysis</h6>
            <div class="table-responsive">
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th>Feature</th>
                            <th>Change</th>
                            <th>Risk Impact</th>
                            <th>New Risk Level</th>
                        </tr>
                    </thead>
                    <tbody>
        `;

        data.scenarios.forEach(scenario => {
            const impactIcon = scenario.risk_change === 'decreased' ? 'fa-arrow-down text-success' : 
                              scenario.risk_change === 'increased' ? 'fa-arrow-up text-danger' : 
                              'fa-minus text-muted';
            
            html += `
                <tr>
                    <td>${scenario.feature}</td>
                    <td>${scenario.original_value} → ${scenario.new_value}</td>
                    <td><i class="fas ${impactIcon}"></i> ${scenario.probability_change > 0 ? '+' : ''}${(scenario.probability_change * 100).toFixed(1)}%</td>
                    <td><span class="badge bg-${this.getRiskBadgeClass(scenario.new_risk)}">${scenario.new_risk}</span></td>
                </tr>
            `;
        });

        html += `
                    </tbody>
                </table>
            </div>
        `;

        resultsDiv.innerHTML = html;
    }

    async getLoanRecommendations() {
        const income = parseInt(document.getElementById('recIncome').value);
        const creditScore = parseInt(document.getElementById('recCreditScore').value);
        const debtRatio = parseFloat(document.getElementById('recDebtRatio').value);
        const maxLoan = parseInt(document.getElementById('maxLoan').value);

        const applicantData = {
            age: 35,
            income: income,
            loan_amount: 25000,
            credit_score: creditScore,
            employment_length: 5,
            debt_to_income_ratio: debtRatio,
            home_ownership: 'RENT',
            loan_purpose: 'debt_consolidation',
            employment_status: 'employed'
        };

        try {
            const response = await fetch(`${this.apiBase}/loan-recommendations`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    applicant_data: applicantData,
                    max_loan_amount: maxLoan
                })
            });

            const result = await response.json();

            if (result.success) {
                this.displayRecommendations(result.data);
            } else {
                this.showAlert(result.error || 'Recommendations failed', 'danger');
            }
        } catch (error) {
            console.error('Recommendations error:', error);
            this.showAlert('Network error getting recommendations', 'danger');
        }
    }

    displayRecommendations(data) {
        const resultsDiv = document.getElementById('recommendationsResults');
        
        let html = `
            <div class="alert alert-success">
                <h6><i class="fas fa-lightbulb me-2"></i>Best Recommendation</h6>
                <p><strong>₹${data.best_recommendation.loan_amount.toLocaleString('en-IN')}</strong> - ${data.best_recommendation.recommendation_level}</p>
                <p>Max Safe Amount: <strong>₹${data.max_safe_amount.toLocaleString('en-IN')}</strong></p>
            </div>
            <h6><i class="fas fa-list me-2"></i>All Recommendations</h6>
            <div class="table-responsive">
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th>Loan Amount</th>
                            <th>Risk Level</th>
                            <th>Probability</th>
                            <th>LTV Ratio</th>
                            <th>Recommendation</th>
                        </tr>
                    </thead>
                    <tbody>
        `;

        data.recommendations.forEach(rec => {
            html += `
                <tr>
                    <td>₹${rec.loan_amount.toLocaleString('en-IN')}</td>
                    <td><span class="badge bg-${this.getRiskBadgeClass(rec.risk_level)}">${rec.risk_level}</span></td>
                    <td>${(rec.probability * 100).toFixed(1)}%</td>
                    <td>${rec.loan_to_income_ratio}x</td>
                    <td><span class="badge" style="background-color: ${rec.color}">${rec.recommendation_level}</span></td>
                </tr>
            `;
        });

        html += `
                    </tbody>
                </table>
            </div>
        `;

        resultsDiv.innerHTML = html;
    }

    getRiskBadgeClass(riskLevel) {
        switch (riskLevel) {
            case 'Low': return 'success';
            case 'Medium': return 'warning';
            case 'High': return 'danger';
            default: return 'secondary';
        }
    }

    animateCounter(elementId, targetValue) {
        const element = document.getElementById(elementId);
        const startValue = parseInt(element.textContent) || 0;
        const duration = 1000;
        const steps = 20;
        const stepValue = (targetValue - startValue) / steps;
        let currentStep = 0;

        const timer = setInterval(() => {
            currentStep++;
            const currentValue = Math.round(startValue + (stepValue * currentStep));
            element.textContent = currentValue;

            if (currentStep >= steps) {
                element.textContent = targetValue;
                clearInterval(timer);
            }
        }, duration / steps);
    }

    showAlert(message, type) {
        // Remove existing alerts
        const existingAlerts = document.querySelectorAll('.alert');
        existingAlerts.forEach(alert => alert.remove());

        // Create new alert
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alert.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(alert);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }

    async refreshDashboard() {
        this.showAlert('Refreshing dashboard...', 'info');
        await this.loadDashboardData();
        this.showAlert('Dashboard refreshed successfully!', 'success');
    }
}

// Global function for refresh button
function refreshDashboard() {
    dashboard.refreshDashboard();
}

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new AnalyticsDashboard();
});
