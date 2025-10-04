// AI Task Priority Predictor - API-Enhanced JavaScript Implementation
class TaskPriorityAI {
    constructor() {
        this.apiBaseUrl = 'http://localhost:5000/api';
        this.taskTypes = ['email', 'coding', 'meeting', 'personal', 'research', 'review'];
        this.timePeriods = ['morning', 'afternoon', 'evening'];
        this.urgencyLevels = ['high', 'medium', 'low'];
        this.priorityLevels = ['HIGH', 'MEDIUM', 'LOW'];
        
        this.setupEventListeners();
        this.initializeCharts();
        this.loadAnalytics();
    }

    async loadAnalytics() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/analytics`);
            const data = await response.json();
            
            if (data.success) {
                this.updateChartsWithData(data.analytics);
            }
        } catch (error) {
            console.error('Failed to load analytics:', error);
            // Fallback to local data
            this.initializeCharts();
        }
    }

    async predictPriority(taskType, timeOfDay, urgency) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    task_type: taskType,
                    time_of_day: timeOfDay,
                    urgency: urgency
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                return data.prediction;
            } else {
                throw new Error(data.error || 'Prediction failed');
            }
        } catch (error) {
            console.error('API prediction failed:', error);
            // Fallback to local prediction
            return this.localPredictPriority(taskType, timeOfDay, urgency);
        }
    }

    localPredictPriority(taskType, timeOfDay, urgency) {
        // Fallback local prediction logic
        const rules = [
            { condition: (t, time, u) => u === 'high' && time === 'morning', priority: 'HIGH', confidence: 0.9 },
            { condition: (t, time, u) => t === 'email' && time === 'afternoon', priority: 'MEDIUM', confidence: 0.8 },
            { condition: (t, time, u) => ['coding', 'research'].includes(t) && time === 'morning', priority: 'HIGH', confidence: 0.85 },
            { condition: (t, time, u) => t === 'meeting' && time === 'afternoon', priority: 'MEDIUM', confidence: 0.75 },
            { condition: (t, time, u) => time === 'evening', priority: 'LOW', confidence: 0.7 },
            { condition: (t, time, u) => u === 'high', priority: 'HIGH', confidence: 0.8 },
            { condition: (t, time, u) => u === 'medium', priority: 'MEDIUM', confidence: 0.7 },
            { condition: (t, time, u) => true, priority: 'LOW', confidence: 0.6 }
        ];

        for (const rule of rules) {
            if (rule.condition(taskType, timeOfDay, urgency)) {
                return { priority: rule.priority, confidence: rule.confidence };
            }
        }
    }

    getReasoning(taskType, timeOfDay, urgency) {
        const reasons = [];
        
        if (urgency === 'high') {
            reasons.push('High urgency task');
        }
        if (timeOfDay === 'morning') {
            reasons.push('Morning time slot (typically high productivity)');
        }
        if (['coding', 'research'].includes(taskType)) {
            reasons.push('Creative/technical task');
        }
        if (taskType === 'email') {
            reasons.push('Communication task');
        }
        
        if (reasons.length === 0) {
            reasons.push('Based on learned patterns');
        }
        
        return reasons.join(' + ');
    }

    setupEventListeners() {
        // Form submission
        const form = document.getElementById('taskForm');
        if (form) {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleFormSubmission();
            });
        }

        // Navigation
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href').substring(1);
                this.scrollToSection(targetId);
                this.updateActiveNav(link);
            });
        });

        // CTA button
        const ctaButton = document.querySelector('.cta-button');
        if (ctaButton) {
            ctaButton.addEventListener('click', () => {
                this.scrollToSection('predict');
            });
        }
    }

    async handleFormSubmission() {
        const taskDescription = document.getElementById('taskDescription').value;
        const taskType = document.getElementById('taskType').value;
        const timeOfDay = document.getElementById('timeOfDay').value;
        const urgency = document.getElementById('urgency').value;

        if (!taskDescription || !taskType || !timeOfDay || !urgency) {
            this.showNotification('Please fill in all fields', 'error');
            return;
        }

        this.showLoading();
        
        try {
            const prediction = await this.predictPriority(taskType, timeOfDay, urgency);
            const reasoning = this.getReasoning(taskType, timeOfDay, urgency);
            
            this.displayPrediction({
                description: taskDescription,
                taskType: taskType,
                timeOfDay: timeOfDay,
                urgency: urgency,
                priority: prediction.priority,
                confidence: prediction.confidence,
                reasoning: reasoning
            });
            
            this.showNotification('Prediction completed successfully!', 'success');
        } catch (error) {
            this.showNotification('Prediction failed. Please try again.', 'error');
            console.error('Prediction error:', error);
        } finally {
            this.hideLoading();
        }
    }

    displayPrediction(result) {
        const resultsDiv = document.getElementById('predictionResults');
        const priorityDisplay = document.getElementById('priorityDisplay');
        const confidenceBadge = document.getElementById('confidenceBadge');
        const reasoning = document.getElementById('reasoning');
        const confidenceFill = document.getElementById('confidenceFill');
        const confidenceText = document.getElementById('confidenceText');

        // Update priority display
        priorityDisplay.textContent = result.priority;
        priorityDisplay.className = `priority-display ${result.priority.toLowerCase()}`;

        // Update confidence badge
        confidenceBadge.textContent = `${(result.confidence * 100).toFixed(1)}% confidence`;

        // Update reasoning
        reasoning.textContent = result.reasoning;

        // Update confidence meter
        const confidencePercent = result.confidence * 100;
        confidenceFill.style.width = `${confidencePercent}%`;
        confidenceText.textContent = `${confidencePercent.toFixed(1)}%`;

        // Show results with animation
        resultsDiv.style.display = 'block';
        resultsDiv.scrollIntoView({ behavior: 'smooth' });

        // Update analytics after prediction
        this.loadAnalytics();
    }

    showLoading() {
        document.getElementById('loadingOverlay').style.display = 'flex';
    }

    hideLoading() {
        document.getElementById('loadingOverlay').style.display = 'none';
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Style the notification
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 2rem;
            border-radius: 10px;
            color: white;
            font-weight: 500;
            z-index: 10000;
            animation: slideIn 0.3s ease;
            max-width: 300px;
        `;
        
