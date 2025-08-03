import ast
import re
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict, Counter
import numpy as np
from typing import Dict, List, Tuple, Set
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

class CodeAnalyzer:
    def __init__(self, api_key: str = None):
        """Initialize the code analyzer with Google GenAI"""
        if api_key:
            os.environ["GOOGLE_API_KEY"] = api_key
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")
    
    def parse_cpp_code(self, code: str) -> Dict:
        """Parse C++ code to extract functions, variables, and structure"""
        # Remove comments
        code = re.sub(r'//.*', '', code)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        
        # Extract functions
        function_pattern = r'(\w+\s+)?(\w+)\s*\([^)]*\)\s*{'
        functions = re.findall(function_pattern, code)
        
        # Extract variables
        variable_pattern = r'(\w+)\s+(\w+)\s*[;=]'
        variables = re.findall(variable_pattern, code)
        
        # Extract loops
        loop_pattern = r'for\s*\([^)]*\)|while\s*\([^)]*\)'
        loops = re.findall(loop_pattern, code)
        
        # Extract conditionals
        conditional_pattern = r'if\s*\([^)]*\)'
        conditionals = re.findall(conditional_pattern, code)
        
        return {
            'functions': [f[1] for f in functions if f[1]],
            'variables': [v[1] for v in variables if v[1]],
            'loops': loops,
            'conditionals': conditionals,
            'lines': len(code.split('\n')),
            'raw_code': code
        }

    def visualize_code_structure(self, code: str, output_path: str = "code_structure") -> str:
        """Generate a real graph of code structure using networkx and matplotlib"""
        parsed = self.parse_cpp_code(code)
        
        # Create directed graph
        G = nx.DiGraph()
        
        # Add function nodes
        for func in parsed['functions']:
            G.add_node(func, node_type='function', color='lightblue')
        
        # Add variable nodes
        for var in parsed['variables'][:10]:  # Limit to first 10 variables
            G.add_node(var, node_type='variable', color='lightgreen')
        
        # Add control structure nodes
        for i, loop in enumerate(parsed['loops'][:5]):
            loop_name = f"loop_{i+1}"
            G.add_node(loop_name, node_type='loop', color='orange')
        
        # Create some logical connections (simplified)
        if parsed['functions']:
            main_func = parsed['functions'][0]
            for var in parsed['variables'][:3]:
                G.add_edge(main_func, var)
            for i in range(min(3, len(parsed['loops']))):
                G.add_edge(main_func, f"loop_{i+1}")
        
        # Plot the graph
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Draw nodes by type
        node_colors = [G.nodes[node].get('color', 'gray') for node in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_color=node_colors, 
                node_size=2000, font_size=10, font_weight='bold',
                arrows=True, edge_color='gray', alpha=0.7)
        
        plt.title("Code Structure Visualization", fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        # Save the plot
        output_file = f"{output_path}.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_file

    def suggest_code_refactoring(self, code: str) -> str:
        """Use LLM to suggest real refactoring improvements"""
        prompt = PromptTemplate.from_template("""
        Analyze the following C++ code and provide specific refactoring suggestions:
        
        ```cpp
        {code}
        ```
        
        Please provide:
        1. Code structure improvements
        2. Variable naming suggestions
        3. Logic optimization opportunities
        4. Modern C++ best practices
        5. Specific code examples where applicable
        
        Format as clear, actionable bullet points.
        """)
        
        try:
            response = self.llm.invoke(prompt.format(code=code))
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            return f"Error generating refactoring suggestions: {str(e)}"

    def analyze_complexity(self, code: str, output_path: str = "complexity_graph.png") -> str:
        """Perform real complexity analysis with LeetCode-style visualization"""
        parsed = self.parse_cpp_code(code)
        
        # Count nested loops for time complexity estimation
        nested_loops = code.count('for') + code.count('while')
        nested_level = 0
        max_nested = 0
        
        for char in code:
            if char == '{':
                nested_level += 1
                max_nested = max(max_nested, nested_level)
            elif char == '}':
                nested_level -= 1
        
        # Estimate complexity based on loop patterns
        if nested_loops == 0:
            time_complexity = "O(1)"
            complexity_color = "#00C851"  # Green
        elif nested_loops == 1:
            time_complexity = "O(n)"
            complexity_color = "#ffbb33"  # Amber
        elif nested_loops >= 2 and max_nested >= 3:
            time_complexity = "O(n²)"
            complexity_color = "#ff4444"  # Red
        else:
            time_complexity = "O(n log n)"
            complexity_color = "#ff8800"  # Orange
        
        # Space complexity analysis
        variable_count = len(parsed['variables'])
        if variable_count <= 5:
            space_complexity = "O(1)"
        else:
            space_complexity = "O(n)"
        
        # Create LeetCode-style complexity visualization
        plt.style.use('default')
        fig, ax = plt.subplots(figsize=(12, 8))
        fig.patch.set_facecolor('#1a1a1a')  # Dark background like LeetCode
        ax.set_facecolor('#1a1a1a')
        
        # Generate input size range
        n_values = np.logspace(1, 4, 1000)
        
        # Define complexity functions and colors
        complexities = {
            'O(1)': (np.ones_like(n_values), '#00C851', 2),
            'O(log n)': (np.log2(n_values), '#33b5e5', 2),
            'O(n)': (n_values, '#ffbb33', 2),
            'O(n log n)': (n_values * np.log2(n_values), '#ff8800', 2),
            'O(n²)': (n_values**2, '#ff4444', 2),
            'O(2ⁿ)': (2**np.log2(n_values), '#aa66cc', 2)
        }
        
        # Plot all complexity curves
        for label, (y_values, color, linewidth) in complexities.items():
            if label == time_complexity:
                # Highlight the detected complexity
                ax.loglog(n_values, y_values, label=label, color=color, 
                         linewidth=4, alpha=0.9, zorder=10)
                # Add glow effect
                ax.loglog(n_values, y_values, color=color, linewidth=8, alpha=0.3)
            else:
                ax.loglog(n_values, y_values, label=label, color=color, 
                         linewidth=linewidth, alpha=0.6)
        
        # Styling to match LeetCode
        ax.set_xlabel('Input Size (n)', fontsize=14, color='white', fontweight='bold')
        ax.set_ylabel('Time Complexity', fontsize=14, color='white', fontweight='bold')
        ax.set_title(f'Algorithm Complexity Analysis\nDetected: {time_complexity}', 
                    fontsize=16, color='white', fontweight='bold', pad=20)
        
        # Grid styling
        ax.grid(True, alpha=0.3, color='gray', linestyle='-', linewidth=0.5)
        ax.set_axisbelow(True)
        
        # Legend styling
        legend = ax.legend(loc='upper left', fontsize=12, framealpha=0.9)
        legend.get_frame().set_facecolor('#2d2d2d')
        legend.get_frame().set_edgecolor('gray')
        for text in legend.get_texts():
            text.set_color('white')
        
        # Axis styling
        ax.tick_params(colors='white', labelsize=11)
        ax.spines['bottom'].set_color('gray')
        ax.spines['top'].set_color('gray')
        ax.spines['right'].set_color('gray')
        ax.spines['left'].set_color('gray')
        
        # Set axis limits for better visualization
        ax.set_xlim(10, 10000)
        ax.set_ylim(1, 10**8)
        
        # Add complexity annotation box
        textstr = f'''Algorithm Analysis:
• Time Complexity: {time_complexity}
• Space Complexity: {space_complexity}
• Nested Loops: {nested_loops}
• Max Nesting: {max_nested}
• Functions: {len(parsed['functions'])}
• Variables: {len(parsed['variables'])}'''
        
        props = dict(boxstyle='round', facecolor='#2d2d2d', alpha=0.9, edgecolor='gray')
        ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=11,
                verticalalignment='top', bbox=props, color='white', fontfamily='monospace')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', 
                   facecolor='#1a1a1a', edgecolor='none')
        plt.close()
        
        analysis = f"""
        COMPLEXITY ANALYSIS:
        ===================
        Time Complexity: {time_complexity}
        Space Complexity: {space_complexity}
        
        DETAILED BREAKDOWN:
        - Number of loops: {nested_loops}
        - Maximum nesting level: {max_nested}
        - Functions defined: {len(parsed['functions'])}
        - Variables declared: {len(parsed['variables'])}
        - Lines of code: {parsed['lines']}
        
        EXPLANATION:
        - The time complexity is estimated based on loop nesting patterns
        - Space complexity considers variable declarations and data structures
        - Graph saved to {output_path}
        """
        
        return analysis

    def generate_documentation(self, code: str) -> str:
        """Generate comprehensive documentation using LLM"""
        prompt = PromptTemplate.from_template("""
        Generate comprehensive markdown documentation for this C++ code:
        
        ```cpp
        {code}
        ```
        
        Include:
        1. **Purpose**: What does this code do?
        2. **Algorithm**: Explain the algorithm/logic
        3. **Functions**: Detailed description of each function
        4. **Parameters**: Input parameters and their types
        5. **Return Values**: What the functions return
        6. **Time/Space Complexity**: Brief complexity analysis
        7. **Example Usage**: How to use this code
        8. **Potential Improvements**: What could be enhanced
        
        Use proper markdown formatting.
        """)
        
        try:
            response = self.llm.invoke(prompt.format(code=code))
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            return f"Error generating documentation: {str(e)}"

    def suggest_improvements(self, code: str) -> str:
        """Generate specific improvement suggestions using LLM"""
        prompt = PromptTemplate.from_template("""
        Analyze this C++ code and provide specific, actionable improvement suggestions:
        
        ```cpp
        {code}
        ```
        
        Focus on:
        1. **Performance Optimizations**: Specific ways to make it faster
        2. **Memory Efficiency**: How to reduce memory usage
        3. **Code Quality**: Better naming, structure, readability
        4. **Modern C++ Features**: C++11/14/17/20 features that could help
        5. **Security Considerations**: Potential security issues
        6. **Error Handling**: How to make it more robust
        7. **Best Practices**: Industry standard practices
        
        Provide specific code examples where possible.
        """)
        
        try:
            response = self.llm.invoke(prompt.format(code=code))
            return response.content if hasattr(response, 'content') else str(response)
        except Exception as e:
            return f"Error generating improvements: {str(e)}"

    def analyze_code_all(self, code: str) -> Dict[str, str]:
        """Run complete code analysis"""
        results = {}
        
        print("📊 [1] Visualizing code structure...")
        try:
            structure_img = self.visualize_code_structure(code)
            results['structure_image'] = structure_img
            print(f"✅ Saved diagram to {structure_img}\n")
        except Exception as e:
            print(f"❌ Error in visualization: {e}\n")
            results['structure_image'] = None

        print("🔧 [2] Generating refactoring suggestions...")
        try:
            refactoring = self.suggest_code_refactoring(code)
            results['refactoring'] = refactoring
            print("✅ Refactoring analysis complete\n")
        except Exception as e:
            print(f"❌ Error in refactoring: {e}\n")
            results['refactoring'] = None

        print("🧮 [3] Analyzing complexity...")
        try:
            complexity = self.analyze_complexity(code)
            results['complexity'] = complexity
            print("✅ Complexity analysis complete\n")
        except Exception as e:
            print(f"❌ Error in complexity analysis: {e}\n")
            results['complexity'] = None

        print("📄 [4] Generating documentation...")
        try:
            documentation = self.generate_documentation(code)
            results['documentation'] = documentation
            print("✅ Documentation generated\n")
        except Exception as e:
            print(f"❌ Error in documentation: {e}\n")
            results['documentation'] = None

        print("💡 [5] Suggesting improvements...")
        try:
            improvements = self.suggest_improvements(code)
            results['improvements'] = improvements
            print("✅ Improvement suggestions complete\n")
        except Exception as e:
            print(f"❌ Error in improvements: {e}\n")
            results['improvements'] = None
        
        return results

