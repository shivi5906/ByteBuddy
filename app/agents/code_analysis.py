import ast
import re
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx
from collections import defaultdict, Counter
import numpy as np
from typing import Dict, List, Tuple, Set
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from enum import Enum

class Language(Enum):
    CPP = "cpp"
    PYTHON = "python"
    JAVA = "java"
    C = "c"
    GO = "go"
    RUST = "rust"

class DataStructureVisualizer:
    """Specialized class for visualizing different data structures"""
    
    @staticmethod
    def draw_array(ax, data, position=(0, 0), title="Array"):
        """Draw array as connected boxes"""
        x, y = position
        box_width = 1.5
        box_height = 0.8
        
        # Draw array boxes
        for i, value in enumerate(data):
            rect = patches.Rectangle((x + i * box_width, y), box_width, box_height, 
                                   linewidth=2, edgecolor='#2E86AB', facecolor='#A23B72', alpha=0.7)
            ax.add_patch(rect)
            
            # Add value text
            ax.text(x + i * box_width + box_width/2, y + box_height/2, str(value),
                   ha='center', va='center', fontsize=12, fontweight='bold', color='white')
            
            # Add index below
            ax.text(x + i * box_width + box_width/2, y - 0.3, f'[{i}]',
                   ha='center', va='center', fontsize=10, color='#666')
        
        # Title
        ax.text(x + len(data) * box_width / 2, y + box_height + 0.5, title,
               ha='center', va='center', fontsize=14, fontweight='bold')
        
        return len(data) * box_width, box_height + 1

    @staticmethod
    def draw_linked_list(ax, data, position=(0, 0), title="Linked List"):
        """Draw linked list as connected nodes"""
        x, y = position
        node_radius = 0.6
        spacing = 3.0
        
        for i, value in enumerate(data):
            # Draw node circle
            circle = patches.Circle((x + i * spacing, y), node_radius, 
                                  linewidth=2, edgecolor='#F18F01', facecolor='#C73E1D', alpha=0.8)
            ax.add_patch(circle)
            
            # Add value text
            ax.text(x + i * spacing, y, str(value),
                   ha='center', va='center', fontsize=12, fontweight='bold', color='white')
            
            # Draw arrow to next node
            if i < len(data) - 1:
                ax.arrow(x + i * spacing + node_radius, y, 
                        spacing - 2 * node_radius, 0,
                        head_width=0.2, head_length=0.3, fc='#333', ec='#333', linewidth=2)
        
        # Draw NULL at the end
        ax.text(x + len(data) * spacing, y, 'NULL',
               ha='center', va='center', fontsize=10, style='italic', color='#666')
        
        # Title
        ax.text(x + (len(data) - 1) * spacing / 2, y + node_radius + 0.8, title,
               ha='center', va='center', fontsize=14, fontweight='bold')
        
        return len(data) * spacing + 1, node_radius * 2 + 1

    @staticmethod
    def draw_binary_tree(ax, nodes, position=(0, 0), title="Binary Tree"):
        """Draw binary tree structure"""
        if not nodes:
            return 0, 0
            
        x, y = position
        levels = int(np.log2(len(nodes))) + 1
        
        # Calculate positions for each level
        for i, value in enumerate(nodes):
            if value is None:
                continue
                
            level = int(np.log2(i + 1))
            pos_in_level = i - (2**level - 1)
            
            # Calculate x position based on level and position in level
            level_width = 8 / (2**level)
            node_x = x + pos_in_level * level_width + level_width/2
            node_y = y - level * 2
            
            # Draw node
            circle = patches.Circle((node_x, node_y), 0.5, 
                                  linewidth=2, edgecolor='#3A86FF', facecolor='#06FFA5', alpha=0.8)
            ax.add_patch(circle)
            
            # Add value text
            ax.text(node_x, node_y, str(value),
                   ha='center', va='center', fontsize=10, fontweight='bold')
            
            # Draw edges to children
            left_child = 2 * i + 1
            right_child = 2 * i + 2
            
            if left_child < len(nodes) and nodes[left_child] is not None:
                child_level = int(np.log2(left_child + 1))
                child_pos_in_level = left_child - (2**child_level - 1)
                child_level_width = 8 / (2**child_level)
                child_x = x + child_pos_in_level * child_level_width + child_level_width/2
                child_y = y - child_level * 2
                
                ax.plot([node_x, child_x], [node_y - 0.5, child_y + 0.5], 'k-', linewidth=2)
            
            if right_child < len(nodes) and nodes[right_child] is not None:
                child_level = int(np.log2(right_child + 1))
                child_pos_in_level = right_child - (2**child_level - 1)
                child_level_width = 8 / (2**child_level)
                child_x = x + child_pos_in_level * child_level_width + child_level_width/2
                child_y = y - child_level * 2
                
                ax.plot([node_x, child_x], [node_y - 0.5, child_y + 0.5], 'k-', linewidth=2)
        
        # Title
        ax.text(x + 4, y + 1, title, ha='center', va='center', fontsize=14, fontweight='bold')
        
        return 8, levels * 2 + 2

    @staticmethod
    def draw_stack(ax, data, position=(0, 0), title="Stack"):
        """Draw stack as vertical boxes"""
        x, y = position
        box_width = 2
        box_height = 0.8
        
        for i, value in enumerate(data):
            rect = patches.Rectangle((x, y + i * box_height), box_width, box_height,
                                   linewidth=2, edgecolor='#FF6B35', facecolor='#F7931E', alpha=0.8)
            ax.add_patch(rect)
            
            # Add value text
            ax.text(x + box_width/2, y + i * box_height + box_height/2, str(value),
                   ha='center', va='center', fontsize=12, fontweight='bold')
        
        # Add "TOP" indicator
        if data:
            ax.text(x + box_width + 0.5, y + (len(data) - 1) * box_height + box_height/2, '← TOP',
                   ha='left', va='center', fontsize=10, fontweight='bold', color='red')
        
        # Title
        ax.text(x + box_width/2, y + len(data) * box_height + 0.5, title,
               ha='center', va='center', fontsize=14, fontweight='bold')
        
        return box_width + 1, len(data) * box_height + 1

    @staticmethod
    def draw_queue(ax, data, position=(0, 0), title="Queue"):
        """Draw queue as horizontal boxes with FRONT and REAR indicators"""
        x, y = position
        box_width = 1.5
        box_height = 1
        
        for i, value in enumerate(data):
            rect = patches.Rectangle((x + i * box_width, y), box_width, box_height,
                                   linewidth=2, edgecolor='#8E44AD', facecolor='#9B59B6', alpha=0.8)
            ax.add_patch(rect)
            
            # Add value text
            ax.text(x + i * box_width + box_width/2, y + box_height/2, str(value),
                   ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        
        # Add FRONT and REAR indicators
        if data:
            ax.text(x + box_width/2, y + box_height + 0.3, 'FRONT',
                   ha='center', va='center', fontsize=10, fontweight='bold', color='green')
            ax.text(x + (len(data) - 1) * box_width + box_width/2, y + box_height + 0.3, 'REAR',
                   ha='center', va='center', fontsize=10, fontweight='bold', color='red')
        
        # Title
        ax.text(x + len(data) * box_width / 2, y + box_height + 0.8, title,
               ha='center', va='center', fontsize=14, fontweight='bold')
        
        return len(data) * box_width, box_height + 1.2

    @staticmethod
    def draw_hash_table(ax, data, position=(0, 0), title="Hash Table"):
        """Draw hash table with key-value pairs"""
        x, y = position
        bucket_width = 3
        bucket_height = 0.8
        
        for i, (key, value) in enumerate(data.items()):
            # Draw bucket
            rect = patches.Rectangle((x, y - i * bucket_height), bucket_width, bucket_height,
                                   linewidth=2, edgecolor='#16537E', facecolor='#1F77B4', alpha=0.8)
            ax.add_patch(rect)
            
            # Add key-value text
            ax.text(x + bucket_width/2, y - i * bucket_height + bucket_height/2, f'{key}: {value}',
                   ha='center', va='center', fontsize=11, fontweight='bold', color='white')
            
            # Add index
            ax.text(x - 0.5, y - i * bucket_height + bucket_height/2, f'[{i}]',
                   ha='center', va='center', fontsize=10, color='#666')
        
        # Title
        ax.text(x + bucket_width/2, y + 1, title,
               ha='center', va='center', fontsize=14, fontweight='bold')
        
        return bucket_width + 1, len(data) * bucket_height + 1.5


class MultiLanguageCodeAnalyzer:
    def __init__(self, api_key: str = None):
        """Initialize the multi-language code analyzer with Google GenAI"""
        self.has_llm = False
        try:
            if api_key:
                os.environ["GOOGLE_API_KEY"] = api_key
                self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")
                self.has_llm = True
        except Exception as e:
            print(f"⚠️  Warning: LLM initialization failed ({e}). Using fallback mode.")
            
        self.visualizer = DataStructureVisualizer()
        
        # Language-specific patterns
        self.language_patterns = {
            Language.CPP: self._get_cpp_patterns(),
            Language.C: self._get_c_patterns(),
            Language.PYTHON: self._get_python_patterns(),
            Language.JAVA: self._get_java_patterns(),
            Language.GO: self._get_go_patterns(),
            Language.RUST: self._get_rust_patterns()
        }
    
    def _get_cpp_patterns(self):
        return {
            'functions': r'(\w+\s+)?(\w+)\s*\([^)]*\)\s*{',
            'variables': r'(\w+)\s+(\w+)\s*[;=]',
            'arrays': r'(\w+)\s+(\w+)\s*\[\s*\d*\s*\]',
            'loops': r'for\s*\([^)]*\)|while\s*\([^)]*\)',
            'conditionals': r'if\s*\([^)]*\)',
            'classes': r'class\s+(\w+)',
            'includes': r'#include\s*[<"]([^>"]+)[>"]',
            'comments': [(r'//.*', ''), (r'/\*.*?\*/', '')],
            'data_structures': {
                'vector': r'vector\s*<\s*\w+\s*>',
                'stack': r'stack\s*<\s*\w+\s*>',
                'queue': r'queue\s*<\s*\w+\s*>',
                'map': r'map\s*<\s*\w+\s*,\s*\w+\s*>',
                'set': r'set\s*<\s*\w+\s*>'
            }
        }
    
    def _get_c_patterns(self):
        return {
            'functions': r'(\w+\s+)?(\w+)\s*\([^)]*\)\s*{',
            'variables': r'(\w+)\s+(\w+)\s*[;=]',
            'loops': r'for\s*\([^)]*\)|while\s*\([^)]*\)',
            'conditionals': r'if\s*\([^)]*\)',
            'classes': r'struct\s+(\w+)',
            'includes': r'#include\s*[<"]([^>"]+)[>"]',
            'comments': [(r'//.*', ''), (r'/\*.*?\*/', '')],
            'file_extensions': ['.c', '.h']
        }
    
    def _get_python_patterns(self):
        return {
            'functions': r'def\s+(\w+)\s*\([^)]*\):',
            'variables': r'(\w+)\s*=\s*',
            'lists': r'(\w+)\s*=\s*\[.*\]',
            'loops': r'for\s+\w+\s+in\s+|while\s+',
            'conditionals': r'if\s+|elif\s+',
            'classes': r'class\s+(\w+)',
            'imports': r'import\s+(\w+)|from\s+(\w+)\s+import',
            'comments': [(r'#.*', ''), (r'""".*?"""', ''), (r"'''.*?'''", '')],
            'data_structures': {
                'list': r'\[.*\]',
                'dict': r'\{.*:.*\}',
                'set': r'\{.*\}',
                'tuple': r'\(.*,.*\)'
            }
        }
    
    def _get_java_patterns(self):
        return {
            'functions': r'(?:public|private|protected)?\s*(?:static)?\s*\w+\s+(\w+)\s*\([^)]*\)\s*{',
            'variables': r'(?:public|private|protected)?\s*(?:static|final)?\s*\w+\s+(\w+)\s*[;=]',
            'arrays': r'(\w+)\s*\[\s*\]\s*(\w+)',
            'loops': r'for\s*\([^)]*\)|while\s*\([^)]*\)',
            'conditionals': r'if\s*\([^)]*\)',
            'classes': r'(?:public|private)?\s*class\s+(\w+)',
            'imports': r'import\s+([\w.]+)',
            'comments': [(r'//.*', ''), (r'/\*.*?\*/', '')],
            'data_structures': {
                'ArrayList': r'ArrayList\s*<\s*\w+\s*>',
                'HashMap': r'HashMap\s*<\s*\w+\s*,\s*\w+\s*>',
                'Stack': r'Stack\s*<\s*\w+\s*>',
                'Queue': r'Queue\s*<\s*\w+\s*>'
            }
        }
    
    def _get_go_patterns(self):
        return {
            'functions': r'func\s+(?:\(\w+\s+\*?\w+\)\s+)?(\w+)\s*\([^)]*\)',
            'variables': r'var\s+(\w+)|(\w+)\s*:=',
            'slices': r'(\w+)\s+\[\]\w+',
            'loops': r'for\s+|range\s+',
            'conditionals': r'if\s+',
            'structs': r'type\s+(\w+)\s+struct',
            'imports': r'import\s+"([^"]+)"|import\s+(\w+)',
            'comments': [(r'//.*', ''), (r'/\*.*?\*/', '')],
            'data_structures': {
                'slice': r'\[\]\w+',
                'map': r'map\s*\[\s*\w+\s*\]\s*\w+',
                'channel': r'chan\s+\w+'
            }
        }
    
    def _get_rust_patterns(self):
        return {
            'functions': r'fn\s+(\w+)\s*\([^)]*\)',
            'variables': r'let\s+(?:mut\s+)?(\w+)',
            'vectors': r'Vec\s*<\s*\w+\s*>',
            'loops': r'for\s+\w+\s+in\s+|while\s+|loop\s*{',
            'conditionals': r'if\s+|match\s+',
            'structs': r'struct\s+(\w+)',
            'imports': r'use\s+([\w:]+)',
            'comments': [(r'//.*', ''), (r'/\*.*?\*/', '')],
            'data_structures': {
                'Vec': r'Vec\s*<\s*\w+\s*>',
                'HashMap': r'HashMap\s*<\s*\w+\s*,\s*\w+\s*>',
                'BTreeMap': r'BTreeMap\s*<\s*\w+\s*,\s*\w+\s*>'
            }
        }

    def detect_language(self, code: str, filename: str = None) -> Language:
        """Detect programming language from code or filename"""
        if filename:
            for lang, patterns in self.language_patterns.items():
                if 'file_extensions' in patterns:
                    for ext in patterns['file_extensions']:
                        if filename.endswith(ext):
                            return lang
        
        # Language detection based on code patterns
        scores = {lang: 0 for lang in Language}
        
        # Check for language-specific keywords
        language_keywords = {
            Language.PYTHON: ['def ', 'import ', 'from ', 'class ', 'elif', 'None', 'True', 'False'],
            Language.JAVA: ['public class', 'private ', 'public ', 'import java', 'System.out'],
            Language.CPP: ['#include', 'using namespace', 'cout', 'cin', 'std::'],
            Language.C: ['#include', 'printf', 'scanf', 'malloc', 'free'],
            Language.GO: ['func ', 'package ', 'import ', 'fmt.', 'var '],
            Language.RUST: ['fn ', 'let ', 'mut ', 'impl ', 'use ', 'println!']
        }
        
        for lang, keywords in language_keywords.items():
            for keyword in keywords:
                scores[lang] += code.count(keyword)
        
        return max(scores, key=scores.get)

    def extract_data_structures(self, code: str, language: Language) -> Dict:
        """Extract data structures and their sample data from code"""
        patterns = self.language_patterns[language]
        data_structures = {}
        
        # Detect arrays/lists with sample data
        if 'arrays' in code.lower() or '[' in code:
            # Try to extract array initialization values
            array_patterns = [
                r'\{([^}]+)\}',  # C/C++/Java style: {1, 2, 3}
                r'\[([^\]]+)\]'  # Python/JS style: [1, 2, 3]
            ]
            
            for pattern in array_patterns:
                matches = re.findall(pattern, code)
                for match in matches:
                    try:
                        # Try to parse as numbers
                        values = [int(x.strip()) for x in match.split(',') if x.strip().isdigit()]
                        if values:
                            data_structures['array'] = values[:6]  # Limit to 6 elements
                            break
                    except:
                        continue
            
            # Default array if none found
            if 'array' not in data_structures:
                data_structures['array'] = [64, 34, 25, 12, 22]
        
        # Detect linked list operations
        if 'node' in code.lower() or 'next' in code.lower() or 'linkedlist' in code.lower():
            data_structures['linked_list'] = [10, 20, 30, 40]
        
        # Detect stack operations
        if 'stack' in code.lower() or 'push' in code.lower() or 'pop' in code.lower():
            data_structures['stack'] = [1, 2, 3, 4, 5]
        
        # Detect queue operations
        if 'queue' in code.lower() or 'enqueue' in code.lower() or 'dequeue' in code.lower():
            data_structures['queue'] = ['A', 'B', 'C', 'D']
        
        # Detect binary tree
        if 'tree' in code.lower() or 'binary' in code.lower() or 'root' in code.lower():
            data_structures['binary_tree'] = [1, 2, 3, 4, 5, 6, 7]  # Level order
        
        # Detect hash table/map
        if any(word in code.lower() for word in ['map', 'hash', 'dict', 'hashmap']):
            data_structures['hash_table'] = {'key1': 'val1', 'key2': 'val2', 'key3': 'val3'}
        
        return data_structures

    def create_personalized_visualization(self, code: str, language: Language = None, 
                                        output_path: str = "data_structures_viz") -> str:
        """Create personalized visualization based on detected data structures"""
        
        if language is None:
            language = self.detect_language(code)
        
        # Extract data structures from code
        data_structures = self.extract_data_structures(code, language)
        
        if not data_structures:
            # If no specific data structures detected, show a simple algorithm flow
            data_structures = {'array': [5, 2, 8, 1, 9]}  # Default
        
        # Create visualization
        fig, ax = plt.subplots(figsize=(16, 12))
        fig.patch.set_facecolor('#f8f9fa')
        ax.set_facecolor('#f8f9fa')
        
        # Remove axes
        ax.set_xlim(0, 20)
        ax.set_ylim(0, 15)
        ax.axis('off')
        
        # Title
        language_name = language.value.upper() if hasattr(language, 'value') else str(language).upper()
        ax.text(10, 14, f'{language_name} - Data Structure Visualization', 
                ha='center', va='center', fontsize=20, fontweight='bold', color='#2c3e50')
        
        # Draw data structures
        current_y = 12
        
        for ds_type, data in data_structures.items():
            if ds_type == 'array' and isinstance(data, list):
                width, height = self.visualizer.draw_array(ax, data, (2, current_y))
                current_y -= height + 1
                
            elif ds_type == 'linked_list' and isinstance(data, list):
                width, height = self.visualizer.draw_linked_list(ax, data, (1, current_y))
                current_y -= height + 1
                
            elif ds_type == 'stack' and isinstance(data, list):
                width, height = self.visualizer.draw_stack(ax, data, (2, current_y - len(data) * 0.8))
                current_y -= height + 1
                
            elif ds_type == 'queue' and isinstance(data, list):
                width, height = self.visualizer.draw_queue(ax, data, (2, current_y))
                current_y -= height + 1
                
            elif ds_type == 'binary_tree' and isinstance(data, list):
                width, height = self.visualizer.draw_binary_tree(ax, data, (2, current_y))
                current_y -= height + 1
                
            elif ds_type == 'hash_table' and isinstance(data, dict):
                width, height = self.visualizer.draw_hash_table(ax, data, (2, current_y))
                current_y -= height + 1
        
        # Add code complexity info box
        complexity_info = self._get_complexity_summary(code, language)
        ax.text(15, 8, complexity_info, ha='left', va='top', fontsize=10,
                bbox=dict(boxstyle="round,pad=0.5", facecolor='#ecf0f1', edgecolor='#bdc3c7'),
                fontfamily='monospace')
        
        plt.tight_layout()
        
        # Save visualization
        output_file = f"{output_path}_{language.value if hasattr(language, 'value') else language}.png"
        plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='#f8f9fa')
        plt.close()
        
        return output_file

    def visualize_code_structure(self, code: str, output_path: str = "code_structure.png") -> str:
        """Create code structure visualization"""
        language = self.detect_language(code)
        parsed = self.parse_code(code, language)
        
        # Create networkx graph
        G = nx.DiGraph()
        
        # Add function nodes
        for func in parsed.get('functions', []):
            func_name = func if isinstance(func, str) else func.get('name', 'unknown')
            G.add_node(func_name, node_type='function', color='#ff7f0e')
        
        # Add variable nodes
        for var in parsed.get('variables', []):
            var_name = var if isinstance(var, str) else var.get('name', 'unknown')
            G.add_node(var_name, node_type='variable', color='#2ca02c')
        
        # Create visualization
        plt.figure(figsize=(14, 10))
        plt.style.use('default')
        
        pos = nx.spring_layout(G, k=3, iterations=50)
        
        # Draw nodes
        function_nodes = [n for n, d in G.nodes(data=True) if d.get('node_type') == 'function']
        variable_nodes = [n for n, d in G.nodes(data=True) if d.get('node_type') == 'variable']
        
        nx.draw_networkx_nodes(G, pos, nodelist=function_nodes, 
                              node_color='#ff7f0e', node_size=1000, alpha=0.8)
        nx.draw_networkx_nodes(G, pos, nodelist=variable_nodes, 
                              node_color='#2ca02c', node_size=800, alpha=0.8)
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20)
        
        plt.title(f'Code Structure - {language.value.upper()}', fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        return output_path

    def parse_cpp_code(self, code: str) -> Dict:
        """Parse C++ code specifically"""
        return self.parse_code(code, Language.CPP)

    def suggest_code_refactoring(self, code: str) -> str:
        """Use LLM to suggest real refactoring improvements"""
        if not self.has_llm:
            return self.generate_fallback_refactoring(code)
            
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

    def generate_fallback_refactoring(self, code: str) -> str:
        """Generate basic refactoring suggestions without LLM"""
        suggestions = []
        
        if code.count('cout') > 3:
            suggestions.append("Consider wrapping repeated cout statements in a function")
        
        if 'int main()' in code and code.count('return') == 1:
            suggestions.append("Consider adding error handling with different return codes")
        
        if code.count('for') >= 2:
            suggestions.append("Consider extracting nested loops into separate functions")
        
        if not any(word in code for word in ['const', 'auto']):
            suggestions.append("Consider using 'const' for immutable variables and 'auto' for type deduction")
        
        if '#include <iostream>' in code and 'using namespace std' in code:
            suggestions.append("Consider avoiding 'using namespace std' in larger projects")
        
        return "REFACTORING SUGGESTIONS:\n" + "\n".join(f"• {s}" for s in suggestions)

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
    
    def generate_fallback_documentation(self, code: str) -> str:
        parsed = self.parse_cpp_code(code)
        
        # Analyze complexity
        nested_loops = len(parsed.get('loops', []))
        if nested_loops == 0:
            time_complexity = "O(1)"
        elif nested_loops == 1:
            time_complexity = "O(n)"
        elif nested_loops >= 2:
            time_complexity = "O(n²) or higher"
        else:
            time_complexity = "O(n log n)"
        
        # Generate documentation
        doc = f"""# C++ Code Documentation

**Lines of Code**: {parsed['lines']}
**Functions**: {len(parsed.get('functions', []))}
**Variables**: {len(parsed.get('variables', []))}

## Includes
```cpp
{chr(10).join(parsed.get('includes', [])) if parsed.get('includes') else 'No includes found'}
```

## Functions Analysis
"""
        
        for func in parsed.get('functions', []):
            return_type = func.get('return_type', 'void') if isinstance(func, dict) else 'void'
            func_name = func.get('name') if isinstance(func, dict) else func
            doc += f"""
### `{func_name}()`
- **Return Type**: `{return_type}`
- **Purpose**: {'Main entry point' if func_name == 'main' else 'Utility function'}
"""
        
        doc += f"""
## Variables
"""
        for var in parsed.get('variables', []):
            if isinstance(var, dict):
                doc += f"- `{var.get('type', 'unknown')} {var.get('name', 'unknown')}`: {var.get('type', 'unknown')} variable\n"
            else:
                doc += f"- `{var}`: Variable\n"
        
        doc += f"""
## Control Structures
- **Loops**: {len(parsed.get('loops', []))} loop(s) detected
- **Conditionals**: {len(parsed.get('conditionals', []))} conditional(s) detected

## Complexity Analysis
- **Estimated Time Complexity**: {time_complexity}
- **Space Complexity**: O(1) to O(n) depending on data structures used

## Code Structure
"""
        
        if parsed.get('loops'):
            doc += "- Contains iterative logic (loops)\n"
        if parsed.get('conditionals'):
            doc += "- Contains conditional logic (if statements)\n"
        if any((func.get('name') if isinstance(func, dict) else func) == 'main' for func in parsed.get('functions', [])):
            doc += "- Has main function (executable program)\n"
        
        doc += f"""
## Recommendations
1. **Code Quality**: Add comments to explain complex logic
2. **Error Handling**: Consider adding input validation
3. **Modern C++**: Use modern C++ features like auto, range-based loops
4. **Performance**: {'Consider optimizing nested loops' if nested_loops >= 2 else 'Performance looks acceptable'}

---
*Generated by CodeAnalyzer (Fallback Mode)*
"""
        
        return doc

    def generate_documentation(self, code: str) -> str:
        if not self.has_llm:
            return self.generate_fallback_documentation(code)
        
        prompt = PromptTemplate.from_template("""
Generate comprehensive markdown documentation for this C++ code:

```cpp
{code}
```

Include:
1. **Purpose**: What does this code do?
2. **Algorithm**: Explain the algorithm/logic step by step
3. **Functions**: Detailed description of each function
4. **Parameters**: Input parameters and their types
5. **Return Values**: What the functions return
6. **Time/Space Complexity**: Brief complexity analysis
7. **Example Usage**: How to use this code
8. **Potential Improvements**: What could be enhanced
9. **Code Flow**: Explain the execution flow

Use proper markdown formatting with headers, code blocks, and bullet points.
Be detailed and educational.
""")
        
        try:
            response = self.llm.invoke(prompt.format(code=code))
            content = response.content if hasattr(response, 'content') else str(response)
            return content
        except Exception as e:
            print(f"⚠️  LLM failed ({e}), using fallback documentation")
            return self.generate_fallback_documentation(code)

    def save_documentation_to_file(self, documentation: str, filename: str = "code_documentation.md") -> str:
        """Save documentation to markdown file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(documentation)
            return filename
        except Exception as e:
            print(f"Error saving documentation: {e}")
            return None

    def display_documentation_terminal(self, documentation: str, title: str = "Code Documentation"):
        terminal_width = 80
        
        print("\n" + "="*terminal_width)
        print(f" {title.center(terminal_width-2)} ")
        print("="*terminal_width)
        
        # Process markdown for terminal display
        lines = documentation.split('\n')
        for line in lines:
            if line.startswith('# '):
                # Main header
                header = line[2:]
                print(f"\n🔷 {header.upper()}")
                print("─" * min(len(header) + 3, terminal_width))
            elif line.startswith('## '):
                # Sub header
                subheader = line[3:]
                print(f"\n📋 {subheader}")
                print("─" * min(len(subheader) + 3, terminal_width//2))
            elif line.startswith('### '):
                # Function header
                funcheader = line[4:]
                print(f"\n⚙️  {funcheader}")
            elif line.startswith('```'):
                # Code block markers
                if 'cpp' in line:
                    print("\n💻 Code:")
                    print("┌" + "─" * (terminal_width-2) + "┐")
                else:
                    print("└" + "─" * (terminal_width-2) + "┘")
            elif line.startswith('- '):
                # Bullet point
                print(f"   • {line[2:]}")
            elif line.strip().startswith('**') and line.strip().endswith('**'):
                # Bold text
                bold_text = line.strip()[2:-2]
                print(f"\n🔸 {bold_text}")
            elif line.strip():
                # Regular text
                print(f"   {line}")
            else:
                # Empty line
                print()
        
        print("\n" + "="*terminal_width)

    def suggest_improvements(self, code: str) -> str:
        """Generate specific improvement suggestions using LLM"""
        if not self.has_llm:
            return self.generate_fallback_improvements(code)
            
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

    def generate_fallback_improvements(self, code: str) -> str:
        """Generate basic improvement suggestions without LLM"""
        improvements = []
        
        if 'int main()' in code and 'const' not in code:
            improvements.append("Use const for variables that don't change")
        
        if code.count('for') >= 2:
            improvements.append("Consider using range-based for loops where possible")
        
        if 'cout' in code and code.count('endl') > 2:
            improvements.append("Consider using '\\n' instead of endl for better performance")
        
        if 'malloc' in code or 'free' in code:
            improvements.append("Use smart pointers instead of manual memory management")
        
        return "IMPROVEMENT SUGGESTIONS:\n" + "\n".join(f"• {s}" for s in improvements)

    def _get_complexity_summary(self, code: str, language: Language) -> str:
        """Get a brief complexity summary for the info box"""
        parsed = self.parse_code(code, language)
        time_complexity, space_complexity, _ = self.estimate_complexity(parsed)
        
        return f"""CODE ANALYSIS SUMMARY
Language: {language.value.upper() if hasattr(language, 'value') else str(language).upper()}
Time Complexity: {time_complexity}
Space Complexity: {space_complexity}
Functions: {len(parsed.get('functions', []))}
Variables: {len(parsed.get('variables', []))}
Lines: {parsed.get('lines', 0)}"""

    def parse_code(self, code: str, language: Language = None) -> Dict:
        """Parse code based on detected or specified language"""
        if language is None:
            language = self.detect_language(code)
        
        patterns = self.language_patterns[language]
        
        # Remove comments
        cleaned_code = code
        for comment_pattern, replacement in patterns['comments']:
            cleaned_code = re.sub(comment_pattern, replacement, cleaned_code, flags=re.DOTALL)
        
        # Extract components
        result = {
            'language': language.value if hasattr(language, 'value') else str(language),
            'raw_code': code,
            'cleaned_code': cleaned_code,
            'lines': len(code.split('\n'))
        }
        
        # Extract functions
        if 'functions' in patterns:
            functions = re.findall(patterns['functions'], cleaned_code)
            if language == Language.PYTHON:
                result['functions'] = [f for f in functions if f]
            elif language in [Language.GO, Language.RUST]:
                result['functions'] = [f for f in functions if f]
            else:
                result['functions'] = [f[1] if isinstance(f, tuple) and len(f) > 1 else f for f in functions if f]
        
        # Extract variables
        if 'variables' in patterns:
            variables = re.findall(patterns['variables'], cleaned_code)
            result['variables'] = [v[1] if isinstance(v, tuple) and len(v) > 1 else v for v in variables if v]
        
        # Extract loops and conditionals
        for pattern_name in ['loops', 'conditionals']:
            if pattern_name in patterns:
                result[pattern_name] = re.findall(patterns[pattern_name], cleaned_code)
        
        return result

    def estimate_complexity(self, parsed_data: Dict) -> Tuple[str, str, str]:
        """Estimate time and space complexity"""
        loops = len(parsed_data.get('loops', []))
        
        if loops == 0:
            return "O(1)", "O(1)", "#00C851"
        elif loops == 1:
            return "O(n)", "O(1)", "#ffbb33"
        else:
            return "O(n²)", "O(n)", "#ff4444"

    def analyze_code_complete(self, code: str, display_docs: bool = True, save_docs: bool = True) -> Dict[str, str]:
        """Run complete code analysis with all features"""
        results = {}
        
        print("🚀 Starting Multi-Language Code Analysis...")
        print("="*60)
        
        # Detect language first
        language = self.detect_language(code)
        print(f"🔍 Detected Language: {language.value.upper()}")
        
        print("\n📊 [1] Creating personalized visualization...")
        try:
            viz_file = self.create_personalized_visualization(code, language)
            results['visualization'] = viz_file
            print(f"✅ Saved visualization to {viz_file}")
        except Exception as e:
            print(f"❌ Error in visualization: {e}")
            results['visualization'] = None

        

        print("\n🔧 [3] Generating refactoring suggestions...")
        try:
            refactoring = self.suggest_code_refactoring(code)
            results['refactoring'] = refactoring
            print("✅ Refactoring analysis complete")
        except Exception as e:
            print(f"❌ Error in refactoring: {e}")
            results['refactoring'] = None

        print("\n🧮 [4] Analyzing complexity...")
        try:
            complexity = self.analyze_complexity(code)
            results['complexity'] = complexity
            print("✅ Complexity analysis complete")
        except Exception as e:
            print(f"❌ Error in complexity analysis: {e}")
            results['complexity'] = None

        print("\n📄 [5] Generating documentation...")
        try:
            documentation = self.generate_documentation(code)
            results['documentation'] = documentation
            
            if display_docs:
                self.display_documentation_terminal(documentation, "Generated Code Documentation")
            
            if save_docs:
                doc_file = self.save_documentation_to_file(documentation)
                results['documentation_file'] = doc_file
                if doc_file:
                    print(f"✅ Documentation saved to {doc_file}")
            
            print("✅ Documentation generated")
        except Exception as e:
            print(f"❌ Error in documentation: {e}")
            results['documentation'] = None

        print("\n💡 [6] Suggesting improvements...")
        try:
            improvements = self.suggest_improvements(code)
            results['improvements'] = improvements
            print("✅ Improvement suggestions complete")
        except Exception as e:
            print(f"❌ Error in improvements: {e}")
            results['improvements'] = None
        
        print("\n🎉 Analysis Complete!")
        print("="*60)
        
        return results

    def analyze_code_all(self, code: str, display_docs: bool = True, save_docs: bool = True) -> Dict[str, str]:
        """Alias for analyze_code_complete for backward compatibility"""
        return self.analyze_code_complete(code, display_docs, save_docs)


# Simple test case
def test_analyzer():
    """Simple test with one example"""
    analyzer = MultiLanguageCodeAnalyzer()
    
    # Test with a simple array sorting algorithm
    test_code = """
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

int main() {
    int arr[] = {64, 34, 25, 12, 22, 11, 90};
    int n = 7;
    bubbleSort(arr, n);
    return 0;
}
"""
    
    print("🧪 Testing Multi-Language Code Analyzer")
    print("Testing with C++ Bubble Sort Algorithm")
    print("=" * 60)
    
    results = analyzer.analyze_code_complete(test_code)
    
    if results.get('visualization'):
        print(f"\n✅ Generated personalized visualization: {results['visualization']}")
        print("📊 The visualization shows:")
        print("   • Array elements as connected boxes")
        print("   • Algorithm complexity information")
        print("   • Data structure layout")
    
    return results


if __name__ == "__main__":
    # You can test with or without API key
    # analyzer = MultiLanguageCodeAnalyzer(api_key="your-google-api-key-here")
    analyzer = MultiLanguageCodeAnalyzer()
    
    test_code = """
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

int main() {
    int arr[] = {64, 34, 25, 12, 22, 11, 90};
    int n = 7;
    bubbleSort(arr, n);
    return 0;
}
"""
    
    results = analyzer.analyze_code_complete(test_code)
    
    if results.get('visualization'):
        print(f"\n✅ Generated personalized visualization: {results['visualization']}")
        print("📊 The visualization shows:")
        print("   • Array elements as connected boxes")
        print("   • Algorithm complexity information")
        print("   • Data structure layout")