        // Set background color based on type
        const colors = {
            success: '#51cf66',
            error: '#ff6b6b',
            info: '#667eea'
        };
        notification.style.backgroundColor = colors[type] || colors.info;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    scrollToSection(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
            section.scrollIntoView({ behavior: 'smooth' });
        }
    }

    updateActiveNav(activeLink) {
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        activeLink.classList.add('active');
    }

    initializeCharts() {
        // Initialize with empty data, will be updated by loadAnalytics
        this.updatePriorityChart({});
        this.updateTimeChart({});
        this.updateTaskTypeChart({});
    }

    updateChartsWithData(analytics) {
        this.updatePriorityChart(analytics.priority_distribution || {});
        this.updateTimeChart(analytics.time_distribution || {});
        this.updateTaskTypeChart(analytics.task_type_distribution || {});
    }

    updateCharts() {
        // This will be called by loadAnalytics
        this.loadAnalytics();
    }

    updatePriorityChart(data) {
        const ctx = document.getElementById('priorityChart');
        if (!ctx) return;

        const labels = Object.keys(data);
        const values = Object.values(data);

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels.length > 0 ? labels : ['HIGH', 'MEDIUM', 'LOW'],
                datasets: [{
                    data: values.length > 0 ? values : [10, 20, 15],
                    backgroundColor: ['#ff6b6b', '#ffd93d', '#51cf66'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    updateTimeChart(data) {
        const ctx = document.getElementById('timeChart');
        if (!ctx) return;

        const labels = Object.keys(data);
        const values = Object.values(data);

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels.length > 0 ? labels : ['morning', 'afternoon', 'evening'],
                datasets: [{
                    label: 'Tasks',
                    data: values.length > 0 ? values : [15, 25, 10],
                    backgroundColor: ['#667eea', '#764ba2', '#f093fb'],
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    updateTaskTypeChart(data) {
        const ctx = document.getElementById('taskTypeChart');
        if (!ctx) return;

        const labels = Object.keys(data);
        const values = Object.values(data);

        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels.length > 0 ? labels : ['email', 'coding', 'meeting', 'personal', 'research', 'review'],
                datasets: [{
                    data: values.length > 0 ? values : [8, 12, 6, 5, 7, 4],
                    backgroundColor: [
                        '#667eea', '#764ba2', '#f093fb', 
                        '#4facfe', '#00f2fe', '#43e97b'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }
}

// Quick prediction function for demo buttons
function quickPredict(description, taskType, timeOfDay, urgency) {
    // Fill the form
    document.getElementById('taskDescription').value = description;
    document.getElementById('taskType').value = taskType;
    document.getElementById('timeOfDay').value = timeOfDay;
    document.getElementById('urgency').value = urgency;
    
    // Trigger form submission
    document.getElementById('taskForm').dispatchEvent(new Event('submit'));
}

// Scroll to section function
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    window.taskAI = new TaskPriorityAI();
    
    // Add smooth scrolling to all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add scroll-based navigation highlighting
    window.addEventListener('scroll', () => {
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.nav-link');
        
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (scrollY >= (sectionTop - 200)) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