# =========================
# Test Cases
# =========================
def run_test_cases():
    """Run comprehensive test cases"""
    print("🧪 RUNNING TEST CASES")
    print("=" * 50)
    
    # Initialize analyzer (you'll need to set your API key)
    analyzer = CodeAnalyzer()  # Add your API key here if needed
    
    # Test Case 1: Simple Pattern Printing Function
    test_case_1 = """
    #include <iostream>
    using namespace std;
    
    void pattern_print(){
        int rows = 10;
        
        for(int i = 0; i < rows; i++){
            for (int j = 0; j <= i; j++){
                if(j <= i ){
                    cout << '*';
                }
            }
            cout << endl;
        }
    }
    
    int main(){
        pattern_print();
        return 0;
    }
    """
    
    # Test Case 2: Bubble Sort Algorithm
    test_case_2 = """
    #include <iostream>
    using namespace std;
    
    void bubbleSort(int arr[], int n) {
        for (int i = 0; i < n-1; i++) {
            for (int j = 0; j < n-i-1; j++) {
                if (arr[j] > arr[j+1]) {
                    int temp = arr[j];
                    arr[j] = arr[j+1];
                    arr[j+1] = temp;
                }
            }
        }
    }
    
    void printArray(int arr[], int size) {
        for (int i = 0; i < size; i++)
            cout << arr[i] << " ";
        cout << endl;
    }
    """
    
    # Test Case 3: Binary Search
    test_case_3 = """
    #include <iostream>
    using namespace std;
    
    int binarySearch(int arr[], int left, int right, int target) {
        if (right >= left) {
            int mid = left + (right - left) / 2;
            
            if (arr[mid] == target)
                return mid;
            
            if (arr[mid] > target)
                return binarySearch(arr, left, mid - 1, target);
            
            return binarySearch(arr, mid + 1, right, target);
        }
        return -1;
    }
    """
    
    test_cases = [
        ("Pattern Printing Function", test_case_1)
        
    ]
    
    for i, (name, code) in enumerate(test_cases, 1):
        print(f"\n🔬 TEST CASE {i}: {name}")
        print("-" * 40)
        
        try:
            results = analyzer.analyze_code_all(code)
            
            # Print complexity analysis if available
            if results.get('complexity'):
                print("COMPLEXITY ANALYSIS:")
                print(results['complexity'][:200] + "..." if len(results['complexity']) > 200 else results['complexity'])
            
            print(f"✅ Test case {i} completed successfully")
            
        except Exception as e:
            print(f"❌ Test case {i} failed: {e}")
        
        print("\n" + "="*50)

if __name__ == "__main__":
    # Run the test cases
    run_test_cases()
    
    # Example of using the analyzer directly
    print("\n🔧 DIRECT USAGE EXAMPLE")
    print("=" * 50)
    
    sample_code = """
    void pattern_print(){
        int rows = 10;

        for(int i = 0; i < rows; i++){
            for (int j = 0; j <= i; j++){
                if(j <= i ){
                    cout << '*';
                }
            }
            cout << endl;
        }
    }
    """
    
    analyzer = CodeAnalyzer()
    results = analyzer.analyze_code_all(sample_code)
    
    print("Analysis completed! Check the generated files:")
    if results.get('structure_image'):
        print(f"- Code structure: {results['structure_image']}")
    print("- Complexity graph: complexity_graph.png")