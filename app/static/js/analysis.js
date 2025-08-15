class ByteBuddyAnalyzer {
    constructor() {
        this.currentSessionId = null;
        this.completedTasks = new Set();
        this.progressInterval = null;
        this.animationQueue = [];

        // Initialize form handling
        this.initializeFormHandling();
        this.initializeHackerEnhancements();
    }

    initializeHackerEnhancements() {
        // Add smooth scroll behavior
        document.documentElement.style.scrollBehavior = 'smooth';
        
        // Initialize hacker-themed elements
        this.enhanceHackerElements();
        
        // Add hacker-themed styles
        this.injectHackerStyles();
        
    }

    injectHackerStyles() {
        const style = document.createElement('style');
        style.textContent = `
            /* Hacker Terminal Enhancements */
            .terminal-glow {
                box-shadow: 0 0 10px rgba(0, 123, 255, 0.5);
                border: 1px solid rgba(0, 123, 255, 0.3);
                background: rgba(18, 18, 18, 0.95);
                backdrop-filter: blur(5px);
            }
            
            .terminal-glow:hover {
                box-shadow: 0 0 20px rgba(0, 191, 255, 0.7);
                border-color: rgba(0, 191, 255, 0.5);
            }
            
            .hacker-border {
                border: 1px solid #007BFF;
                border-image: linear-gradient(45deg, #007BFF, #40E0D0, #007BFF) 1;
                animation: border-pulse 2s infinite;
            }
            
            @keyframes border-pulse {
                0%, 100% { border-color: #007BFF; }
                50% { border-color: #40E0D0; }
            }
            
            .code-block {
                background: #0a0a0a;
                border: 1px solid #333;
                border-left: 4px solid #007BFF;
                font-family: 'JetBrains Mono', monospace;
                color: #00FF00;
                padding: 16px;
                border-radius: 4px;
                margin: 12px 0;
                position: relative;
                overflow: hidden;
            }
            
            .code-block::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 1px;
                background: linear-gradient(90deg, transparent, #007BFF, transparent);
                animation: scan-line 2s linear infinite;
            }
            
            @keyframes scan-line {
                0% { transform: translateX(-100%); }
                100% { transform: translateX(100%); }
            }
            
            .complexity-display {
                background: linear-gradient(135deg, #1a1a1a, #121212);
                border: 2px solid #007BFF;
                border-radius: 8px;
                padding: 24px;
                text-align: center;
                position: relative;
                overflow: hidden;
            }
            
            .complexity-display::before {
                content: '';
                position: absolute;
                top: -2px;
                left: -2px;
                right: -2px;
                bottom: -2px;
                background: linear-gradient(45deg, #007BFF, #40E0D0, #007BFF);
                z-index: -1;
                animation: rotate-border 3s linear infinite;
                border-radius: 10px;
            }
            
            @keyframes rotate-border {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .complexity-value {
                font-size: 3rem;
                font-weight: bold;
                background: linear-gradient(45deg, #00FF00, #40E0D0);
                -webkit-background-clip: text;
                background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
                animation: glow-text 2s ease-in-out infinite alternate;
            }
            
            @keyframes glow-text {
                from { filter: brightness(1); }
                to { filter: brightness(1.2); }
            }
            
            .terminal-card {
                background: rgba(18, 18, 18, 0.95);
                border: 1px solid #2A2A2A;
                border-radius: 8px;
                padding: 20px;
                margin: 16px 0;
                position: relative;
                transition: all 0.3s ease;
            }
            
            .terminal-card:hover {
                border-color: #007BFF;
                box-shadow: 0 0 15px rgba(0, 123, 255, 0.3);
                transform: translateY(-2px);
            }
            
            .terminal-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 4px;
                height: 100%;
                background: linear-gradient(to bottom, #FF4757, #FFA726, #2ED573, #007BFF);
                border-radius: 2px;
            }
            
            .suggestion-item {
                background: rgba(26, 26, 26, 0.8);
                border: 1px solid #333;
                border-left: 3px solid #007BFF;
                padding: 16px;
                margin: 12px 0;
                border-radius: 4px;
                transition: all 0.3s ease;
                position: relative;
            }
            
            .suggestion-item:hover {
                border-left-color: #40E0D0;
                background: rgba(26, 26, 26, 0.95);
                transform: translateX(8px);
            }
            
            .suggestion-item::after {
                content: '>';
                position: absolute;
                right: 16px;
                top: 50%;
                transform: translateY(-50%);
                color: #007BFF;
                font-weight: bold;
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .suggestion-item:hover::after {
                opacity: 1;
            }
            
            .terminal-header {
                display: flex;
                align-items: center;
                margin-bottom: 16px;
                padding-bottom: 8px;
                border-bottom: 1px solid #333;
            }
            
            .terminal-header::before {
                content: '$';
                color: #2ED573;
                margin-right: 8px;
                font-weight: bold;
            }
            
            .error-message {
                background: rgba(255, 71, 87, 0.1);
                border: 1px solid #FF4757;
                color: #FF4757;
                padding: 16px;
                border-radius: 4px;
                margin: 16px 0;
                font-family: 'JetBrains Mono', monospace;
            }
            
            .success-message {
                background: rgba(46, 213, 115, 0.1);
                border: 1px solid #2ED573;
                color: #2ED573;
                padding: 16px;
                border-radius: 4px;
                margin: 16px 0;
                font-family: 'JetBrains Mono', monospace;
            }
            
            .matrix-rain {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: -1;
                overflow: hidden;
            }
            
            .matrix-char {
                position: absolute;
                color: #007BFF;
                font-family: 'JetBrains Mono', monospace;
                font-size: 14px;
                opacity: 0.1;
                animation: matrix-fall linear infinite;
            }
            
            @keyframes matrix-fall {
                0% {
                    transform: translateY(-100vh);
                    opacity: 0;
                }
                10% {
                    opacity: 0.3;
                }
                90% {
                    opacity: 0.1;
                }
                100% {
                    transform: translateY(100vh);
                    opacity: 0;
                }
            }
            
            .typing-animation {
                overflow: hidden;
                white-space: nowrap;
                border-right: 2px solid #007BFF;
                animation: typing 2s steps(40) forwards, blink 1s infinite;
            }
            
            @keyframes typing {
                0% { width: 0; }
                100% { width: 100%; }
            }
            
            @keyframes blink {
                0%, 50% { border-color: #007BFF; }
                51%, 100% { border-color: transparent; }
            }
            
            .progress-bar {
                width: 100%;
                height: 4px;
                background: #333;
                border-radius: 2px;
                overflow: hidden;
                margin: 16px 0;
            }
            
            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #007BFF, #40E0D0, #2ED573);
                border-radius: 2px;
                animation: progress-scan 2s linear infinite;
            }
            
            @keyframes progress-scan {
                0% { transform: translateX(-100%); }
                100% { transform: translateX(100%); }
            }

            /* Additional Hacker Enhancements */
            .glass-card {
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(0, 123, 255, 0.3);
                border-radius: 16px;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .glass-card:hover {
                background: rgba(255, 255, 255, 0.08);
                border-color: rgba(0, 191, 255, 0.5);
                transform: translateY(-2px);
                box-shadow: 0 20px 40px rgba(0, 123, 255, 0.3);
            }

            .neon-glow {
                box-shadow: 0 0 20px currentColor;
                animation: pulse-glow 2s ease-in-out infinite alternate;
            }

            .gradient-text {
                background: linear-gradient(45deg, #00f5ff, #ff4081, #00f5ff);
                background-size: 200% 200%;
                -webkit-background-clip: text;
                background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: gradient-shift 3s ease infinite;
            }
            
            @keyframes gradient-shift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            .complexity-ring {
                width: 200px;
                height: 200px;
                border-radius: 50%;
                position: relative;
                background: conic-gradient(from 0deg, #ff4757 0deg, #ffa726 120deg, #2ed573 240deg, #007BFF 360deg);
                padding: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto;
            }
            
            .complexity-inner {
                width: calc(100% - 16px);
                height: calc(100% - 16px);
                border-radius: 50%;
                background: #1a1a1a;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }

            .floating-particle {
                position: absolute;
                width: 4px;
                height: 4px;
                background: #00f5ff;
                border-radius: 50%;
                opacity: 0.6;
                animation: float 3s ease-in-out infinite;
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0px) scale(1); opacity: 0.6; }
                50% { transform: translateY(-20px) scale(1.2); opacity: 1; }
            }

            .progress-wave {
                width: 100%;
                height: 4px;
                background: linear-gradient(90deg, #ff4757, #ffa726, #2ed573, #00f5ff);
                background-size: 200% 100%;
                animation: wave 2s linear infinite;
                border-radius: 2px;
            }
            
            @keyframes wave {
                0% { background-position: -200% 0; }
                100% { background-position: 200% 0; }
            }
        `;
        document.head.appendChild(style);
    }

    

    enhanceHackerElements() {
        // Add terminal glow to existing terminal windows
        const terminalWindows = document.querySelectorAll('.terminal-window');
        terminalWindows.forEach(window => {
            window.classList.add('terminal-glow');
        });
    }

   
    initializeFormHandling() {
        const form = document.getElementById('code-analysis-form');
        if (form) {
            form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        } else {
            console.error('CRITICAL: Form with ID "code-analysis-form" was not found!');
        }
    }

    async handleFormSubmit(event) {
        event.preventDefault();

        const code = document.getElementById('code-input').value;
        const language = document.getElementById('language').value;

        if (!code || code.trim() === '') {
            this.showHackerAlert('ERROR: No code detected in input buffer!', 'error');
            return;
        }
        
        // Get selected options
        const selectedOptions = [];
        const checkboxes = document.querySelectorAll('input[name="options"]:checked');
        checkboxes.forEach(cb => selectedOptions.push(cb.value));

        if (selectedOptions.length === 0) {
            this.showHackerAlert('ERROR: No analysis modules selected!', 'error');
            return;
        }
        
        // Show hacker loading state
        this.showHackerLoadingState();

        try {
            // Create form data
            const formData = new FormData();
            formData.append('code', code);
            formData.append('language', language);
            formData.append('options', selectedOptions.join(','));
            
            console.log('🚀 Initiating deep scan...');

            const response = await fetch('/analyze/code', {
                method: 'POST',
                body: formData
            });

            console.log(`📡 Response received with status: ${response.status}`);
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({'results': {'error': 'Server returned a non-JSON error response.'}}));
                throw new Error(errorData.results?.error || `HTTP error! status: ${response.status}`);
            }
            const result = await response.json();
            console.log('🔥 Analysis complete:', result);

            // Validate the response format
            if (!this.validateResponse(result)) {
                throw new Error('Invalid response format from server');
            }
            
            if (result.results.success === false) {
                 throw new Error(result.results.error || 'Analysis failed on the server.');
            }

            // Store session ID if available
            this.currentSessionId = result.results?.analysis_id || Date.now().toString();

            // Process results with hacker styling
            this.processHackerAnalysisResults(result, code);

            this.hideHackerLoadingState();
            this.showHackerAlert('SUCCESS: Analysis completed successfully!', 'success');

        } catch (error) {
            console.error('❌ Analysis failed:', error);
            this.showHackerAlert(`CRITICAL ERROR: ${error.message}`, 'error');
            this.hideHackerLoadingState();
        }
    }

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

    processHackerAnalysisResults(result, code) {
        console.log('🔄 Processing analysis with hacker theme...');
        const analysisData = result.results;

        // Store the analysis ID
        if (analysisData.analysis_id) {
            this.currentSessionId = analysisData.analysis_id;
            console.log('🔐 Session ID set to:', this.currentSessionId);
        }

        try {
            // 1. Update Complexity Tab with hacker styling
            console.log('🧮 Updating complexity display...');
            const complexityData = this.parseComplexityFromAgent(analysisData.complexity_analysis);
            if (complexityData) {
                this.updateHackerComplexityTab(complexityData);
                console.log('✅ Complexity display updated');
            } else {
                this.setComplexityTabError('SCAN ERROR: Could not parse complexity data');
                console.warn('❌ Could not parse complexity');
            }

            // 2. Update Documentation Tab with hacker styling
            console.log('📄 Updating documentation display...');
            if (analysisData.documentation && analysisData.documentation.trim() !== 'No documentation generated') {
                this.updateHackerDocumentationTab({
                    content: analysisData.documentation
                });
                console.log('✅ Documentation display updated');
            } else {
                this.setDocumentationTabError('NO DATA: Documentation generation failed.');
                console.warn('❌ No documentation found');
            }

            // 3. Update Refactoring Tab with hacker styling
            console.log('🔧 Updating refactoring display...');
            const refactoringSuggestions = this.parseRefactoringSuggestionsFromAgent(analysisData.refactoring_suggestions);
            if (refactoringSuggestions.length > 0) {
                this.updateHackerRefactoringTab({
                    suggestions: refactoringSuggestions
                });
                console.log('✅ Refactoring display updated');
            } else {
                this.setRefactoringTabError('NO OPTIMIZATIONS: Code already optimized.');
                console.warn('❌ No refactoring suggestions');
            }

            // 4. Update Structure Tab with hacker styling
            console.log('📊 Updating structure display...');
            const structureData = {
                functions_count: this.countFunctions(code),
                lines_count: code.split('\n').length,
                complexity_score: complexityData ? complexityData.score || 5 : 5,
                dependencies: 0,
                structure_image: analysisData.structure_img
            };
            this.updateHackerStructureTab(structureData);
            console.log('✅ Structure display updated with image:', analysisData.structure_img);

            // 5. Update Improvements Tab with hacker styling
            console.log('💡 Updating improvements display...');
            this.updateHackerImprovementsTab({
                performance_score: complexityData ? complexityData.performance_score || 65 : 65,
                readability_score: 75,
                documentation_score: analysisData.documentation ? 80 : 30,
                testing_score: 10,
                content: analysisData.improvement_suggestions || 'NO IMPROVEMENTS DETECTED'
            });
            console.log('✅ Improvements display updated');

            // Switch to complexity tab with hacker effect
            if (typeof switchTab === 'function') {
                switchTab('complexity');
            }
            
            // Trigger entrance animations
            this.triggerHackerEntranceAnimations();
            console.log('🎉 All displays updated with hacker theme!');
        } catch (error) {
            console.error('❌ Error processing analysis results:', error);
            this.showHackerAlert(`FATAL ERROR: ${error.message}`, 'error');
        }
    }

    triggerHackerEntranceAnimations() {
        // Add staggered entrance animations with hacker theme
        const elements = document.querySelectorAll('.terminal-card, .glass-card, .suggestion-item, .complexity-display');
        elements.forEach((el, index) => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px) scale(0.95)';
            el.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            
            setTimeout(() => {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0) scale(1)';
                // Add temporary glow effect
                el.style.boxShadow = '0 0 30px rgba(0, 123, 255, 0.5)';
                setTimeout(() => {
                    el.style.boxShadow = '';
                }, 1000);
            }, index * 150);
        });
    }

    // Parse complexity analysis from agent's text output
    parseComplexityFromAgent(complexityText) {
        if (!complexityText || typeof complexityText !== 'string') {
            console.warn('No complexity text to parse');
            return null;
        }
        console.log('🔍 Parsing complexity data...', complexityText.substring(0, 200) + '...');
        
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

    // Parse refactoring suggestions from agent's text output
    parseRefactoringSuggestionsFromAgent(refactoringText) {
        if (!refactoringText || refactoringText.includes("No refactoring suggestions")) return [];

        console.log('🔧 Parsing refactoring suggestions...');

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
                title: `[OPTIMIZATION #${index + 1}]`,
                description: cleanLine,
                priority: index < 2 ? 'HIGH' : 'MEDIUM',
                category: 'REFACTOR',
                color: this.getComplexityColor('O(1)')
            };
        });
    }

    // Helper functions for complexity calculation
    getComplexityColor(complexity) {
        const c = String(complexity).toLowerCase();
        if (c.includes('1')) return '#2ED573'; // Green
        if (c.includes('log n')) return '#40E0D0'; // Cyan
        if (c.includes('n log n')) return '#FFA726'; // Orange
        if (c.includes('n^2') || c.includes('n²')) return '#FF4757'; // Red
        if (c.includes('2^n')) return '#FF1744'; // Bright Red
        if (c.includes('n')) return '#00BFFF'; // Blue
        return '#FF4757'; // Default to red
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

    // Hacker-themed Tab Update Methods
    updateHackerComplexityTab(data) {
        console.log('Updating hacker complexity display with:', data);
        
        // Update Time Complexity
        const timeEl = document.querySelector('#complexity .time-complexity');
        if (timeEl) {
            timeEl.innerHTML = `<span class="complexity-value">${data.time_complexity}</span>`;
            timeEl.style.color = data.time_color;
        }
        
        const timeDescEl = document.querySelector('#complexity .complexity-description');
        if (timeDescEl) {
            timeDescEl.innerHTML = `
                <div class="terminal-header">Time Analysis Complete</div>
                <div class="text-sm text-terminal-text">
                    Performance Rating: <span style="color: ${data.time_color}">${this.getComplexityLevel(data.time_complexity)}</span>
                </div>
            `;
        }
        
        // Update Space Complexity
        const spaceEl = document.querySelector('#complexity .space-complexity');
        if (spaceEl) {
            spaceEl.innerHTML = `<span class="complexity-value">${data.space_complexity}</span>`;
            spaceEl.style.color = data.space_color;
        }
        
        // Add detailed analysis with hacker styling
        const complexitySection = document.getElementById('complexity');
        if (complexitySection && data.full_analysis) {
            let detailedAnalysis = complexitySection.querySelector('.detailed-analysis');
            if (!detailedAnalysis) {
                detailedAnalysis = document.createElement('div');
                detailedAnalysis.className = 'detailed-analysis';
                complexitySection.appendChild(detailedAnalysis);
            }
            
            detailedAnalysis.innerHTML = `
                <div class="terminal-card mt-6">
                    <div class="terminal-header">DETAILED COMPLEXITY SCAN</div>
                    <div class="code-block">
                        <pre class="text-sm">${data.full_analysis}</pre>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${data.performance_score}%"></div>
                    </div>
                    <div class="text-center mt-2">
                        <span class="text-cyan">Performance Score: </span>
                        <span class="complexity-value text-electric-blue font-bold">${data.performance_score}%</span>
                    </div>
                </div>
            `;
        }
    }

    updateHackerStructureTab(data) {
        console.log('Updating hacker structure display with:', data);

        // Update metrics with hacker styling
        const metricsUpdate = [
            { id: 'functions-count', value: data.functions_count, suffix: '' },
            { id: 'lines-count', value: data.lines_count, suffix: '' },
            { id: 'complexity-score', value: data.complexity_score, suffix: '/10' }
        ];

        metricsUpdate.forEach(metric => {
            const element = document.getElementById(metric.id);
            if (element) {
                // Add hacker-style animation
                element.className += ' typing-animation';
                element.textContent = metric.value + metric.suffix;
            }
        });

        // Update structure image with hacker container
        const imageContainer = document.getElementById('structure-image-container');
        if (imageContainer && data.structure_image) {
            console.log('📊 Loading structure visualization:', data.structure_image);
            imageContainer.innerHTML = `
                <div class="terminal-header">CODE STRUCTURE SCAN</div>
                <div class="hacker-border p-4 rounded">
                    <img src="${data.structure_image}?t=${new Date().getTime()}" 
                         alt="Code Structure Visualization"
                         class="w-full h-auto rounded"
                         onload="console.log('✅ Structure visualization loaded successfully')"
                         onerror="this.parentElement.innerHTML='<div class=\\'error-message\\'>⚠️ VISUALIZATION LOAD FAILED</div>'">
                </div>
                <div class="mt-4 text-center">
                    <span class="text-bright-blue">Functions: ${data.functions_count} | </span>
                    <span class="text-cyan">Lines: ${data.lines_count} | </span>
                    <span class="text-success-green">Score: ${data.complexity_score}/10</span>
                </div>
            `;
        } else if (imageContainer) {
            imageContainer.innerHTML = `
                <div class="terminal-card">
                    <div class="terminal-header">STRUCTURE SCAN FAILED</div>
                    <div class="error-message">
                        No structure visualization was generated for this code sample.
                    </div>
                </div>
            `;
        }
    }

    updateHackerRefactoringTab(data) {
        console.log('Updating hacker refactoring display with:', data);

        const container = document.querySelector('#refactoring .refactoring-content');
        if (!container || !data.suggestions) return;

        const suggestionsHTML = data.suggestions.map((suggestion, index) => `
            <div class="suggestion-item">
                <div class="flex items-center mb-2">
                    <span class="text-warning-orange font-bold mr-2">[${suggestion.priority}]</span>
                    <span class="text-bright-blue">${suggestion.category}</span>
                    <span class="text-terminal-text ml-auto">#${index + 1}</span>
                </div>
                <h4 class="font-bold text-electric-blue mb-2">${suggestion.title}</h4>
                <p class="text-terminal-text text-sm leading-relaxed">${suggestion.description}</p>
                <div class="mt-2 text-xs text-cyan">
                    → Estimated improvement: ${suggestion.priority === 'HIGH' ? 'Significant' : 'Moderate'}
                </div>
            </div>
        `).join('');
        
        container.innerHTML = `
            <div class="terminal-header">OPTIMIZATION RECOMMENDATIONS</div>
            ${suggestionsHTML || '<div class="success-message">✅ NO OPTIMIZATIONS NEEDED - CODE IS ALREADY EFFICIENT</div>'}
        `;
    }

    updateHackerDocumentationTab(data) {
        console.log('Updating hacker documentation display with content length:', data.content?.length || 0);

        const contentElement = document.querySelector('#documentation .documentation-content');
        if (contentElement && data.content) {
            const enhancedContent = this.hackerMarkdownToHtml(data.content);
            contentElement.innerHTML = `
                <div class="terminal-card">
                    <div class="terminal-header">AUTO-GENERATED DOCUMENTATION</div>
                    <div class="code-block">
                        ${enhancedContent}
                    </div>
                </div>
            `;
        }
    }

    updateHackerImprovementsTab(data) {
        console.log('Updating hacker improvements display with:', data);
        
        const improvementsSection = document.getElementById('improvements-content');
        if (improvementsSection && data.content) {
            improvementsSection.innerHTML = `
                <div class="terminal-card mb-6">
                    <div class="terminal-header">PERFORMANCE ENHANCEMENT REPORT</div>
                    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
    <div class="bg-terminal-bg rounded-lg p-4 text-center">
        <div class="text-2xl font-bold text-bright-blue mb-1">${data.performance_score}%</div>
        <div class="text-sm text-terminal-text">Performance</div>
    </div>
    <div class="bg-terminal-bg rounded-lg p-4 text-center">
        <div class="text-2xl font-bold text-cyan mb-1">${data.readability_score}%</div>
        <div class="text-sm text-terminal-text">Readability</div>
    </div>
    <div class="bg-terminal-bg rounded-lg p-4 text-center">
        <div class="text-2xl font-bold text-success-green mb-1">${data.documentation_score}%</div>
        <div class="text-sm text-terminal-text">Documentation</div>
    </div>
    <div class="bg-terminal-bg rounded-lg p-4 text-center">
        <div class="text-2xl font-bold text-warning-orange mb-1">${data.testing_score}%</div>
        <div class="text-sm text-terminal-text">Testing</div>
    </div>
</div>
                    <div class="code-block">
                        <pre class="text-sm text-terminal-text whitespace-pre-wrap">${data.content}</pre>
                    </div>
                </div>
            `;
        }
    }

    // Enhanced Markdown Processing with Hacker Theme
    hackerMarkdownToHtml(markdown) {
        if (!markdown) return '<div class="error-message">NO DOCUMENTATION GENERATED</div>';
        
        let html = markdown
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");

        // Enhanced code blocks with hacker styling
        html = html.replace(/```(\w*?)\n([\s\S]*?)```/g, (match, lang, code) => {
            return `<div class="code-block mt-4 mb-4">
                        <div class="terminal-header">${lang.toUpperCase() || 'CODE'} SEGMENT</div>
                        <pre><code class="text-success-green">${code.trim()}</code></pre>
                    </div>`;
        });

        // Inline code with hacker styling
        html = html.replace(/`([^`]+)`/g, '<span class="text-cyan bg-terminal-bg-secondary px-2 py-1 rounded text-sm font-mono">$1</span>');

        // Headers with hacker styling
        html = html.replace(/^### (.*$)/gim, '<h3 class="text-lg font-bold text-bright-blue mt-4 mb-2 border-l-4 border-electric-blue pl-3">$1</h3>');
        html = html.replace(/^## (.*$)/gim, '<h2 class="text-xl font-bold gradient-text mt-6 mb-3 border-b border-terminal-border pb-2">$1</h2>');
        html = html.replace(/^# (.*$)/gim, '<h1 class="text-2xl font-bold gradient-text mt-6 mb-4 border-b-2 border-electric-blue pb-2">$1</h1>');

        // Enhanced text formatting
        html = html.replace(/\*\*(.*?)\*\*/g, '<strong class="text-terminal-white font-bold">$1</strong>');
        html = html.replace(/\*(.*?)\*/g, '<em class="text-cyan italic">$1</em>');

        // Enhanced lists with hacker bullets
        html = html.replace(/^\s*[\*\-]\s(.*)/gm, '<div class="suggestion-item mb-2"><span class="text-electric-blue">▶</span> $1</div>');

        // Convert line breaks to proper formatting
        html = html.replace(/\n/g, '<br>');
        
        return `<div class="hacker-documentation">${html}</div>`;
    }

    getComplexityLevel(complexity) {
        const levels = {
            'O(1)': 'OPTIMAL',
            'O(log n)': 'EXCELLENT',
            'O(n)': 'GOOD',
            'O(n log n)': 'MODERATE',
            'O(n²)': 'POOR',
            'O(n^2)': 'POOR',
            'O(2^n)': 'CRITICAL'
        };
        return levels[complexity] || 'UNKNOWN';
    }

    // Hacker-themed UI State Methods
    showHackerLoadingState() {
        const submitBtn = document.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = `
                <div class="flex items-center">
                    <div class="w-4 h-4 border-2 border-terminal-white border-t-transparent rounded-full animate-spin mr-2"></div>
                    <span class="root-prompt">./analyzing --deep-scan</span>
                </div>
            `;
        }

        // Show loading overlay with hacker theme
        let loadingOverlay = document.getElementById('hacker-loading-overlay');
        if (!loadingOverlay) {
            loadingOverlay = document.createElement('div');
            loadingOverlay.id = 'hacker-loading-overlay';
            loadingOverlay.className = 'fixed inset-0 bg-terminal-bg bg-opacity-90 flex items-center justify-center z-50';
            document.body.appendChild(loadingOverlay);
        }

        loadingOverlay.innerHTML = `
            <div class="terminal-card p-8 max-w-md text-center">
                <div class="relative mb-6">
                    <div class="complexity-ring">
                        <div class="complexity-inner">
                            <div class="text-4xl mb-2">🔍</div>
                            <div class="text-sm gradient-text">SCANNING...</div>
                        </div>
                    </div>
                </div>
                <h3 class="text-xl font-bold gradient-text mb-2">DEEP CODE ANALYSIS</h3>
                <p class="text-terminal-text mb-4">AI systems analyzing complexity patterns...</p>
                <div class="progress-bar">
                    <div class="progress-fill"></div>
                </div>
                <div class="terminal-header mt-4">
                    <span class="typing-animation">root@bytebuddy:~# analyze --verbose --deep</span>
                </div>
            </div>
        `;
        loadingOverlay.classList.remove('hidden');
    }

    hideHackerLoadingState() {
        const submitBtn = document.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<span class="root-prompt">sudo ./analyze --deep</span>';
        }

        const loadingOverlay = document.getElementById('hacker-loading-overlay');
        if (loadingOverlay) {
            loadingOverlay.classList.add('hidden');
        }
    }

    showHackerAlert(message, type = 'info') {
        const alertContainer = document.body;

        const typeStyles = {
            success: { color: '#2ED573', icon: '✅', prefix: '[SUCCESS]' },
            error: { color: '#FF4757', icon: '❌', prefix: '[ERROR]' },
            info: { color: '#007BFF', icon: 'ℹ️', prefix: '[INFO]' }
        };

        const style = typeStyles[type] || typeStyles.info;

        const alertDiv = document.createElement('div');
        alertDiv.className = 'fixed top-5 right-5 terminal-card max-w-md z-50 transform translate-x-full transition-transform duration-500';
        alertDiv.style.borderLeftColor = style.color;
        
        alertDiv.innerHTML = `
            <div class="terminal-header" style="color: ${style.color}">
                ${style.icon} ${style.prefix}
            </div>
            <div class="text-terminal-text text-sm">
                ${message}
            </div>
            <div class="progress-bar mt-3">
                <div class="progress-fill" style="background: ${style.color}; width: 100%; animation: none;"></div>
            </div>
        `;

        alertContainer.appendChild(alertDiv);
        
        // Animate in
        setTimeout(() => {
            alertDiv.classList.remove('translate-x-full');
        }, 10);
        
        // Animate out and remove
        setTimeout(() => {
            alertDiv.classList.add('translate-x-full');
            setTimeout(() => alertDiv.remove(), 500);
        }, 4000);
    }

    // Enhanced Error State Handlers with Hacker Theme
    createHackerErrorHtml(message) {
        return `
            <div class="terminal-card">
                <div class="terminal-header text-warning-red">SYSTEM ERROR</div>
                <div class="error-message">
                    <div class="text-center mb-4">
                        <div class="text-6xl">⚠️</div>
                        <div class="text-lg font-bold mt-2">ANALYSIS FAILED</div>
                    </div>
                    <div class="code-block">
                        <pre class="text-warning-red">${message}</pre>
                    </div>
                    <div class="mt-4 text-center">
                        <span class="text-terminal-text">Error Code: </span>
                        <span class="text-warning-red font-mono">0x${Math.random().toString(16).substr(2, 6).toUpperCase()}</span>
                    </div>
                </div>
            </div>
        `;
    }
    
    setComplexityTabError(message) {
        const container = document.getElementById('complexity');
        if (container) {
            let errorContainer = container.querySelector('.error-container');
            if (!errorContainer) {
                errorContainer = document.createElement('div');
                errorContainer.className = 'error-container mt-4';
                container.appendChild(errorContainer);
            }
            errorContainer.innerHTML = this.createHackerErrorHtml(message);
        }
    }

    setDocumentationTabError(message) {
        const container = document.querySelector('#documentation .documentation-content');
        if (container) {
            container.innerHTML = this.createHackerErrorHtml(message);
        }
    }
    
    setRefactoringTabError(message) {
        const container = document.querySelector('#refactoring .refactoring-content');
        if (container) {
            container.innerHTML = this.createHackerErrorHtml(message);
        }
    }

    // Utility methods for enhanced effects
    getScoreColor(score) {
        if (score >= 80) return '#2ED573'; // Green
        if (score >= 60) return '#FFA726'; // Orange  
        if (score >= 40) return '#FF4757'; // Red
        return '#FF1744'; // Bright Red
    }

    getEfficiencyRating(score) {
        if (score >= 90) return 'ELITE';
        if (score >= 75) return 'ADVANCED';
        if (score >= 60) return 'STANDARD';
        if (score >= 40) return 'BASIC';
        return 'CRITICAL';
    }

    // Legacy method compatibility
    markdownToHtml(markdown) {
        return this.hackerMarkdownToHtml(markdown);
    }

    showLoadingState() {
        this.showHackerLoadingState();
    }

    hideLoadingState() {
        this.hideHackerLoadingState();
    }

    showAlert(message, type = 'info') {
        this.showHackerAlert(message, type);
    }
}

// Initialize the hacker analyzer when DOM is ready
let byteBuddyAnalyzer;
document.addEventListener('DOMContentLoaded', function() {
    byteBuddyAnalyzer = new ByteBuddyAnalyzer();
    console.log('🚀 Hacker ByteBuddy Analyzer initialized successfully!');
    console.log('💀 Welcome to the matrix...');
});