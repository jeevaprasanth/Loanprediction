// Loan Default Prediction System - Frontend JavaScript

class LoanPredictionApp {
    constructor() {
        this.apiBase = 'http://localhost:5000';
        this.lastPredictionData = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadHistory();
    }

    setupEventListeners() {
        // Form submission
        document.getElementById('predictionForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.makePrediction();
        });

        // What-If Analysis Form (Main Page)
        const whatIfFormMain = document.getElementById('whatIfFormMain');
        if (whatIfFormMain) {
            whatIfFormMain.addEventListener('submit', (e) => {
                e.preventDefault();
                this.performWhatIfAnalysis();
            });
        }

        // Recommendations Form (Main Page)
        const recommendationsFormMain = document.getElementById('recommendationsFormMain');
        if (recommendationsFormMain) {
            recommendationsFormMain.addEventListener('submit', (e) => {
                e.preventDefault();
                this.getLoanRecommendations();
            });
        }

        // Real-time validation
        const inputs = document.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearValidation(input));
        });
    }

    validateField(field) {
        const value = field.value.trim();
        const fieldName = field.name;
        let isValid = true;
        let message = '';

        switch (fieldName) {
            case 'applicant_name':
                if (value.length < 3) {
                    isValid = false;
                    message = 'Name must be at least 3 characters long';
                } else if (value.length > 100) {
                    isValid = false;
                    message = 'Name must be less than 100 characters';
                } else if (!/^[a-zA-Z\s]+$/.test(value)) {
                    isValid = false;
                    message = 'Name should only contain letters and spaces';
                }
                break;
            case 'age':
                const age = parseInt(value);
                if (age < 18 || age > 80) {
                    isValid = false;
                    message = 'Age must be between 18 and 80';
                }
                break;
            case 'income':
                const income = parseInt(value);
                if (income < 200000 || income > 30000000) {
                    isValid = false;
                    message = 'Income must be between ₹2L and ₹3Cr';
                }
                break;
            case 'credit_score':
                const credit = parseInt(value);
                if (credit < 300 || credit > 850) {
                    isValid = false;
                    message = 'Credit score must be between 300 and 850';
                }
                break;
            case 'loan_amount':
                const loan = parseInt(value);
                if (loan < 50000 || loan > 50000000) {
                    isValid = false;
                    message = 'Loan amount must be between ₹50K and ₹5Cr';
                }
                break;
            case 'employment_length':
                const empLength = parseFloat(value);
                if (empLength < 0 || empLength > 40) {
                    isValid = false;
                    message = 'Employment length must be between 0 and 40 years';
                }
                break;
            case 'debt_to_income_ratio':
                const ratio = parseFloat(value);
                if (ratio < 0 || ratio > 0.6) {
                    isValid = false;
                    message = 'Debt-to-income ratio must be between 0 and 0.6';
                }
                break;
        }

        // Check if required
        if (!value && field.hasAttribute('required')) {
            isValid = false;
            message = 'This field is required';
        }

        // Field-specific validation
        if (value && isValid) {
            switch (fieldName) {
                case 'age':
                    const age = parseInt(value);
                    if (age < 18 || age > 80) {
                        isValid = false;
                        message = 'Age must be between 18 and 80';
                    }
                    break;
                case 'income':
                    const income = parseInt(value);
                    if (income < 200000 || income > 30000000) {
                        isValid = false;
                        message = 'Income must be between ₹2L and ₹3Cr';
                    }
                    break;
                case 'credit_score':
                    const credit = parseInt(value);
                    if (credit < 300 || credit > 850) {
                        isValid = false;
                        message = 'Credit score must be between 300 and 850';
                    }
                    break;
                case 'loan_amount':
                    const loan = parseInt(value);
                    if (loan < 50000 || loan > 50000000) {
                        isValid = false;
                        message = 'Loan amount must be between ₹50K and ₹5Cr';
                    }
                    break;
                case 'employment_length':
                    const empLength = parseFloat(value);
                    if (empLength < 0 || empLength > 40) {
                        isValid = false;
                        message = 'Employment length must be between 0 and 40 years';
                    }
                    break;
                case 'debt_to_income_ratio':
                    const ratio = parseFloat(value);
                    if (ratio < 0 || ratio > 0.6) {
                        isValid = false;
                        message = 'Debt-to-income ratio must be between 0 and 0.6';
                    }
                    break;
            }
        }

        // Apply validation
        if (!isValid) {
            field.classList.add('is-invalid');
            this.showFieldError(field, message);
        } else if (value) {
            field.classList.add('is-valid');
        }

        return isValid;
    }

    clearValidation(field) {
        field.classList.remove('is-invalid', 'is-valid');
        this.hideFieldError(field);
    }

    showFieldError(field, message) {
        let feedback = field.parentNode.querySelector('.invalid-feedback');
        if (!feedback) {
            feedback = document.createElement('div');
            feedback.className = 'invalid-feedback';
            field.parentNode.appendChild(feedback);
        }
        feedback.textContent = message;
    }

    hideFieldError(field) {
        const feedback = field.parentNode.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.remove();
        }
    }

    async makePrediction() {
        // Validate all fields
        const form = document.getElementById('predictionForm');
        const inputs = form.querySelectorAll('input, select');
        let isFormValid = true;

        inputs.forEach(input => {
            if (!this.validateField(input)) {
                isFormValid = false;
            }
        });

        if (!isFormValid) {
            this.showAlert('Please correct the errors in the form', 'danger');
            return;
        }

        // Show loading state
        const predictBtn = document.getElementById('predictBtn');
        const originalText = predictBtn.innerHTML;
        predictBtn.innerHTML = '<span class="loading-spinner"></span> Processing...';
        predictBtn.disabled = true;

        try {
            // Collect form data
            const formData = new FormData(form);
            const data = {};
            formData.forEach((value, key) => {
                if (key === 'income' || key === 'loan_amount') {
                    data[key] = parseFloat(value);
                } else if (key === 'debt_to_income_ratio') {
                    data[key] = parseFloat(value);
                } else if (key === 'age' || key === 'credit_score' || key === 'employment_length') {
                    data[key] = parseInt(value);
                } else {
                    data[key] = value;
                }
            });

            // Make API call
            const response = await fetch(`${this.apiBase}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            console.log('API Response:', result);

            if (result.success) {
                this.displayResults(result.result, data);
                this.showAlert(result.message, 'success');
                this.loadHistory(); // Refresh history
            } else {
                this.showAlert(result.error || 'Prediction failed', 'danger');
            }
        } catch (error) {
            console.error('Prediction error:', error);
            this.showAlert('Network error. Please try again.', 'danger');
        } finally {
            // Restore button
            predictBtn.innerHTML = originalText;
            predictBtn.disabled = false;
        }
    }

    displayResults(result, applicantData) {
        console.log('Displaying results:', result);
        const resultsPanel = document.getElementById('resultsPanel');
        console.log('Results panel found:', resultsPanel);
        
        // Store last prediction data for explainable AI
        this.lastPredictionData = {
            applicant_data: applicantData,
            result: result
        };
        
        // Determine risk class
        let riskClass = 'success';
        let riskIcon = 'fa-check-circle';
        let riskMessage = '';
        
        switch(result.risk_level) {
            case 'Low':
                riskClass = 'success';
                riskIcon = 'fa-check-circle';
                riskMessage = 'Low risk - Good chance of approval';
                break;
            case 'Medium':
                riskClass = 'warning';
                riskIcon = 'fa-exclamation-triangle';
                riskMessage = 'Medium risk - Some concerns';
                break;
            case 'High':
                riskClass = 'danger';
                riskIcon = 'fa-times-circle';
                riskMessage = 'High risk - Unlikely to be approved';
                break;
        }
        
        // Calculate probability percentage
        const probabilityPercent = (result.probability * 100).toFixed(1);
        console.log('Probability percent:', probabilityPercent);
        
        const resultsHTML = `
            <div class="alert alert-${riskClass} d-flex align-items-center" role="alert">
                <div class="me-3">
                    <i class="fas ${riskIcon} fa-2x"></i>
                </div>
                <div class="flex-grow-1">
                    <h5 class="mb-1">Risk Assessment: ${result.risk_level}</h5>
                    <p class="mb-0">${riskMessage}</p>
                    ${result.prediction === 1 ? 
                        '<p><strong>Prediction:</strong> Likely to default on loan</p>' : 
                        '<p><strong>Prediction:</strong> Unlikely to default on loan</p>'
                    }
                    <div class="mt-2">
                        <strong>Probability: </strong>
                        <div class="progress" style="height: 20px;">
                            <div class="progress-bar bg-${riskClass}" role="progressbar" 
                                 style="width: ${probabilityPercent}%" 
                                 aria-valuenow="${probabilityPercent}" 
                                 aria-valuemin="0" aria-valuemax="100">
                                ${probabilityPercent}%
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="mt-3">
                <small class="text-muted">
                    <i class="fas fa-info-circle me-1"></i>
                    Based on applicant's financial profile and credit history
                </small>
            </div>
            
            <div class="mt-3">
                <button class="btn btn-outline-primary btn-sm w-100" onclick="app.resetForm()">
                    <i class="fas fa-redo me-2"></i>New Prediction
                </button>
            </div>
        `;
        
        console.log('Setting results HTML...');
        resultsPanel.innerHTML = resultsHTML;
        console.log('Results HTML set successfully');
    }

    async performWhatIfAnalysis() {
        const baseCreditScore = parseInt(document.getElementById('baseCreditScoreMain').value);
        const newCreditScore = parseInt(document.getElementById('newCreditScoreMain').value);
        const baseIncome = parseInt(document.getElementById('baseIncomeMain').value);
        const newIncome = parseInt(document.getElementById('newIncomeMain').value);

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
        const resultsDiv = document.getElementById('whatIfResultsMain');
        
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
        const income = parseInt(document.getElementById('recIncomeMain').value);
        const creditScore = parseInt(document.getElementById('recCreditScoreMain').value);
        const debtRatio = parseFloat(document.getElementById('recDebtRatioMain').value);
        const maxLoan = parseInt(document.getElementById('maxLoanMain').value);

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
        const resultsDiv = document.getElementById('recommendationsResultsMain');
        
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

    async explainLastPrediction() {
        if (!this.lastPredictionData) {
            this.showAlert('Please make a prediction first', 'warning');
            return;
        }

        try {
            const response = await fetch(`${this.apiBase}/explain-prediction`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    applicant_data: this.lastPredictionData.applicant_data
                })
            });

            const result = await response.json();

            if (result.success) {
                this.displayExplanation(result.data);
            } else {
                this.showAlert(result.error || 'Explanation failed', 'danger');
            }
        } catch (error) {
            console.error('Explanation error:', error);
            this.showAlert('Network error getting explanation', 'danger');
        }
    }

    displayExplanation(data) {
        const resultsDiv = document.getElementById('explainResults');
        
        let html = `
            <div class="alert alert-primary">
                <h6><i class="fas fa-brain me-2"></i>AI Explanation</h6>
                <p>${data.summary}</p>
            </div>
            <h6><i class="fas fa-list-ol me-2"></i>Top Contributing Factors</h6>
            <div class="table-responsive">
                <table class="table table-sm">
                    <thead>
                        <tr>
                            <th>Feature</th>
                            <th>Value</th>
                            <th>Impact</th>
                            <th>Explanation</th>
                        </tr>
                    </thead>
                    <tbody>
        `;

        data.contributions.slice(0, 5).forEach(contribution => {
            const impactIcon = contribution.impact === 'positive' ? 'fa-arrow-up text-success' : 'fa-arrow-down text-danger';
            
            html += `
                <tr>
                    <td>${contribution.feature}</td>
                    <td>${contribution.value}</td>
                    <td><i class="fas ${impactIcon}"></i> ${contribution.impact}</td>
                    <td><small>${contribution.explanation}</small></td>
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

    resetForm() {
        const form = document.getElementById('predictionForm');
        form.reset();
        
        // Clear validation
        const inputs = form.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.classList.remove('is-valid', 'is-invalid');
            this.hideFieldError(input);
        });
        
        // Clear results
        document.getElementById('resultsPanel').innerHTML = `
            <div class="text-center text-muted py-5">
                <i class="fas fa-clipboard-list fa-3x mb-3"></i>
                <p>Complete the form and click "Predict Loan Risk" to see results</p>
            </div>
        `;
    }

    async loadHistory() {
        try {
            const response = await fetch(`${this.apiBase}/history?limit=20`);
            const result = await response.json();

            if (result.success) {
                this.displayHistory(result.history);
            } else {
                console.error('Failed to load history:', result.error);
            }
        } catch (error) {
            console.error('History loading error:', error);
        }
    }

    displayHistory(history) {
        const historyTableBody = document.getElementById('historyTableBody');
        
        if (!history || history.length === 0) {
            historyTableBody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center text-muted py-4">
                        <i class="fas fa-inbox fa-2x mb-2"></i>
                        <div>No prediction history available</div>
                    </td>
                </tr>
            `;
            return;
        }
        
        historyTableBody.innerHTML = history.map(record => {
            const riskClass = `risk-${record.risk_level.toLowerCase()}`;
            const riskBadge = `badge bg-${this.getRiskBadgeClass(record.risk_level)}`;
            const formattedDate = new Date(record.timestamp).toLocaleString('en-IN', {
                day: '2-digit',
                month: 'short',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
            
            return `
                <tr class="history-row">
                    <td>
                        <small class="text-muted">${formattedDate}</small>
                    </td>
                    <td>
                        <strong>${record.applicant_data.applicant_name || 'N/A'}</strong>
                    </td>
                    <td>${record.applicant_data.age}</td>
                    <td>₹${record.applicant_data.income.toLocaleString('en-IN')}</td>
                    <td>${record.applicant_data.credit_score}</td>
                    <td>₹${record.applicant_data.loan_amount.toLocaleString('en-IN')}</td>
                    <td>
                        <span class="badge ${riskBadge} ${riskClass}">
                            ${record.risk_level}
                        </span>
                    </td>
                </tr>
            `;
        }).join('');
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
}

// Model Info Functions
async function showModelInfo() {
    const modal = new bootstrap.Modal(document.getElementById('modelInfoModal'));
    const content = document.getElementById('modelInfoContent');
    
    content.innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `;
    
    modal.show();

    try {
        const response = await fetch('/model_info');
        const result = await response.json();

        if (result.success) {
            content.innerHTML = `
                <div class="row">
                    <div class="col-md-6">
                        <h6 class="text-primary">Model Details</h6>
                        <table class="table table-sm">
                            <tr>
                                <td><strong>Algorithm:</strong></td>
                                <td>${result.model_name}</td>
                            </tr>
                            <tr>
                                <td><strong>Accuracy:</strong></td>
                                <td>${result.accuracy}</td>
                            </tr>
                            <tr>
                                <td><strong>AUC Score:</strong></td>
                                <td>${result.auc_score}</td>
                            </tr>
                            <tr>
                                <td><strong>Description:</strong></td>
                                <td>${result.description}</td>
                            </tr>
                        </table>
                    </div>
                    <div class="col-md-6">
                        <h6 class="text-primary">Features Used</h6>
                        <ul class="list-unstyled">
                            ${result.features.map(feature => `
                                <li><i class="fas fa-check text-success me-2"></i>${feature.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</li>
                            `).join('')}
                        </ul>
                    </div>
                </div>
                <div class="mt-3">
                    <div class="alert alert-info">
                        <i class="fas fa-info-circle me-2"></i>
                        This model was trained on synthetic loan data and should be used for demonstration purposes only.
                    </div>
                </div>
            `;
        } else {
            content.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-triangle me-2"></i>
                    Failed to load model information: ${result.error}
                </div>
            `;
        }
    } catch (error) {
        content.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Failed to load model information. Please try again.
            </div>
        `;
    }
}

// Global functions
function loadHistory() {
    app.loadHistory();
}

function explainLastPrediction() {
    app.explainLastPrediction();
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.app = new LoanPredictionApp();
});
