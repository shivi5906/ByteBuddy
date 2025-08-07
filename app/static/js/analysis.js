class ByteBuddyAnalyzer {
    constructor() {
        this.currentSessionId = null;
        this.completedTasks = new Set();
        this.progressInterval = null;

        // Initialize form handling
        this.initializeFormHandling();
    }

    initializeFormHandling() {
        const form = document.getElementById('codeAnalysisForm');
        if (form) {
            form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }
    }

    async handleFormSubmit(event) {
        event.preventDefault();

        const code = document.getElementById('code-input').value;
        const language = document.getElementById('language').value;

        if (!code || code.trim() === '') {
            this.showAlert('Please enter some code to analyze!', 'error');
            return;
        }
        // Get selected options
        const selectedOptions = [];
        const checkboxes = document.querySelectorAll('input[name="options"]:checked');
        checkboxes.forEach(cb => selectedOptions.push(cb.value));

        if (selectedOptions.length === 0) {
            this.showAlert('Please select at least one analysis option!', 'error');
            return;
        }
        // Show loading state
        this.showLoadingState();

        try {
            // Create form data that matches your backend
            const formData = new FormData();
            formData.append('code', code);
            formData.append('language', language);
            formData.append('options', selectedOptions.join(','));
            console.log('🚀 Sending request to /analyze/code...');

            const response = await fetch('/analyze/code', {
                method: 'POST',
                body: formData
            });

            console.log(`📡 Response status: ${response.status}`);
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({'results': {'error': 'Server returned a non-JSON error response.'}}));
                throw new Error(errorData.results?.error || `HTTP error! status: ${response.status}`);
            }
            const result = await response.json();
            console.log('📥 Analysis result received:', result);

            // Validate the response format
            if (!this.validateResponse(result)) {
                throw new Error('Invalid response format from server');
            }
            
            if (result.results.success === false) {
                 throw new Error(result.results.error || 'Analysis failed on the server.');
            }

            // Store session ID if available
            this.currentSessionId = result.results?.analysis_id || Date.now().toString();

            // Process results using the agent's output format
            this.processAnalysisResults(result, code);

            this.hideLoadingState();
            this.showAlert('Analysis completed successfully!', 'success');

        } catch (error) {
            console.error('❌ Analysis failed:', error);
            this.showAlert(`Analysis failed: ${error.message}`, 'error');
            this.hideLoadingState();
        }
    }

    /**
     * Validates that the response has the expected structure
     */
    validateResponse(result) {
        console.log('🔍 Validating response structure...');

        if (!result || !result.results) {
            console.error('❌ Missing results property in response');
            return false;
        }

        const required = [
            'complexity_analysis',
            'documentation',
            'refactoring_suggestions',
            'improvement_suggestions'
        ];

        const missing = required.filter(prop => !(prop in result.results));
        if (missing.length > 0) {
            console.warn('⚠️ Missing properties:', missing);
        }

        console.log('✅ Response structure validated');
        return true;
    }

    /**
     * Processes the agent analysis results and updates all tabs
     */
    processAnalysisResults(result, code) {
        console.log('🔄 Processing agent analysis results...');
        const analysisData = result.results;
        console.log('📊 Analysis data:', analysisData);

        // Store the analysis ID
        if (analysisData.analysis_id) {
            this.currentSessionId = analysisData.analysis_id;
            console.log('📝 Session ID set to:', this.currentSessionId);
        }

        try {
            // 1. Update Complexity Tab
            console.log('🧮 Updating complexity tab...');
            const complexityData = this.parseComplexityFromAgent(analysisData.complexity_analysis);
            if (complexityData) {
                this.updateComplexityTab(complexityData);
                console.log('✅ Complexity tab updated');
            } else {
                this.setComplexityTabError('Could not parse complexity data');
                console.warn('❌ Could not parse complexity');
            }

            // 2. Update Documentation Tab
            console.log('📄 Updating documentation tab...');
            if (analysisData.documentation && analysisData.documentation.trim() !== 'No documentation generated') {
                this.updateDocumentationTab({
                    content: analysisData.documentation
                });
                console.log('✅ Documentation tab updated');
            } else {
                this.setDocumentationTabError('No documentation was generated.');
                console.warn('❌ No documentation found');
            }

            // 3. Update Refactoring Tab
            console.log('🔧 Updating refactoring tab...');
            const refactoringSuggestions = this.parseRefactoringSuggestionsFromAgent(analysisData.refactoring_suggestions);
            if (refactoringSuggestions.length > 0) {
                this.updateRefactoringTab({
                    suggestions: refactoringSuggestions
                });
                console.log('✅ Refactoring tab updated');
            } else {
                this.setRefactoringTabError('No refactoring suggestions available.');
                console.warn('❌ No refactoring suggestions');
            }

            // 4. Update Structure Tab (with agent visualization)
            console.log('📊 Updating structure tab...');
            const structureData = {
                functions_count: this.countFunctions(code),
                lines_count: code.split('\n').length,
                complexity_score: complexityData ? complexityData.score || 5 : 5,
                dependencies: 0,
                structure_image: analysisData.structure_img // This comes from agent
            };
            this.updateStructureTab(structureData);
            console.log('✅ Structure tab updated with image:', analysisData.structure_img);

            // 5. Update Improvements Tab
            console.log('💡 Updating improvements tab...');
            this.updateImprovementsTab({
                performance_score: complexityData ? complexityData.performance_score || 65 : 65,
                readability_score: 75,
                documentation_score: analysisData.documentation ? 80 : 30,
                testing_score: 10,
                content: analysisData.improvement_suggestions || 'No specific improvements suggested'
            });
            console.log('✅ Improvements tab updated');

            // Switch to complexity tab to show results
            if (typeof switchTab === 'function') {
                switchTab('complexity');
            }
            console.log('🎉 All tabs updated successfully!');
        } catch (error) {
            console.error('❌ Error processing analysis results:', error);
            this.showAlert(`Error displaying results: ${error.message}`, 'error');
        }
    }

    /**
     * Parse complexity analysis from agent's text output
     */
    parseComplexityFromAgent(complexityText) {
        if (!complexityText || typeof complexityText !== 'string') {
            console.warn('No complexity text to parse');
            return null;
        }
        console.log('🔍 Parsing agent complexity text:', complexityText.substring(0, 200) + '...');
        // Extract time and space complexity using regex
        const timeMatch = complexityText.match(/Time Complexity:\s*([O\(][^)]*\))/i) ||
            complexityText.match(/([O\(][^)]*\))/); // Fallback

        const spaceMatch = complexityText.match(/Space Complexity:\s*([O\(][^)]*\))/i);
        const timeComplexity = timeMatch ? timeMatch[1] : 'O(n)';
        const spaceComplexity = spaceMatch ? spaceMatch[1] : 'O(1)';
        console.log('📊 Extracted complexities:', {
            time: timeComplexity,
            space: spaceComplexity
        });

        return {
            time_complexity: timeComplexity,
            time_color: this.getComplexityColor(timeComplexity),
            space_complexity: spaceComplexity,
            space_color: this.getComplexityColor(spaceComplexity),
            performance_score: this.calculatePerformanceScore({
                time: timeComplexity
            }),
            score: this.calculateComplexityScore({
                time: timeComplexity,
                space: spaceComplexity
            }),
            full_analysis: complexityText
        };
    }

    /**
     * Parse refactoring suggestions from agent's text output
     */
    parseRefactoringSuggestionsFromAgent(refactoringText) {
        if (!refactoringText || refactoringText.includes("No refactoring suggestions")) return [];

        console.log('🔧 Parsing agent refactoring text...');

        // Split by lines and clean up
        const lines = refactoringText
            .split(/\n+/)
            .map(line => line.trim())
            .filter(line => line.length > 0)
            .filter(line => !line.match(/^(REFACTORING|SUGGESTIONS?|={3,}|-{3,})/i));

        return lines.map((line, index) => {
            // Clean bullet points
            const cleanLine = line.replace(/^[\d\.\-\*\+•\s]+/, '').trim();

            return {
                id: index,
                title: `Refactoring Suggestion ${index + 1}`,
                description: cleanLine,
                priority: index < 2 ? 'High' : 'Medium',
                category: 'Refactoring',
                color: 'electric-blue'
            };
        });
    }

    /**
     * Helper functions for complexity calculation
     */
    getComplexityColor(complexity) {
        const c = String(complexity).toLowerCase();
        if (c.includes('1')) return '#00C851'; // Green
        if (c.includes('log n')) return '#33b5e5'; // Blue
        if (c.includes('n log n')) return '#FF8800'; // Orange
        if (c.includes('n^2') || c.includes('n²')) return '#FF4444'; // Red
        if (c.includes('2^n')) return '#FF1744'; // Bright Red
        if (c.includes('n')) return '#FFA500'; // Amber
        return '#FF4444'; // Default to red
    }

    calculatePerformanceScore(complexityAnalysis) {
        if (!complexityAnalysis) return 50;

        const timeComplexity = complexityAnalysis.time || 'O(n)';

        const performanceScores = {
            'O(1)': 95,
            'O(log n)': 85,
            'O(n)': 70,
            'O(n log n)': 55,
            'O(n²)': 25,
            'O(n^2)': 25,
            'O(2^n)': 5
        };

        return performanceScores[timeComplexity] || 50;
    }

    calculateComplexityScore(complexityAnalysis) {
        if (!complexityAnalysis) return 5;

        const timeComplexity = complexityAnalysis.time || 'O(n)';
        const spaceComplexity = complexityAnalysis.space || 'O(1)';

        const complexityScores = {
            'O(1)': 10,
            'O(log n)': 8,
            'O(n)': 6,
            'O(n log n)': 4,
            'O(n²)': 2,
            'O(n^2)': 2,
            'O(2^n)': 1
        };

        const timeScore = complexityScores[timeComplexity] || 5;
        const spaceScore = complexityScores[spaceComplexity] || 8;

        return Math.round((timeScore + spaceScore) / 2);
    }

    countFunctions(code) {
        const functionPatterns = [
            /function\s+\w+/g, // function name()
            /const\s+\w+\s*=\s*\(/g, // const name = (
            /def\s+\w+/g, // Python functions
            /public\s+(static\s+)?\w+\s+\w+\s*\(/g, // Java methods
            /private\s+(static\s+)?\w+\s+\w+\s*\(/g, // Java methods
            /func\s+\w+\s*\(/g, // Go functions
            /fn\s+\w+\s*\(/g, // Rust functions
            /\w+\s+\w+\s*\([^)]*\)\s*{/g // C/C++ style functions
        ];

        let count = 0;
        functionPatterns.forEach(pattern => {
            const matches = code.match(pattern);
            if (matches) count += matches.length;
        });

        return Math.max(1, count);
    }

    // Tab update methods
    updateComplexityTab(data) {
        console.log('Updating complexity tab with:', data);
        const container = document.getElementById('complexity-content');
        if (!container) return;
        
        container.innerHTML = `
            <div class="terminal-window flex-1">
                <div class="flex items-center mb-4">
                    <div class="w-3 h-3 rounded-full bg-success-green mr-3"></div>
                    <h3 class="font-bold text-success-green text-lg">Time Complexity</h3>
                </div>
                <div class="text-center py-4">
                    <p class="text-3xl font-mono font-bold" style="color: ${data.time_color};">${data.time_complexity}</p>
                    <p class="text-sm text-terminal-text mt-2">${this.getComplexityLevel(data.time_complexity)} time complexity detected</p>
                </div>
            </div>
            <div class="terminal-window flex-1">
                <div class="flex items-center mb-4">
                    <div class="w-3 h-3 rounded-full bg-info-blue mr-3"></div>
                    <h3 class="font-bold text-info-blue text-lg">Space Complexity</h3>
                </div>
                <div class="text-center py-4">
                    <p class="text-3xl font-mono font-bold" style="color: ${data.space_color};">${data.space_complexity}</p>
                    <p class="text-sm text-terminal-text mt-2">${this.getComplexityLevel(data.space_complexity)} space complexity</p>
                </div>
            </div>
        `;
    }

    getComplexityLevel(complexity) {
        const levels = {
            'O(1)': 'Excellent',
            'O(log n)': 'Good',
            'O(n)': 'Fair',
            'O(n log n)': 'Moderate',
            'O(n²)': 'Poor',
            'O(n^2)': 'Poor',
            'O(2^n)': 'Exponential'
        };
        return levels[complexity] || 'Unknown';
    }

    updateStructureTab(data) {
        console.log('Updating structure tab with:', data);

        // Update metrics
        document.getElementById('functions-count').textContent = data.functions_count;
        document.getElementById('lines-count').textContent = data.lines_count;
        document.getElementById('complexity-score').textContent = data.complexity_score;

        // Update structure image from agent
        const imageContainer = document.getElementById('structure-image-container');
        if (imageContainer && data.structure_image) {
            console.log('📊 Loading agent visualization:', data.structure_image);
            imageContainer.innerHTML = `
                <img src="${data.structure_image}?t=${new Date().getTime()}" alt="Code Structure Visualization"
                     class="w-full h-auto rounded max-h-96 object-contain"
                     onload="console.log('✅ Agent visualization loaded successfully')"
                     onerror="this.outerHTML='<div class=\\'text-center text-terminal-border p-8\\'>Visualization could not be loaded. Check server logs.</div>'">
            `;
        } else if (imageContainer) {
            imageContainer.innerHTML = `<div class="text-center text-terminal-border p-8">No visualization was generated.</div>`;
        }
    }

    updateRefactoringTab(data) {
        console.log('Updating refactoring tab with:', data);

        const container = document.querySelector('#refactoring .space-y-6');
        if (!container || !data.suggestions) return;
        const suggestionsHTML = data.suggestions.map(suggestion => `
            <div class="border-l-4 border-electric-blue pl-4">
                <div class="flex items-center mb-2">
                    <span class="text-electric-blue font-bold mr-2">${suggestion.priority} PRIORITY</span>
                    <span class="bg-electric-blue text-terminal-bg px-2 py-1 rounded text-xs">${suggestion.category}</span>
                </div>
                <h4 class="font-bold text-terminal-white mb-2">${suggestion.title}</h4>
                <p class="text-sm text-terminal-text">${suggestion.description}</p>
            </div>
        `).join('');
        container.innerHTML = suggestionsHTML || '<div class="text-center text-terminal-border">No refactoring suggestions available.</div>';
    }

    updateDocumentationTab(data) {
        console.log('Updating documentation tab with content length:', data.content.length);

        const contentElement = document.querySelector('#documentation .prose');
        if (contentElement) {
            contentElement.innerHTML = this.markdownToHtml(data.content);
        }
    }

    updateImprovementsTab(data) {
        console.log('Updating improvements tab with:', data);
        
        const improvementsSection = document.getElementById('improvements-content');
        if (improvementsSection && data.content) {
             improvementsSection.innerHTML = `<pre class="text-xs text-terminal-text whitespace-pre-wrap font-mono">${data.content}</pre>`;
        }
        
        // Update circular progress indicators
        const scores = [
            { value: data.performance_score, color: this.getScoreColor(data.performance_score) },
            { value: data.readability_score, color: this.getScoreColor(data.readability_score) },
            { value: data.documentation_score, color: this.getScoreColor(data.documentation_score) },
            { value: data.testing_score, color: this.getScoreColor(data.testing_score) }
        ];
        const circularProgress = document.querySelectorAll('#improvements .circular-progress');
        circularProgress.forEach((circle, index) => {
            if (scores[index]) {
                this.updateCircularProgress(circle, scores[index].value, scores[index].color);
            }
        });
    }

    getScoreColor(score) {
        if (score < 30) return '#FF4757'; // Red
        if (score < 60) return '#FFA726'; // Orange
        if (score < 80) return '#ffbb33'; // Amber
        return '#2ED573'; // Green
    }

    updateCircularProgress(container, percentage, color) {
        const circle = container.querySelector('circle.progress-ring-circle');
        const text = container.querySelector('.progress-text');

        if (circle && text) {
            const radius = circle.r.baseVal.value;
            const circumference = 2 * Math.PI * radius;
            const offset = circumference - (percentage / 100) * circumference;

            circle.style.stroke = color;
            circle.style.strokeDashoffset = offset;
            circle.style.strokeDasharray = `${circumference} ${circumference}`;
            
            text.textContent = `${Math.round(percentage)}%`;
        }
    }
    
    // --- UI State Changers ---
    
    showLoadingState() {
        document.getElementById('loading-overlay').classList.remove('hidden');
        document.getElementById('results-container').classList.add('hidden');
    }

    hideLoadingState() {
        document.getElementById('loading-overlay').classList.add('hidden');
        document.getElementById('results-container').classList.remove('hidden');
    }

    showAlert(message, type = 'info') {
        const alertContainer = document.getElementById('alert-container');
        if (!alertContainer) return;

        const colorClasses = {
            success: 'bg-green-500',
            error: 'bg-red-500',
            info: 'bg-blue-500'
        };

        const alertDiv = document.createElement('div');
        alertDiv.className = `fixed top-5 right-5 text-white p-4 rounded-lg shadow-lg z-50 transition-transform transform translate-x-full ${colorClasses[type]}`;
        alertDiv.textContent = message;

        alertContainer.appendChild(alertDiv);
        
        // Animate in
        setTimeout(() => {
            alertDiv.classList.remove('translate-x-full');
        }, 10);
        
        // Animate out and remove
        setTimeout(() => {
            alertDiv.classList.add('translate-x-full');
            setTimeout(() => alertDiv.remove(), 300);
        }, 4000);
    }
    
    // --- Error State Handlers for Tabs ---
    
    createErrorHtml(message) {
        return `<div class="text-center text-terminal-border p-8 rounded-lg bg-terminal-bg-secondary">⚠️ ${message}</div>`;
    }
    
    setComplexityTabError(message) {
        const container = document.getElementById('complexity-content');
        if (container) container.innerHTML = this.createErrorHtml(message);
    }

    setDocumentationTabError(message) {
        const container = document.querySelector('#documentation .prose');
        if (container) container.innerHTML = this.createErrorHtml(message);
    }
    
    setRefactoringTabError(message) {
        const container = document.querySelector('#refactoring .space-y-6');
        if (container) container.innerHTML = this.createErrorHtml(message);
    }
    
    // --- Utility ---

    markdownToHtml(markdown) {
        if (!markdown) return '';
        let html = markdown;

        // Escape HTML to prevent XSS
        const escapeHtml = (unsafe) => {
            return unsafe
                 .replace(/&/g, "&amp;")
                 .replace(/</g, "&lt;")
                 .replace(/>/g, "&gt;")
                 .replace(/"/g, "&quot;")
                 .replace(/'/g, "&#039;");
        }
    
        // Code blocks (```...```)
        html = html.replace(/```(\w*)\n([\s\S]*?)```/g, (match, lang, code) => {
            return `<pre><code class="language-${lang || 'plaintext'}">${escapeHtml(code.trim())}</code></pre>`;
        });
    
        // Inline code (`)
        html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
    
        // Headings (#, ##, ###)
        html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
        html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
        html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');
    
        // Bold (**)
        html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
        // Italic (*)
        html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
        // Lists (*, -)
        html = html.replace(/^\s*[\*\-]\s(.*)/gm, '<ul>\n<li>$1</li>\n</ul>');
        html = html.replace(/<\/ul>\n<ul>/g, ''); // Fix consecutive list items
    
        // Paragraphs (newlines)
        html = html.split('\n').map(p => p.trim() ? `<p>${p}</p>` : '').join('');
        // Clean up paragraphs inside other elements
        html = html.replace(/<p><(h[1-3]|ul|li|pre)>/g, '<$1>');
        html = html.replace(/<\/(h[1-3]|ul|li|pre)><\/p>/g, '</$1>');

        return html;
    }
}

// Instantiate the analyzer class once the DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new ByteBuddyAnalyzer();
});